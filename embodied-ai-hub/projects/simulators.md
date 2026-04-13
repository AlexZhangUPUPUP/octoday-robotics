# 仿真器与物理引擎

## 常用选择

| 工具 | 适合场景 | 特点 |
| --- | --- | --- |
| MuJoCo | RL、控制、manipulation | 快、稳、研究生态成熟 |
| Isaac Sim | 工程部署、合成数据、NVIDIA 生态 | 工业化工具链强 |
| Isaac Gym | GPU 并行训练 | 大规模强化学习 |
| Habitat Sim | 导航与 3D 场景 | 具身导航主流底座 |
| SAPIEN | 交互式操作任务 | 部件级交互优秀 |
| Genesis | 物理 AI 场景 | 轻量、快速、Python 友好 |
| Gazebo Sim | ROS 生态 | 软件工程衔接好 |
| PyBullet | 原型开发 | 轻量、门槛低 |
| Webots | 教学与跨平台使用 | 桌面应用友好 |
| CoppeliaSim | 教学/工业研究 | 多接口支持 |

## 怎么选

| 你的目标 | 推荐起步 |
| --- | --- |
| 强化学习复现 | MuJoCo / Isaac Gym |
| 导航研究 | Habitat Sim |
| Manipulation 研究 | SAPIEN / MuJoCo / Isaac Sim |
| ROS 工程项目 | Gazebo Sim |
| 快速原型 | PyBullet |

## 来源

- 整理自 [`../../04-tools.md`](../../04-tools.md)
