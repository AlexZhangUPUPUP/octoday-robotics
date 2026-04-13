# 项目与工具

这里把原来的“论文里的代码入口”和“工具与平台”合并成一个更像开发者工作台的版块。

## 子页导航

| 子页 | 内容 |
| --- | --- |
| [simulators.md](simulators.md) | 仿真器、物理引擎与环境选择 |
| [frameworks.md](frameworks.md) | 开发框架、模型和工具链 |
| [hardware.md](hardware.md) | 硬件平台与开放机器人底座 |

## 你会在这里找到什么

| 类型 | 代表项目 |
| --- | --- |
| 仿真平台 | MuJoCo, Isaac Sim, Habitat Sim, SAPIEN, Genesis, PyBullet |
| 机器人开发框架 | ROS/ROS2, Drake, OMPL |
| 具身模型/策略 | OpenVLA, Diffusion Policy, UMI, GR-1 |
| 场景/开发平台 | Gazebo Sim, Webots, CoppeliaSim |
| 硬件与开放平台 | TurtleBot 4, Clearpath Husky, kscale K-Bot |

## 开源项目地图

| 项目 | 类型 | 用途 |
| --- | --- | --- |
| OpenVLA | VLA 模型 | 通用机器人策略与微调入口 |
| Diffusion Policy | 操作策略 | 灵巧操作和模仿学习经典框架 |
| UMI | 数据采集 / 操作接口 | 真实世界机器人示教入口 |
| ROS / ROS2 | 系统框架 | 机器人软件工程基础设施 |
| MuJoCo | 物理仿真 | RL 与控制实验高频选择 |
| Isaac Sim | 仿真平台 | NVIDIA 体系下训练、部署和合成数据入口 |
| Habitat Sim | 导航仿真 | 3D 场景与导航研究基础平台 |
| SAPIEN | 交互仿真 | 操作和铰接物体交互常用 |
| Genesis | 物理引擎 | 轻量快速，适合 Embodied/Physical AI 场景 |
| Drake | 规划与控制 | 偏系统建模和控制分析 |
| OMPL | 运动规划 | 经典运动规划库 |
| Gazebo Sim | 通用机器人仿真 | ROS 生态兼容度高 |

## 常见组合方式

| 目标 | 推荐组合 |
| --- | --- |
| 机器人学入门 | `ROS2 + Gazebo Sim + TurtleBot 4` |
| 操作任务复现 | `MuJoCo / SAPIEN + Diffusion Policy + OpenVLA` |
| 导航研究 | `Habitat Sim + HM3D + NavGPT/VLFM` |
| 工程部署 | `Isaac Sim + ROS2 + Jetson / 真机平台` |

## 对应原始内容

- 论文/代码总表：[`../../03-papers-code.md`](../../03-papers-code.md)
- 工具/平台总表：[`../../04-tools.md`](../../04-tools.md)
