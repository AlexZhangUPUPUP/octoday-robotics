# 《Probabilistic Robotics》

[返回推荐书籍](../../00-basics.md#recommended-books) | [返回书籍索引](README.md)

![《Probabilistic Robotics》封面](<covers/Probabilistic-Robotics-en.pdf.png>)

> 封面图来自本地 PDF 首页缩略图。

> 说明：本页是仓库导读页，不是官方书摘或出版信息页。内容以仓库现有推荐理由、已核实资料和学习用途说明为主。

## 已核实资料

- MIT Press 页面：[https://mitpress.mit.edu/9780262201629/probabilistic-robotics/](https://mitpress.mit.edu/9780262201629/probabilistic-robotics/)
- 本地目录来源：`Probabilistic-Robotics-en.pdf`

- 作者：Sebastian Thrun、Wolfram Burgard、Dieter Fox
- 出版社：The MIT Press
- 出版信息：MIT Press 页面显示 Hardcover ISBN 9780262201629，2005。

## 这本书适合谁

- 想做真实机器人系统，而不是只停留在仿真里的读者。
- 关注定位、建图、状态估计和传感器不确定性的读者。
- 做移动机器人、导航、SLAM 或多传感器融合的读者。

## 这本书通常用来补什么

- 贝叶斯滤波作为机器人估计问题的统一框架。
- 运动模型、观测模型、定位、地图构建和 SLAM 的基本问题意识。
- 如何严肃处理噪声、误差和部分可观测性。

## 为什么推荐给具身智能学习者

只要系统进入真实环境，感知就不再干净、状态也不再完整可见。很多具身系统的真实瓶颈，其实不是模型太小，而是估计不稳。

## 建议怎么读

1. 不要把它只当成“移动机器人老教材”，它训练的是处理不确定性的底层习惯。
2. 先吃透状态估计主线，再看 SLAM 和地图问题。
3. 如果数学压力大，先建立概念图，再回头补推导。

## 学习导航

| 节 | 学习重点 |
| --- | --- |
| [Chapter 1 Introduction](#pr-ch1) | 先建立概率机器人学的问题边界 |
| [Chapter 2 Recursive State Estimation](#pr-ch2) | 把贝叶斯滤波作为全书骨架吃透 |
| [Chapter 3 Gaussian Filters](#pr-ch3) | 理解 KF / EKF / UKF 适用场景 |
| [Chapter 4 Nonparametric Filters](#pr-ch4) | 看离散和采样方法如何处理复杂分布 |
| [Chapter 5 Robot Motion](#pr-ch5) | 建立机器人运动模型与不确定性的联系 |
| [Chapter 6 Robot Perception](#pr-ch6) | 理解传感器模型怎样进入估计过程 |
| [Chapter 7 Mobile Robot Localization: Markov and Gaussian](#pr-ch7) | 从概率角度看定位问题 |
| [Chapter 8 Mobile Robot Localization: Grid and Monte Carlo](#pr-ch8) | 比较网格法和粒子法的差异 |
| [Chapter 9 Occupancy Grid Mapping](#pr-ch9) | 把地图构建问题形式化 |
| [Chapter 10 Simultaneous Localization and Mapping](#pr-ch10) | 理解 SLAM 的联合估计本质 |
| [Chapter 11 The GraphSLAM Algorithm](#pr-ch11) | 看图优化思路如何重构 SLAM |
| [Chapter 12 The Sparse Extended Information Filter](#pr-ch12) | 理解稀疏表示为何重要 |
| [Chapter 13 The FastSLAM Algorithm](#pr-ch13) | 理解粒子方法与地图因子分解 |
| [Chapter 14 Markov Decision Processes](#pr-ch14) | 从估计走向决策与控制 |
| [Chapter 15 Partially Observable Markov Decision Processes](#pr-ch15) | 在不完全观测下做规划 |
| [Chapter 16 Approximate POMDP Techniques](#pr-ch16) | 看近似方法如何解决可计算性问题 |
| [Chapter 17 Exploration](#pr-ch17) | 把主动探索和信息增益联系起来 |

## 按章节怎么学

<a id="pr-ch1"></a>
### Chapter 1 Introduction

- 核心问题：为什么机器人学必须严肃面对不确定性。
- 阅读提示：先建立“信念分布”视角，再读后面具体算法。

<a id="pr-ch2"></a>
### Chapter 2 Recursive State Estimation

- 核心问题：预测和更新怎样组成统一的估计闭环。
- 阅读提示：这章是全书骨架，值得反复回看。

<a id="pr-ch3"></a>
### Chapter 3 Gaussian Filters

- 核心问题：什么时候高斯假设足够，什么时候会失真。
- 阅读提示：重点比较 KF、EKF、UKF 各自的近似方式。

<a id="pr-ch4"></a>
### Chapter 4 Nonparametric Filters

- 核心问题：状态分布复杂时，怎样摆脱高斯限制。
- 阅读提示：把直方图滤波和粒子滤波放到同一个近似框架里看。

<a id="pr-ch5"></a>
### Chapter 5 Robot Motion

- 核心问题：机器人运动误差如何被建模和传播。
- 阅读提示：运动模型不是实现细节，而是定位和 SLAM 的前提。

<a id="pr-ch6"></a>
### Chapter 6 Robot Perception

- 核心问题：传感器观测如何转成似然模型。
- 阅读提示：建议把量测模型和你熟悉的传感器类型对照着读。

<a id="pr-ch7"></a>
### Chapter 7 Mobile Robot Localization: Markov and Gaussian

- 核心问题：不同定位场景下，估计方法的假设如何变化。
- 阅读提示：把全局定位、跟踪定位、数据关联放在一起理解。

<a id="pr-ch8"></a>
### Chapter 8 Mobile Robot Localization: Grid and Monte Carlo

- 核心问题：大状态空间下如何做可计算的定位。
- 阅读提示：这一章很适合和实际 AMR / SLAM 系统联想。

<a id="pr-ch9"></a>
### Chapter 9 Occupancy Grid Mapping

- 核心问题：如何把环境构造成可更新的概率地图。
- 阅读提示：重点理解独立性假设带来的方便和局限。

<a id="pr-ch10"></a>
### Chapter 10 Simultaneous Localization and Mapping

- 核心问题：位置和地图互为前提时，问题为什么变难。
- 阅读提示：这一章要抓住“联合估计”四个字。

<a id="pr-ch11"></a>
### Chapter 11 The GraphSLAM Algorithm

- 核心问题：SLAM 为什么能被重写成图优化问题。
- 阅读提示：如果你后来要看现代后端优化，这章很重要。

<a id="pr-ch12"></a>
### Chapter 12 The Sparse Extended Information Filter

- 核心问题：大规模问题里，稀疏性怎样换来效率。
- 阅读提示：这章适合作为“计算结构”补课来读。

<a id="pr-ch13"></a>
### Chapter 13 The FastSLAM Algorithm

- 核心问题：如何把路径不确定性和地图估计拆分处理。
- 阅读提示：重点看 posterior factoring 的直觉。

<a id="pr-ch14"></a>
### Chapter 14 Markov Decision Processes

- 核心问题：已知状态时，怎样在不确定动作结果下规划。
- 阅读提示：把它和强化学习里的 MDP 对照起来看很有帮助。

<a id="pr-ch15"></a>
### Chapter 15 Partially Observable Markov Decision Processes

- 核心问题：看不全状态时，如何在信念空间里决策。
- 阅读提示：这是从估计进入主动决策的重要桥梁。

<a id="pr-ch16"></a>
### Chapter 16 Approximate POMDP Techniques

- 核心问题：POMDP 很强，但为什么原始形式通常算不动。
- 阅读提示：把近似理解成工程折中，而不是“降级版”。

<a id="pr-ch17"></a>
### Chapter 17 Exploration

- 核心问题：机器人怎样主动探索环境并获取信息。
- 阅读提示：这一章和主动感知、探索式导航联系最紧。

## 延伸资源

- [yvonshong/Probabilistic-Robotics](https://github.com/yvonshong/Probabilistic-Robotics)：适合中文读者快速进入整本书的问题框架。
- [Bazs/probabilistic-robotics](https://github.com/Bazs/probabilistic-robotics)：习题实现更全，适合拿来做算法对照。
- [bornabesic/probabilistic-robotics](https://github.com/bornabesic/probabilistic-robotics)：偏算法落地，可直接帮助理解运动模型、滤波和 SLAM 的执行流程。

## 建议阅读顺序

- 如果你偏移动机器人，主线建议是 `2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 10`。
- 如果你偏感知与状态估计，至少把 `2、3、4、6` 读透。
- 读完后再看 [Navigation & Spatial Intelligence](../../03-papers.md#navigation-spatial-intelligence) 会更有判断力。
