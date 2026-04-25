# CS285: Deep Reinforcement Learning

[返回在线课程](../../00-basics.md#online-courses) | [返回课程索引](README.md)

> 说明：本页是仓库导读页，不是官方 syllabus 镜像页。内容以仓库原表格、已核实资料和学习用途建议为主。

## 已核实资料

- 课程主页：[https://rail.eecs.berkeley.edu/deeprlcourse/](https://rail.eecs.berkeley.edu/deeprlcourse/)

- 机构：UC Berkeley
- 讲师：Sergey Levine
- 备注：官方课程页会随学期更新；当前能看到 Spring 2026 课程框架。

## 这门课适合谁

- 已经有基础强化学习概念，想进到深度强化学习实践的读者。
- 后续准备做 robot learning、policy learning 或 decision making 的读者。

## 这门课通常用来补什么

- imitation learning、policy gradient、offline RL 等核心主题。
- 课程作业驱动的 deep RL 实践路径。

## 为什么推荐给具身智能学习者

如果你准备进入机器人学习或长期决策问题，这门课很适合补现代 RL 训练套路。

## 建议怎么学

1. 建议先有 Sutton & Barto 的基础。
2. 可以把课程内容与仓库里的 [论文合集](../../03-papers.md#embodied-agents-reasoning) 交叉阅读。

## 课程导航

以下表格按 Berkeley CS285 官方课程页的 lecture schedule 整理。

| 讲次 | 主题 | 学习重点 |
| :--- | :--- | :--- |
| Lecture 1 | Introduction | 先建立 imitation learning 和 RL 的整体地图 |
| Lecture 2 | Behavioral Cloning | 理解监督式模仿学习为什么能成为强基线 |
| Lecture 3 | Behavioral Cloning Part 2 | 看清分布偏移和数据收集问题 |
| Lecture 4 | RL Basics | 把回报、轨迹、MDP 和策略优化的基本定义串起来 |
| Lecture 5 | Policy Gradients | 进入直接优化策略的第一条主线 |
| Lecture 6 | Actor Critic | 理解策略和值函数如何协同更新 |
| Lecture 7 | Value-Based RL | 对比 value-based 和 policy-based 两类思路 |
| Lecture 8 | Q-learning in Practice | 关注深度 Q 学习里的稳定训练问题 |
| Lecture 9 | Advanced Policy Gradients Part 1 | 理解更稳健的策略更新为什么重要 |
| Lecture 10 | Advanced Policy Gradients Part 2 | 继续梳理 TRPO / PPO 一类方法的动机 |
| Lecture 11 | Variational Inference | 把 RL 放回概率推断视角中看 |
| Lecture 12 | VI in RL | 理解推断框架如何重写 RL 目标 |
| Lecture 13 | Control as Inference | 学会从另一条推导路径理解策略优化 |
| Lecture 14 | LLM RL | 看到 RL 如何进入语言模型后训练 |
| Lecture 15 | Model-Based RL Part 1 | 理解 dynamics model 在决策里的作用 |
| Lecture 16 | Model-Based RL Part 2 | 关注模型误差、规划和样本效率之间的权衡 |
| Lecture 17 | Offline RL Part 1 | 先建立“只看数据集也要学策略”的场景认识 |
| Lecture 18 | Offline RL Part 2 | 理解分布偏移和保守学习的核心难点 |
| Lecture 19 | Exploration | 认识稀疏奖励下为什么探索会变难 |
| Lecture 20 | RL Theory | 从理论角度回看收敛与样本复杂度 |
| Lecture 21 | Midterm Review Part 1 | 复盘前半程算法之间的关系 |
| Lecture 22 | Midterm Review Part 2 | 把策略梯度、值函数和推断视角再串一次 |
| Lecture 23 | Advanced Exploration | 进一步看内在奖励和不确定性驱动的探索 |
| Lecture 24 | Multi-task RL | 理解共享表示、迁移和多任务训练 |
| Lecture 25 | Challenges and Open Problems | 对当前 deep RL 的瓶颈和研究空白形成判断 |
