# MuJoCo 摩擦力

[English](04_friction.md) | [中文](04_friction_zh.md)

---


## 概览

本笔记整理的是 Albusgive MuJoCo 学习来源中关于 `friction` 的内容。

主要包括：

- `friction="a b c"`
- 滑动摩擦
- 扭转摩擦
- 滚动摩擦
- `condim`
- 摩擦锥模型
- `cone="elliptic"`
- `cone="pyramidal"`
- `priority`
- 两个 geom 接触时摩擦参数如何选择
- 约束维度
- MuJoCo 内部 friction 参数展开
- 对照实验中的实际效果

最核心的关系是：

```text
friction
→ 决定各种摩擦有多强

condim
→ 决定哪些摩擦模式会被纳入接触模型

cone
→ 决定摩擦约束在数学上如何表示
```

---

## 1. Friction 参数

MuJoCo 的 geom 可以定义：

```xml
<geom friction="a b c"/>
```

三个参数依次表示：

```text
a
→ sliding friction
→ 滑动摩擦

b
→ torsional friction
→ 扭转摩擦

c
→ rolling friction
→ 滚动摩擦
```

例如：

```xml
<geom friction="1 0.005 0.0001"/>
```

表示：

```text
滑动摩擦 = 1
扭转摩擦 = 0.005
滚动摩擦 = 0.0001
```

---

## 2. Sliding Friction - 滑动摩擦

滑动摩擦用于阻碍物体沿接触面发生相对滑动。

例如：

```text
[ box ] →→→
────────────
```

第一个 friction 参数控制这种作用：

```text
friction[0]
→ sliding friction
```

通常三个 friction 参数中，第一个值会明显大于后两个。

---

## 3. Torsional Friction - 扭转摩擦

扭转摩擦用于阻碍物体绕接触面的法线方向旋转。

可以理解为：

```text
     ↻
 [ object ]
────────────
```

第二个 friction 参数控制这种作用：

```text
friction[1]
→ torsional friction
```

只有当接触模型包含 torsional friction 时，这个参数才真正发挥作用。

---

## 4. Rolling Friction - 滚动摩擦

滚动摩擦用于阻碍物体滚动。

例如：

```text
O →→→
────────────
```

第三个 friction 参数控制滚动阻力：

```text
friction[2]
→ rolling friction
```

它对于以下物体特别重要：

- 球
- 轮子
- 滚子

---

## 5. `condim`

`condim` 决定一次接触中包含哪些接触方向和摩擦模式。

常见值为：

```text
condim = 1
→ 只有法向接触

condim = 3
→ 法向 + 滑动摩擦

condim = 4
→ 法向 + 滑动摩擦 + 扭转摩擦

condim = 6
→ 法向 + 滑动摩擦 + 扭转摩擦 + 滚动摩擦
```

可以简单记成：

```text
1
→ 不让穿透

3
→ 再限制滑动

4
→ 再限制原地扭转

6
→ 再限制滚动
```

---

## 6. 为什么 `condim` 是 1、3、4、6

这是因为不同摩擦模式占用的方向数不同。

滑动摩擦有两个切向方向：

```text
切向方向 1
切向方向 2
```

滚动摩擦也有两个旋转方向。

因此：

```text
1
→ 只有法向方向

3
→ +2 个滑动方向

4
→ +1 个扭转方向

6
→ +2 个滚动方向
```

所以维度变化是：

```text
1 → 3 → 4 → 6
```

---

## 7. Friction 参数要配合对应的 `condim`

即使 XML 中写了完整的三个摩擦参数：

```xml
<geom friction="1 0.01 0.001"
      condim="3"/>
```

由于：

```text
condim = 3
```

只包含：

```text
法向接触
+
滑动摩擦
```

所以 torsional friction 和 rolling friction 并不会完整进入这个接触模型。

如果需要扭转摩擦：

```text
condim = 4
```

如果还需要滚动摩擦：

```text
condim = 6
```

因此：

```text
friction
→ 决定摩擦大小

condim
→ 决定哪些摩擦模式存在
```

---

## 8. Friction Cone - 摩擦锥

MuJoCo 支持两种主要摩擦锥表示方法：

```xml
<option cone="elliptic"/>
```

以及：

```xml
<option cone="pyramidal"/>
```

这两个参数并不是直接改变 friction coefficient。

而是：

> 改变 MuJoCo 在数学上如何表示和求解摩擦约束。

---

## 9. Elliptic Friction Cone

`elliptic` 使用更直接、更平滑的摩擦锥表示。

其约束维度为：

```text
约束维度 = condim
```

所以：

```text
condim = 1
→ 1 维

condim = 3
→ 3 维

condim = 4
→ 4 维

condim = 6
→ 6 维
```

对于：

```text
condim = 6
```

物理上包含：

```text
1 个 normal

2 个 sliding

1 个 torsional

2 个 rolling
```

总共：

```text
6 个方向
```

---

## 10. Pyramidal Friction Cone

`pyramidal` 使用多面体边界去近似摩擦锥。

对于大多数带摩擦的接触：

```text
约束维度
=
2 × (condim - 1)
```

因此：

```text
condim = 3
→ 4 个约束方向

condim = 4
→ 6 个约束方向

condim = 6
→ 10 个约束方向
```

而：

```text
condim = 1
```

仍然只是一个法向约束。

---

## 11. 为什么 Pyramidal 会有更多约束方向

Pyramidal 会把一个摩擦方向拆成正方向和负方向。

例如：

```text
sliding direction 1
→ +m1
→ -m1

sliding direction 2
→ +m2
→ -m2
```

所以原本两个 sliding direction 会变成：

```text
4 个 pyramidal constraint direction
```

同理：

```text
torsional
→ +m3
→ -m3
```

而两个 rolling direction 会变成：

```text
+m4
-m4

+m5
-m5
```

因此当：

```text
condim = 6
```

时：

```text
2 个 sliding direction
→ 4 个约束

1 个 torsional direction
→ 2 个约束

2 个 rolling direction
→ 4 个约束
```

总共：

```text
10 个约束方向
```

需要注意：

> 这不是多出了 10 种不同的物理摩擦，而只是用更多数学约束方向去近似同一个接触摩擦模型。

---

## 12. Elliptic 与 Pyramidal 对比

可以整理成：

| condim | elliptic | pyramidal |
|---|---:|---:|
| 1 | 1 | 1 |
| 3 | 3 | 4 |
| 4 | 4 | 6 |
| 6 | 6 | 10 |

核心区别：

```text
elliptic
→ 更直接、更平滑
→ 约束维度 = condim

pyramidal
→ 用多面体近似
→ 一个摩擦方向拆成正负边
→ 通常会产生更多约束方向
```

---

## 13. MuJoCo 内部对 Friction 的展开

在 XML 中只需要写三个 friction 参数：

```text
[a, b, c]
```

对应：

```text
a = sliding

b = torsional

c = rolling
```

但 MuJoCo 内部会把它展开成 5 个方向参数：

```text
[a, a, b, c, c]
```

也就是：

```text
2 个 sliding direction

1 个 torsional direction

2 个 rolling direction
```

因此内部可以理解为：

```text
friction[0]
→ sliding direction 1

friction[1]
→ sliding direction 2

friction[2]
→ torsional

friction[3]
→ rolling direction 1

friction[4]
→ rolling direction 2
```

但是在 MJCF XML 里仍然只需要写三个参数。

---

## 14. `priority`

当两个 geom 发生接触时，MuJoCo 需要决定使用谁的接触参数。

一个重要参数是：

```xml
priority="..."
```

如果两个 geom 的 priority 不同：

```text
priority 更高的 geom
→ 它的接触参数优先
```

这可能影响：

- friction
- `condim`
- `solref`
- `solimp`

---

## 15. Priority 相同时

如果两个 geom 的 priority 一样，MuJoCo 会分别比较摩擦参数，并使用每一项中的较大值。

例如：

```text
geom A:
friction = 1.0 0.01 0.001

geom B:
friction = 0.6 0.02 0.0005
```

如果 priority 相同，最终：

```text
friction = 1.0 0.02 0.001
```

因为每一项独立取最大值：

```text
sliding
→ max(1.0, 0.6)

torsional
→ max(0.01, 0.02)

rolling
→ max(0.001, 0.0005)
```

---

## 16. 为什么实验里会把 Floor / Slope 的 Priority 设成 -1

在 friction 对照实验中，地面和斜坡设置：

```xml
priority="-1"
```

而运动物体一般使用默认更高的 priority。

因此：

```text
运动物体的接触参数
→ 优先于地面 / 斜坡
```

这样就可以方便地分别测试：

```text
不同 condim

不同 friction
```

而不会被 floor 或 slope 的参数覆盖。

---

## 17. `impratio`

`impratio` 会影响 friction constraint 相对于 normal constraint 的阻抗比例。

可以先简单理解为：

```text
impratio 增大
→ friction constraint 相对更强
→ 更不容易发生滑动
```

但是：

```text
impratio
```

并不是“摩擦系数替代品”。

不能简单理解成：

```text
摩擦不够
→ 就一直增加 impratio
```

仍然应该合理设置：

```text
friction
condim
contact parameter
solver setting
```

当前阶段只需要理解其高层作用，不需要掌握底层阻抗公式。

---

## 18. Box 对照实验

两个 box 可以使用完全相同的 friction：

```xml
friction="1 0.005 0.0001"
```

但是分别设置：

```text
Box A
condim = 1

Box B
condim = 3
```

那么：

### Box A

```text
只有法向接触
```

所以：

```text
sliding friction 不参与
```

即使 XML 中写了第一个 friction 参数，也没有被这个接触模型启用。

### Box B

```text
法向
+
sliding friction
```

所以：

```text
friction[0]
```

真正发挥作用。

因此在水平力作用下：

```text
condim=1
→ 更容易滑

condim=3
→ 会受到明显滑动摩擦
```

---

## 19. Sphere 对照实验

两个 sphere 可以设置：

```text
Sphere A
condim = 3

Sphere B
condim = 6
```

并且都使用：

```xml
friction="1 0.01 0.01"
```

对于 Sphere A：

```text
normal
+
sliding friction
```

被启用。

而 Sphere B：

```text
normal
+
sliding
+
torsional
+
rolling
```

都会被启用。

因此：

```text
condim=6
```

可以真正表现 rolling resistance。

---

## 20. 斜坡实验

斜坡实验中可以比较：

```text
cylinder condim=1
vs
cylinder condim=3
```

其中：

```text
condim=1
→ 主要只有法向接触
→ 更容易沿斜坡运动

condim=3
→ 增加 sliding friction
→ 下滑会受到更明显阻力
```

还可以比较：

```text
sphere condim=4
vs
sphere condim=6
```

用来观察：

```text
有没有 rolling friction
```

对运动的影响。

---

## 21. 控制变量实验思路

这个 friction 场景本质上是一个控制变量实验。

场景尽量保持其他条件相似，只改变：

```text
condim
friction
priority
```

来观察接触行为变化。

整个对照关系可以总结为：

```text
Box
1 vs 3
→ 比较有没有 sliding friction

Sphere
3 vs 6
→ 比较 torsional / rolling friction

Cylinder on slope
1 vs 3
→ 比较斜坡上的 sliding friction

Sphere on slope
4 vs 6
→ 比较 rolling friction
```

---

## 22. 核心理解

最重要的关系是：

```text
friction="a b c"

a
→ sliding friction

b
→ torsional friction

c
→ rolling friction
```

以及：

```text
condim = 1
→ normal only

condim = 3
→ + sliding

condim = 4
→ + torsional

condim = 6
→ + rolling
```

再加上：

```text
elliptic
→ 约束维度 = condim

pyramidal
→ 约束维度通常为 2 × (condim - 1)
```

以及：

```text
priority 不同
→ 高 priority 的 geom 优先

priority 相同
→ friction 每一项分别取较大值
```

---

## 23. 当前阶段需要记住什么

现在最重要的是：

```text
friction
→ 摩擦有多强

condim
→ 哪些摩擦模式存在

cone
→ 摩擦约束如何表示

priority
→ 两个 geom 接触时谁的参数优先
```

至于更底层的 solver equation、constraint impedance 和源码实现，目前不用记。

---

## 来源

本笔记基于：

```text
Albusgive/mujoco_learning
```

来源仓库：

https://github.com/Albusgive/mujoco_learning

原始仓库与教学材料归对应作者所有。

本文记录的是我在学习过程中的个人理解、例子分析、仿真观察与总结。