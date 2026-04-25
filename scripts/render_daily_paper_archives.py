from __future__ import annotations

import json
import re
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DAILY_ROOT = ROOT / "daily-paper"
GENERATED_ROOT = ROOT / "generated" / "embodied-daily"
README_PATH = ROOT / "README.md"
README_EN_PATH = ROOT / "README_EN.md"
PAPERS_PATH = ROOT / "03-papers.md"
CACHE_PATH = GENERATED_ROOT / "daily" / "archive_metadata_cache.json"
ARXIV_API_BASE = "https://export.arxiv.org/api/query"
ARXIV_BATCH_SIZE = 40
ARXIV_SLEEP_SECONDS = 3.0
USER_AGENT = "octoday-robotics-daily-archive/0.1 (+https://github.com/AlexZhangUPUPUP/octoday-robotics)"
AUTO_BACKFILL_IDS = {
    "2604.20627",
    "2604.19683",
    "2604.21241",
    "2603.00110",
    "2604.21453",
    "2407.00848",
    "2308.00513",
    "2506.15518",
    "2501.07399",
    "2603.28032",
    "2604.21138",
    "2604.21686",
    "2604.17969",
    "2604.21192",
    "2604.05320",
    "2604.03956",
    "2604.20472",
    "2604.20347",
}
MANUAL_OVERRIDES = {
    "2604.20627": "离线目标条件强化学习的奖励塑形方法，从世界模型占据测度中提取时序几何结构，缓解稀疏奖励下的信用分配难题",
    "2604.19683": "用于机器人策略学习的掩码世界模型，只预测与决策最相关的状态变化，提升世界模型训练效率与策略鲁棒性",
    "2604.21241": "为生成式动作头引入稀疏空间锚点与显式容差走廊，用可解释的物理约束提升VLA策略的动作对齐与成功率",
    "2603.00110": "利用预训练视频模型学习连续与序列物理交互，构建服务机器人操作的多模态世界交互模型",
    "2604.21453": "面向遮挡场景的实例级主动视觉跟踪方法，把目标跟踪与遮挡感知规划结合起来提升持续跟踪稳定性",
    "2407.00848": "用于水下ROV交互遥操作的自我中心与外部视角融合框架，结合2.5D地面估计提升复杂水下环境感知与操控安全性",
    "2308.00513": "UWB辅助的视觉惯性里程计框架，通过偏置补偿的锚点初始化提升定位收敛速度与稳定性",
    "2506.15518": "面向UWB辅助导航的未知锚点实时初始化方法，在无需先验锚点布局的情况下提升定位可用性",
    "2501.07399": "利用点云密度图高效完成激光SLAM回环检测与验证，在保证精度的同时降低计算开销",
    "2603.28032": "在CARLA中统一空地机器人仿真，支持无人机与地面智能体的协同训练、感知和评测",
    "2604.21138": "面向拥挤环境多机器人控制的双层规划框架，通过路点表示和可行性反馈联合优化任务规划与运动规划",
    "2604.21686": "统一评测交互式视频世界模型的基准套件，用于比较世界模型在预测、交互和可控生成上的能力",
    "2604.17969": "面向3D高斯场景主动感知的评测基准，专门测试视角相关任务中的探索、观察与决策能力",
    "2604.21192": "系统分析VLA在开放世界环境中的真实工作机制，重点观察其空间感知、任务分解与执行失效模式",
    "2604.05320": "面向人机交互的富表达移动操作行为框架，把动作执行与社会表达结合起来提升交互自然性与可理解性",
    "2604.03956": "面向具身基础模型的遗忘方法，研究如何安全移除VLA中的特定知识或行为能力，同时尽量保持整体性能",
    "2604.20472": "将时序差分校准引入VLA训练与评估，用于减轻长序列决策中的误差累积和价值偏移",
    "2604.20347": "将VLA用于自适应超声引导下的穿刺与针体跟踪，把视觉理解、动作决策与医疗机器人控制结合起来",
}

RANGE_FILE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}_to_\d{4}-\d{2}-\d{2}\.md$")
DAILY_FILE_RE = re.compile(r"^\d{2}-\d{1,2}-\d{1,2}paper\.md$")
RANGE_ENTRY_RE = re.compile(
    r"^- \[(?P<day>\d{4}-\d{2}-\d{2})\] "
    r"\[(?P<title>.+?)\]\((?P<url>https://arxiv\.org/abs/[^)]+)\) "
    r"\| arXiv: `(?P<arxiv_id>[^`]+)`"
    r"(?: \| Primary: `(?P<primary>[^`]+)`)?"
    r"(?: \| Categories: (?P<categories>.+?))?"
    r"(?: \| Keywords: (?P<keywords>.+))?$"
)
DAILY_TITLE_RE = re.compile(r"^- \[(?P<title>.+?)\]\((?P<url>https://arxiv\.org/abs/[^)]+)\)$")
DAILY_META_RE = re.compile(
    r"^\s+arXiv: `(?P<arxiv_id>[^`]+)` \| Date: (?P<day>\d{4}-\d{2}-\d{2}) \| Sources: (?P<sources>.+)$"
)


@dataclass
class ArchiveRecord:
    base_id: str
    arxiv_id: str
    title: str
    abs_url: str
    day: str
    keywords: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    source_file: str = ""
    summary: str = ""
    primary_category: str = ""
    cn_summary: str = ""


def canonical_arxiv_id(value: str) -> str:
    match = re.search(r"(\d{4}\.\d{4,5})", value)
    if match:
        return match.group(1)
    return value.strip()


def canonical_abs_url(value: str) -> str:
    return f"https://arxiv.org/abs/{canonical_arxiv_id(value)}"


def parse_backtick_values(value: str) -> list[str]:
    if not value:
        return []
    matches = re.findall(r"`([^`]+)`", value)
    if matches:
        return matches
    return [part.strip() for part in value.split(",") if part.strip()]


def parse_range_file(path: Path) -> tuple[list[ArchiveRecord], int]:
    records: list[ArchiveRecord] = []
    count = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        match = RANGE_ENTRY_RE.match(line)
        if not match:
            continue
        count += 1
        arxiv_id = match.group("arxiv_id")
        records.append(
            ArchiveRecord(
                base_id=canonical_arxiv_id(arxiv_id),
                arxiv_id=arxiv_id,
                title=match.group("title").strip(),
                abs_url=canonical_abs_url(match.group("url")),
                day=match.group("day"),
                keywords=parse_backtick_values(match.group("keywords") or ""),
                source_file=path.name,
            )
        )
    return records, count


def parse_daily_file(path: Path) -> tuple[list[ArchiveRecord], int]:
    lines = path.read_text(encoding="utf-8").splitlines()
    records: list[ArchiveRecord] = []
    count = 0
    pending: tuple[str, str] | None = None

    for line in lines:
        title_match = DAILY_TITLE_RE.match(line)
        if title_match:
            pending = (title_match.group("title").strip(), title_match.group("url"))
            continue

        meta_match = DAILY_META_RE.match(line)
        if meta_match and pending:
            title, url = pending
            count += 1
            arxiv_id = meta_match.group("arxiv_id")
            sources = [part.strip() for part in meta_match.group("sources").split(",") if part.strip()]
            records.append(
                ArchiveRecord(
                    base_id=canonical_arxiv_id(arxiv_id),
                    arxiv_id=arxiv_id,
                    title=title,
                    abs_url=canonical_abs_url(url),
                    day=meta_match.group("day"),
                    sources=sources,
                    source_file=path.name,
                )
            )
            pending = None

    return records, count


def load_archive_records() -> tuple[list[ArchiveRecord], list[tuple[str, int]], list[tuple[str, int]]]:
    range_records: list[ArchiveRecord] = []
    range_sources: list[tuple[str, int]] = []
    daily_sources: list[tuple[str, int]] = []

    for path in sorted(DAILY_ROOT.iterdir(), key=lambda item: item.name, reverse=True):
        if not path.is_file() or path.name == "README.md":
            continue
        if RANGE_FILE_RE.match(path.name):
            parsed, count = parse_range_file(path)
            range_records.extend(parsed)
            range_sources.append((path.name, count))
        elif DAILY_FILE_RE.match(path.name):
            parsed, count = parse_daily_file(path)
            range_records.extend(parsed)
            daily_sources.append((path.name, count))

    deduped: OrderedDict[str, ArchiveRecord] = OrderedDict()
    for record in range_records:
        deduped.setdefault(record.base_id, record)

    return list(deduped.values()), range_sources, daily_sources


def arxiv_year_month(record: ArchiveRecord) -> tuple[int, int]:
    match = re.match(r"(?P<year>\d{2})(?P<month>\d{2})\.\d{4,5}", record.base_id)
    if match:
        year = 2000 + int(match.group("year"))
        month = int(match.group("month"))
        if 1 <= month <= 12:
            return year, month
    return int(record.day[:4]), int(record.day[5:7])


def normalize_spaces(value: str) -> str:
    return " ".join(value.replace("\n", " ").split())


def trim_summary(value: str, limit: int = 44) -> str:
    text = normalize_spaces(value).rstrip("。.;； ")
    if len(text) <= limit:
        return text
    cut = text[:limit]
    for sep in ("，", "；", "。"):
        if sep in cut:
            cut = cut.rsplit(sep, 1)[0]
    return cut.rstrip("，；。 ")


def ensure_terminal_punct(value: str) -> str:
    text = normalize_spaces(value).rstrip()
    if not text:
        return text
    if text.endswith(("。", ".", "；", ";", "！", "!", "？", "?")):
        return text
    return text + "。"


def load_cache() -> dict[str, dict]:
    if not CACHE_PATH.exists():
        return {}
    return json.loads(CACHE_PATH.read_text(encoding="utf-8"))


def save_cache(cache: dict[str, dict]) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def request_arxiv_feed(id_batch: list[str]) -> bytes:
    query = urllib.parse.urlencode({"id_list": ",".join(id_batch)})
    request = urllib.request.Request(f"{ARXIV_API_BASE}?{query}", headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read()


def parse_arxiv_feed(xml_bytes: bytes) -> dict[str, dict]:
    namespace = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }
    root = ET.fromstring(xml_bytes)
    parsed: dict[str, dict] = {}
    for entry in root.findall("atom:entry", namespace):
        raw_id = entry.findtext("atom:id", default="", namespaces=namespace)
        base_id = canonical_arxiv_id(raw_id)
        parsed[base_id] = {
            "title": normalize_spaces(entry.findtext("atom:title", default="", namespaces=namespace)),
            "summary": normalize_spaces(entry.findtext("atom:summary", default="", namespaces=namespace)),
            "primary_category": "",
        }
        primary = entry.find("arxiv:primary_category", namespace)
        if primary is not None:
            parsed[base_id]["primary_category"] = primary.attrib.get("term", "")
    return parsed


def ensure_metadata(ids: list[str], cache: dict[str, dict] | None = None) -> dict[str, dict]:
    cache = cache or load_cache()
    missing_ids = [paper_id for paper_id in ids if paper_id and paper_id not in cache]
    if not missing_ids:
        return cache

    for index in range(0, len(missing_ids), ARXIV_BATCH_SIZE):
        batch = missing_ids[index : index + ARXIV_BATCH_SIZE]
        parsed = parse_arxiv_feed(request_arxiv_feed(batch))
        cache.update(parsed)
        save_cache(cache)
        if index + ARXIV_BATCH_SIZE < len(missing_ids):
            time.sleep(ARXIV_SLEEP_SECONDS)
    return cache


def extract_curated_descriptions() -> dict[str, str]:
    text = PAPERS_PATH.read_text(encoding="utf-8")
    pattern = re.compile(
        r"- \*\*\[(?P<tag>[^\]]+)\]\*\* (?P<title>.+?)\. (?P<desc>.+?) \[link\]\((?P<link>https://arxiv\.org/abs/[^)]+)\)"
    )
    result: dict[str, str] = {}
    for match in pattern.finditer(text):
        desc = normalize_spaces(match.group("desc"))
        if "待补人工中文摘要" in desc:
            continue
        if desc.startswith("来自每日自动抓取"):
            continue
        base_id = canonical_arxiv_id(match.group("link"))
        if base_id in AUTO_BACKFILL_IDS:
            continue
        result[base_id] = desc.rstrip("。")
    return result


def detect_topic(text: str, keywords: list[str]) -> str:
    lowered = f"{' '.join(keywords)} {text}".lower()
    topic_rules = [
        (("multi-robot", "multi robot"), "多机器人协作"),
        (("vision-language-action", "vla"), "视觉-语言-动作"),
        (("world model", "world models"), "世界模型"),
        (("vision language navigation", "vision-and-language navigation", "vln"), "视觉语言导航"),
        (("slam", "localization", "mapping", "odometry", "place recognition"), "导航与空间建图"),
        (("tactile",), "触觉感知"),
        (("dexterous", "grasp", "bimanual", "manipulation", "mobile manipulation"), "机器人操作"),
        (("humanoid",), "人形机器人"),
        (("benchmark", "evaluation"), "评测"),
        (("dataset",), "数据"),
        (("sim2real", "simulation"), "仿真到真实迁移"),
        (("robot learning",), "机器人学习"),
        (("teleoperation",), "遥操作"),
        (("medical robotics", "ultrasound"), "医疗机器人"),
    ]
    for needles, topic in topic_rules:
        if any(needle in lowered for needle in needles):
            return topic
    return "具身智能"


def detect_type(title: str, summary: str) -> str:
    lowered_title = title.lower()
    lowered = f"{title} {summary}".lower()
    type_rules = [
        (("benchmark", "bench"), "评测基准"),
        (("dataset",), "数据集"),
        (("survey", "review"), "综述"),
        (("roadmap",), "路线图"),
        (("framework", "pipeline", "architecture", "foundry"), "框架"),
        (("system", "platform", "playground", "infrastructure"), "系统"),
        (("simulator", "simulation framework"), "仿真框架"),
        (("foundation model",), "基础模型"),
        (("world model",), "模型"),
        (("policy", "unlearning"), "方法"),
        (("planner", "planning"), "规划方法"),
        (("tracking", "odometry", "localization", "slam"), "感知方法"),
        (("model",), "模型"),
    ]
    for needles, value in type_rules:
        if any(needle in lowered_title for needle in needles):
            return value
    if "we propose" in lowered or "we present" in lowered:
        return "方法"
    return "方法"


def detect_problem(text: str) -> str:
    lowered = text.lower()
    problem_rules = [
        ("long-horizon", "长时程任务"),
        ("open-world", "开放世界场景"),
        ("cross-embodiment", "跨本体泛化"),
        ("cascading failures", "级联失败"),
        ("occlusion", "遮挡场景"),
        ("unlearning", "知识删除"),
        ("bimanual", "双臂协作"),
        ("tactile", "触觉交互"),
        ("real-world deployment", "真实世界部署"),
        ("robot autonomy", "机器人自主性"),
        ("generalization", "泛化能力"),
        ("robustness", "鲁棒性"),
        ("multi-step", "多步骤执行"),
        ("safe", "安全约束"),
        ("efficient", "效率"),
    ]
    for needle, label in problem_rules:
        if needle in lowered:
            return label
    return ""


def detect_method(text: str) -> str:
    lowered = text.lower()
    method_rules = [
        ("hierarchical", "采用层次化设计"),
        ("waypoint", "采用基于路点的双层规划"),
        ("multi-source", "结合多源数据"),
        ("heterogeneous", "结合异构数据"),
        ("diffusion", "引入扩散式建模"),
        ("world model", "引入世界模型"),
        ("visual trace", "加入视觉轨迹条件"),
        ("anchor", "通过稀疏空间锚点约束动作生成"),
        ("action-space unification", "通过动作空间统一"),
        ("multi-agent", "结合多智能体协同"),
        ("simulation-generated", "融合仿真生成轨迹"),
        ("egocentric", "利用第一视角数据"),
        ("pretrained video", "利用预训练视频模型学习物理"),
        ("benchmark", "提供统一评测设置"),
        ("dataset", "提供数据支撑"),
        ("retrieval", "结合检索增强"),
        ("tactile", "结合触觉信息"),
    ]
    for needle, label in method_rules:
        if needle in lowered:
            return label
    return ""


def detect_benefit(text: str) -> str:
    lowered = text.lower()
    benefit_rules = [
        ("success", "提升任务成功率"),
        ("generalization", "增强泛化能力"),
        ("robust", "提升鲁棒性"),
        ("real-world", "兼顾真实场景部署"),
        ("zero-shot", "支持零样本泛化"),
        ("benchmark", "支持评测与比较"),
        ("dataset", "支持训练与评测"),
        ("long-horizon", "提升长时程执行稳定性"),
        ("autonomy", "增强机器人自主能力"),
        ("unlearning", "支持安全删除具身模型知识"),
    ]
    for needle, label in benefit_rules:
        if needle in lowered:
            return label
    return ""


def extract_alias(title: str) -> str:
    if ":" not in title:
        return ""
    alias = title.split(":", 1)[0].strip()
    if 1 <= len(alias) <= 24:
        return alias
    return ""


def generate_cn_summary(record: ArchiveRecord, curated_descs: dict[str, str]) -> str:
    if record.base_id in MANUAL_OVERRIDES:
        return ensure_terminal_punct(MANUAL_OVERRIDES[record.base_id])
    curated = curated_descs.get(record.base_id)
    if curated:
        return ensure_terminal_punct(curated)

    title_and_summary = normalize_spaces(f"{record.title}. {record.summary}")
    topic = detect_topic(title_and_summary, record.keywords)
    item_type = detect_type(record.title, record.summary)
    problem = detect_problem(title_and_summary)
    method = detect_method(title_and_summary)
    benefit = detect_benefit(title_and_summary)
    alias = extract_alias(record.title)

    if item_type in {"数据集", "评测基准", "综述", "路线图"}:
        opening = f"围绕{topic}的{item_type}"
    else:
        opening = f"面向{topic}的{item_type}"

    middle_parts = []
    if problem:
        middle_parts.append(f"聚焦{problem}")
    if method:
        middle_parts.append(method)
    if benefit:
        middle_parts.append(benefit)

    if not middle_parts and record.keywords:
        middle_parts.append(f"关注{'、'.join(record.keywords[:3])}")
    if not middle_parts and record.sources:
        middle_parts.append(f"来自{'、'.join(record.sources[:2])}的自动归档")

    summary = f"提出{alias}" if alias and method else opening
    if middle_parts:
        summary += "，" + "，".join(middle_parts)
    elif alias and topic:
        summary += f"，面向{topic}"
    summary += "。"
    return ensure_terminal_punct(trim_summary(summary, limit=56))


def enrich_records(records: list[ArchiveRecord]) -> None:
    cache = ensure_metadata([record.base_id for record in records])
    curated_descs = extract_curated_descriptions()
    for record in records:
        cached = cache.get(record.base_id, {})
        if cached:
            record.title = cached.get("title") or record.title
            record.summary = cached.get("summary") or record.summary
            record.primary_category = cached.get("primary_category") or record.primary_category
        record.cn_summary = generate_cn_summary(record, curated_descs)


def backfill_papers_index() -> None:
    text = PAPERS_PATH.read_text(encoding="utf-8")
    line_pattern = re.compile(
        r"^- \*\*\[(?P<tag>[^\]]+)\]\*\* (?P<title>.+?)\. (?P<desc>.+?) \[link\]\((?P<link>https://arxiv\.org/abs/[^)]+)\)$",
        re.MULTILINE,
    )
    curated_descs = extract_curated_descriptions()
    placeholder_ids = []
    for match in line_pattern.finditer(text):
        desc = normalize_spaces(match.group("desc"))
        base_id = canonical_arxiv_id(match.group("link"))
        if (
            base_id in AUTO_BACKFILL_IDS
            or "待补人工中文摘要" in desc
            or desc.startswith("来自每日自动抓取去重")
        ):
            placeholder_ids.append(base_id)

    cache = ensure_metadata(placeholder_ids)

    def replace_line(match: re.Match) -> str:
        desc = normalize_spaces(match.group("desc"))
        base_id = canonical_arxiv_id(match.group("link"))
        if (
            base_id not in AUTO_BACKFILL_IDS
            and "待补人工中文摘要" not in desc
            and not desc.startswith("来自每日自动抓取去重")
        ):
            return match.group(0)

        cached = cache.get(base_id, {})
        record = ArchiveRecord(
            base_id=base_id,
            arxiv_id=base_id,
            title=cached.get("title") or match.group("title"),
            abs_url=canonical_abs_url(match.group("link")),
            day=f"{2000 + int(base_id[:2])}-{base_id[2:4]}-01",
            summary=cached.get("summary", ""),
            primary_category=cached.get("primary_category", ""),
        )
        cn_summary = generate_cn_summary(record, curated_descs)
        return (
            f"- **[{match.group('tag')}]** {record.title}. "
            f"{cn_summary} [link]({record.abs_url})"
        )

    updated = line_pattern.sub(replace_line, text)
    PAPERS_PATH.write_text(updated, encoding="utf-8")


def render_daily_readme(
    records: list[ArchiveRecord],
    range_sources: list[tuple[str, int]],
    daily_sources: list[tuple[str, int]],
    curated_resource_count: int,
    total_theme_count: int,
    repo_total_entries: int,
    repo_total_unique: int,
) -> str:
    lines: list[str] = [
        "# Daily Paper",
        "",
        f"> 当前共收录 `{len(records)}` 条每日归档论文条目。",
        (
            f"> 若与 [03-papers.md](../03-papers.md) 的 `{curated_resource_count}` 条精选主表一起统计，"
            f"当前仓库共汇总 `{repo_total_entries}` 条论文条目，去重后为 `{repo_total_unique}` 篇。"
        ),
        "> 排序方式：按天从新到旧；同一天内保留自动抓取去重后的唯一条目。",
        "",
        "## Source Files",
        "",
    ]

    for name, count in sorted(daily_sources, reverse=True):
        lines.append(f"- [{name}]({name})：每日快照原文件，`{count}` 条三源去重候选。")
    for name, count in sorted(range_sources, reverse=True):
        lines.append(f"- [{name}]({name})：时间范围归档原文件，`{count}` 条自动筛选候选论文。")

    lines.extend(
        [
            "",
            "## Combined Daily Archive",
            "",
            (
                f"> 这部分以按天浏览为主，适合快速扫当天或某一时间段的新论文；"
                f"如果你想看主题化精选，请回到 [03-papers.md](../03-papers.md)。"
            ),
            "",
        ]
    )

    grouped: OrderedDict[str, list[ArchiveRecord]] = OrderedDict()
    for record in sorted(records, key=lambda item: (item.day, item.base_id), reverse=True):
        grouped.setdefault(record.day, []).append(record)

    for day, day_records in grouped.items():
        lines.append(f"## {day}")
        lines.append("")
        for record in day_records:
            year, month = arxiv_year_month(record)
            lines.append(
                f"- **[arXiv {year}年{month}月]** {record.title}. {record.cn_summary} "
                f"[link]({record.abs_url})"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def read_curated_counts() -> tuple[int, int]:
    text = PAPERS_PATH.read_text(encoding="utf-8")
    match = re.search(r"当前(?:精选主表)?共收录 `(\d+)` 条论文相关资源，覆盖 `(\d+)` 个研究主题板块", text)
    if not match:
        raise RuntimeError("Could not parse curated paper count from 03-papers.md")
    return int(match.group(1)), int(match.group(2))


def read_curated_unique_ids() -> set[str]:
    text = PAPERS_PATH.read_text(encoding="utf-8")
    return set(re.findall(r"arxiv\.org/abs/(\d{4}\.\d{4,5})(?:v\d+)?", text))


def update_readme_counts(
    archive_count: int,
    curated_resource_count: int,
    total_theme_count: int,
    repo_total_entries: int,
    repo_total_unique: int,
) -> None:
    cn = README_PATH.read_text(encoding="utf-8")
    cn = re.sub(
        r"> 当前.*?条论文相关资源，覆盖 `\d+` 个研究主题板块。",
        (
            f"> 当前精选主表共收录 `{curated_resource_count}` 条论文相关资源，"
            f"覆盖 `{total_theme_count}` 个研究主题板块；Daily Paper 另收录 "
            f"`{archive_count}` 条自动归档论文条目。"
        ),
        cn,
        count=1,
    )
    cn = re.sub(
        r"如果你想看(?:按天自动更新的 \[Daily Paper(?: Archives)?\]\(daily-paper/README\.md\)|自动抓取后的时间范围全量归档).*?去重后为 `\d+` 篇。",
        (
            f"如果你想看按天自动更新的 [Daily Paper](daily-paper/README.md)，"
            f"当前已收录 `{archive_count}` 条自动归档论文条目。"
            f"若与主表一起统计，仓库当前共汇总 `{repo_total_entries}` 条论文条目，"
            f"去重后为 `{repo_total_unique}` 篇。"
        ),
        cn,
        count=1,
        flags=re.DOTALL,
    )
    README_PATH.write_text(cn, encoding="utf-8")

    en = README_EN_PATH.read_text(encoding="utf-8")
    en = re.sub(
        r"If you want (?:the daily-updated \[Daily Paper(?: Archives)?\]\(daily-paper/README\.md\)|the full time-range automated archive).*?deduplication\.",
        (
            f"If you want the daily-updated [Daily Paper](daily-paper/README.md), "
            f"it currently contains `{archive_count}` automatically archived paper entries. "
            f"Together with the curated main index, the repository now tracks `{repo_total_entries}` paper entries, "
            f"or `{repo_total_unique}` unique papers after deduplication."
        ),
        en,
        count=1,
        flags=re.DOTALL,
    )
    README_EN_PATH.write_text(en, encoding="utf-8")

    papers = PAPERS_PATH.read_text(encoding="utf-8")
    papers = re.sub(
        r"> 当前.*?条论文相关资源，覆盖 `\d+` 个研究主题板块。",
        (
            f"> 当前精选主表共收录 `{curated_resource_count}` 条论文相关资源，"
            f"覆盖 `{total_theme_count}` 个研究主题板块。"
        ),
        papers,
        count=1,
    )
    papers = re.sub(
        r"> (?:如果你想查看按时间范围自动抓取的全量候选归档.*|.*Daily Paper(?: Archives)?.*)",
        (
            f"> [Daily Paper](daily-paper/README.md) 当前另收录 `{archive_count}` 条自动归档论文条目；"
            f"两部分合计 `{repo_total_entries}` 条条目，去重后为 `{repo_total_unique}` 篇。"
        ),
        papers,
        count=1,
    )
    PAPERS_PATH.write_text(papers, encoding="utf-8")


def main() -> int:
    records, range_sources, daily_sources = load_archive_records()
    enrich_records(records)
    backfill_papers_index()
    curated_resource_count, total_theme_count = read_curated_counts()
    curated_unique_ids = read_curated_unique_ids()
    archive_unique_ids = {record.base_id for record in records}
    repo_total_entries = curated_resource_count + len(records)
    repo_total_unique = len(curated_unique_ids | archive_unique_ids)

    daily_readme = render_daily_readme(
        records=records,
        range_sources=range_sources,
        daily_sources=daily_sources,
        curated_resource_count=curated_resource_count,
        total_theme_count=total_theme_count,
        repo_total_entries=repo_total_entries,
        repo_total_unique=repo_total_unique,
    )
    (DAILY_ROOT / "README.md").write_text(daily_readme, encoding="utf-8")

    update_readme_counts(
        archive_count=len(records),
        curated_resource_count=curated_resource_count,
        total_theme_count=total_theme_count,
        repo_total_entries=repo_total_entries,
        repo_total_unique=repo_total_unique,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
