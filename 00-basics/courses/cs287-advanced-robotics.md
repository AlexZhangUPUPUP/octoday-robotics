# CS287: Advanced Robotics

[返回在线课程](../../00-basics.md#online-courses) | [返回课程索引](README.md)

> 说明：本页是仓库导读页，不是官方 syllabus 镜像页。内容以仓库原表格、已核实资料和学习用途建议为主。

## 已核实资料

- 课程主页：[https://people.eecs.berkeley.edu/~pabbeel/cs287-fa19/](https://people.eecs.berkeley.edu/~pabbeel/cs287-fa19/)

- 机构：UC Berkeley
- 讲师：Pieter Abbeel
- 备注：当前仓库使用的是 Fall 2019 官方课程页。

## 这门课适合谁

- 已经具备基础数学和机器人背景，想进入高级专题的读者。
- 准备看 learning-based robotics、control、probabilistic methods 的读者。

## 这门课通常用来补什么

- 高级机器人课程常见的主题组织方式。
- 从作业、项目到研究论文的过渡路径。

## 为什么推荐给具身智能学习者

这是从课程学习走向研究阅读的一个很好过渡。

## 建议怎么学

1. 建议在机器人学基础和概率基础比较稳后再看。
2. 适合作为“进阶课程参照系”。

## 课程导航

以下表格按 Berkeley CS287 Fall 2019 官方 syllabus 整理，保留了行业讲座与课程收尾环节。

| 讲次 | 主题 | 学习重点 |
| :--- | :--- | :--- |
| Lecture 1 | Course Introduction | 先建立整门课的算法地图 |
| Lecture 2 | MDPs: Exact Methods | 把最优控制离散化成可解的动态规划问题 |
| Lecture 3 | Discretization of Continuous State Space MDPs | 理解连续状态问题如何做近似求解 |
| Lecture 4 | Function Approximation / Feature-based Representations | 看到逼近方法如何替代 tabular 表示 |
| Lecture 5 | LQR, iterative LQR / Differential Dynamic Programming | 进入局部最优控制的核心工具箱 |
| Lecture 6 | Unconstrained Optimization | 看懂很多机器人算法背后的优化基础 |
| Lecture 7 | Constrained Optimization | 把约束显式纳入控制和规划问题 |
| Lecture 8 | Optimization-based Control: Basics | 建立 collocation、shooting、MPC 的基本直觉 |
| Lecture 9 | Optimization-based Control: Advanced | 理解接触和复杂约束会怎样提高难度 |
| Lecture 10 | Motion Planning: RRT, PRM, TrajOpt | 区分采样法和优化法的适用场景 |
| Lecture 11 | Probability Review, Bayes Filters, Multivariate Gaussians | 回到状态估计和不确定性建模基础 |
| Lecture 12 | Kalman Filtering, EKF, UKF | 理解线性与非线性滤波框架 |
| Lecture 13 | Smoother, MAP, Maximum Likelihood, EM | 把状态估计和参数学习连起来 |
| Lecture 14 | Particle Filters | 进入非参数 belief 跟踪方法 |
| Lecture 15 | POMDPs | 理解部分可观测下的规划与决策 |
| Lecture 16 | Industry: Ike | 看自动驾驶卡车系统的真实约束 |
| Lecture 17 | Imitation Learning | 从 demonstration 学策略 |
| Lecture 18 | RL1: Policy Gradients | 把强化学习拉回可优化策略框架 |
| Lecture 19 | RL2: Off-policy RL | 关注样本复用和训练稳定性 |
| Lecture 20 | RL3: Model-based RL | 连接 dynamics model、planning 和 data efficiency |
| Lecture 21 | How do simulators work? | 理解仿真器为何影响 robot learning 质量 |
| Lecture 22 | Sim2Real | 直面 domain gap 和迁移问题 |
| Lecture 23 | Industry: Waymo | 看大规模自动驾驶研发视角 |
| Lecture 24 | Industry: Skydio | 看无人机系统里的视觉自治问题 |
| Lecture 25 | Backstories behind Papers | 了解研究想法是如何成形和迭代的 |
| Lecture 26 | Autonomous Helicopters and Course Wrap-Up | 用经典案例回收整门课的主线 |
| Lecture 27 | Project Presentations | 用项目检验方法是否真的能迁移 |
