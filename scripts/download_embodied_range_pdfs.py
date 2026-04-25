from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from datetime import date, datetime, time as dt_time, timedelta, timezone
from pathlib import Path

import fetch_embodied_arxiv as arxiv_helpers


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = ROOT / "downloads" / "embodied-robot-papers"
API_PAGE_SIZE = 200
API_SLEEP_SECONDS = 3.0
PROGRESS_EVERY = 25
DEFAULT_WORKERS = 4


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download embodied/robot-related arXiv PDFs for a custom UTC date range."
    )
    parser.add_argument("--start-date", required=True, help="Inclusive UTC date in YYYY-MM-DD format.")
    parser.add_argument("--end-date", required=True, help="Inclusive UTC date in YYYY-MM-DD format.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Optional output directory. Defaults to downloads/embodied-robot-papers/<start>_to_<end>.",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=API_PAGE_SIZE,
        help="How many entries to request per arXiv API page.",
    )
    parser.add_argument(
        "--metadata-only",
        action="store_true",
        help="Fetch and filter metadata, but do not download PDFs.",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip PDF files that already exist on disk.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help="How many PDFs to download concurrently.",
    )
    return parser.parse_args()


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise SystemExit(f"Invalid date: {value}") from exc


def range_start_dt(value: date) -> datetime:
    return datetime.combine(value, dt_time.min, tzinfo=timezone.utc)


def range_end_dt(value: date) -> datetime:
    return datetime.combine(value, dt_time(hour=23, minute=59), tzinfo=timezone.utc)


def sanitize_filename(value: str, limit: int = 120) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-._")
    if not cleaned:
        cleaned = "paper"
    return cleaned[:limit].rstrip("-._")


def default_output_dir(start_date: date, end_date: date) -> Path:
    return DEFAULT_OUTPUT_ROOT / f"{start_date.isoformat()}_to_{end_date.isoformat()}"


def fetch_all_papers(search_query: str, keywords: list[str], page_size: int) -> list[arxiv_helpers.Paper]:
    papers: list[arxiv_helpers.Paper] = []
    start_index = 0
    total_results: int | None = None

    while total_results is None or start_index < total_results:
        url = arxiv_helpers.build_request_url(search_query, start_index=start_index, page_size=page_size)
        xml_bytes = arxiv_helpers.request_feed(url)
        page_papers, total_results = arxiv_helpers.parse_papers(xml_bytes, keywords)
        if not page_papers:
            break
        papers.extend(page_papers)
        start_index += len(page_papers)
        print(f"Fetched {start_index}/{total_results} metadata entries...", flush=True)
        if start_index < total_results:
            time.sleep(API_SLEEP_SECONDS)

    return papers


def pdf_url_for(paper: arxiv_helpers.Paper) -> str:
    if paper.pdf_url:
        return paper.pdf_url
    return f"https://arxiv.org/pdf/{paper.arxiv_id}.pdf"


def pdf_filename_for(paper: arxiv_helpers.Paper) -> str:
    published = paper.published[:10] if paper.published else "unknown-date"
    title_slug = sanitize_filename(paper.title)
    return f"{published}_{paper.arxiv_id}_{title_slug}.pdf"


def manifest_path(output_dir: Path) -> Path:
    return output_dir / "manifest.json"


def write_manifest(output_dir: Path, payload: dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path(output_dir).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def download_pdf(url: str, output_path: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": arxiv_helpers.USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            output_path.write_bytes(response.read())
        return
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise
        fallback_url = re.sub(r"(\d{4}\.\d{4,5})v\d+(\.pdf)?$", r"\1.pdf", url)
        if fallback_url == url:
            raise
        fallback_request = urllib.request.Request(fallback_url, headers={"User-Agent": arxiv_helpers.USER_AGENT})
        with urllib.request.urlopen(fallback_request, timeout=180) as response:
            output_path.write_bytes(response.read())


def main() -> int:
    args = parse_args()
    start_date = parse_date(args.start_date)
    end_date = parse_date(args.end_date)
    if end_date < start_date:
        raise SystemExit("--end-date must be greater than or equal to --start-date.")
    if args.page_size <= 0:
        raise SystemExit("--page-size must be greater than 0.")
    if args.workers <= 0:
        raise SystemExit("--workers must be greater than 0.")

    output_dir = args.output_dir or default_output_dir(start_date, end_date)
    start_dt = range_start_dt(start_date)
    end_dt = range_end_dt(end_date)
    search_query = arxiv_helpers.build_search_query(
        categories=arxiv_helpers.DEFAULT_CATEGORIES,
        keywords=arxiv_helpers.DEFAULT_KEYWORDS,
        start=start_dt,
        end=end_dt,
    )

    try:
        candidates = fetch_all_papers(
            search_query=search_query,
            keywords=arxiv_helpers.DEFAULT_KEYWORDS,
            page_size=args.page_size,
        )
    except urllib.error.HTTPError as exc:
        print(f"arXiv API HTTP error: {exc.code} {exc.reason}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"arXiv API connection error: {exc.reason}", file=sys.stderr)
        return 1

    filtered = arxiv_helpers.filter_and_sort(
        papers=candidates,
        start_dt=start_dt,
        end_dt=end_dt,
        max_results=100000,
    )

    manifest_records: list[dict | None] = [None] * len(filtered)
    downloaded = 0
    skipped = 0
    failed = 0

    output_dir.mkdir(parents=True, exist_ok=True)
    download_jobs: list[tuple[int, dict, Path]] = []

    for index, paper in enumerate(filtered):
        filename = pdf_filename_for(paper)
        output_path = output_dir / filename
        record = {
            **asdict(paper),
            "pdf_download_url": pdf_url_for(paper),
            "local_filename": filename,
            "local_path": str(output_path.relative_to(ROOT)),
            "downloaded": False,
            "skipped_existing": False,
            "error": "",
        }

        if args.metadata_only:
            manifest_records[index] = record
            continue

        if args.skip_existing and output_path.exists():
            record["skipped_existing"] = True
            manifest_records[index] = record
            skipped += 1
            if (downloaded + skipped + failed) % PROGRESS_EVERY == 0:
                print(
                    f"Progress: {downloaded} downloaded, {skipped} skipped, {failed} failed, "
                    f"{downloaded + skipped + failed}/{len(filtered)} processed.",
                    flush=True,
                )
            continue
        download_jobs.append((index, record, output_path))

    if not args.metadata_only and download_jobs:
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            future_map = {
                executor.submit(download_pdf, record["pdf_download_url"], output_path): (index, record)
                for index, record, output_path in download_jobs
            }
            for future in as_completed(future_map):
                index, record = future_map[future]
                try:
                    future.result()
                    record["downloaded"] = True
                    downloaded += 1
                except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
                    record["error"] = str(exc)
                    failed += 1
                manifest_records[index] = record
                if (downloaded + skipped + failed) % PROGRESS_EVERY == 0:
                    print(
                        f"Progress: {downloaded} downloaded, {skipped} skipped, {failed} failed, "
                        f"{downloaded + skipped + failed}/{len(filtered)} processed.",
                        flush=True,
                    )

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "range": {
            "start_date_utc": start_date.isoformat(),
            "end_date_utc": end_date.isoformat(),
        },
        "search_query": search_query,
        "categories": arxiv_helpers.DEFAULT_CATEGORIES,
        "keywords": arxiv_helpers.DEFAULT_KEYWORDS,
        "candidate_count": len(candidates),
        "filtered_count": len(filtered),
        "downloaded_count": downloaded,
        "skipped_existing_count": skipped,
        "failed_count": failed,
        "output_dir": str(output_dir.relative_to(ROOT)),
        "papers": [record for record in manifest_records if record is not None],
    }
    write_manifest(output_dir, payload)

    print(f"Output directory: {output_dir.relative_to(ROOT)}")
    print(f"Filtered papers: {len(filtered)}")
    if args.metadata_only:
        print("Metadata only: no PDFs downloaded.")
    else:
        print(f"Downloaded: {downloaded}")
        print(f"Skipped existing: {skipped}")
        print(f"Failed: {failed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
