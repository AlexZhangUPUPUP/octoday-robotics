# 《Mechanics of Robotic Manipulation》

[返回推荐书籍](../../00-basics.md#recommended-books) | [返回书籍索引](README.md)

![《Mechanics of Robotic Manipulation》封面](<covers/Mechanics of Robotic Manipulation (Matthew T. Mason) (z-library.sk, 1lib.sk, z-lib.sk).pdf.png>)

> 封面图来自本地 PDF 首页缩略图。

> 说明：本页是仓库导读页，不是官方书摘或出版信息页。内容以仓库现有推荐理由、已核实资料和学习用途说明为主。

## 已核实资料

- MIT Press 页面：[https://mitpress.mit.edu/9780262133968/mechanics-of-robotic-manipulation/](https://mitpress.mit.edu/9780262133968/mechanics-of-robotic-manipulation/)
- 本地目录来源：`Mechanics of Robotic Manipulation (Matthew T. Mason) (z-library.sk, 1lib.sk, z-lib.sk).pdf`

- 作者：Matthew T. Mason
- 出版社：The MIT Press
- 备注：根据 MIT Press 官方页，正式书名为 Mechanics of Robotic Manipulation。仓库原条目标题与官方书名不一致，本次已按官方页修正。

## 这本书适合谁

- 明确想深入机械臂抓取、接触与操作问题的读者。
- 对 manipulation 的力学本质感兴趣的读者。
- 做灵巧手、抓取、装配和精细操作的研究型读者。

## 这本书通常用来补什么

- 接触、摩擦、约束和稳定性这些操作任务里最本质的力学结构。
- 为什么“抓到”不等于“能稳稳地操控”。
- manipulation 任务里几何、力学和控制如何耦合。

## 为什么推荐给具身智能学习者

真正的 manipulation 不是 prompt engineering，而是物体、接触面、力和运动在物理世界里的共同作用。这本书专门讲这个底层问题。

## 建议怎么读

1. 不要期待它像工程手册那样直接给配方，它更像一本帮你建立问题本质的书。
2. 如果你主要做操作任务，这本书值得反复看。
3. 读的时候要始终把“接触约束”放在中心位置。

## 学习导航

| 节 | 学习重点 |
| --- | --- |
| [Chapter 1 Manipulation](#mom-ch1) | 先建立 manipulation 问题全貌 |
| [Chapter 2 Kinematics](#mom-ch2) | 从运动自由度和约束看操作问题 |
| [Chapter 3 Kinematic Representation](#mom-ch3) | 理解旋转、位姿与约束的表达方式 |
| [Chapter 4 Kinematic Manipulation](#mom-ch4) | 把路径、接触和非完整约束联系起来 |
| [Chapter 5 Rigid Body Statics](#mom-ch5) | 从力和力矩进入操作力学 |
| [Chapter 6 Friction](#mom-ch6) | 理解摩擦为什么决定操作成败 |
| [Chapter 7 Quasistatic Manipulation](#mom-ch7) | 看低速操作任务里的典型结构 |
| [Chapter 8 Dynamics](#mom-ch8) | 从准静态走向真实动力学 |
| [Chapter 9 Impact](#mom-ch9) | 处理瞬时接触和碰撞 |
| [Chapter 10 Dynamic Manipulation](#mom-ch10) | 进入更高速、更主动的动态操作 |

## 按章节怎么学

<a id="mom-ch1"></a>
### Chapter 1 Manipulation

- 核心问题：什么叫 manipulation，它和简单移动或定位有何不同。
- 阅读提示：这章建议当作全书的问题设定来读。

<a id="mom-ch2"></a>
### Chapter 2 Kinematics

- 核心问题：操作中的几何关系、自由度和约束如何组织。
- 阅读提示：如果运动学基础薄弱，这章要放慢速度。

<a id="mom-ch3"></a>
### Chapter 3 Kinematic Representation

- 核心问题：如何用合适表示法描述位姿和约束。
- 阅读提示：这章是后面所有接触与操作建模的语言层。

<a id="mom-ch4"></a>
### Chapter 4 Kinematic Manipulation

- 核心问题：路径规划、非完整约束和接触运动学如何连接。
- 阅读提示：这章能帮你把几何建模和操作任务真正接起来。

<a id="mom-ch5"></a>
### Chapter 5 Rigid Body Statics

- 核心问题：操作里作用力、力矩和 wrench 应该怎样理解。
- 阅读提示：这是抓取与稳定性分析的基础章。

<a id="mom-ch6"></a>
### Chapter 6 Friction

- 核心问题：摩擦模型怎样改变系统可行运动和可行受力。
- 阅读提示：不要把摩擦当成修正项，它是主角之一。

<a id="mom-ch7"></a>
### Chapter 7 Quasistatic Manipulation

- 核心问题：低速、缓慢操作时，接触与约束怎样主导任务。
- 阅读提示：插接、推操、抓持等很多任务都适合从这里入门。

<a id="mom-ch8"></a>
### Chapter 8 Dynamics

- 核心问题：当惯性不可忽略时，操作问题如何变化。
- 阅读提示：这章建议和第 7 章对照读，感受难度跃迁。

<a id="mom-ch9"></a>
### Chapter 9 Impact

- 核心问题：碰撞和冲击时，系统状态如何瞬时变化。
- 阅读提示：如果你关注快速接触任务，这章很关键。

<a id="mom-ch10"></a>
### Chapter 10 Dynamic Manipulation

- 核心问题：什么时候操作必须依赖动态行为而不是缓慢稳定控制。
- 阅读提示：把这章当作现代 dynamic manipulation 的经典前导。

## 延伸资源

- [angmavrogiannis/16-741-Mechanics-of-Manipulation](https://github.com/angmavrogiannis/16-741-Mechanics-of-Manipulation)：更接近课程配套资料，适合边学边做。
- [SiliconWit/robotics](https://github.com/SiliconWit/robotics)：可以作为操作力学和雅可比相关主题的轻量补充。
- [NxRLab/ModernRobotics](https://github.com/NxRLab/ModernRobotics)：不是这本书本身的配套，但和操作、规划、控制的现代表示法联系紧密。

## 建议阅读顺序

- 如果你主攻操作任务，建议走 `1 -> 5 -> 6 -> 7 -> 10`。
- 如果你想补底层几何，再加上 `2、3、4`。
- 读完后再看 [Manipulation](../../03-papers.md#manipulation) 会明显更顺。
