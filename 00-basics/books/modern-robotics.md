# 《现代机器人学》

[返回推荐书籍](../../00-basics.md#recommended-books) | [返回书籍索引](README.md)

![《现代机器人学》封面](<covers/《Modern Robotics, Mechanics, Planning, And Control》- Kevin M. Lynch - 第二版.pdf.png>)

> 封面图来自本地 PDF 首页缩略图。

> 说明：本页是仓库导读页，不是官方书摘或出版信息页。内容以仓库现有推荐理由、已核实资料和学习用途说明为主。

## 已核实资料

- 官方配套站：[https://modernrobotics.northwestern.edu/](https://modernrobotics.northwestern.edu/)
- 配套课程页：[https://www.coursera.org/specializations/modernrobotics](https://www.coursera.org/specializations/modernrobotics)

- 作者：Kevin M. Lynch、Frank C. Park
- 出版信息：官方配套站页面注明该书对应 Cambridge University Press。
- 备注：这里补的是作者团队维护的官方配套站，不是单独的出版社售卖页。

## 这本书适合谁

- 想用更现代、更统一的数学框架理解机器人学的读者。
- 对旋量理论、李群李代数、指数坐标有兴趣的读者。
- 计划深入控制、规划和动力学建模的研究型读者。

## 这本书通常用来补什么

- 用现代表示法统一描述位姿、速度与运动。
- 用更结构化的方式理解运动学、动力学和控制。
- 把“公式堆砌”转成“几何结构 + 变换关系”的理解路径。

## 为什么推荐给具身智能学习者

很多具身模型最后都要落回机器人本体。你需要一个稳定的底层数学语言，把 perception、planning 和 action 接到真实系统上。

## 建议怎么读

1. 如果你之前没接触过旋量理论，先把基础概念慢慢吃透。
2. 读的时候尽量自己推一遍关键公式，而不是只看结论。
3. 可以和《机器人学导论》对照阅读，效果通常更好。

## 学习导航

> 我保留原书章节名，是为了方便和 PDF 对照；下面写的是学习导读，不按原书目录逐条复述。

| 章节 | 学习重点 |
| --- | --- |
| [Chapter 1 Preview](#mr-ch1) | 先看清整本书要解决什么问题 |
| [Chapter 2 Configuration Space](#mr-ch2) | 建立机器人状态空间与约束意识 |
| [Chapter 3 Rigid-Body Motions](#mr-ch3) | 把 SE(3)、twist、wrench 变成直觉 |
| [Chapter 4 Forward Kinematics](#mr-ch4) | 理解 PoE 为什么比死记参数更自然 |
| [Chapter 5 Velocity Kinematics and Statics](#mr-ch5) | 把雅可比真正用起来 |
| [Chapter 6 Inverse Kinematics](#mr-ch6) | 学会从任务目标回到关节空间 |
| [Chapter 7 Kinematics of Closed Chains](#mr-ch7) | 扩展到并联和闭链结构 |
| [Chapter 8 Dynamics of Open Chains](#mr-ch8) | 进入力矩、惯量和递推动力学 |
| [Chapter 9 Trajectory Generation](#mr-ch9) | 区分几何路径和时间安排 |
| [Chapter 10 Motion Planning](#mr-ch10) | 看清主流规划方法的取舍 |
| [Chapter 11 Robot Control](#mr-ch11) | 把模型变成稳定闭环行为 |
| [Chapter 12 Grasping and Manipulation](#mr-ch12) | 从控制机器人走向控制接触与操作 |
| [Chapter 13 Wheeled Mobile Robots](#mr-ch13) | 把机器人学主线扩展到底盘移动 |

## 按章节怎么学

<a id="mr-ch1"></a>
### Chapter 1 Preview

- 本章讲什么：先从机器人机构、执行器、减速器、传感器和课程目标切入，给整本书搭一个统一框架。
- 为什么重要：它明确了本书不是泛 AI 机器人综述，而是围绕 mechanics、planning、control 展开的现代机器人学主线。
- 建议关注：把“现代螺旋理论视角”和“本书后续 12 章的分工”先建立起来，读后面会轻松很多。

<a id="mr-ch2"></a>
### Chapter 2 Configuration Space

- 本章讲什么：讲自由度、构型空间、Grubler 公式、拓扑表示，以及 holonomic / nonholonomic 约束、任务空间和工作空间。
- 为什么重要：它告诉你机器人“有哪些可能状态”，这是规划和控制前必须明确的状态空间基础。
- 建议关注：不要只把 C-space 当作抽象数学空间，尽量把它和实际机构的关节约束、闭链结构、移动底盘联系起来。

<a id="mr-ch3"></a>
### Chapter 3 Rigid-Body Motions

- 本章讲什么：系统引入平面/空间刚体运动、旋转矩阵、齐次变换、指数坐标、twist 和 wrench。
- 为什么重要：这是全书最核心的语言层。PoE、雅可比、动力学和控制都在这里统一到 SE(3) 框架下。
- 建议关注：重点理解“旋转/位姿是群”“速度/力是 twist 与 wrench”这两个现代机器人学的核心视角。

<a id="mr-ch4"></a>
### Chapter 4 Forward Kinematics

- 本章讲什么：围绕 Product of Exponentials 公式建立正运动学，用空间坐标和本体坐标两种方式描述关节螺旋轴。
- 为什么重要：它把关节变量和末端位姿的映射写成了结构清晰、几何意义很强的表达。
- 建议关注：先把 PoE 的几何解释吃透，再去对照附录里的 D-H 表示，就能看出两者取舍。

<a id="mr-ch5"></a>
### Chapter 5 Velocity Kinematics and Statics

- 本章讲什么：讨论 manipulator Jacobian、空间/本体雅可比、奇异性、操控性和静力映射。
- 为什么重要：雅可比是运动学和力学之间最常用的中间层，也是后面控制和操作分析的核心工具。
- 建议关注：重点看雅可比秩退化意味着什么，以及它为什么同时决定速度能力和受力能力。

<a id="mr-ch6"></a>
### Chapter 6 Inverse Kinematics

- 本章讲什么：分别处理解析逆运动学、数值逆运动学和逆速度学，并顺带说明闭环约束带来的变化。
- 为什么重要：任务给的往往是末端目标，而不是关节角，所以 IK 是“目标表达”向“机器人执行”落地的关键层。
- 建议关注：把解析法和数值法的适用边界看清楚，工程里多数复杂系统最终都要依赖数值法。

<a id="mr-ch7"></a>
### Chapter 7 Kinematics of Closed Chains

- 本章讲什么：讨论平行机构和一般闭链机构的正逆运动学、微分运动学和奇异性。
- 为什么重要：闭链机器人、并联平台和多环机构无法简单照搬开链结论，这一章是结构扩展。
- 建议关注：要特别留意闭链约束如何改变可动性分析和奇异性判断。

<a id="mr-ch8"></a>
### Chapter 8 Dynamics of Open Chains

- 本章讲什么：从拉格朗日法、单刚体动力学、牛顿-欧拉递推到正动力学、任务空间动力学、约束和驱动摩擦。
- 为什么重要：这一章把“位姿与速度”推进到“力矩、惯量、加速度”，是控制和仿真的核心基础。
- 建议关注：优先理解动力学结构而不是推导细节，尤其是质量矩阵、逆动力学和递推算法。

<a id="mr-ch9"></a>
### Chapter 9 Trajectory Generation

- 本章讲什么：定义轨迹的路径与时间标定，介绍点到点轨迹、经由点轨迹和时间最优时间缩放。
- 为什么重要：规划不仅要决定去哪里，还要决定何时到、速度多快、是否满足执行器约束。
- 建议关注：把 geometric path 和 time scaling 分开理解，这会直接影响你对规划器和控制器接口的认识。

<a id="mr-ch10"></a>
### Chapter 10 Motion Planning

- 本章讲什么：从配置空间障碍和图搜索讲起，再进入网格法、采样法、虚拟势场和优化方法。
- 为什么重要：它回答的是“如何在约束环境中找到可行运动”，是机器人自主性的核心问题之一。
- 建议关注：每类方法都有明确取舍，读的时候要把 completeness、效率、可扩展性和工程可用性对比着看。

<a id="mr-ch11"></a>
### Chapter 11 Robot Control

- 本章讲什么：系统介绍速度输入控制、力/力矩输入控制、力控制、混合运动-力控制和阻抗控制。
- 为什么重要：这章把前面的运动学和动力学真正转成闭环行为，是“机器人会不会按要求做事”的关键。
- 建议关注：先理解误差动力学，再理解为什么接触任务必须区分运动方向和受力方向。

<a id="mr-ch12"></a>
### Chapter 12 Grasping and Manipulation

- 本章讲什么：建立接触运动学、摩擦与接触力模型，再进入 form closure、force closure 和操作问题。
- 为什么重要：具身智能最终要操作物体，这一章是从“控制机器人”迈向“控制机器人与物体耦合系统”。
- 建议关注：把接触约束和摩擦锥看清楚，它们是抓取、推操和稳定性分析的基础。

<a id="mr-ch13"></a>
### Chapter 13 Wheeled Mobile Robots

- 本章讲什么：区分全向和非完整约束轮式机器人，讨论建模、可控性、规划、反馈控制、里程计和移动操作。
- 为什么重要：它把前面那套机器人学语言扩展到移动底盘，也自然衔接今天大量 AMR / mobile manipulation 场景。
- 建议关注：重点看 nonholonomic constraint 为什么和闭链约束不同，以及这会怎样改变控制与规划。

## 建议阅读顺序

- 如果你要打基础，先以 Chapter 2 到 Chapter 6 为主线。
- 如果你偏操作与控制，Chapter 5、8、11、12 是主轴。
- 如果你偏移动机器人，Chapter 2、3、10、13 可以单独拉成一条学习线。
