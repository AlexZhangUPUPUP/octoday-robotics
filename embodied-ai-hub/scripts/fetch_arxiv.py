#!/usr/bin/env python3
"""Fetch embodied-AI paper snapshots from the arXiv Atom API."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "weekly" / "config" / "arxiv_topics.json"
ARXIV_API_URL = "https://export.arxiv.org/api/query"
ATOM_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch arXiv Atom feeds and save a normalized JSON snapshot."
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--days", type=int, default=None)
    parser.add_argument("--query", help="Single arXiv search query for ad-hoc use.")
    parser.add_argument(
        "--query-name",
        default="Custom Topic",
        help="Topic label to use with --query.",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=5,
        help="Max results for ad-hoc --query mode.",
    )
    parser.add_argument(
        "--feed-file",
        type=Path,
        help="Local Atom XML file for offline parsing in ad-hoc --query mode.",
    )
    parser.add_argument(
        "--sort-by",
        default="submittedDate",
        choices=["relevance", "lastUpdatedDate", "submittedDate"],
    )
    parser.add_argument(
        "--sort-order",
        default="descending",
        choices=["ascending", "descending"],
    )
    return parser.parse_args()


def load_topics(args: argparse.Namespace) -> tuple[list[dict[str, Any]], int]:
    if args.query:
        topics = [
            {
                "name": args.query_name,
                "query": args.query,
                "max_results": args.max_results,
            }
        ]
        days = 14 if args.days is None else args.days
        return topics, days

    config = json.loads(args.config.read_text(encoding="utf-8"))
    topics = config.get("topics", [])
    days = config.get("default_days", 14) if args.days is None else args.days
    if not topics:
        raise SystemExit(f"No topics found in config: {args.config}")
    return topics, days


def fetch_xml(
    query: str,
    *,
    max_results: int,
    sort_by: str,
    sort_order: str,
) -> str:
    params = urlencode(
        {
            "search_query": query,
            "start": 0,
            "max_results": max_results,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
    )
    request = Request(
        f"{ARXIV_API_URL}?{params}",
        headers={
            "User-Agent": "octoday-robotics/1.0 (embodied-ai weekly automation)",
        },
    )
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def clean_text(value: str) -> str:
    return " ".join(value.split())


def parse_feed(xml_text: str, cutoff: datetime | None) -> list[dict[str, Any]]:
    root = ET.fromstring(xml_text)
    entries: list[dict[str, Any]] = []

    for node in root.findall("atom:entry", ATOM_NS):
        entry_id = node.findtext("atom:id", default="", namespaces=ATOM_NS).strip()
        title = clean_text(
            node.findtext("atom:title", default="", namespaces=ATOM_NS)
        )
        summary = clean_text(
            node.findtext("atom:summary", default="", namespaces=ATOM_NS)
        )
        published = node.findtext("atom:published", default="", namespaces=ATOM_NS)
        updated = node.findtext("atom:updated", default="", namespaces=ATOM_NS)
        published_dt = parse_timestamp(published) if published else None
        updated_dt = parse_timestamp(updated) if updated else None

        if cutoff and updated_dt and updated_dt < cutoff:
            continue

        authors = [
            clean_text(author.findtext("atom:name", default="", namespaces=ATOM_NS))
            for author in node.findall("atom:author", ATOM_NS)
        ]
        categories = [tag.attrib.get("term", "") for tag in node.findall("atom:category", ATOM_NS)]
        primary_category = ""
        primary_node = node.find("arxiv:primary_category", ATOM_NS)
        if primary_node is not None:
            primary_category = primary_node.attrib.get("term", "")

        abs_url = entry_id
        pdf_url = ""
        for link in node.findall("atom:link", ATOM_NS):
            href = link.attrib.get("href", "")
            if not href:
                continue
            if href.endswith(".pdf") or link.attrib.get("title") == "pdf":
                pdf_url = href
            if link.attrib.get("rel") == "alternate":
                abs_url = href

        entries.append(
            {
                "id": entry_id.rsplit("/", 1)[-1],
                "title": title,
                "summary": summary,
                "authors": authors,
                "published": published,
                "updated": updated,
                "primary_category": primary_category,
                "categories": categories,
                "abs_url": abs_url,
                "pdf_url": pdf_url,
            }
        )

    return entries


def build_snapshot(args: argparse.Namespace) -> dict[str, Any]:
    topics, days = load_topics(args)
    cutoff = datetime.now(timezone.utc) - timedelta(days=days) if days >= 0 else None

    snapshot_topics: list[dict[str, Any]] = []
    total_entries = 0

    for topic in topics:
        query = topic["query"]
        max_results = int(topic.get("max_results", args.max_results))

        if args.feed_file and args.query:
            xml_text = args.feed_file.read_text(encoding="utf-8")
        else:
            xml_text = fetch_xml(
                query,
                max_results=max_results,
                sort_by=args.sort_by,
                sort_order=args.sort_order,
            )

        entries = parse_feed(xml_text, cutoff)
        total_entries += len(entries)
        snapshot_topics.append(
            {
                "name": topic["name"],
                "query": query,
                "max_results": max_results,
                "entries": entries,
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "days": days,
        "source": "arXiv Atom API",
        "topic_count": len(snapshot_topics),
        "entry_count": total_entries,
        "topics": snapshot_topics,
    }


def main() -> None:
    args = parse_args()
    if args.feed_file and not args.query:
        raise SystemExit("--feed-file is only supported together with --query.")

    snapshot = build_snapshot(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
