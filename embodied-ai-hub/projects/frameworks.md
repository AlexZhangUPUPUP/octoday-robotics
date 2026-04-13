# 开发框架与模型工具链

## 核心工具链

| 工具 | 类型 | 作用 |
| --- | --- | --- |
| ROS / ROS2 | 机器人软件框架 | 模块化系统开发基础设施 |
| OpenVLA | 具身模型 | 开源 VLA 基座 |
| Diffusion Policy | 操作策略 | 模仿学习与动作生成 |
| UMI | 操作接口 | 真实世界机器人示教 |
| GR-1 | 多模态机器人模型 | 视频驱动操作模型 |
| Drake | 规划与控制 | 系统分析与控制研究 |
| OMPL | 运动规划 | 经典运动规划算法库 |
| Tairos / LinkCraft / 悟能 | 产业平台 | 大模型与机器人能力平台化 |

## 推荐组合

- `ROS2 + Gazebo + TurtleBot 4`：机器人软件入门。
- `MuJoCo + Diffusion Policy + OpenVLA`：操作任务复现。
- `Isaac Sim + ROS2 + 真机平台`：偏工程化部署。

## 来源

- 整理自 [`../../04-tools.md`](../../04-tools.md)
