from __future__ import annotations

"""
Fetch the latest embodied-AI-related papers from arXiv.

Official references:
- arXiv API Basics: https://info.arxiv.org/help/api/basics.html
- arXiv API User's Manual: https://info.arxiv.org/help/api/user-manual.html
- arXiv API Terms of Use: https://info.arxiv.org/help/api/tou.html
- arXiv submission availability: https://info.arxiv.org/help/availability.html

Examples:
  python3 scripts/fetch_embodied_arxiv.py --window day --max-results 20
  python3 scripts/fetch_embodied_arxiv.py --window week --format json --output out/embodied-week.json
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path


API_URL = "https://export.arxiv.org/api/query"
USER_AGENT = "octoday-robotics-arxiv-fetcher/0.1 (+https://github.com/AlexZhangUPUPUP/octoday-robotics)"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
SECTION_ORDER = [
    "Embodied Foundation Models",
    "Vision-Language-Action (VLA)",
    "Embodied Agents & Reasoning",
    "Manipulation",
    "Navigation & Spatial Intelligence",
    "Multi-Robot Systems & HRI",
    "Simulation & Sim2Real",
    "Datasets",
    "Benchmarks & Evaluation",
    "Embodied Safety & Alignment",
    "Survey",
]

DEFAULT_CATEGORIES = ["cs.RO", "cs.AI", "cs.CV", "cs.LG"]
DEFAULT_KEYWORDS = [
    "embodied ai",
    "embodied intelligence",
    "vision-language-action",
    "vision language action",
    "vla",
    "world model",
    "robot foundation model",
    "robot learning",
    "visuomotor",
    "mobile manipulation",
    "robot manipulation",
    "humanoid robot",
    "dexterous manipulation",
    "sim2real",
    "tactile",
]
DEFAULT_CONTEXT_TERMS = [
    "embodied",
    "robot",
    "robotic",
    "robotics",
    "manipulation",
    "navigation",
    "humanoid",
    "visuomotor",
    "tactile",
    "grasp",
    "gripper",
    "locomotion",
]


@dataclass
class Paper:
    arxiv_id: str
    title: str
    summary: str
    authors: list[str]
    published: str
    updated: str
    primary_category: str
    categories: list[str]
    abs_url: str
    pdf_url: str
    matched_keywords: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch the latest embodied-AI-related papers from arXiv."
    )
    parser.add_argument(
        "--window",
        choices=("day", "week"),
        default="week",
        help="Relative time window in UTC. Ignored if --days is provided.",
    )
    parser.add_argument(
        "--days",
        type=int,
        help="Custom lookback window in days, counted backwards from now in UTC.",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=50,
        help="Maximum number of papers to return after filtering.",
    )
    parser.add_argument(
        "--fetch-size",
        type=int,
        default=200,
        help="How many candidates to request from arXiv before local filtering.",
    )
    parser.add_argument(
        "--categories",
        nargs="*",
        default=DEFAULT_CATEGORIES,
        help="arXiv categories to search, for example cs.RO cs.AI cs.CV cs.LG.",
    )
    parser.add_argument(
        "--keywords",
        nargs="*",
        default=DEFAULT_KEYWORDS,
        help="Keyword phrases used for API query construction and local matching.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json", "candidates"),
        default="markdown",
        help="Output format.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output file path. If omitted, print to stdout.",
    )
    parser.add_argument(
        "--abstract-chars",
        type=int,
        default=280,
        help="Maximum abstract length in markdown mode.",
    )
    return parser.parse_args()


def resolve_window_days(args: argparse.Namespace) -> int:
    if args.days is not None:
        if args.days <= 0:
            raise SystemExit("--days must be greater than 0.")
        return args.days
    return 1 if args.window == "day" else 7


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def arxiv_timestamp(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y%m%d%H%M")


def quote_term(term: str) -> str:
    clean = term.strip()
    if not clean:
        return ""
    if any(ch.isspace() for ch in clean) or "-" in clean:
        escaped = clean.replace('"', '\\"')
        return f'"{escaped}"'
    return clean


def build_field_query(prefix: str, term: str) -> str:
    quoted = quote_term(term)
    return f"{prefix}:{quoted}"


def build_or_group(parts: list[str]) -> str:
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0]
    return f"({' OR '.join(parts)})"


def build_search_query(categories: list[str], keywords: list[str], start: datetime, end: datetime) -> str:
    category_expr = build_or_group([f"cat:{category}" for category in categories])
    keyword_expr = build_or_group([build_field_query("all", keyword) for keyword in keywords])
    date_expr = f"submittedDate:[{arxiv_timestamp(start)} TO {arxiv_timestamp(end)}]"

    parts = [date_expr]
    if category_expr:
        parts.append(category_expr)
    if keyword_expr:
        parts.append(keyword_expr)
    return " AND ".join(parts)


def build_request_url(search_query: str, start_index: int, page_size: int) -> str:
    params = {
        "search_query": search_query,
        "start": start_index,
        "max_results": page_size,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    return f"{API_URL}?{urllib.parse.urlencode(params)}"


def request_feed(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def parse_datetime(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def normalize_text(value: str) -> str:
    return " ".join(value.lower().split())


def matched_keywords(title: str, summary: str, keywords: list[str]) -> list[str]:
    haystack = normalize_text(f"{title} {summary}")
    matches: list[str] = []
    for keyword in keywords:
        needle = normalize_text(keyword)
        if not needle:
            continue
        if " " in needle or "-" in needle:
            matched = needle in haystack
        else:
            matched = re.search(rf"\b{re.escape(needle)}\b", haystack) is not None
        if matched:
            matches.append(keyword)
    return matches


def has_embodied_context(paper: Paper) -> bool:
    if paper.primary_category == "cs.RO" or "cs.RO" in paper.categories:
        return True

    haystack = normalize_text(f"{paper.title} {paper.summary}")
    for term in DEFAULT_CONTEXT_TERMS:
        if re.search(rf"\b{re.escape(term)}\b", haystack):
            return True
    return False


def entry_text(entry: ET.Element, path: str) -> str:
    element = entry.find(path, ATOM_NS)
    return "" if element is None or element.text is None else " ".join(element.text.split())


def parse_papers(xml_bytes: bytes, keywords: list[str]) -> tuple[list[Paper], int]:
    root = ET.fromstring(xml_bytes)
    total_results_text = root.findtext("atom:totalResults", namespaces=ATOM_NS)
    if total_results_text is None:
        total_results_text = root.findtext("{http://a9.com/-/spec/opensearch/1.1/}totalResults", default="0")
    total_results = int(total_results_text)

    papers: list[Paper] = []
    for entry in root.findall("atom:entry", ATOM_NS):
        title = entry_text(entry, "atom:title")
        summary = entry_text(entry, "atom:summary")
        abs_url = ""
        pdf_url = ""
        for link in entry.findall("atom:link", ATOM_NS):
            href = link.attrib.get("href", "")
            rel = link.attrib.get("rel", "")
            link_title = link.attrib.get("title", "")
            if rel == "alternate" and href:
                abs_url = href
            if link_title == "pdf" and href:
                pdf_url = href

        authors = [entry_text(author, "atom:name") for author in entry.findall("atom:author", ATOM_NS)]
        categories = [category.attrib.get("term", "") for category in entry.findall("atom:category", ATOM_NS)]
        primary_category = ""
        primary = entry.find("arxiv:primary_category", ATOM_NS)
        if primary is not None:
            primary_category = primary.attrib.get("term", "")

        paper = Paper(
            arxiv_id=abs_url.rsplit("/", 1)[-1] if abs_url else entry_text(entry, "atom:id").rsplit("/", 1)[-1],
            title=title,
            summary=summary,
            authors=[author for author in authors if author],
            published=entry_text(entry, "atom:published"),
            updated=entry_text(entry, "atom:updated"),
            primary_category=primary_category,
            categories=[category for category in categories if category],
            abs_url=abs_url,
            pdf_url=pdf_url,
            matched_keywords=matched_keywords(title, summary, keywords),
        )
        papers.append(paper)
    return papers, total_results


def fetch_papers(search_query: str, fetch_size: int, keywords: list[str]) -> list[Paper]:
    if fetch_size <= 0:
        raise SystemExit("--fetch-size must be greater than 0.")
    if fetch_size > 30000:
        raise SystemExit("--fetch-size cannot exceed 30000 due to arXiv API limits.")

    url = build_request_url(search_query, start_index=0, page_size=fetch_size)
    xml_bytes = request_feed(url)
    papers, _ = parse_papers(xml_bytes, keywords)
    return papers


def filter_and_sort(
    papers: list[Paper],
    start_dt: datetime,
    end_dt: datetime,
    max_results: int,
) -> list[Paper]:
    filtered: list[Paper] = []
    seen_ids: set[str] = set()

    for paper in papers:
        published_dt = parse_datetime(paper.published)
        if not (start_dt <= published_dt <= end_dt):
            continue
        if not paper.matched_keywords:
            continue
        if not has_embodied_context(paper):
            continue
        if paper.arxiv_id in seen_ids:
            continue
        seen_ids.add(paper.arxiv_id)
        filtered.append(paper)

    filtered.sort(key=lambda paper: (paper.published, len(paper.matched_keywords)), reverse=True)
    return filtered[:max_results]


def suggest_section(paper: Paper) -> str:
    title_haystack = normalize_text(paper.title)
    haystack = normalize_text(f"{paper.title} {paper.summary}")

    if any(term in title_haystack for term in ("survey", "systematic review", "comprehensive review", "overview")):
        return "Survey"
    if any(term in title_haystack for term in ("dataset", "corpus", "annotation", "data collection")):
        return "Datasets"
    if any(term in title_haystack for term in ("benchmark", "evaluation", "eval", "metric", "score", "leaderboard")):
        return "Benchmarks & Evaluation"
    if any(term in title_haystack for term in ("sim2real", "simulation", "simulator", "synthetic data", "real2sim")):
        return "Simulation & Sim2Real"
    if any(term in haystack for term in ("safety", "safe", "alignment", "iso-compliant", "risk")):
        return "Embodied Safety & Alignment"
    if any(term in haystack for term in ("multi-robot", "swarm", "human-robot", "hri", "collaboration")):
        return "Multi-Robot Systems & HRI"
    if any(term in haystack for term in ("navigation", "slam", "localization", "mapping", "spatial", "vln")):
        return "Navigation & Spatial Intelligence"
    if any(term in haystack for term in ("vision-language-action", "vision language action", "vla")):
        return "Vision-Language-Action (VLA)"
    if any(term in haystack for term in ("world model", "foundation model", "generalist", "post-training", "robot foundation model")):
        return "Embodied Foundation Models"
    if any(term in haystack for term in ("manipulation", "grasp", "gripper", "dexterous", "pick and place", "fingertip")):
        return "Manipulation"
    if any(term in haystack for term in ("agent", "reasoning", "planner", "planning", "long-horizon")):
        return "Embodied Agents & Reasoning"
    if paper.primary_category == "cs.RO":
        return "Manipulation"
    return "Embodied Agents & Reasoning"


def candidate_reason(paper: Paper) -> str:
    reasons: list[str] = []
    if paper.primary_category:
        reasons.append(f"主分类 `{paper.primary_category}`")
    if paper.matched_keywords:
        reasons.append("命中关键词 " + ", ".join(f"`{keyword}`" for keyword in paper.matched_keywords))
    return "；".join(reasons) if reasons else "命中默认具身过滤规则"


def format_entry_prefix(paper: Paper) -> str:
    published_dt = parse_datetime(paper.published)
    return f"[arXiv {published_dt.year}年{published_dt.month}月]"


def render_copyable_entry(paper: Paper) -> str:
    return (
        f"- **{format_entry_prefix(paper)}** {paper.title}. "
        f"待补人工中文摘要. [link]({paper.abs_url})"
    )


def shorten(text: str, limit: int) -> str:
    if limit <= 0 or len(text) <= limit:
        return text
    return text[: max(0, limit - 1)].rstrip() + "…"


def render_markdown(
    papers: list[Paper],
    search_query: str,
    categories: list[str],
    keywords: list[str],
    start_dt: datetime,
    end_dt: datetime,
    abstract_chars: int,
) -> str:
    lines = [
        "# Latest Embodied AI Papers from arXiv",
        "",
        f"- Window (UTC): {start_dt.strftime('%Y-%m-%d %H:%M')} to {end_dt.strftime('%Y-%m-%d %H:%M')}",
        f"- Categories: {', '.join(categories)}",
        f"- Keywords: {', '.join(keywords)}",
        f"- Search query: `{search_query}`",
        f"- Papers: {len(papers)}",
        "",
    ]

    if not papers:
        lines.append("No matching papers were found in this window.")
        return "\n".join(lines) + "\n"

    for index, paper in enumerate(papers, start=1):
        lines.extend(
            [
                f"## {index}. {paper.title}",
                "",
                f"- arXiv: `{paper.arxiv_id}`",
                f"- Published: {paper.published}",
                f"- Updated: {paper.updated}",
                f"- Authors: {', '.join(paper.authors)}",
                f"- Primary category: {paper.primary_category or 'N/A'}",
                f"- Categories: {', '.join(paper.categories)}",
                f"- Matched keywords: {', '.join(paper.matched_keywords)}",
                f"- Links: [abs]({paper.abs_url}) | [pdf]({paper.pdf_url})",
                f"- Summary: {shorten(paper.summary, abstract_chars)}",
                "",
            ]
        )
    return "\n".join(lines)


def render_json(
    papers: list[Paper],
    search_query: str,
    categories: list[str],
    keywords: list[str],
    start_dt: datetime,
    end_dt: datetime,
) -> str:
    payload = {
        "generated_at_utc": now_utc().isoformat(),
        "window": {
            "start_utc": start_dt.isoformat(),
            "end_utc": end_dt.isoformat(),
        },
        "categories": categories,
        "keywords": keywords,
        "search_query": search_query,
        "count": len(papers),
        "papers": [asdict(paper) for paper in papers],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def render_candidates_markdown(
    papers: list[Paper],
    search_query: str,
    categories: list[str],
    keywords: list[str],
    start_dt: datetime,
    end_dt: datetime,
) -> str:
    grouped: dict[str, list[Paper]] = {section: [] for section in SECTION_ORDER}
    for paper in papers:
        grouped[suggest_section(paper)].append(paper)

    lines = [
        "# Candidates for 03-papers.md",
        "",
        f"- Window (UTC): {start_dt.strftime('%Y-%m-%d %H:%M')} to {end_dt.strftime('%Y-%m-%d %H:%M')}",
        f"- Categories: {', '.join(categories)}",
        f"- Keywords: {', '.join(keywords)}",
        f"- Search query: `{search_query}`",
        f"- Candidates: {len(papers)}",
        "",
        "> 说明：这是自动生成的候选清单。建议人工补中文摘要后再并入 `03-papers.md`。",
        "",
    ]

    if not papers:
        lines.append("No candidate papers were found in this window.")
        return "\n".join(lines) + "\n"

    for section in SECTION_ORDER:
        section_papers = grouped[section]
        if not section_papers:
            continue
        lines.append(f"## {section}")
        lines.append("")
        for paper in section_papers:
            lines.append(f"- [{paper.title}]({paper.abs_url})")
            lines.append(f"  arXiv: `{paper.arxiv_id}` | Published: {paper.published[:10]} | {candidate_reason(paper)}")
            lines.append(f"  可复制条目：`{render_copyable_entry(paper)}`")
            lines.append("")
    return "\n".join(lines)


def write_output(content: str, output_path: Path | None) -> None:
    if output_path is None:
        sys.stdout.write(content)
        return
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"Wrote {output_path}")


def main() -> int:
    args = parse_args()
    days = resolve_window_days(args)
    end_dt = now_utc()
    start_dt = end_dt - timedelta(days=days)

    search_query = build_search_query(
        categories=args.categories,
        keywords=args.keywords,
        start=start_dt,
        end=end_dt,
    )

    try:
        candidates = fetch_papers(
            search_query=search_query,
            fetch_size=args.fetch_size,
            keywords=args.keywords,
        )
    except urllib.error.HTTPError as exc:
        print(f"arXiv API HTTP error: {exc.code} {exc.reason}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"arXiv API connection error: {exc.reason}", file=sys.stderr)
        return 1

    papers = filter_and_sort(
        papers=candidates,
        start_dt=start_dt,
        end_dt=end_dt,
        max_results=args.max_results,
    )

    if args.format == "json":
        content = render_json(
            papers=papers,
            search_query=search_query,
            categories=args.categories,
            keywords=args.keywords,
            start_dt=start_dt,
            end_dt=end_dt,
        )
    elif args.format == "candidates":
        content = render_candidates_markdown(
            papers=papers,
            search_query=search_query,
            categories=args.categories,
            keywords=args.keywords,
            start_dt=start_dt,
            end_dt=end_dt,
        )
    else:
        content = render_markdown(
            papers=papers,
            search_query=search_query,
            categories=args.categories,
            keywords=args.keywords,
            start_dt=start_dt,
            end_dt=end_dt,
            abstract_chars=args.abstract_chars,
        )

    write_output(content, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
