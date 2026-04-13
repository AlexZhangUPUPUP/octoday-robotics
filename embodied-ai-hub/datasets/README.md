# 数据与基准

具身智能里很多问题最后都会回到两个核心：`有没有合适的数据`，以及 `怎么评测才算真的进步`。

## 子页导航

| 子页 | 内容 |
| --- | --- |
| [benchmarks.md](benchmarks.md) | 重点 benchmark 与评测维度 |

## 数据集地图

| 类别 | 代表数据集 | 适用方向 |
| --- | --- | --- |
| 多机器人 / 多本体 | Open X-Embodiment, RH20T, BridgeData V2 | 通用策略、跨本体学习 |
| Manipulation | DROID, RoboTwin Dataset, DexYCB, GraspNet | 抓取、双臂、灵巧操作 |
| 第一人称 / 视频 | Ego4D, AMASS | 行为理解、模仿学习、视频预训练 |
| 3D 场景 / 空间感知 | EmbodiedScan, ScanNet, PartNet, ShapeNet | 感知、场景理解、导航 |
| 合成数据 | Nimbus, Synthetic Household Data | 低成本扩数据、仿真增强 |

## 高优先级数据集

| 数据集 | 为什么重要 |
| --- | --- |
| Open X-Embodiment | 多机器人大规模轨迹数据，通用策略主线必看 |
| DROID | 真实世界大规模操作数据集 |
| RH20T | 国内高质量真实技能数据集 |
| RoboTwin Dataset | 双臂操作方向代表数据 |
| EmbodiedScan | 具身场景理解多模态数据集 |
| Ego4D | 第一人称视频大规模基础资源 |

## Benchmark 与评测

| 基准 | 适合看什么 |
| --- | --- |
| ManiBench | 细粒度操作能力 |
| CALVIN | 语言条件策略学习 |
| RLBench | 机器人学习常用标准基准 |
| CRAM | 组合推理与操作 |
| VIMABench | VLA 模型评测 |
| OpenEQA | 具身问答 |
| EmbSpatial-Bench | 空间推理 |
| BEHAVIOR-1K / BEHAVIOR Challenge | 日常活动与长时程任务 |

## 使用建议

1. 先根据任务类型选数据，不要先被“规模最大”吸引。
2. 做模型时同时看 `数据分布 + 评测协议 + 真实部署条件`。
3. 如果要做工程复现，优先选有公开代码、公开评测协议的数据集和 benchmark。

## 对应原始全文

- 全量数据集和 benchmark 列表请看 [`../../03-papers-code.md`](../../03-papers-code.md)
