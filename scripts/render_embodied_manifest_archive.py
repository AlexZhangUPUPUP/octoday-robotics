from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a markdown archive page from an embodied paper manifest."
    )
    parser.add_argument("--manifest", type=Path, required=True, help="Path to manifest.json.")
    parser.add_argument("--output", type=Path, required=True, help="Markdown output path.")
    parser.add_argument(
        "--title",
        help="Optional page title. Defaults to 'Embodied Paper Archive · <start> to <end>'.",
    )
    return parser.parse_args()


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def display_date(value: str) -> str:
    return parse_timestamp(value).date().isoformat()


def format_code_list(values: list[str]) -> str:
    return ", ".join(f"`{value}`" for value in values)


def format_keywords(values: list[str]) -> str:
    if not values:
        return "None"
    return ", ".join(f"`{value}`" for value in values)


def build_title(manifest: dict, override: str | None) -> str:
    if override:
        return override
    date_range = manifest["range"]
    return (
        "Embodied Paper Archive · "
        f"{date_range['start_date_utc']} to {date_range['end_date_utc']}"
    )


def render_markdown(manifest: dict, title: str) -> str:
    papers = manifest["papers"]
    month_counts = Counter(display_date(paper["published"])[:7] for paper in papers)

    lines: list[str] = [f"# {title}", ""]
    lines.extend(
        [
            "> 说明：这是按仓库当前“具身 / 机器人相关”自动检索规则生成的时间范围归档，不等于 `03-papers.md` 的人工精选主表。",
            "",
            f"- UTC date range: `{manifest['range']['start_date_utc']}` to `{manifest['range']['end_date_utc']}`",
            f"- Filtered papers: `{manifest['filtered_count']}`",
            f"- Candidate papers before filtering: `{manifest['candidate_count']}`",
            f"- Categories: {format_code_list(manifest['categories'])}",
            f"- Keywords: {format_keywords(manifest['keywords'])}",
            "",
            "## Month Summary",
            "",
            "| Month | Paper Count |",
            "| :--- | ---: |",
        ]
    )

    for month, count in sorted(month_counts.items(), reverse=True):
        lines.append(f"| `{month}` | `{count}` |")

    lines.extend(
        [
            "",
            "## Full Archive",
            "",
            "> 每条记录只保留论文元信息，便于扫描和去重；若需要精选版分类导读，请回到 `03-papers.md`。",
            "",
        ]
    )

    current_month: str | None = None
    for paper in papers:
        month = display_date(paper["published"])[:7]
        if month != current_month:
            if current_month is not None:
                lines.append("")
            lines.append(f"### {month}")
            lines.append("")
            current_month = month

        categories = paper.get("categories") or [paper.get("primary_category", "unknown")]
        lines.append(
            "- "
            f"[{display_date(paper['published'])}] "
            f"[{paper['title']}]({paper['abs_url']})"
            f" | arXiv: `{paper['arxiv_id']}`"
            f" | Primary: `{paper['primary_category']}`"
            f" | Categories: {format_code_list(categories)}"
            f" | Keywords: {format_keywords(paper.get('matched_keywords', []))}"
        )

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    manifest_path = args.manifest.resolve()
    output_path = args.output.resolve()
    manifest = load_manifest(manifest_path)
    title = build_title(manifest, args.title)
    markdown = render_markdown(manifest, title)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    print(output_path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
