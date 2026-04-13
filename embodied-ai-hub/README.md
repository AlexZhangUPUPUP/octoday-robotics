# 🤖 星期八 · Embodied AI Hub

<div align="center">
  <img src="../image.png" width="100%" alt="Embodied AI Hub Banner" />
</div>

`embodied-ai-hub/` 是这次仓库重构后的结构化内容中心。

它的目标很明确：把原先分散在根目录长文里的知识、产业、项目、数据、招聘和趋势，重新组织成一套更适合 GitHub 浏览、维护和持续扩展的目录式知识库。

## 从这里开始

| 如果你现在最关心的是 | 建议先看 |
| --- | --- |
| 零基础入门 | [learning](learning/README.md) |
| 想知道先看哪些版块 | [navigation](navigation/README.md) |
| 看研究路线和关键论文 | [papers](papers/README.md) |
| 找代码、平台、仿真和工具链 | [projects](projects/README.md) |
| 找数据集、基准和评测 | [datasets](datasets/README.md) |
| 看产业玩家和产品方向 | [companies](companies/README.md) |
| 看招聘需求和岗位画像 | [jobs](jobs/README.md) |
| 跟进趋势和重点赛道 | [trends](trends/README.md) |
| 想沉淀固定更新节奏 | [weekly](weekly/README.md) |

## 模块说明

| 模块 | 它解决什么问题 | 旧内容来源 |
| --- | --- | --- |
| [navigation](navigation/README.md) | 我该从哪里开始看 | 全仓库融合 |
| [learning](learning/README.md) | 如何系统入门具身智能 | [`../00-basics.md`](../00-basics.md) |
| [papers](papers/README.md) | 论文脉络怎样建立 | [`../03-papers-code.md`](../03-papers-code.md) |
| [projects](projects/README.md) | 有哪些可复现项目和工具链 | [`../03-papers-code.md`](../03-papers-code.md), [`../04-tools.md`](../04-tools.md) |
| [datasets](datasets/README.md) | 数据从哪里找，怎么做评测 | [`../03-papers-code.md`](../03-papers-code.md) |
| [companies](companies/README.md) | 这个行业有哪些关键玩家 | [`../01-companies.md`](../01-companies.md) |
| [jobs](jobs/README.md) | 市场到底在招聘什么能力 | [`../02-jobs.md`](../02-jobs.md) |
| [trends](trends/README.md) | 最近应该追哪些方向 | 跨论文/公司/岗位/会议总结 |
| [weekly](weekly/README.md) | 如何把更新沉淀成周报机制 | `scripts/` |

## 当前重构原则

1. 不删除旧长文，先保留根目录内容作为全量信息源。
2. 先搭建结构化入口，再逐步把内容按专题拆细。
3. 所有新栏目页优先承担“导航”和“索引”功能，避免再次变成长篇杂糅大文档。

## 你接下来最值得做的三件事

1. 持续补 `weekly/`，让这个仓库真正形成节奏感。
2. 把 `papers/` 和 `datasets/` 继续拆成更多专题页。
3. 给 `companies/` 和 `jobs/` 增加更强的标签体系，形成真正的产业地图和人才画像。
