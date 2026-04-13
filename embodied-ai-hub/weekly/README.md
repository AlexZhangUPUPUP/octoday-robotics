# Weekly

这个目录适合被你继续发展成“具身智能周报”机制。

## 目录结构

| 路径 | 作用 |
| --- | --- |
| `weekly/config/arxiv_topics.json` | arXiv 抓取主题配置 |
| `weekly/config/sample_signals.json` | 项目、产业、岗位和观察示例输入 |
| `weekly/templates/weekly-template.md` | 周报模板 |
| `weekly/data/` | 原始或缓存数据 |
| `weekly/<year>/week-xx.md` | 每周生成的 Markdown 周报 |

## 推荐周报结构

| 模块 | 建议内容 |
| --- | --- |
| 本周论文 | 3-5 篇最值得看的论文，附一句话点评 |
| 本周项目 | 新开源代码、工具链、仿真平台更新 |
| 本周产业 | 公司融资、产品发布、真实部署案例 |
| 本周岗位 | 新增代表岗位和能力关键词变化 |
| 本周观察 | 你对赛道变化的判断，而不是只贴链接 |

## 每周更新 checklist

1. 从 `papers/` 里挑出本周最值得看的研究线。
2. 从 `companies/` 和 `jobs/` 里筛出产业与人才信号。
3. 从 `projects/` 和 `datasets/` 里补工程与评测层面的更新。
4. 最后写一段你自己的判断，形成真正的“周报”而不是“链接合集”。

## 自动化预留

当前已经有第一版自动化脚本：

- `scripts/fetch_arxiv.py`
- `scripts/update_weekly.py`

## 用法示例

```bash
python embodied-ai-hub/scripts/fetch_arxiv.py \
  --config embodied-ai-hub/weekly/config/arxiv_topics.json \
  --output embodied-ai-hub/weekly/data/latest_arxiv.json
```

```bash
python embodied-ai-hub/scripts/update_weekly.py \
  --papers-json embodied-ai-hub/weekly/data/latest_arxiv.json \
  --signals-file embodied-ai-hub/weekly/config/sample_signals.json \
  --overwrite
```

如果你暂时没有真实抓取结果，也可以用 `weekly/data/sample_arxiv_feed.xml` 做离线测试。

## 建议的第一版命名方式

- `weekly/2026/week-01.md`
- `weekly/2026/week-16.md`
- `weekly/2026/week-32.md`

这样更适合自动按 ISO week 生成。
