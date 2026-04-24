from __future__ import annotations

import argparse
from pathlib import Path

import fetch_embodied_arxiv as fetcher


ROOT = Path(__file__).resolve().parents[1]
GENERATED_ROOT = ROOT / "generated" / "arxiv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate daily/weekly embodied arXiv snapshots and 03-papers candidates."
    )
    parser.add_argument(
        "--mode",
        choices=("daily", "weekly", "all"),
        default="all",
        help="Which snapshot set to generate.",
    )
    parser.add_argument(
        "--daily-days",
        type=int,
        default=1,
        help="Lookback days for the daily snapshot.",
    )
    parser.add_argument(
        "--weekly-days",
        type=int,
        default=7,
        help="Lookback days for the weekly snapshot.",
    )
    parser.add_argument(
        "--daily-max-results",
        type=int,
        default=20,
        help="Maximum filtered papers for the daily snapshot.",
    )
    parser.add_argument(
        "--weekly-max-results",
        type=int,
        default=60,
        help="Maximum filtered papers for the weekly snapshot.",
    )
    parser.add_argument(
        "--daily-fetch-size",
        type=int,
        default=120,
        help="Initial fetch size for the daily snapshot.",
    )
    parser.add_argument(
        "--weekly-fetch-size",
        type=int,
        default=300,
        help="Initial fetch size for the weekly snapshot.",
    )
    return parser.parse_args()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")


def generate_snapshot(
    name: str,
    days: int,
    max_results: int,
    fetch_size: int,
) -> None:
    end_dt = fetcher.now_utc()
    start_dt = end_dt - fetcher.timedelta(days=days)
    search_query = fetcher.build_search_query(
        categories=fetcher.DEFAULT_CATEGORIES,
        keywords=fetcher.DEFAULT_KEYWORDS,
        start=start_dt,
        end=end_dt,
    )
    papers = fetcher.filter_and_sort(
        papers=fetcher.fetch_papers(
            search_query=search_query,
            fetch_size=fetch_size,
            keywords=fetcher.DEFAULT_KEYWORDS,
        ),
        start_dt=start_dt,
        end_dt=end_dt,
        max_results=max_results,
    )

    output_dir = GENERATED_ROOT / name
    write_text(
        output_dir / "latest.md",
        fetcher.render_markdown(
            papers=papers,
            search_query=search_query,
            categories=fetcher.DEFAULT_CATEGORIES,
            keywords=fetcher.DEFAULT_KEYWORDS,
            start_dt=start_dt,
            end_dt=end_dt,
            abstract_chars=280,
        ),
    )
    write_text(
        output_dir / "latest.json",
        fetcher.render_json(
            papers=papers,
            search_query=search_query,
            categories=fetcher.DEFAULT_CATEGORIES,
            keywords=fetcher.DEFAULT_KEYWORDS,
            start_dt=start_dt,
            end_dt=end_dt,
        ),
    )
    write_text(
        output_dir / "candidates-for-03-papers.md",
        fetcher.render_candidates_markdown(
            papers=papers,
            search_query=search_query,
            categories=fetcher.DEFAULT_CATEGORIES,
            keywords=fetcher.DEFAULT_KEYWORDS,
            start_dt=start_dt,
            end_dt=end_dt,
        ),
    )


def main() -> int:
    args = parse_args()

    if args.mode in ("daily", "all"):
        generate_snapshot(
            name="daily",
            days=args.daily_days,
            max_results=args.daily_max_results,
            fetch_size=args.daily_fetch_size,
        )

    if args.mode in ("weekly", "all"):
        generate_snapshot(
            name="weekly",
            days=args.weekly_days,
            max_results=args.weekly_max_results,
            fetch_size=args.weekly_fetch_size,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
