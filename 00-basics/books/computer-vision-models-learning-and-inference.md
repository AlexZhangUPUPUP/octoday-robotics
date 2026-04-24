# 《计算机视觉：模型、学习和推理》

[返回推荐书籍](../../00-basics.md#recommended-books) | [返回书籍索引](README.md)

![《计算机视觉：模型、学习和推理》封面](<covers/计算机视觉：模型、学习和推理 (Simon J. D. Prince) (z-library.sk, 1lib.sk, z-lib.sk).pdf.png>)

> 封面图来自本地 PDF 首页缩略图。

> 说明：本页是仓库导读页，不是官方书摘或出版信息页。内容以仓库现有推荐理由、已核实资料和学习用途说明为主。

## 已核实资料

- Cambridge 页面：[https://www.cambridge.org/highereducation/books/computer-vision/90B5BA0D2088E0A952170C2AD6043438](https://www.cambridge.org/highereducation/books/computer-vision/90B5BA0D2088E0A952170C2AD6043438)
- 官方目录 PDF：[https://assets.cambridge.org/97811070/11793/toc/9781107011793_toc.pdf](https://assets.cambridge.org/97811070/11793/toc/9781107011793_toc.pdf)
- 本地 PDF：`计算机视觉：模型、学习和推理 (Simon J. D. Prince) (z-library.sk, 1lib.sk, z-lib.sk).pdf`

- 作者：Simon J. D. Prince
- 出版社：Cambridge University Press
- 备注：本地 PDF 更像扫描版，目录文字无法稳定抽取；下面的章节导航按 Cambridge 官方目录整理。

## 这本书适合谁

- 想把视觉问题看得更“模型化”而不是只记网络结构的读者。
- 需要补图像建模、推理和概率视角的读者。
- 做机器人感知、场景理解、3D 重建的读者。

## 这本书通常用来补什么

- 从图像形成到高层推理的统一问题表达方式。
- 视觉问题里“观测、不确定性、结构关系”这几层经常被忽略的核心。
- 为什么很多视觉任务本质上是在做建模和推断，而不是只做特征提取。

## 为什么推荐给具身智能学习者

具身系统里的视觉要回答的不只是“看到了什么”，还包括“东西在哪里、能不能操作、接下来会怎样变化”。

## 建议怎么读

1. 把它当成视觉思维训练，而不是模型清单。
2. 读的时候尽量把抽象建模对应到导航、抓取、场景理解这些真实任务。
3. 如果你已经习惯端到端网络，这本书会帮你把被隐藏掉的中间结构重新找回来。

## 学习导航

| 节 | 学习重点 |
| --- | --- |
| [Chapter 1 Introduction](#cv-ch1) | 先建立这本书的建模视角 |
| [Chapter 2 Introduction to Probability](#cv-ch2) | 把概率语言补成视觉建模底座 |
| [Chapter 3 Common Probability Distributions](#cv-ch3) | 认识视觉里最常见的分布工具 |
| [Chapter 4 Fitting Probability Models](#cv-ch4) | 学会从数据拟合模型 |
| [Chapter 5 The Normal Distribution](#cv-ch5) | 为后面大量模型准备高斯直觉 |
| [Chapter 6 Learning and Inference in Vision](#cv-ch6) | 看视觉任务怎样被写成学习与推断问题 |
| [Chapter 7 Modeling Complex Data Densities](#cv-ch7) | 进入更复杂的数据分布建模 |
| [Chapter 8 Regression Models](#cv-ch8) | 学会从图像到连续量的预测 |
| [Chapter 9 Classification Models](#cv-ch9) | 理解视觉分类模型背后的统一结构 |
| [Chapter 10 Graphical Models](#cv-ch10) | 引入局部关系与结构依赖 |
| [Chapter 11 Models for Chains and Trees](#cv-ch11) | 处理序列和树形依赖关系 |
| [Chapter 12 Models for Grids](#cv-ch12) | 把图像网格结构显式建模 |
| [Chapter 13 Image Preprocessing and Feature Extraction](#cv-ch13) | 从原始像素走向可用特征 |
| [Chapter 14 The Pinhole Camera](#cv-ch14) | 建立相机与三维几何基础 |
| [Chapter 15 Models for Transformations](#cv-ch15) | 理解图像与平面之间的变换 |
| [Chapter 16 Multiple Cameras](#cv-ch16) | 进入多视图几何与重建 |
| [Chapter 17 Models for Shape](#cv-ch17) | 处理轮廓、形状和结构 |
| [Chapter 18 Models for Style and Identity](#cv-ch18) | 看身份、风格和外观因素如何分解 |
| [Chapter 19 Temporal Models](#cv-ch19) | 让视觉进入时间维度 |
| [Chapter 20 Models for Visual Words](#cv-ch20) | 理解经典视觉检索与识别思路 |

## 按章节怎么学

<a id="cv-ch1"></a>
### Chapter 1 Introduction

- 核心问题：这本书为什么用“模型、学习、推理”而不是任务清单来组织视觉知识。
- 阅读提示：先接受它的组织方式，再读后面会顺很多。

<a id="cv-ch2"></a>
### Chapter 2 Introduction to Probability

- 核心问题：为什么视觉离不开概率。
- 阅读提示：如果这章跳过，后面很多模型会失去共同语言。

<a id="cv-ch3"></a>
### Chapter 3 Common Probability Distributions

- 核心问题：哪些分布最常出现在视觉建模里。
- 阅读提示：读这章时多想每种分布适合描述什么类型的数据。

<a id="cv-ch4"></a>
### Chapter 4 Fitting Probability Models

- 核心问题：模型参数怎样从数据里学出来。
- 阅读提示：把这一章看成后面所有学习方法的基础课。

<a id="cv-ch5"></a>
### Chapter 5 The Normal Distribution

- 核心问题：高斯模型为什么如此常见。
- 阅读提示：这一章很基础，但后面会不断回到这里。

<a id="cv-ch6"></a>
### Chapter 6 Learning and Inference in Vision

- 核心问题：视觉任务如何统一写成观测到世界状态的映射问题。
- 阅读提示：这是全书从数学基础进入视觉问题的关键转折。

<a id="cv-ch7"></a>
### Chapter 7 Modeling Complex Data Densities

- 核心问题：真实视觉数据为什么通常不是简单单峰分布。
- 阅读提示：适合和聚类、隐变量、EM 一起理解。

<a id="cv-ch8"></a>
### Chapter 8 Regression Models

- 核心问题：从视觉输入预测连续变量时，模型有哪些路线。
- 阅读提示：把它和深度模型之前的经典回归视角联系起来看。

<a id="cv-ch9"></a>
### Chapter 9 Classification Models

- 核心问题：分类问题在概率建模里怎样被表达。
- 阅读提示：读这一章时不要只盯着分类精度，要看建模假设。

<a id="cv-ch10"></a>
### Chapter 10 Graphical Models

- 核心问题：视觉中大量局部依赖关系怎样被结构化表示。
- 阅读提示：这是理解 MRF、CRF 和结构推断的入口。

<a id="cv-ch11"></a>
### Chapter 11 Models for Chains and Trees

- 核心问题：链式和树式结构怎样支持高效推断。
- 阅读提示：如果你后面要看时序或姿态模型，这章很有价值。

<a id="cv-ch12"></a>
### Chapter 12 Models for Grids

- 核心问题：图像天然是网格，怎样把这个结构真正用起来。
- 阅读提示：和分割、恢复、标签传播问题联系着读最合适。

<a id="cv-ch13"></a>
### Chapter 13 Image Preprocessing and Feature Extraction

- 核心问题：视觉系统怎样从像素层走向结构化表示。
- 阅读提示：这一章更像很多经典 pipeline 的中间层总览。

<a id="cv-ch14"></a>
### Chapter 14 The Pinhole Camera

- 核心问题：二维图像和三维世界到底如何连接。
- 阅读提示：如果你做机器人视觉，这章必须扎实。

<a id="cv-ch15"></a>
### Chapter 15 Models for Transformations

- 核心问题：平面、视角和图像之间的变换如何建模。
- 阅读提示：这章适合和配准、追踪、拼接任务一起读。

<a id="cv-ch16"></a>
### Chapter 16 Multiple Cameras

- 核心问题：为什么多视图会带来三维重建能力。
- 阅读提示：这是从单相机视觉进入真正空间理解的核心章。

<a id="cv-ch17"></a>
### Chapter 17 Models for Shape

- 核心问题：形状、轮廓和统计形状模型怎样组织。
- 阅读提示：这章对姿态估计、人体建模、轮廓跟踪都很重要。

<a id="cv-ch18"></a>
### Chapter 18 Models for Style and Identity

- 核心问题：身份信息、风格变化和外观因素如何被分解。
- 阅读提示：可以把它看成今天 representation disentanglement 的经典前史。

<a id="cv-ch19"></a>
### Chapter 19 Temporal Models

- 核心问题：一旦进入时间维度，视觉怎样做跟踪和动态估计。
- 阅读提示：这章和机器人状态估计、视频理解的联系非常强。

<a id="cv-ch20"></a>
### Chapter 20 Models for Visual Words

- 核心问题：经典 bag-of-words 视觉路线在识别和检索中如何工作。
- 阅读提示：虽然今天范式更新了，但这章仍有历史和方法论价值。

## 延伸资源

- [jwdinius/prince-computer-vision](https://github.com/jwdinius/prince-computer-vision)：更偏学习笔记路线，适合第二遍梳理概念。
- [insidedctm/prince_mv](https://github.com/insidedctm/prince_mv)：带习题思路和实现，更适合边做边学。
- [udlbook/cvbook](https://github.com/udlbook/cvbook)：作者维护的资源入口，适合作为权威补充。

## 建议阅读顺序

- 如果你偏机器人感知，优先走 `2 -> 6 -> 13 -> 14 -> 16 -> 19`。
- 如果你偏视觉建模，建议从 `2 -> 3 -> 4 -> 5 -> 7 -> 8 -> 9 -> 10` 打基础。
- 读完后可以继续看 [Navigation & Spatial Intelligence](../../03-papers.md#navigation-spatial-intelligence) 和 [Datasets](../../03-papers.md#datasets)。
