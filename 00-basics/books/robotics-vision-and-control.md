# 《Robotics, Vision and Control》

[返回推荐书籍](../../00-basics.md#recommended-books) | [返回书籍索引](README.md)

![《Robotics, Vision and Control》封面](<covers/Robotics, Vision and Control Fundamental Algorithms in Python (3rd ed.) (Peter Corke) (z-library.sk, 1lib.sk, z-lib.sk).pdf.png>)

> 封面图来自本地 PDF 首页缩略图。

> 说明：本页是仓库导读页，不是官方书摘或出版信息页。内容以仓库现有推荐理由、已核实资料和学习用途说明为主。

## 已核实资料

- 作者官方页（MATLAB 版）：[https://www.petercorke.com/RVC1/](https://www.petercorke.com/RVC1/)
- Springer 页面（Python 3rd ed.）：[https://link.springer.com/book/10.1007/978-3-031-07262-8](https://link.springer.com/book/10.1007/978-3-031-07262-8)

- 作者：Peter Corke
- 备注：当前封面图与本地 PDF 对应的是 Python 第三版；作者官网保留了经典 MATLAB 版本介绍，Springer 页面展示新版延展版本。
- 当前仓库原描述兼顾经典 MATLAB 路线与新版资料，因此本页同时给出作者官网与 Springer 页面。

## 这本书适合谁

- 想通过代码示例快速建立机器人系统直觉的读者。
- 需要把机器人学、视觉和控制放在一起理解的读者。
- 想做教学实验、课程作业和快速原型验证的读者。

## 这本书通常用来补什么

- 机器人学、计算机视觉与控制之间的实际连接方式。
- 如何通过示例和工具快速验证算法想法。
- 从数学模型到实验原型的一条更平滑的路径。

## 为什么推荐给具身智能学习者

很多书在理论上很强，但离动手有距离。这本书的价值在于把多个模块放进同一条实践链路里。

## 建议怎么读

1. 把它当成“理论到实验”的桥梁材料。
2. 适合和具体平台、仿真环境一起配套学习。
3. 如果你更偏工程实践，这本书通常会比纯理论教材更容易形成正反馈。

## 学习导航

> 我保留原书章节名，是为了方便和 PDF 对照；下面更偏学习导读，不复述原书内容。

| 章节 | 学习重点 |
| --- | --- |
| [Chapter 1 Introduction](#rvc-ch1) | 先建立机器人与视觉是一条链路的直觉 |
| [Chapter 2 Representing Position and Orientation](#rvc-ch2) | 打牢位姿表达和坐标变换 |
| [Chapter 3 Time and Motion](#rvc-ch3) | 从静态几何过渡到动态系统 |
| [Chapter 4 Mobile Robot Vehicles](#rvc-ch4) | 认识不同移动平台的约束 |
| [Chapter 5 Navigation](#rvc-ch5) | 区分局部避障和全局规划 |
| [Chapter 6 Localization](#rvc-ch6) | 把定位、建图和 SLAM 串起来 |
| [Chapter 7 Robot Arm Kinematics](#rvc-ch7) | 从操作任务理解机械臂运动学 |
| [Chapter 8 Manipulator Velocity](#rvc-ch8) | 把雅可比和数值 IK 落到控制层 |
| [Chapter 9 Dynamics and Control](#rvc-ch9) | 从几何运动过渡到受力控制 |
| [Chapter 10 Light and Color](#rvc-ch10) | 回到视觉输入的物理基础 |
| [Chapter 11 Image Formation](#rvc-ch11) | 把相机模型和标定看明白 |
| [Chapter 12 Images and Image Processing](#rvc-ch12) | 掌握图像处理常见中间层 |
| [Chapter 13 Image Feature Extraction](#rvc-ch13) | 学会从图像里抽结构化特征 |
| [Chapter 14 Using Multiple Images](#rvc-ch14) | 进入三维重建与多视图几何 |
| [Chapter 15 Vision-Based Control](#rvc-ch15) | 看视觉如何直接驱动机器人动作 |
| [Chapter 16 Advanced Visual Servoing](#rvc-ch16) | 理解视觉伺服的扩展空间 |

## 按章节怎么学

### Part I Foundations

<a id="rvc-ch1"></a>
### Chapter 1 Introduction

- 本章讲什么：先给出机器人发展的背景、分类和基本问题，再用 sense-plan-act 建立对机器人系统的整体理解。
- 为什么重要：这本书不是纯数学教材，它一开始就在强调机器人是“数据驱动、依赖传感、最终要行动”的系统。
- 建议关注：把“机器人学问题”和“视觉问题”看成同一条工程链路里的不同环节。

<a id="rvc-ch2"></a>
### Chapter 2 Representing Position and Orientation

- 本章讲什么：从二维到三维，系统介绍位置、姿态、旋转和变换的表达方式，并结合工具箱做计算。
- 为什么重要：机器人与视觉都绕不开坐标系和位姿表示，这是贯穿全书的共同语言。
- 建议关注：本章一边学数学表示，一边对照工具箱接口，会更容易把抽象概念落到程序里。

<a id="rvc-ch3"></a>
### Chapter 3 Time and Motion

- 本章讲什么：讲时变位姿、刚体运动、参考系变化以及惯性导航等典型应用。
- 为什么重要：一旦进入真实机器人系统，状态不再是静态量，而是连续随时间演化的过程。
- 建议关注：重点看运动描述和参考系切换怎么影响状态估计与控制。

### Part II Mobile Robots

<a id="rvc-ch4"></a>
### Chapter 4 Mobile Robot Vehicles

- 本章讲什么：介绍轮式移动机器人和飞行机器人等移动平台的建模与基本特性。
- 为什么重要：移动底盘决定了机器人如何与环境发生空间关系，是导航、定位和任务执行的前提。
- 建议关注：把不同平台的约束差异看清楚，尤其是轮式和飞行平台在机动性上的根本不同。

<a id="rvc-ch5"></a>
### Chapter 5 Navigation

- 本章讲什么：从反应式导航到基于地图的路径规划，讲机器人如何在环境中到达目标。
- 为什么重要：导航是自主系统最直接的能力之一，也是把感知结果转成行动的第一个闭环。
- 建议关注：区分“局部避障”和“全局规划”，它们解决的问题粒度并不一样。

<a id="rvc-ch6"></a>
### Chapter 6 Localization

- 本章讲什么：围绕 dead reckoning、地图定位、建图、SLAM、pose graph 和激光应用展开。
- 为什么重要：机器人如果不知道自己在哪，导航和控制都无从谈起。
- 建议关注：把里程计误差累积、观测修正和 SLAM 的联合估计关系串起来理解。

### Part III Arm-Type Robots

<a id="rvc-ch7"></a>
### Chapter 7 Robot Arm Kinematics

- 本章讲什么：处理机械臂的正逆运动学、轨迹以及若干应用示例，把几何建模和运动生成连起来。
- 为什么重要：这是从移动机器人转向操作机器人的核心入口，强调“机械臂如何到达目标位姿”。
- 建议关注：一边看数学，一边跑示例，尤其适合把抽象运动学直觉变成可视化结果。

<a id="rvc-ch8"></a>
### Chapter 8 Manipulator Velocity

- 本章讲什么：围绕雅可比、操控性、resolved-rate control、欠驱动/冗余机械臂和数值逆运动学展开。
- 为什么重要：这章把几何位姿进一步推进到速度层，是很多在线控制与视觉伺服的基础。
- 建议关注：重点看雅可比与数值 IK 的关系，以及冗余自由度如何影响控制策略。

<a id="rvc-ch9"></a>
### Chapter 9 Dynamics and Control

- 本章讲什么：介绍刚体动力学方程、独立关节控制、正动力学和动力学补偿控制。
- 为什么重要：它把机械臂从“几何运动体”变成“受力驱动的真实系统”。
- 建议关注：优先看控制结构和补偿思想，不必一开始就陷入所有动力学细节。

### Part IV Computer Vision

<a id="rvc-ch10"></a>
### Chapter 10 Light and Color

- 本章讲什么：从光谱表示、颜色感知到颜色图像建模，建立视觉输入的物理基础。
- 为什么重要：如果不了解光和颜色，后面的图像算法就容易变成只会调库、不会判断适用边界。
- 建议关注：把光照、颜色空间和成像效果联系起来想。

<a id="rvc-ch11"></a>
### Chapter 11 Image Formation

- 本章讲什么：讨论透视相机、标定、广视场成像、鱼眼/全景等更复杂的成像模型。
- 为什么重要：视觉测量的几何关系都从这里来，尤其是三维重建、位姿估计和视觉伺服。
- 建议关注：相机模型与标定误差会直接影响后面多视图和控制结果。

<a id="rvc-ch12"></a>
### Chapter 12 Images and Image Processing

- 本章讲什么：介绍图像获取、直方图、像素运算、空间滤波、模板匹配、形态学和几何变换。
- 为什么重要：这是把原始图像转成可用特征和中间表示的基础处理层。
- 建议关注：区分增强、分割、匹配和几何变换各自解决的是什么问题。

<a id="rvc-ch13"></a>
### Chapter 13 Image Feature Extraction

- 本章讲什么：讨论区域特征、线特征、点特征及其表示、描述和分类。
- 为什么重要：很多定位、配准和识别问题都依赖稳定、可重复的特征。
- 建议关注：不要只记特征名称，要理解“什么样的结构适合被哪类特征捕捉”。

<a id="rvc-ch14"></a>
### Chapter 14 Using Multiple Images

- 本章讲什么：从特征匹配走到多视图几何、双目视觉、Bundle Adjustment、点云和结构光。
- 为什么重要：单张图像信息有限，多视图是三维重建、深度估计和视觉定位的重要来源。
- 建议关注：把 correspondence、geometry、optimization 三层关系连起来理解。

### Part V Robotics, Vision and Control

<a id="rvc-ch15"></a>
### Chapter 15 Vision-Based Control

- 本章讲什么：介绍 position-based visual servoing 和 image-based visual servoing 两条经典路线。
- 为什么重要：这是本书最直接体现“视觉驱动机器人动作”的一章，也是具身感知闭环的典型案例。
- 建议关注：理解 PBVS 和 IBVS 各自依赖什么信息、各自容易在哪些地方出问题。

<a id="rvc-ch16"></a>
### Chapter 16 Advanced Visual Servoing

- 本章讲什么：继续扩展视觉伺服到分区式 IBVS、极坐标表达、球面相机和具体应用场景。
- 为什么重要：它说明视觉伺服不是一个固定模板，而是一套可针对成像模型和任务结构继续扩展的控制框架。
- 建议关注：把相机模型变化对控制律设计的影响看清楚，这一点对真实系统很关键。

## 建议阅读顺序

- 如果你偏工程实践，可以先读 Chapter 2、5、6、7、11、15。
- 如果你偏视觉方向，Chapter 10 到 Chapter 16 是一条很完整的主线。
- 如果你想做具身系统，最值得反复回看的通常是 Chapter 6、8、14、15、16。
