from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "02-jobs.md"
HTML_PATH = ROOT / "02-jobs.html"


DETAIL_RE = re.compile(
    r'<details(?: open)? id="(?P<id>jobs-(?P<group>domestic|overseas|special)-\d+)">\n'
    r"<summary><strong>(?P<name>.*?)</strong> · (?P<count>\d+) 个岗位</summary>\n\n"
    r"\| No\. \| 岗位 / 项目 \| 地点 \| 类别 \| 链接 \|\n"
    r"\| --- \| --- \| --- \| --- \| --- \|\n"
    r"(?P<body>.*?)\n"
    r"</details>",
    re.S,
)

ROW_RE = re.compile(
    r"^\| (?P<no>\d+) \| (?P<title>.*?) \| (?P<location>.*?) \| "
    r"(?P<kind>.*?) \| \[查看\]\((?P<url>.*?)\) \|$"
)


def parse_block_lines(text: str, heading: str, stop_marker: str) -> list[str]:
    start = text.index(heading) + len(heading)
    end = text.index(stop_marker, start)
    lines = []
    for raw in text[start:end].splitlines():
        line = raw.strip()
        if line:
            lines.append(line)
    return lines


def parse_alerts(text: str) -> list[dict[str, str]]:
    lines = parse_block_lines(text, "## ⚠️ 特别提醒", '<a id="featured-jobs"></a>')
    alerts: list[dict[str, str]] = []
    for line in lines:
        if not line.startswith("- "):
            continue
        match = re.match(r"- \*\*(.*?)\*\*：(.+)", line)
        if match:
            alerts.append({"title": match.group(1), "detail": match.group(2)})
    return alerts


def parse_featured(text: str) -> list[dict[str, str]]:
    lines = parse_block_lines(text, "## 📢 新增亮点岗位", "### 💡 求职小贴士")
    featured: list[dict[str, str]] = []
    for line in lines:
        match = re.match(r"\d+\. \*\*(.*?)\*\*：(.+)", line)
        if match:
            featured.append({"title": match.group(1), "detail": match.group(2)})
    return featured


def parse_tips(text: str) -> list[dict[str, str]]:
    lines = parse_block_lines(text, "### 💡 求职小贴士", "---")
    tips: list[dict[str, str]] = []
    for line in lines:
        match = re.match(r"- \*\*(.*?)\*\*：(.+)", line)
        if match:
            tips.append({"title": match.group(1), "detail": match.group(2)})
    return tips


def parse_jobs(text: str) -> list[dict[str, object]]:
    group_meta = {
        "domestic": {
            "id": "jobs-domestic",
            "label": "国内机会",
            "icon": "🏢",
            "description": "国内机器人公司、平台团队、研究机构与产业链岗位。",
        },
        "overseas": {
            "id": "jobs-overseas",
            "label": "海外机会",
            "icon": "🌍",
            "description": "海外机器人公司、实验室、研究机构与企业岗位。",
        },
        "special": {
            "id": "jobs-special",
            "label": "专项计划",
            "icon": "🌟",
            "description": "博士后、顶尖人才项目、专项计划与特殊培养机会。",
        },
    }

    grouped = {
        key: {**value, "items": []}
        for key, value in group_meta.items()
    }

    for match in DETAIL_RE.finditer(text):
        rows = []
        for raw in match.group("body").strip().splitlines():
            row_match = ROW_RE.match(raw.strip())
            if not row_match:
                continue
            rows.append(
                {
                    "no": int(row_match.group("no")),
                    "title": row_match.group("title"),
                    "location": row_match.group("location"),
                    "kind": row_match.group("kind"),
                    "url": row_match.group("url"),
                }
            )

        grouped[match.group("group")]["items"].append(
            {
                "id": match.group("id"),
                "name": match.group("name"),
                "count": int(match.group("count")),
                "rows": rows,
            }
        )

    return [grouped["domestic"], grouped["overseas"], grouped["special"]]


def build_html(payload: dict[str, object]) -> str:
    data_json = json.dumps(payload, ensure_ascii=False)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>具身智能招聘信息 · HTML Preview</title>
  <meta name="description" content="由 02-jobs.md 生成的固定表格布局 HTML 预览页。">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Azeret+Mono:wght@400;500;600&family=Noto+Serif+SC:wght@500;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #f4efe8;
      --bg-soft: rgba(255, 252, 247, 0.82);
      --panel: rgba(255, 250, 243, 0.88);
      --panel-strong: rgba(255, 248, 239, 0.96);
      --line: rgba(73, 50, 33, 0.14);
      --line-strong: rgba(73, 50, 33, 0.24);
      --ink: #23160f;
      --muted: #6a5140;
      --accent: #ba4f2b;
      --accent-strong: #8b2b0a;
      --accent-soft: rgba(186, 79, 43, 0.12);
      --navy: #1f3442;
      --navy-soft: rgba(31, 52, 66, 0.1);
      --shadow: 0 24px 60px rgba(44, 24, 8, 0.12);
      --radius-xl: 28px;
      --radius-lg: 20px;
      --radius-md: 14px;
      --content-width: 1480px;
    }}

    * {{
      box-sizing: border-box;
    }}

    html {{
      scroll-behavior: smooth;
    }}

    body {{
      margin: 0;
      color: var(--ink);
      font-family: "IBM Plex Sans", "Noto Sans SC", sans-serif;
      background:
        radial-gradient(circle at top left, rgba(186, 79, 43, 0.16), transparent 24%),
        radial-gradient(circle at top right, rgba(31, 52, 66, 0.16), transparent 22%),
        linear-gradient(180deg, #f7f2eb 0%, #efe7dc 100%);
      min-height: 100vh;
    }}

    body::before {{
      content: "";
      position: fixed;
      inset: 0;
      background-image:
        linear-gradient(rgba(35, 22, 15, 0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(35, 22, 15, 0.025) 1px, transparent 1px);
      background-size: 24px 24px;
      pointer-events: none;
      opacity: 0.45;
    }}

    a {{
      color: inherit;
    }}

    .shell {{
      width: min(var(--content-width), calc(100vw - 32px));
      margin: 0 auto;
      padding: 24px 0 64px;
      position: relative;
      z-index: 1;
    }}

    .hero {{
      position: relative;
      overflow: hidden;
      background:
        linear-gradient(135deg, rgba(255, 246, 235, 0.95), rgba(252, 248, 242, 0.9)),
        linear-gradient(120deg, rgba(186, 79, 43, 0.08), rgba(31, 52, 66, 0.08));
      border: 1px solid rgba(73, 50, 33, 0.12);
      box-shadow: var(--shadow);
      border-radius: 36px;
      padding: 34px 34px 30px;
    }}

    .hero::after {{
      content: "";
      position: absolute;
      right: -40px;
      top: -40px;
      width: 220px;
      height: 220px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(186, 79, 43, 0.18), transparent 70%);
      pointer-events: none;
    }}

    .eyebrow {{
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 8px 14px;
      border-radius: 999px;
      background: rgba(35, 22, 15, 0.05);
      border: 1px solid rgba(35, 22, 15, 0.08);
      font-size: 12px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--muted);
    }}

    h1 {{
      margin: 18px 0 12px;
      font-family: "Noto Serif SC", serif;
      font-size: clamp(32px, 6vw, 62px);
      line-height: 1.05;
      letter-spacing: -0.03em;
      max-width: 11ch;
    }}

    .hero p {{
      margin: 0;
      max-width: 72ch;
      color: var(--muted);
      font-size: 16px;
      line-height: 1.7;
    }}

    .hero-grid {{
      display: grid;
      grid-template-columns: 1.5fr 1fr;
      gap: 22px;
      margin-top: 26px;
      align-items: end;
    }}

    .metrics {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
    }}

    .metric {{
      border-radius: var(--radius-lg);
      background: rgba(255, 253, 249, 0.78);
      border: 1px solid rgba(73, 50, 33, 0.1);
      padding: 16px 16px 14px;
      min-height: 106px;
    }}

    .metric strong {{
      display: block;
      font-family: "Azeret Mono", monospace;
      font-size: 26px;
      color: var(--navy);
      margin-bottom: 10px;
    }}

    .metric span {{
      font-size: 12px;
      color: var(--muted);
      line-height: 1.5;
    }}

    .hero-note {{
      border-radius: var(--radius-lg);
      background: linear-gradient(135deg, rgba(31, 52, 66, 0.96), rgba(19, 34, 45, 0.96));
      color: #f7f2eb;
      padding: 18px 20px;
      min-height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 16px;
    }}

    .hero-note h2 {{
      margin: 0;
      font-size: 16px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: rgba(247, 242, 235, 0.72);
    }}

    .hero-note p {{
      color: rgba(247, 242, 235, 0.84);
      font-size: 14px;
      line-height: 1.7;
    }}

    .hero-note code {{
      font-family: "Azeret Mono", monospace;
      font-size: 12px;
      background: rgba(255, 255, 255, 0.08);
      padding: 2px 6px;
      border-radius: 6px;
    }}

    .hero-links {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 14px;
    }}

    .pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      text-decoration: none;
      padding: 10px 14px;
      border-radius: 999px;
      border: 1px solid rgba(73, 50, 33, 0.12);
      background: rgba(255, 252, 247, 0.88);
      color: var(--ink);
      font-size: 13px;
      transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
    }}

    .pill:hover {{
      transform: translateY(-1px);
      border-color: rgba(186, 79, 43, 0.32);
      background: #fffaf4;
    }}

    .layout {{
      display: grid;
      grid-template-columns: 280px minmax(0, 1fr);
      gap: 22px;
      margin-top: 22px;
      align-items: start;
    }}

    .sidebar {{
      position: sticky;
      top: 18px;
      display: grid;
      gap: 16px;
    }}

    .panel {{
      border-radius: var(--radius-xl);
      background: var(--panel);
      border: 1px solid rgba(73, 50, 33, 0.1);
      box-shadow: var(--shadow);
      backdrop-filter: blur(14px);
    }}

    .sidebar-card {{
      padding: 18px;
    }}

    .sidebar-card h3 {{
      margin: 0 0 12px;
      font-size: 13px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--muted);
    }}

    .jump-list,
    .legend-list {{
      display: grid;
      gap: 10px;
    }}

    .jump-link {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      text-decoration: none;
      border-radius: 14px;
      padding: 12px 14px;
      background: rgba(255, 255, 255, 0.72);
      border: 1px solid rgba(73, 50, 33, 0.08);
      color: var(--ink);
    }}

    .jump-link:hover {{
      border-color: rgba(186, 79, 43, 0.32);
      background: rgba(255, 250, 243, 0.96);
    }}

    .jump-link strong {{
      display: block;
      font-size: 14px;
    }}

    .jump-link span {{
      color: var(--muted);
      font-size: 12px;
    }}

    .jump-link em {{
      font-style: normal;
      font-family: "Azeret Mono", monospace;
      font-size: 11px;
      color: var(--accent-strong);
    }}

    .search-box {{
      display: grid;
      gap: 10px;
    }}

    .search-box label {{
      font-size: 13px;
      color: var(--muted);
    }}

    .search-box input {{
      width: 100%;
      border: 1px solid rgba(73, 50, 33, 0.14);
      border-radius: 14px;
      padding: 12px 14px;
      background: rgba(255, 255, 255, 0.9);
      color: var(--ink);
      font: inherit;
      outline: none;
    }}

    .search-box input:focus {{
      border-color: rgba(186, 79, 43, 0.4);
      box-shadow: 0 0 0 4px rgba(186, 79, 43, 0.08);
    }}

    .legend-list div {{
      display: grid;
      gap: 4px;
      padding: 10px 12px;
      border-radius: 14px;
      background: rgba(255, 255, 255, 0.68);
      border: 1px solid rgba(73, 50, 33, 0.07);
    }}

    .legend-list strong {{
      font-size: 13px;
    }}

    .legend-list span {{
      font-size: 12px;
      color: var(--muted);
      line-height: 1.55;
    }}

    .content {{
      display: grid;
      gap: 22px;
    }}

    .section {{
      padding: 22px;
    }}

    .section-head {{
      display: flex;
      align-items: end;
      justify-content: space-between;
      gap: 18px;
      margin-bottom: 18px;
    }}

    .section-head h2 {{
      margin: 0;
      font-family: "Noto Serif SC", serif;
      font-size: clamp(24px, 4vw, 38px);
    }}

    .section-head p {{
      margin: 8px 0 0;
      color: var(--muted);
      max-width: 70ch;
      line-height: 1.65;
      font-size: 14px;
    }}

    .section-stat {{
      min-width: 168px;
      padding: 14px 16px;
      border-radius: 18px;
      background: rgba(31, 52, 66, 0.06);
      border: 1px solid rgba(31, 52, 66, 0.1);
      text-align: right;
    }}

    .section-stat strong {{
      display: block;
      font-family: "Azeret Mono", monospace;
      font-size: 22px;
      color: var(--navy);
    }}

    .section-stat span {{
      font-size: 12px;
      color: var(--muted);
    }}

    .cards {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
    }}

    .company-card {{
      display: grid;
      grid-template-rows: auto 1fr;
      min-height: 320px;
      background: var(--panel-strong);
      border: 1px solid rgba(73, 50, 33, 0.1);
      border-radius: 24px;
      overflow: hidden;
      box-shadow: 0 18px 36px rgba(44, 24, 8, 0.08);
    }}

    .company-head {{
      display: flex;
      align-items: start;
      justify-content: space-between;
      gap: 16px;
      padding: 18px 18px 12px;
      border-bottom: 1px solid rgba(73, 50, 33, 0.08);
      background:
        linear-gradient(135deg, rgba(186, 79, 43, 0.12), rgba(186, 79, 43, 0.02)),
        rgba(255, 255, 255, 0.32);
    }}

    .company-head h3 {{
      margin: 0;
      font-size: 20px;
      line-height: 1.2;
    }}

    .company-head p {{
      margin: 6px 0 0;
      color: var(--muted);
      font-size: 12px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}

    .count-badge {{
      white-space: nowrap;
      border-radius: 999px;
      padding: 8px 12px;
      background: rgba(35, 22, 15, 0.06);
      border: 1px solid rgba(35, 22, 15, 0.08);
      font-family: "Azeret Mono", monospace;
      font-size: 11px;
      color: var(--navy);
    }}

    .table-wrap {{
      padding: 10px 14px 14px;
      overflow: auto;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
      min-width: 0;
    }}

    col.col-no {{
      width: 56px;
    }}

    col.col-title {{
      width: 47%;
    }}

    col.col-location {{
      width: 20%;
    }}

    col.col-kind {{
      width: 13%;
    }}

    col.col-link {{
      width: 94px;
    }}

    thead th {{
      text-align: left;
      padding: 11px 10px;
      font-size: 11px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
      border-bottom: 1px solid var(--line-strong);
    }}

    tbody td {{
      padding: 10px 10px;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
      font-size: 13px;
      line-height: 1.4;
    }}

    tbody tr:last-child td {{
      border-bottom: none;
    }}

    .num {{
      font-family: "Azeret Mono", monospace;
      color: var(--muted);
      font-size: 12px;
    }}

    .clamp-two,
    .clamp-one {{
      display: -webkit-box;
      overflow: hidden;
      -webkit-box-orient: vertical;
      word-break: break-word;
    }}

    .clamp-two {{
      -webkit-line-clamp: 2;
      min-height: calc(1.4em * 2);
      max-height: calc(1.4em * 2);
    }}

    .clamp-one {{
      -webkit-line-clamp: 1;
      min-height: 1.4em;
      max-height: 1.4em;
    }}

    .job-link {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      text-decoration: none;
      width: 100%;
      min-height: 34px;
      border-radius: 999px;
      background: var(--accent-soft);
      color: var(--accent-strong);
      font-weight: 600;
      border: 1px solid rgba(186, 79, 43, 0.12);
      transition: transform 160ms ease, background 160ms ease;
    }}

    .job-link:hover {{
      transform: translateY(-1px);
      background: rgba(186, 79, 43, 0.18);
    }}

    .meta-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
    }}

    .meta-card {{
      padding: 20px;
    }}

    .meta-card h3 {{
      margin: 0 0 12px;
      font-size: 15px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--muted);
    }}

    .meta-list {{
      display: grid;
      gap: 12px;
    }}

    .meta-item {{
      padding: 14px;
      border-radius: 16px;
      background: rgba(255, 255, 255, 0.7);
      border: 1px solid rgba(73, 50, 33, 0.08);
    }}

    .meta-item strong {{
      display: block;
      margin-bottom: 6px;
      font-size: 14px;
    }}

    .meta-item span {{
      color: var(--muted);
      font-size: 13px;
      line-height: 1.65;
    }}

    .footer-note {{
      margin-top: 22px;
      padding: 16px 18px;
      border-radius: 18px;
      background: rgba(31, 52, 66, 0.08);
      border: 1px solid rgba(31, 52, 66, 0.1);
      color: var(--muted);
      font-size: 13px;
      line-height: 1.7;
    }}

    .hidden {{
      display: none !important;
    }}

    @media (max-width: 1180px) {{
      .layout {{
        grid-template-columns: 1fr;
      }}

      .sidebar {{
        position: static;
      }}
    }}

    @media (max-width: 980px) {{
      .hero-grid,
      .meta-grid,
      .cards {{
        grid-template-columns: 1fr;
      }}

      .metrics {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}

      .section-head {{
        flex-direction: column;
        align-items: start;
      }}

      .section-stat {{
        text-align: left;
      }}
    }}

    @media (max-width: 640px) {{
      .shell {{
        width: min(calc(100vw - 18px), var(--content-width));
        padding-top: 10px;
      }}

      .hero,
      .section,
      .meta-card {{
        padding-left: 16px;
        padding-right: 16px;
      }}

      .metrics {{
        grid-template-columns: 1fr;
      }}

      .company-head {{
        flex-direction: column;
      }}

      table {{
        min-width: 560px;
      }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <header class="hero">
      <div class="eyebrow">HTML Preview · Fixed Table Layout Demo</div>
      <h1>具身智能招聘信息的 HTML 版实验页面</h1>
      <p>这个页面直接从 <code>02-jobs.md</code> 生成，重点测试独立公司卡片、固定列宽、受控行高和统一表格布局在 HTML 里的实际观感。相较于 GitHub Markdown 版，这里可以稳定控制每列宽度与卡片尺寸。</p>
      <div class="hero-grid">
        <div class="metrics" id="metrics"></div>
        <div class="hero-note">
          <div>
            <h2>Design Note</h2>
            <p>这个版本采用偏编辑化、工业资料册的排版方向。表格开启 <code>table-layout: fixed</code>，每列宽度固定；文本单元格做了行数截断，用来验证“统一尺寸”是否比 Markdown 版更适合你。</p>
          </div>
          <div class="hero-links" id="hero-links"></div>
        </div>
      </div>
    </header>

    <div class="layout">
      <aside class="sidebar">
        <section class="panel sidebar-card">
          <h3>快速跳转</h3>
          <div class="jump-list" id="jump-list"></div>
        </section>
        <section class="panel sidebar-card">
          <div class="search-box">
            <h3>筛选</h3>
            <label for="search">按公司名或岗位关键词过滤</label>
            <input id="search" type="search" placeholder="例如：智元 / SLAM / PhD / 强化学习">
          </div>
        </section>
        <section class="panel sidebar-card">
          <h3>布局说明</h3>
          <div class="legend-list">
            <div>
              <strong>统一卡片宽度</strong>
              <span>所有公司卡片使用相同栅格宽度，桌面端两列展示。</span>
            </div>
            <div>
              <strong>固定列宽</strong>
              <span>通过 <code>colgroup</code> 和 <code>table-layout: fixed</code> 限制每列比例。</span>
            </div>
            <div>
              <strong>受控行高</strong>
              <span>岗位名、地点、类别分别做单行或双行截断，避免表格跳动。</span>
            </div>
          </div>
        </section>
      </aside>

      <main class="content">
        <div id="sections"></div>
        <section class="meta-grid">
          <article class="panel meta-card">
            <h3>特别提醒</h3>
            <div class="meta-list" id="alerts"></div>
          </article>
          <article class="panel meta-card">
            <h3>新增亮点岗位</h3>
            <div class="meta-list" id="featured"></div>
          </article>
          <article class="panel meta-card">
            <h3>求职小贴士</h3>
            <div class="meta-list" id="tips"></div>
          </article>
        </section>
        <div class="footer-note">
          当前文件生成时间：{generated_at}。数据源来自仓库内的 <code>02-jobs.md</code>，生成脚本为 <code>scripts/generate_jobs_html.py</code>。如果你认可这种视觉方向，下一步可以继续决定是否把它升级成 GitHub Pages 页面。
        </div>
      </main>
    </div>
  </div>

  <script>
    const JOBS_DATA = {data_json};

    const sectionIntro = {{
      "jobs-domestic": "偏向国内具身智能公司、机器人平台、研究团队与应用机构的岗位分布。",
      "jobs-overseas": "偏向海外机器人公司、研究实验室与跨国产业团队的岗位分布。",
      "jobs-special": "偏向人才计划、博士后、专项项目与 Top Talent 通道。"
    }};

    const metricsRoot = document.getElementById("metrics");
    const heroLinksRoot = document.getElementById("hero-links");
    const jumpListRoot = document.getElementById("jump-list");
    const sectionsRoot = document.getElementById("sections");
    const searchInput = document.getElementById("search");
    const alertsRoot = document.getElementById("alerts");
    const featuredRoot = document.getElementById("featured");
    const tipsRoot = document.getElementById("tips");

    function metricCard(value, label) {{
      const div = document.createElement("div");
      div.className = "metric";
      div.innerHTML = `<strong>${{value}}</strong><span>${{label}}</span>`;
      return div;
    }}

    function renderMetrics() {{
      const sectionCount = JOBS_DATA.categories.length;
      const companyCount = JOBS_DATA.categories.reduce((sum, category) => sum + category.items.length, 0);
      const jobCount = JOBS_DATA.categories.reduce((sum, category) => sum + category.items.reduce((inner, item) => inner + item.rows.length, 0), 0);
      const featuredCount = JOBS_DATA.featured.length;

      metricsRoot.append(
        metricCard(sectionCount, "大类分区"),
        metricCard(companyCount, "机构 / 公司卡片"),
        metricCard(jobCount, "岗位 / 项目条目"),
        metricCard(featuredCount, "亮点岗位补充")
      );
    }}

    function renderHeroLinks() {{
      JOBS_DATA.categories.forEach((category) => {{
        const link = document.createElement("a");
        link.className = "pill";
        link.href = `#${{category.id}}`;
        link.textContent = `${{category.icon}} ${{category.label}}`;
        heroLinksRoot.appendChild(link);
      }});
    }}

    function renderJumpLinks() {{
      JOBS_DATA.categories.forEach((category) => {{
        const totalJobs = category.items.reduce((sum, item) => sum + item.rows.length, 0);
        const link = document.createElement("a");
        link.className = "jump-link";
        link.href = `#${{category.id}}`;
        link.innerHTML = `
          <div>
            <strong>${{category.icon}} ${{category.label}}</strong>
            <span>${{category.items.length}} 家机构 · ${{totalJobs}} 条记录</span>
          </div>
          <em>jump</em>
        `;
        jumpListRoot.appendChild(link);
      }});
    }}

    function createCell(text, className) {{
      return `<div class="${{className}}">${{text}}</div>`;
    }}

    function renderTableRows(rows) {{
      return rows.map((row) => `
        <tr>
          <td class="num">${{row.no}}</td>
          <td>${{createCell(row.title, "clamp-two")}}</td>
          <td>${{createCell(row.location, "clamp-two")}}</td>
          <td>${{createCell(row.kind, "clamp-one")}}</td>
          <td><a class="job-link" href="${{row.url}}" target="_blank" rel="noreferrer">查看</a></td>
        </tr>
      `).join("");
    }}

    function renderSections(query = "") {{
      sectionsRoot.innerHTML = "";
      const normalized = query.trim().toLowerCase();

      JOBS_DATA.categories.forEach((category) => {{
        const filteredItems = category.items.filter((item) => {{
          if (!normalized) {{
            return true;
          }}
          const text = [
            item.name,
            ...item.rows.map((row) => `${{row.title}} ${{row.location}} ${{row.kind}}`)
          ].join(" ").toLowerCase();
          return text.includes(normalized);
        }});

        if (!filteredItems.length) {{
          return;
        }}

        const section = document.createElement("section");
        section.className = "panel section";
        section.id = category.id;

        const totalJobs = filteredItems.reduce((sum, item) => sum + item.rows.length, 0);
        const cards = filteredItems.map((item) => `
          <article class="company-card" id="${{item.id}}">
            <div class="company-head">
              <div>
                <h3>${{item.name}}</h3>
                <p>${{category.label}} / 固定布局表格</p>
              </div>
              <div class="count-badge">${{item.rows.length}} 条记录</div>
            </div>
            <div class="table-wrap">
              <table>
                <colgroup>
                  <col class="col-no">
                  <col class="col-title">
                  <col class="col-location">
                  <col class="col-kind">
                  <col class="col-link">
                </colgroup>
                <thead>
                  <tr>
                    <th>No.</th>
                    <th>岗位 / 项目</th>
                    <th>地点</th>
                    <th>类别</th>
                    <th>链接</th>
                  </tr>
                </thead>
                <tbody>
                  ${{renderTableRows(item.rows)}}
                </tbody>
              </table>
            </div>
          </article>
        `).join("");

        section.innerHTML = `
          <div class="section-head">
            <div>
              <h2>${{category.icon}} ${{category.label}}</h2>
              <p>${{category.description}} ${{sectionIntro[category.id] || ""}}</p>
            </div>
            <div class="section-stat">
              <strong>${{filteredItems.length}}</strong>
              <span>机构 · ${{totalJobs}} 条结果</span>
            </div>
          </div>
          <div class="cards">${{cards}}</div>
        `;

        sectionsRoot.appendChild(section);
      }});

      if (!sectionsRoot.children.length) {{
        const empty = document.createElement("section");
        empty.className = "panel section";
        empty.innerHTML = `
          <div class="section-head">
            <div>
              <h2>没有匹配结果</h2>
              <p>当前关键词没有命中公司名或岗位信息，换个关键词试试。</p>
            </div>
          </div>
        `;
        sectionsRoot.appendChild(empty);
      }}
    }}

    function renderMetaList(root, items) {{
      root.innerHTML = items.map((item) => `
        <div class="meta-item">
          <strong>${{item.title}}</strong>
          <span>${{item.detail}}</span>
        </div>
      `).join("");
    }}

    renderMetrics();
    renderHeroLinks();
    renderJumpLinks();
    renderSections();
    renderMetaList(alertsRoot, JOBS_DATA.alerts);
    renderMetaList(featuredRoot, JOBS_DATA.featured);
    renderMetaList(tipsRoot, JOBS_DATA.tips);

    searchInput.addEventListener("input", (event) => {{
      renderSections(event.target.value);
    }});
  </script>
</body>
</html>
"""


def main() -> None:
    text = MD_PATH.read_text()
    categories = parse_jobs(text)
    payload = {
        "categories": categories,
        "alerts": parse_alerts(text),
        "featured": parse_featured(text),
        "tips": parse_tips(text),
    }
    HTML_PATH.write_text(build_html(payload))
    print(f"generated {HTML_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
