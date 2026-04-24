# 《深度学习》

[返回推荐书籍](../../00-basics.md#recommended-books) | [返回书籍索引](README.md)

> 说明：本页是仓库导读页，不是官方书摘或出版信息页。内容以仓库现有推荐理由、已核实资料和学习用途说明为主。

## 已核实资料

- 官方在线版：[https://www.deeplearningbook.org/](https://www.deeplearningbook.org/)
- 官方目录页：[https://www.deeplearningbook.org/contents/TOC.html](https://www.deeplearningbook.org/contents/TOC.html)
- 本地 PDF 说明：`00-basics/books` 目录下当前可见的中文 PDF 是另一本《Python 深度学习实战》，不是本条目标书。

- 作者：Ian Goodfellow、Yoshua Bengio、Aaron Courville
- 出版社：MIT Press
- 备注：下面的章节导航按官方在线目录整理，不按当前 books 目录里那本实践书整理。

## 这本书适合谁

- 需要系统补神经网络基础的读者。
- 具备工程经验，但对优化、泛化和表示学习理解还不稳的读者。
- 准备进入视觉、多模态和具身基础模型方向的读者。

## 这本书通常用来补什么

- 从前馈网络、反向传播到优化与正则化的一整套基础语言。
- 深度模型为什么能表达复杂结构，又为什么经常训练不稳。
- 卷积、序列建模、表示学习这些后续大模型和具身模型的底座。

## 为什么推荐给具身智能学习者

很多具身论文的创新点写在 architecture、loss、pretrain 或 policy 上，但如果深度学习底层不扎实，你很难判断这些设计是必要的还是只是包装。

## 建议怎么读

1. 把优化、泛化和表示学习作为第一优先级。
2. 如果你来自机器人背景，不要只盯着模型结构，训练和失效模式同样重要。
3. 读这本书的目标不是“背框架”，而是建立对模型行为的判断力。

## 学习导航

| 节 | 学习重点 |
| --- | --- |
| [Chapter 1 Introduction](#dl-ch1) | 先建立深度学习的基本问题图景 |
| [Chapter 2 Linear Algebra](#dl-ch2) | 补齐深度模型最常用的数学语言 |
| [Chapter 3 Probability and Information Theory](#dl-ch3) | 理解损失、分布和信息量概念 |
| [Chapter 4 Numerical Computation](#dl-ch4) | 进入训练时真正会遇到的数值问题 |
| [Chapter 5 Machine Learning Basics](#dl-ch5) | 把深度学习放回机器学习大框架 |
| [Chapter 6 Deep Feedforward Networks](#dl-ch6) | 学习最基础的深网结构 |
| [Chapter 7 Regularization for Deep Learning](#dl-ch7) | 理解过拟合和控制手段 |
| [Chapter 8 Optimization for Training Deep Models](#dl-ch8) | 解决训练能不能收敛的问题 |
| [Chapter 9 Convolutional Networks](#dl-ch9) | 理解局部结构和卷积偏好 |
| [Chapter 10 Sequence Modeling: Recurrent and Recursive Nets](#dl-ch10) | 处理时序和递归结构 |
| [Chapter 11 Practical Methodology](#dl-ch11) | 建立调参、诊断和实验习惯 |
| [Chapter 12 Applications](#dl-ch12) | 看深度学习如何进入真实任务 |
| [Chapter 13 Linear Factor Models](#dl-ch13) | 回看经典表示学习前史 |
| [Chapter 14 Autoencoders](#dl-ch14) | 进入无监督表示学习经典路线 |
| [Chapter 15 Representation Learning](#dl-ch15) | 理解“学表示”到底在学什么 |
| [Chapter 16 Structured Probabilistic Models for Deep Learning](#dl-ch16) | 把深度模型和概率结构结合起来 |
| [Chapter 17 Monte Carlo Methods](#dl-ch17) | 进入采样与估计问题 |
| [Chapter 18 Confronting the Partition Function](#dl-ch18) | 理解能量模型中的难点 |
| [Chapter 19 Approximate Inference](#dl-ch19) | 处理复杂模型中的推断问题 |
| [Chapter 20 Deep Generative Models](#dl-ch20) | 进入生成模型主线 |

## 按章节怎么学

<a id="dl-ch1"></a>
### Chapter 1 Introduction

- 核心问题：深度学习在解决什么，以及为什么会有效。
- 阅读提示：第一遍不用追细节，先把全书问题图景看清楚。

<a id="dl-ch2"></a>
### Chapter 2 Linear Algebra

- 核心问题：矩阵和向量运算为什么是深度学习的日常语言。
- 阅读提示：重点补齐你在后续公式里会频繁遇到的部分。

<a id="dl-ch3"></a>
### Chapter 3 Probability and Information Theory

- 核心问题：为什么损失函数、似然和信息论概念会反复出现。
- 阅读提示：这章建议和分类、生成模型一起对照理解。

<a id="dl-ch4"></a>
### Chapter 4 Numerical Computation

- 核心问题：为什么模型训练会受到溢出、病态和优化约束的影响。
- 阅读提示：这章很工程，但非常关键。

<a id="dl-ch5"></a>
### Chapter 5 Machine Learning Basics

- 核心问题：深度学习和更一般机器学习框架的关系是什么。
- 阅读提示：如果你只会调模型，这章会帮你补回理论坐标系。

<a id="dl-ch6"></a>
### Chapter 6 Deep Feedforward Networks

- 核心问题：最基本的深网结构怎样工作。
- 阅读提示：这是后面所有复杂模型的起点。

<a id="dl-ch7"></a>
### Chapter 7 Regularization for Deep Learning

- 核心问题：怎样控制模型过拟合和泛化问题。
- 阅读提示：具身数据贵，这章尤其不能跳。

<a id="dl-ch8"></a>
### Chapter 8 Optimization for Training Deep Models

- 核心问题：训练过程为什么难，以及常见优化技巧在解决什么。
- 阅读提示：把这章和你自己的训练经验对起来看最有效。

<a id="dl-ch9"></a>
### Chapter 9 Convolutional Networks

- 核心问题：卷积网络为什么擅长视觉和局部结构任务。
- 阅读提示：虽然今天架构变了，但这章依然是视觉直觉基础。

<a id="dl-ch10"></a>
### Chapter 10 Sequence Modeling: Recurrent and Recursive Nets

- 核心问题：时间序列和结构化序列如何建模。
- 阅读提示：如果你关心动作序列、语言或控制，这章很有用。

<a id="dl-ch11"></a>
### Chapter 11 Practical Methodology

- 核心问题：真实训练流程里怎样做调试、选 baseline 和定位问题。
- 阅读提示：这是最接近“工程实战”的一章之一。

<a id="dl-ch12"></a>
### Chapter 12 Applications

- 核心问题：深度学习在视觉、语音、NLP 等场景中怎样落地。
- 阅读提示：把它当成前面基础章节的回放。

<a id="dl-ch13"></a>
### Chapter 13 Linear Factor Models

- 核心问题：表示学习在深度模型之前有哪些经典思路。
- 阅读提示：适合把它看成历史与方法论补课。

<a id="dl-ch14"></a>
### Chapter 14 Autoencoders

- 核心问题：自编码器为什么曾经是表示学习核心路线。
- 阅读提示：今天很多生成和表征方法都还能看到它的影子。

<a id="dl-ch15"></a>
### Chapter 15 Representation Learning

- 核心问题：什么叫“好的表示”，为什么它值得单独研究。
- 阅读提示：这章和现代多模态、世界模型联系很强。

<a id="dl-ch16"></a>
### Chapter 16 Structured Probabilistic Models for Deep Learning

- 核心问题：深度模型怎样和显式概率结构结合。
- 阅读提示：如果你关心不确定性建模，这章很重要。

<a id="dl-ch17"></a>
### Chapter 17 Monte Carlo Methods

- 核心问题：复杂模型里的采样和估计怎样做。
- 阅读提示：这是后面更难章节的工具章。

<a id="dl-ch18"></a>
### Chapter 18 Confronting the Partition Function

- 核心问题：为什么某些概率模型训练起来特别难。
- 阅读提示：重点抓住“归一化常数难算”这个本质。

<a id="dl-ch19"></a>
### Chapter 19 Approximate Inference

- 核心问题：推断太复杂时，如何用近似方法继续工作。
- 阅读提示：把这章当作复杂模型可落地的关键补丁。

<a id="dl-ch20"></a>
### Chapter 20 Deep Generative Models

- 核心问题：深度模型如何生成数据和学习潜在分布。
- 阅读提示：这是通往现代生成模型的入口章。

## 延伸资源

- [MingchaoZhu/DeepLearning](https://github.com/MingchaoZhu/DeepLearning)：偏底层实现，适合用 `numpy` 重新建立对反向传播和优化的手感。
- [d2l-ai/d2l-zh](https://github.com/d2l-ai/d2l-zh)：更强调动手实验，适合和这本书互补阅读。
- [ujjwalkarn/Machine-Learning-Tutorials](https://github.com/ujjwalkarn/Machine-Learning-Tutorials)：适合查阅一些核心概念的轻量解释和示例。

## 建议阅读顺序

- 如果你是 AI 初学者，先走 `1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 11`。
- 如果你偏视觉和具身，随后重点补 `9、10、12、15、20`。
- 读完后再去看 [Embodied Foundation Models](../../03-papers.md#embodied-foundation-models) 会更容易分辨哪些设计是真的有意义。
