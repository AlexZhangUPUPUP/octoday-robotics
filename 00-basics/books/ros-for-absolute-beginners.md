# 《The Robot Operating System (ROS) for Absolute Beginners》

[返回推荐书籍](../../00-basics.md#recommended-books) | [返回书籍索引](README.md)

![《The Robot Operating System (ROS) for Absolute Beginners》封面](<covers/robot-operating-system-ros-for-absolute-beginners-robotics-programming.pdf.png>)

> 封面图来自本地 PDF 首页缩略图。

> 说明：本页是仓库导读页，不是官方书摘或出版信息页。内容以仓库现有推荐理由、已核实资料和学习用途说明为主。

## 已核实资料

- Springer 1st edition：[https://link.springer.com/book/10.1007/978-1-4842-3405-1](https://link.springer.com/book/10.1007/978-1-4842-3405-1)
- Springer 2nd edition：[https://link.springer.com/book/10.1007/978-1-4842-7750-8](https://link.springer.com/book/10.1007/978-1-4842-7750-8)
- 本地目录来源：`robot-operating-system-ros-for-absolute-beginners-robotics-programming.pdf`

- 作者：Lentin Joseph；2nd edition 由 Lentin Joseph、Aleena Johny 合著。
- 出版社：Apress / Springer
- 备注：当前仓库条目未区分版本，本页补充了 1st edition 与 2nd edition 两个官方页面。

## 这本书适合谁

- 需要第一次真正上手机器人软件系统的读者。
- 想理解 node、topic、service、launch 等基本概念的读者。
- 准备接触真实机器人平台、传感器和控制链路的读者。

## 这本书通常用来补什么

- ROS/ROS2 的基本开发范式和常见组件。
- 机器人软件里消息通信、模块拆分和系统启动的基本方式。
- 从 demo 到最小工程系统的组织思路。

## 为什么推荐给具身智能学习者

很多人对模型很熟，但一接传感器、控制器和硬件通信就卡住。ROS 不是“最前沿模型”，却是很多机器人项目真正跑起来的底层基础设施。

## 建议怎么读

1. 不要只看概念，边读边做最小实验最重要。
2. 先把消息通信和包组织打通，再碰复杂系统。
3. 如果你要上真机，读书时一定要同步建立调试习惯。

## 学习导航

| 节 | 学习重点 |
| --- | --- |
| [Chapter 1 Getting Started with Ubuntu Linux for Robotics](#ros-ch1) | 先把机器人开发环境打稳 |
| [Chapter 2 Fundamentals of C++ for Robotics Programming](#ros-ch2) | 补机器人程序里最常见的 C++ 基础 |
| [Chapter 3 Fundamentals of Python for Robotics Programming](#ros-ch3) | 建立 Python 侧的开发最小能力 |
| [Chapter 4 Kick-Starting Robot Programming Using ROS](#ros-ch4) | 第一次把 ROS 当作系统框架来理解 |
| [Chapter 5 Programming with ROS](#ros-ch5) | 看节点、包、库和硬件接口怎样协作 |
| [Chapter 6 Robotics Project Using ROS](#ros-ch6) | 用一个完整小项目把前面串起来 |

## 按章节怎么学

<a id="ros-ch1"></a>
### Chapter 1 Getting Started with Ubuntu Linux for Robotics

- 核心问题：为什么机器人开发往往从 Linux 环境开始。
- 阅读提示：如果你对终端和系统环境不熟，这章一定别跳。

<a id="ros-ch2"></a>
### Chapter 2 Fundamentals of C++ for Robotics Programming

- 核心问题：机器人软件里常见的 C++ 组织方式和对象模型。
- 阅读提示：这章不用追求面面俱到，重点是够你读懂 ROS 代码。

<a id="ros-ch3"></a>
### Chapter 3 Fundamentals of Python for Robotics Programming

- 核心问题：Python 在原型开发和 ROS 节点编写中的位置。
- 阅读提示：建议边看边写几个最小脚本，把语法变成手感。

<a id="ros-ch4"></a>
### Chapter 4 Kick-Starting Robot Programming Using ROS

- 核心问题：ROS 究竟替机器人项目解决了哪些系统级问题。
- 阅读提示：这一章要建立的是“节点协作”的脑图。

<a id="ros-ch5"></a>
### Chapter 5 Programming with ROS

- 核心问题：workspace、package、client library 和嵌入式板卡如何接到一起。
- 阅读提示：这章建议配合真实命令和目录结构一起看。

<a id="ros-ch6"></a>
### Chapter 6 Robotics Project Using ROS

- 核心问题：怎样把底盘、模型、固件和 ROS 控制链路串成一个完整项目。
- 阅读提示：把它当成“最小真实项目”来读最有效。

## 延伸资源

- [PacktPublishing/The-Robot-Operating-System-ROS-for-Absolute-Beginners](https://github.com/PacktPublishing/The-Robot-Operating-System-ROS-for-Absolute-Beginners)：最适合和这本书一起直接上手的小型代码库。
- [mit-rss/intro_to_ros](https://github.com/mit-rss/intro_to_ros)：更像教学用导览，适合补足入门实验感。
- [A2Amir/Introduction-to-ROS--Robot-Operating-System](https://github.com/A2Amir/Introduction-to-ROS--Robot-Operating-System)：解释更平直，适合零基础快速建立概念。

## 建议阅读顺序

- 新手建议走 `1 -> 4 -> 5 -> 6`，中间按需回补 `2、3`。
- 如果你已经会 Linux 和 Python，可以从第 4 章直接开始。
- 读完后再看 [04-tools.md#framework](../../04-tools.md#framework) 会更容易理解生态分层。
