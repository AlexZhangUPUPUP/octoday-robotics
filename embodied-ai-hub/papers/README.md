# 论文索引

这里承接原来的 `03-papers-code.md`，但把“论文、代码、数据集、基准、综述”重新拆成更清楚的研究入口。

## 研究主线

| 方向 | 说明 | 入口 |
| --- | --- | --- |
| Embodied Foundation Models | 机器人基础模型与通用策略 | [foundation-models.md](foundation-models.md) |
| Vision-Language-Action | 视觉-语言-动作统一模型 | [vla.md](vla.md) |
| Embodied Agents & Reasoning | 推理、规划与长时程智能体 | [agents.md](agents.md) |
| Manipulation | 抓取、双臂、灵巧操作、遥操作与扩散策略 | [manipulation.md](manipulation.md) |
| Perception & Spatial Intelligence | 感知、导航、空间理解 | [perception.md](perception.md) |
| Sim2Real | 从仿真到现实的迁移问题 | [sim2real.md](sim2real.md) |
| Survey | 快速建立全局视角 | [surveys.md](surveys.md) |

## 起步优先读

| 论文 | 为什么先读 |
| --- | --- |
| RT-1 | 大规模真实机器人 Transformer 控制起点 |
| RT-2 | 把视觉语言知识迁移到机器人动作空间 |
| PaLM-E | 多模态语言模型走向具身推理的重要节点 |
| OpenVLA | 开源 VLA 代表作，便于后续复现 |
| RoboCat | 自我改进机器人基础模型路线 |
| Octo | 通用机器人策略与开源生态入口 |
| Diffusion Policy | Manipulation 学习的代表框架 |
| PerAct | 语言条件下的操作基线之一 |
| NavGPT | 视觉语言导航中的显式推理代表作 |
| Embodied AI: A Survey | 快速补全整个领域视图 |

## 关键方向速览

### Embodied Foundation Models

- 入口见 [foundation-models.md](foundation-models.md)
- `RT-1`, `RT-2`, `PaLM-E`, `RoboCat`, `OpenVLA`, `AutoRT`, `GR-2`

### Vision-Language-Action

- 入口见 [vla.md](vla.md)
- `OpenVLA`, `π0`, `DexVLA`, `SwitchVLA`, `Humanoid-VLA`, `SafeVLA`

### Embodied Agents & Reasoning

- 入口见 [agents.md](agents.md)
- `SayCan`, `Voyager`, `SayPlan`, `DEPS`, `Embodied-CoT`, `DualPLAN`

### Sim2Real

- 入口见 [sim2real.md](sim2real.md)
- 重点看视觉编码器预训练、真实-仿真-真实闭环、零样本迁移三条线。
- 这条线和 `projects/` 中的仿真平台、`datasets/` 中的数据质量高度耦合。

### Survey

- 入口见 [surveys.md](surveys.md)
- `Embodied AI: A Survey`, `Vision-Language-Action Models: A Survey`, `Embodied Foundation Models: A Survey`

## 推荐阅读顺序

1. 先读 `Survey`，建立全局图谱。
2. 再读 `RT-1 / RT-2 / PaLM-E / OpenVLA`，建立 VLA 与 Foundation Model 主线。
3. 接着按任务拆到 `Manipulation` 和 `Perception & Spatial Intelligence`。
4. 最后把 `Sim2Real + Datasets + Benchmarks` 接起来看工程可落地性。

## 对应原始全文

- 全量版请看 [`../../03-papers-code.md`](../../03-papers-code.md)
