# Manipulation

这一页聚焦机器人操作主线，包括抓取、双臂、遥操作、扩散策略与精细操作。

## 推荐论文

| 论文 | 关键词 | 为什么值得看 |
| --- | --- | --- |
| Diffusion Policy | 扩散策略 | 当前 manipulation 论文中最常被引用的动作生成路线之一 |
| PerAct | Language-conditioned manipulation | 语言条件操作经典工作 |
| Octo | 通用机器人策略 | 从单任务走向通用策略的重要节点 |
| ACT | 双手操作 | 低成本硬件上的精细双臂操作 |
| UMI | 通用操作接口 | 真实世界示教和操作接口关键工作 |
| DexCap | 动作捕捉数据 | 灵巧操作数据采集入口 |
| AnyTeleop | 遥操作 | 视觉遥操作系统代表 |
| RVT / RVT-2 | 3D 操作 | 3D 物体操作与少样本精确 manipulation |
| VoxPoser | 3D 价值图 | 操作与空间推理结合 |
| ReBot | Real-to-Sim-to-Real | 数据与 sim2real 闭环 |

## 适合一起看的配套资源

- 数据集：`DROID`, `Open X-Embodiment`, `RoboTwin Dataset`
- Benchmark：`ManiBench`, `CALVIN`, `Franka Kitchen`, `RLBench`
- 工具链：`MuJoCo`, `Isaac Sim`, `SAPIEN`, `Diffusion Policy`, `OpenVLA`

## 建议阅读顺序

1. 先看 `PerAct` 和 `Diffusion Policy`，建立操作任务的基本范式。
2. 再看 `Octo`、`UMI`、`AnyTeleop`，理解通用化和数据采集。
3. 最后看 `RVT-2`、`ReBot`、`VoxPoser`，补精细操作与跨域迁移。

## 来源

- 选自 [`../../03-papers-code.md`](../../03-papers-code.md) 的 `Manipulation` 相关内容。
