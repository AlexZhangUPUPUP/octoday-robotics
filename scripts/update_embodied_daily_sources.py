from __future__ import annotations

import argparse
import html
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

import fetch_embodied_arxiv as arxiv_helpers


ROOT = Path(__file__).resolve().parents[1]
GENERATED_ROOT = ROOT / "generated" / "embodied-daily"
DAILY_PAPER_ROOT = ROOT / "daily-paper"
PAPERS_INDEX_PATH = ROOT / "03-papers.md"
README_PATH = ROOT / "README.md"
USER_AGENT = "octoday-robotics-embodied-daily/0.1 (+https://github.com/AlexZhangUPUPUP/octoday-robotics)"
SHANGHAI_TZ = timezone(timedelta(hours=8))

SOURCE_URLS = {
    "Embodied-AI-Daily": "https://raw.githubusercontent.com/luohongk/Embodied-AI-Daily/main/README.md",
    "arXiv cs.RO RSS": "https://rss.arxiv.org/rss/cs.RO",
    "awesome-daily-AI-arxiv": "https://raw.githubusercontent.com/Tavish9/awesome-daily-AI-arxiv/main/hot_topic/Embodied_AI.md",
}
SOURCE_PRIORITY = {
    "Embodied-AI-Daily": 0,
    "awesome-daily-AI-arxiv": 1,
    "arXiv cs.RO RSS": 2,
}

EMBODIED_KEYWORDS = [
    "embodied ai",
    "embodied intelligence",
    "vision-language-action",
    "vision language action",
    "vla",
    "vision-and-language navigation",
    "vision language navigation",
    "vln",
    "world model",
    "world models",
    "robot foundation model",
    "foundation model",
    "robot learning",
    "mobile manipulation",
    "robot manipulation",
    "dexterous manipulation",
    "manipulation",
    "grasp",
    "navigation",
    "slam",
    "visual slam",
    "visual inertial slam",
    "localization",
    "mapping",
    "place recognition",
    "loop closure",
    "humanoid robot",
    "humanoid",
    "visuomotor",
    "tactile",
    "sim2real",
    "teleoperation",
    "3d gaussian splatting",
    "gaussian splatting",
    "3d scene understanding",
    "robotic autonomy",
    "medical robotics",
]
WEAK_KEYWORDS = {
    "world model",
    "world models",
    "foundation model",
    "3d gaussian splatting",
    "gaussian splatting",
    "3d scene understanding",
}
RSS_KEYWORDS = [
    keyword
    for keyword in EMBODIED_KEYWORDS
    if keyword
    not in {
        "navigation",
        "localization",
        "mapping",
        "manipulation",
    }
]
SOURCE1_INCLUDE_SECTION_TERMS = (
    "vision and language navigation",
    "vision language action",
    "world model",
    "slam",
    "odometry",
    "place recognition",
    "loop closure",
    "3d gaussian splatting",
    "manipulation",
    "navigation",
    "robot",
)
SOURCE1_EXCLUDE_SECTION_TERMS = (
    "deep learning",
    "llm",
    "autonomous driving",
    "kalman filter",
)
EMBODIED_CONTEXT_TERMS = (
    "embodied",
    "robot",
    "robotic",
    "robotics",
    "manipulation",
    "grasp",
    "locomotion",
    "navigation",
    "slam",
    "localization",
    "mapping",
    "place recognition",
    "vla",
    "vln",
    "visuomotor",
    "tactile",
    "humanoid",
)


@dataclass
class SourcePaper:
    source: str
    source_url: str
    source_section: str
    title: str
    abs_url: str
    arxiv_id: str
    canonical_arxiv_id: str
    date: str
    summary: str
    authors: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)
    comment: str = ""
    matched_keywords: list[str] = field(default_factory=list)


@dataclass
class MergedPaper:
    arxiv_id: str
    title: str
    abs_url: str
    date: str
    summary: str
    authors: list[str]
    categories: list[str]
    matched_keywords: list[str]
    sources: list[str]
    source_sections: list[str]
    source_dates: dict[str, str]
    comments: dict[str, str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch embodied-AI papers from three public sources, dedupe them, and generate daily outputs."
    )
    parser.add_argument(
        "--lookback-days",
        type=int,
        default=3,
        help="How many recent UTC dates to keep in the merged daily output.",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=80,
        help="Maximum unique merged papers to keep after dedupe and sorting.",
    )
    parser.add_argument(
        "--abstract-chars",
        type=int,
        default=360,
        help="Maximum abstract length in markdown outputs.",
    )
    return parser.parse_args()


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def today_utc() -> date:
    return now_utc().date()


def now_shanghai() -> datetime:
    return now_utc().astimezone(SHANGHAI_TZ)


def today_shanghai() -> date:
    return now_shanghai().date()


def request_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read().decode("utf-8")


def normalize_text(value: str) -> str:
    return arxiv_helpers.normalize_text(value)


def canonical_arxiv_id(value: str) -> str:
    match = re.search(r"(\d{4}\.\d{4,5})(v\d+)?", value)
    if match:
        return match.group(1)
    return value.strip()


def canonical_abs_url(value: str) -> str:
    identifier = canonical_arxiv_id(value)
    return f"https://arxiv.org/abs/{identifier}"


def clean_markup(value: str) -> str:
    text = html.unescape(value or "")
    text = re.sub(r"<summary>.*?</summary>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"</?details[^>]*>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"</?p[^>]*>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("**", " ").replace("__", " ").replace("`", " ")
    return " ".join(text.split())


def parse_iso_date(value: str) -> date | None:
    clean = value.strip()
    if not clean:
        return None
    try:
        return date.fromisoformat(clean[:10])
    except ValueError:
        return None


def parse_rss_date(value: str) -> date | None:
    clean = value.strip()
    if not clean:
        return None
    try:
        return parsedate_to_datetime(clean).astimezone(timezone.utc).date()
    except (TypeError, ValueError):
        return None


def markdown_row_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def extract_title_and_url(cell: str) -> tuple[str, str] | None:
    match = re.search(r"\*\*\[(?P<title>.+?)\]\((?P<url>https://arxiv\.org/abs/[^)]+)\)\*\*", cell)
    if not match:
        return None
    return match.group("title").strip(), match.group("url").strip()


def matched_keywords(title: str, summary: str, keywords: list[str]) -> list[str]:
    return arxiv_helpers.matched_keywords(title, summary, keywords)


def has_embodied_context(title: str, summary: str) -> bool:
    haystack = normalize_text(f"{title} {summary}")
    for term in EMBODIED_CONTEXT_TERMS:
        if term in haystack:
            return True
    return False


def is_source1_section_relevant(section: str, title: str, summary: str, matches: list[str]) -> bool:
    normalized_section = normalize_text(section)
    if any(term in normalized_section for term in SOURCE1_EXCLUDE_SECTION_TERMS):
        return False

    strong_match = any(keyword not in WEAK_KEYWORDS for keyword in matches)
    if any(term in normalized_section for term in SOURCE1_INCLUDE_SECTION_TERMS):
        return has_embodied_context(title, summary) or strong_match
    return has_embodied_context(title, summary) and strong_match


def is_rss_paper_relevant(title: str, summary: str) -> list[str]:
    matches = matched_keywords(title, summary, RSS_KEYWORDS)
    if matches:
        return matches

    haystack = normalize_text(f"{title} {summary}")
    robot_terms = (
        "robot",
        "robotic",
        "robotics",
        "embodied",
        "humanoid",
        "uav",
        "drone",
        "multi-robot",
    )
    task_terms = (
        "manipulation",
        "grasp",
        "navigation",
        "localization",
        "mapping",
        "slam",
        "place recognition",
        "teleoperation",
        "locomotion",
        "tactile",
        "vision-language",
        "policy",
        "planner",
        "coordination",
        "robot learning",
    )

    if any(term in haystack for term in robot_terms) and any(term in haystack for term in task_terms):
        return ["robotics context"]
    return []


def parse_embodied_ai_daily(text: str, start_date: date) -> tuple[list[SourcePaper], int]:
    papers: list[SourcePaper] = []
    raw_count = 0
    current_section = ""

    for line in text.splitlines():
        if line.startswith("## "):
            current_section = line[3:].strip()
            continue
        if not line.startswith("| **["):
            continue

        raw_count += 1
        cells = markdown_row_cells(line)
        if len(cells) < 2:
            continue
        title_and_url = extract_title_and_url(cells[0])
        if title_and_url is None:
            continue

        title, abs_url = title_and_url
        paper_date = parse_iso_date(cells[1])
        if paper_date is None or paper_date < start_date:
            continue

        summary = clean_markup(cells[2]) if len(cells) > 2 else ""
        comment = clean_markup(cells[3]) if len(cells) > 3 else ""
        matches = matched_keywords(title, f"{summary} {comment}", EMBODIED_KEYWORDS)
        if not is_source1_section_relevant(current_section, title, summary, matches):
            continue

        papers.append(
            SourcePaper(
                source="Embodied-AI-Daily",
                source_url=SOURCE_URLS["Embodied-AI-Daily"],
                source_section=current_section,
                title=title,
                abs_url=canonical_abs_url(abs_url),
                arxiv_id=canonical_arxiv_id(abs_url),
                canonical_arxiv_id=canonical_arxiv_id(abs_url),
                date=paper_date.isoformat(),
                summary=summary,
                comment=comment,
                matched_keywords=matches,
            )
        )

    return papers, raw_count


def parse_awesome_embodied_ai(text: str, start_date: date) -> tuple[list[SourcePaper], int]:
    header_date_match = re.search(r"Embodied_AI Papers · (\d{4}-\d{2}-\d{2})", text)
    file_date = parse_iso_date(header_date_match.group(1)) if header_date_match else None
    if file_date is None:
        file_date = today_utc()

    raw_count = 0
    papers: list[SourcePaper] = []
    if file_date < start_date:
        return papers, raw_count

    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.startswith("- **["):
            index += 1
            continue

        raw_count += 1
        title_match = re.search(r"- \*\*\[(?P<title>.+?)\]\((?P<url>https://arxiv\.org/abs/[^)]+)\)\*\*", line)
        if title_match is None:
            index += 1
            continue

        title = title_match.group("title").strip()
        abs_url = canonical_abs_url(title_match.group("url").strip())
        tokens = re.findall(r"`([^`]+)`", line)
        categories = [token for token in tokens if not token.lower().startswith("arxiv:")]
        authors: list[str] = []
        summary_lines: list[str] = []
        index += 1

        if index < len(lines):
            author_line = lines[index].strip()
            if author_line.startswith("_") and author_line.endswith("_"):
                authors = [author.strip() for author in author_line.strip("_").split(",") if author.strip()]
                index += 1

        while index < len(lines):
            current = lines[index].strip()
            if current.startswith("- **["):
                break
            if current.startswith("<details") or current.startswith("<summary>") or current == "</details>":
                index += 1
                continue
            if current:
                summary_lines.append(current)
            index += 1

        summary = clean_markup(" ".join(summary_lines))
        matches = matched_keywords(title, summary, EMBODIED_KEYWORDS)
        if not matches and not has_embodied_context(title, summary):
            continue

        papers.append(
            SourcePaper(
                source="awesome-daily-AI-arxiv",
                source_url=SOURCE_URLS["awesome-daily-AI-arxiv"],
                source_section="Embodied_AI",
                title=title,
                abs_url=abs_url,
                arxiv_id=canonical_arxiv_id(abs_url),
                canonical_arxiv_id=canonical_arxiv_id(abs_url),
                date=file_date.isoformat(),
                summary=summary,
                authors=authors,
                categories=categories,
                matched_keywords=matches,
            )
        )

    return papers, raw_count


def parse_rss_source(text: str, start_date: date) -> tuple[list[SourcePaper], int]:
    root = ET.fromstring(text)
    items = root.findall("./channel/item")
    raw_count = len(items)
    papers: list[SourcePaper] = []

    for item in items:
        title = clean_markup(item.findtext("title", default=""))
        abs_url = canonical_abs_url(item.findtext("link", default=""))
        pub_date = parse_rss_date(item.findtext("pubDate", default=""))
        if pub_date is None or pub_date < start_date:
            continue

        description = clean_markup(item.findtext("description", default=""))
        summary = description.split("Abstract:", 1)[1].strip() if "Abstract:" in description else description
        matches = is_rss_paper_relevant(title, summary)
        if not matches:
            continue

        categories = [clean_markup(category.text or "") for category in item.findall("category") if category.text]
        papers.append(
            SourcePaper(
                source="arXiv cs.RO RSS",
                source_url=SOURCE_URLS["arXiv cs.RO RSS"],
                source_section="cs.RO",
                title=title,
                abs_url=abs_url,
                arxiv_id=canonical_arxiv_id(abs_url),
                canonical_arxiv_id=canonical_arxiv_id(abs_url),
                date=pub_date.isoformat(),
                summary=summary,
                authors=[author.strip() for author in clean_markup(item.findtext("{http://purl.org/dc/elements/1.1/}creator", default="")).split(",") if author.strip()],
                categories=categories,
                comment=clean_markup(item.findtext("{http://arxiv.org/schemas/atom}announce_type", default="")),
                matched_keywords=matches,
            )
        )

    return papers, raw_count


def dedupe_and_merge(papers: list[SourcePaper], max_results: int) -> list[MergedPaper]:
    merged: dict[str, MergedPaper] = {}

    papers.sort(
        key=lambda paper: (
            paper.date,
            -SOURCE_PRIORITY.get(paper.source, 99),
            paper.title.lower(),
        ),
        reverse=True,
    )

    for paper in papers:
        key = paper.canonical_arxiv_id
        if key not in merged:
            merged[key] = MergedPaper(
                arxiv_id=paper.canonical_arxiv_id,
                title=paper.title,
                abs_url=paper.abs_url,
                date=paper.date,
                summary=paper.summary,
                authors=list(paper.authors),
                categories=list(dict.fromkeys(paper.categories)),
                matched_keywords=list(dict.fromkeys(paper.matched_keywords)),
                sources=[paper.source],
                source_sections=[f"{paper.source}: {paper.source_section}"],
                source_dates={paper.source: paper.date},
                comments={paper.source: paper.comment} if paper.comment else {},
            )
            continue

        existing = merged[key]
        if len(paper.summary) > len(existing.summary):
            existing.summary = paper.summary
        if SOURCE_PRIORITY.get(paper.source, 99) < min(
            SOURCE_PRIORITY.get(source, 99) for source in existing.sources
        ):
            existing.title = paper.title
        if paper.date > existing.date:
            existing.date = paper.date

        for author in paper.authors:
            if author not in existing.authors:
                existing.authors.append(author)
        for category in paper.categories:
            if category and category not in existing.categories:
                existing.categories.append(category)
        for keyword in paper.matched_keywords:
            if keyword not in existing.matched_keywords:
                existing.matched_keywords.append(keyword)
        if paper.source not in existing.sources:
            existing.sources.append(paper.source)
        section_label = f"{paper.source}: {paper.source_section}"
        if section_label not in existing.source_sections:
            existing.source_sections.append(section_label)
        existing.source_dates[paper.source] = paper.date
        if paper.comment:
            existing.comments[paper.source] = paper.comment

    merged_papers = list(merged.values())
    merged_papers.sort(key=lambda paper: (paper.date, len(paper.sources), paper.title.lower()), reverse=True)
    return merged_papers[:max_results]


def suggest_section(title: str, summary: str, categories: list[str]) -> str:
    title_haystack = normalize_text(title)
    haystack = normalize_text(f"{title} {summary} {' '.join(categories)}")

    if any(term in title_haystack for term in ("survey", "systematic review", "research roadmap", "overview")):
        return "Survey"
    if any(term in title_haystack for term in ("dataset", "benchmark", "suite", "evaluation")):
        return "Benchmarks & Evaluation"
    if any(term in haystack for term in ("safety", "safe", "compliance", "risk")):
        return "Embodied Safety & Alignment"
    if any(term in haystack for term in ("human-robot", "hri", "multi-robot", "swarm")):
        return "Multi-Robot Systems & HRI"
    if any(term in haystack for term in ("vision-language-action", "vision language action", "vla")):
        return "Vision-Language-Action (VLA)"
    if any(term in haystack for term in ("world model", "foundation model", "generalist", "post-training")):
        return "Embodied Foundation Models"
    if any(term in haystack for term in ("navigation", "slam", "localization", "mapping", "place recognition", "vln")):
        return "Navigation & Spatial Intelligence"
    if any(term in haystack for term in ("manipulation", "grasp", "dexterous", "tactile")):
        return "Manipulation"
    if any(term in haystack for term in ("agent", "planner", "planning", "reasoning", "long-horizon")):
        return "Embodied Agents & Reasoning"
    if "cs.RO" in categories:
        return "Manipulation"
    return "Embodied Agents & Reasoning"


def shorten(text: str, limit: int) -> str:
    if limit <= 0 or len(text) <= limit:
        return text
    return text[: max(0, limit - 1)].rstrip() + "…"


def render_markdown(
    merged_papers: list[MergedPaper],
    start_date: date,
    end_date: date,
    raw_counts: dict[str, int],
    kept_counts: dict[str, int],
    abstract_chars: int,
) -> str:
    lines = [
        "# Daily Merged Embodied AI Papers",
        "",
        f"- Generated at (UTC): {now_utc().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- Window (UTC dates): {start_date.isoformat()} to {end_date.isoformat()}",
        "- Sources:",
        f"  - [Embodied-AI-Daily README]({SOURCE_URLS['Embodied-AI-Daily']})",
        f"  - [arXiv cs.RO RSS]({SOURCE_URLS['arXiv cs.RO RSS']})",
        f"  - [awesome-daily-AI-arxiv Embodied_AI.md]({SOURCE_URLS['awesome-daily-AI-arxiv']})",
        f"- Dedupe key: canonical arXiv id (version suffix stripped)",
        f"- Unique papers: {len(merged_papers)}",
        "",
        "## Source Stats",
        "",
        "| Source | Raw Entries | After Filter |",
        "| --- | ---: | ---: |",
    ]

    for source_name in SOURCE_URLS:
        lines.append(f"| {source_name} | {raw_counts.get(source_name, 0)} | {kept_counts.get(source_name, 0)} |")

    lines.append("")
    if not merged_papers:
        lines.append("No matching papers were found in this window.")
        return "\n".join(lines) + "\n"

    for index, paper in enumerate(merged_papers, start=1):
        lines.extend(
            [
                f"## {index}. {paper.title}",
                "",
                f"- arXiv: `{paper.arxiv_id}`",
                f"- Date: {paper.date}",
                f"- Sources: {', '.join(f'`{source}`' for source in paper.sources)}",
                f"- Source Sections: {', '.join(f'`{section}`' for section in paper.source_sections)}",
                f"- Categories: {', '.join(paper.categories) if paper.categories else 'N/A'}",
                f"- Matched Keywords: {', '.join(paper.matched_keywords) if paper.matched_keywords else 'N/A'}",
                f"- Links: [abs]({paper.abs_url}) | [pdf]({paper.abs_url.replace('/abs/', '/pdf/')})",
                f"- Summary: {shorten(paper.summary, abstract_chars)}",
            ]
        )
        if paper.comments:
            notes = " | ".join(f"{source}: {comment}" for source, comment in paper.comments.items())
            lines.append(f"- Notes: {notes}")
        lines.append("")

    return "\n".join(lines)


def render_json(
    merged_papers: list[MergedPaper],
    start_date: date,
    end_date: date,
    raw_counts: dict[str, int],
    kept_counts: dict[str, int],
) -> str:
    payload = {
        "generated_at_utc": now_utc().isoformat(),
        "window": {
            "start_date_utc": start_date.isoformat(),
            "end_date_utc": end_date.isoformat(),
        },
        "dedupe_key": "canonical_arxiv_id_without_version",
        "sources": {
            source: {
                "url": SOURCE_URLS[source],
                "raw_entries": raw_counts.get(source, 0),
                "after_filter": kept_counts.get(source, 0),
            }
            for source in SOURCE_URLS
        },
        "count": len(merged_papers),
        "papers": [asdict(paper) for paper in merged_papers],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def render_candidates_markdown(
    merged_papers: list[MergedPaper],
    start_date: date,
    end_date: date,
) -> str:
    grouped: dict[str, list[MergedPaper]] = {section: [] for section in arxiv_helpers.SECTION_ORDER}
    for paper in merged_papers:
        grouped[suggest_section(paper.title, paper.summary, paper.categories)].append(paper)

    lines = [
        "# Candidates for 03-papers.md from Daily Merged Sources",
        "",
        f"- Window (UTC dates): {start_date.isoformat()} to {end_date.isoformat()}",
        f"- Candidates: {len(merged_papers)}",
        "",
        "> 说明：这是自动合并后的候选清单。建议人工补中文摘要后再并入 `03-papers.md`。",
        "",
    ]

    if not merged_papers:
        lines.append("No candidate papers were found in this window.")
        return "\n".join(lines) + "\n"

    for section in arxiv_helpers.SECTION_ORDER:
        section_papers = grouped.get(section, [])
        if not section_papers:
            continue
        lines.append(f"## {section}")
        lines.append("")
        for paper in section_papers:
            lines.append(f"- [{paper.title}]({paper.abs_url})")
            lines.append(
                f"  arXiv: `{paper.arxiv_id}` | Date: {paper.date} | Sources: {', '.join(paper.sources)}"
            )
            lines.append(
                "  可复制条目："
                f"`- **[arXiv {paper.date[:4]}年{int(paper.date[5:7])}月]** {paper.title}. 待补人工中文摘要. [link]({paper.abs_url})`"
            )
            lines.append("")

    return "\n".join(lines)


def render_readme() -> str:
    return "\n".join(
        [
            "# Generated Daily Embodied Paper Merge",
            "",
            "This directory stores the daily merged embodied-AI paper feed built from three public sources.",
            "",
            "Sources:",
            f"- [Embodied-AI-Daily README]({SOURCE_URLS['Embodied-AI-Daily']})",
            f"- [arXiv cs.RO RSS]({SOURCE_URLS['arXiv cs.RO RSS']})",
            f"- [awesome-daily-AI-arxiv Embodied_AI.md]({SOURCE_URLS['awesome-daily-AI-arxiv']})",
            "",
            "Outputs:",
            "- `daily/latest.md`: merged markdown snapshot",
            "- `daily/latest.json`: merged JSON snapshot",
            "- `daily/candidates-for-03-papers.md`: candidate list for `03-papers.md`",
            "",
            "Deduplication rule:",
            "- Papers are deduped by canonical arXiv id with the version suffix removed.",
            "",
            "Generation script:",
            "- `scripts/update_embodied_daily_sources.py`",
            "",
        ]
    )


def daily_snapshot_filename(run_date: date) -> str:
    return f"{str(run_date.year)[2:]}-{run_date.month}-{run_date.day}paper.md"


def render_03_papers_entry(paper: MergedPaper) -> str:
    return (
        f"- **[arXiv {paper.date[:4]}年{int(paper.date[5:7])}月]** {paper.title}. "
        f"来自每日自动抓取去重，待补人工中文摘要. [link]({paper.abs_url})"
    )


def extract_existing_arxiv_ids(text: str) -> set[str]:
    return {
        canonical_arxiv_id(url)
        for url in re.findall(r"https?://arxiv\.org/abs/[^\s)]+", text)
    }


def replace_paper_count(text: str, paper_count: int) -> str:
    return re.sub(
        r"当前共收录 `\d+` 条论文相关资源，覆盖 `\d+` 个研究主题板块。",
        f"当前共收录 `{paper_count}` 条论文相关资源，覆盖 `11` 个研究主题板块。",
        text,
        count=1,
    )


def update_03_papers_index(merged_papers: list[MergedPaper]) -> tuple[list[MergedPaper], int]:
    if not PAPERS_INDEX_PATH.exists():
        return [], 0

    text = PAPERS_INDEX_PATH.read_text(encoding="utf-8")
    existing_ids = extract_existing_arxiv_ids(text)
    new_papers = [
        paper
        for paper in merged_papers
        if paper.arxiv_id not in existing_ids
        and (
            len(paper.sources) >= 2
            or any(source in {"Embodied-AI-Daily", "awesome-daily-AI-arxiv"} for source in paper.sources)
        )
    ]
    if not new_papers:
        paper_count = sum(1 for line in text.splitlines() if line.startswith("- **["))
        return [], paper_count

    grouped: dict[str, list[str]] = {section: [] for section in arxiv_helpers.SECTION_ORDER}
    for paper in new_papers:
        grouped[suggest_section(paper.title, paper.summary, paper.categories)].append(render_03_papers_entry(paper))

    for section in arxiv_helpers.SECTION_ORDER:
        entries = grouped[section]
        if not entries:
            continue
        block = "\n".join(entries) + "\n"
        pattern = re.compile(rf"(^# {re.escape(section)}\n\n)", flags=re.MULTILINE)
        text, replaced = pattern.subn(lambda match, block=block: match.group(1) + block, text, count=1)
        if replaced == 0:
            raise SystemExit(f"Could not find section heading in 03-papers.md: {section}")

    paper_count = sum(1 for line in text.splitlines() if line.startswith("- **["))
    PAPERS_INDEX_PATH.write_text(replace_paper_count(text, paper_count), encoding="utf-8")
    return new_papers, paper_count


def update_readme_paper_count(paper_count: int) -> None:
    if not README_PATH.exists():
        return
    text = README_PATH.read_text(encoding="utf-8")
    README_PATH.write_text(replace_paper_count(text, paper_count), encoding="utf-8")


def render_dated_snapshot_markdown(
    run_date: date,
    merged_papers: list[MergedPaper],
    new_papers: list[MergedPaper],
    start_date: date,
    end_date: date,
) -> str:
    grouped: dict[str, list[MergedPaper]] = {section: [] for section in arxiv_helpers.SECTION_ORDER}
    for paper in merged_papers:
        grouped[suggest_section(paper.title, paper.summary, paper.categories)].append(paper)

    lines = [
        f"# Daily Paper · {run_date.isoformat()}",
        "",
        f"- Local date (Asia/Shanghai): {run_date.isoformat()}",
        f"- Source window (UTC dates): {start_date.isoformat()} to {end_date.isoformat()}",
        f"- Merged papers today: {len(merged_papers)}",
        f"- Newly merged into `03-papers.md`: {len(new_papers)}",
        f"- Generated daily file: `daily-paper/{daily_snapshot_filename(run_date)}`",
        "",
        "## New Papers Added to 03-papers.md",
        "",
    ]

    if not new_papers:
        lines.append("No new unique papers were added to `03-papers.md` in this run.")
        lines.append("")
    else:
        for paper in new_papers:
            lines.append(f"- [{paper.title}]({paper.abs_url})")
            lines.append(f"  arXiv: `{paper.arxiv_id}` | Date: {paper.date} | Sources: {', '.join(paper.sources)}")
            lines.append("")

    lines.extend(
        [
            "## Full Daily Merge",
            "",
            "> 说明：以下为三源去重后的当日候选池，未必都已并入主表的人工精选语境。",
            "",
        ]
    )

    for section in arxiv_helpers.SECTION_ORDER:
        section_papers = grouped[section]
        if not section_papers:
            continue
        lines.append(f"## {section}")
        lines.append("")
        for paper in section_papers:
            lines.append(f"- [{paper.title}]({paper.abs_url})")
            lines.append(
                f"  arXiv: `{paper.arxiv_id}` | Date: {paper.date} | Sources: {', '.join(paper.sources)}"
            )
            lines.append("")

    return "\n".join(lines) + "\n"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")


def main() -> int:
    args = parse_args()
    if args.lookback_days <= 0:
        raise SystemExit("--lookback-days must be greater than 0.")
    if args.max_results <= 0:
        raise SystemExit("--max-results must be greater than 0.")

    end_date = today_utc()
    start_date = end_date - timedelta(days=args.lookback_days - 1)

    embodied_text = request_text(SOURCE_URLS["Embodied-AI-Daily"])
    rss_text = request_text(SOURCE_URLS["arXiv cs.RO RSS"])
    awesome_text = request_text(SOURCE_URLS["awesome-daily-AI-arxiv"])

    source1_papers, source1_raw = parse_embodied_ai_daily(embodied_text, start_date)
    rss_papers, rss_raw = parse_rss_source(rss_text, start_date)
    source3_papers, source3_raw = parse_awesome_embodied_ai(awesome_text, start_date)

    merged_papers = dedupe_and_merge(
        source1_papers + rss_papers + source3_papers,
        max_results=args.max_results,
    )
    new_papers, paper_count = update_03_papers_index(merged_papers)
    update_readme_paper_count(paper_count)

    raw_counts = {
        "Embodied-AI-Daily": source1_raw,
        "arXiv cs.RO RSS": rss_raw,
        "awesome-daily-AI-arxiv": source3_raw,
    }
    kept_counts = {
        "Embodied-AI-Daily": len(source1_papers),
        "arXiv cs.RO RSS": len(rss_papers),
        "awesome-daily-AI-arxiv": len(source3_papers),
    }
    write_text(
        DAILY_PAPER_ROOT / daily_snapshot_filename(today_shanghai()),
        render_dated_snapshot_markdown(
            run_date=today_shanghai(),
            merged_papers=merged_papers,
            new_papers=new_papers,
            start_date=start_date,
            end_date=end_date,
        ),
    )

    daily_dir = GENERATED_ROOT / "daily"
    write_text(
        daily_dir / "latest.md",
        render_markdown(
            merged_papers=merged_papers,
            start_date=start_date,
            end_date=end_date,
            raw_counts=raw_counts,
            kept_counts=kept_counts,
            abstract_chars=args.abstract_chars,
        ),
    )
    write_text(
        daily_dir / "latest.json",
        render_json(
            merged_papers=merged_papers,
            start_date=start_date,
            end_date=end_date,
            raw_counts=raw_counts,
            kept_counts=kept_counts,
        ),
    )
    write_text(
        daily_dir / "candidates-for-03-papers.md",
        render_candidates_markdown(
            merged_papers=merged_papers,
            start_date=start_date,
            end_date=end_date,
        ),
    )
    write_text(GENERATED_ROOT / "README.md", render_readme())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
