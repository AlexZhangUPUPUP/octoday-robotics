# 学习中心

这里承接原来的 `00-basics.md`，但不再是一篇单独长文，而是一个适合 GitHub 逐步扩展的学习入口。

## 子页导航

| 子页 | 内容 |
| --- | --- |
| [books.md](books.md) | 推荐书单与阅读顺序 |
| [courses.md](courses.md) | 课程地图与对应能力 |
| [glossary.md](glossary.md) | 高频术语速查 |
| [roadmap.md](roadmap.md) | 7 阶段学习路径 |

## 你会在这里找到什么

| 模块 | 作用 |
| --- | --- |
| 书单 | 帮你补机器人学、RL、CV、ROS、Manipulation 基础 |
| 课程 | 帮你建立从理论到实践的最短课程路径 |
| 术语 | 快速看懂论文里的常见概念 |
| 路线图 | 给零基础或转方向的人一条可执行学习路径 |

## 推荐书籍

| 资源 | 适合谁 | 为什么值得先看 |
| --- | --- | --- |
| 《机器人学导论》 | 初学者 | 建立运动学、动力学和空间描述基础 |
| 《现代机器人学》 | 理论型读者 | 现代机器人学表述更清晰，数学体系更完整 |
| 《强化学习（第2版）》 | AI 背景读者 | 补齐智能体学习与决策核心范式 |
| 《Probabilistic Robotics》 | 研究者 | 感知、定位、地图与不确定性处理经典 |
| 《Embodied AI: How to Train Your Robot》 | 实践者 | 更贴近具身智能工程实践 |
| 《The Robot Operating System for Absolute Beginners》 | 工程开发者 | 快速接轨 ROS/ROS2 软件体系 |

## 优先课程

| 课程 | 机构/讲师 | 作用 |
| --- | --- | --- |
| CS223A: Introduction to Robotics | Stanford | 机器人学基础 |
| CS285: Deep Reinforcement Learning | UC Berkeley | RL 核心算法 |
| MIT 6.S191: Introduction to Deep Learning | MIT | 深度学习基础 |
| MIT 6.4210: Robotic Manipulation | MIT | Manipulation 主线课程 |
| Robot Perception | UPenn | 机器人感知专题 |
| Deep Learning for Robotics | ETH Zurich | 深度学习与机器人结合 |

## 术语速查

| 术语 | 一句话解释 |
| --- | --- |
| Embodied AI | 智能体通过身体与环境闭环交互产生能力 |
| Sim2Real | 策略从仿真迁移到现实世界 |
| VLA | 视觉-语言-动作统一模型 |
| World Model | 用于预测环境变化和规划的内部模型 |
| Diffusion Policy | 把动作学习建模为条件扩散生成 |
| Imitation Learning | 通过专家示教学习策略 |
| Teleoperation | 人类远程操控机器人收集示教或执行任务 |
| Cross-Embodiment Transfer | 跨本体/跨形态迁移策略 |

## 建议学习路径

1. 先补机器人学、深度学习、强化学习三块地基。
2. 再选一个仿真平台跑通最小闭环，例如 `MuJoCo` 或 `Isaac Sim`。
3. 之后读 `OpenVLA`、`RT-2`、`Diffusion Policy` 等代表工作，建立对当前主流范式的认识。
4. 再把视线切到数据集、Benchmark 和开源框架，开始做复现。
5. 最后结合岗位需求决定更偏 `VLA / Manipulation / Navigation / 控制 / 系统工程` 哪条线。

## 对应原始全文

- 全量版请看 [`../../00-basics.md`](../../00-basics.md)
