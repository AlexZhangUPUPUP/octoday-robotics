#!/usr/bin/env python3
"""Generate a weekly markdown digest from fetched paper snapshots."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "weekly" / "templates" / "weekly-template.md"
DEFAULT_PAPERS = ROOT / "weekly" / "data" / "latest_arxiv.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a weekly markdown digest from normalized paper JSON."
    )
    parser.add_argument("--papers-json", type=Path, default=DEFAULT_PAPERS)
    parser.add_argument("--signals-file", type=Path)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--date", help="Digest date in YYYY-MM-DD format.")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--top-per-topic", type=int, default=2)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def parse_digest_date(raw_value: str | None) -> date:
    if not raw_value:
        return date.today()
    return datetime.strptime(raw_value, "%Y-%m-%d").date()


def load_json(path: Path | None) -> dict[str, Any]:
    if not path or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def iso_week_path(digest_date: date) -> Path:
    iso_year, iso_week, _ = digest_date.isocalendar()
    return ROOT / "weekly" / str(iso_year) / f"week-{iso_week:02d}.md"


def short_authors(authors: list[str], limit: int = 3) -> str:
    if not authors:
        return "Unknown authors"
    if len(authors) <= limit:
        return ", ".join(authors)
    return f"{', '.join(authors[:limit])} et al."


def shorten_summary(text: str, limit: int = 150) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def render_papers(snapshot: dict[str, Any], top_per_topic: int) -> tuple[str, int]:
    topics = snapshot.get("topics", [])
    if not topics:
        return "- 待补充：先运行 `scripts/fetch_arxiv.py` 生成论文快照。", 0

    lines: list[str] = []
    seen_ids: set[str] = set()
    rendered = 0

    for topic in topics:
        topic_name = topic.get("name", "Untitled Topic")
        entries = topic.get("entries", [])
        topic_lines: list[str] = []
        for entry in entries:
            entry_id = entry.get("id", "")
            if entry_id in seen_ids:
                continue
            seen_ids.add(entry_id)
            authors = short_authors(entry.get("authors", []))
            updated = entry.get("updated", "")[:10]
            title = entry.get("title", "Untitled Paper")
            abs_url = entry.get("abs_url", "")
            paper_link = f"[{title}]({abs_url})" if abs_url else title
            topic_lines.append(
                f"- {paper_link} | {authors} | updated {updated}"
            )
            topic_lines.append(f"  - {shorten_summary(entry.get('summary', ''))}")
            rendered += 1
            if len([line for line in topic_lines if line.startswith("- ")]) >= top_per_topic:
                break

        if topic_lines:
            lines.append(f"### {topic_name}")
            lines.extend(topic_lines)
            lines.append("")

    if not lines:
        return "- 本周没有抓取到符合筛选条件的新论文。", 0

    return "\n".join(lines).strip(), rendered


def render_signal_section(items: list[dict[str, Any]], fallback: list[str]) -> str:
    if not items:
        return "\n".join(f"- {item}" for item in fallback)

    lines: list[str] = []
    for item in items:
        title = item.get("title", "Untitled")
        detail = item.get("detail", "").strip()
        link = item.get("link", "").strip()
        title_part = f"[{title}]({link})" if link else title
        if detail:
            lines.append(f"- {title_part}：{detail}")
        else:
            lines.append(f"- {title_part}")
    return "\n".join(lines)


def render_observations(values: list[str], fallback: list[str]) -> str:
    source = values or fallback
    return "\n".join(f"- {value}" for value in source)


def build_digest(args: argparse.Namespace) -> tuple[str, Path]:
    digest_date = parse_digest_date(args.date)
    snapshot = load_json(args.papers_json)
    signals = load_json(args.signals_file)
    template = args.template.read_text(encoding="utf-8")
    output = args.output or iso_week_path(digest_date)

    papers_section, paper_count = render_papers(snapshot, args.top_per_topic)
    projects_section = render_signal_section(
        signals.get("projects", []),
        [
            "待补充：从 `projects/` 中挑选本周最值得加入周报的工具和代码库。",
            "待补充：记录仿真平台、框架或 SDK 的重要更新。",
        ],
    )
    industry_section = render_signal_section(
        signals.get("industry", []),
        [
            "待补充：公司融资、产品发布、真实部署案例。",
            "待补充：哪些公司开始从 demo 走向量产或场景闭环。",
        ],
    )
    jobs_section = render_signal_section(
        signals.get("jobs", []),
        [
            "待补充：本周新增代表岗位或技能变化。",
            "待补充：哪些关键词在招聘描述中明显升温。",
        ],
    )
    observation_section = render_observations(
        signals.get("observations", []),
        [
            "本周最值得写的不是“多了几条链接”，而是方向之间的共同信号。",
            "建议把论文、项目、产业和岗位变化放到同一张图里看。",
        ],
    )

    iso_year, iso_week, _ = digest_date.isocalendar()
    summary = signals.get(
        "summary",
        f"本周自动汇总了 {paper_count} 篇候选论文。建议你补上项目、产业、岗位和自己的判断，形成完整周报。",
    )

    rendered = (
        template.replace("{{year}}", str(iso_year))
        .replace("{{week_number}}", f"{iso_week:02d}")
        .replace("{{date}}", digest_date.isoformat())
        .replace("{{summary}}", summary)
        .replace("{{top_papers}}", papers_section)
        .replace("{{projects}}", projects_section)
        .replace("{{industry}}", industry_section)
        .replace("{{jobs}}", jobs_section)
        .replace("{{observations}}", observation_section)
    )

    return rendered, output


def main() -> None:
    args = parse_args()
    rendered, output = build_digest(args)

    if output.exists() and not args.overwrite:
        raise SystemExit(f"Output exists, use --overwrite to replace it: {output}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered.strip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
