# Friction 摩擦对照实验

[English](friction_comparison_report.md) | [中文](friction_comparison_report_zh.md)

---

## 1. 实验目的

本实验用于验证并巩固 Albusgive MuJoCo 学习来源中关于 friction 的相关内容。

主要对比：

- `condim=1` 与 `condim=3`
- `condim=3` 与 `condim=6`
- `condim=4` 与 `condim=6`
- 不同 friction mode 的作用
- `priority` 的作用
- `friction` 与 `condim` 的关系

本实验最核心的问题是：

> 改变 contact dimension 之后，实际参与接触的摩擦类型会发生什么变化？

---

## 2. 模型文件

实验模型保存在：

```text
experiments/M2/MuJoCo/friction_comparison.xml
```

模型中包含四组主要对照：

```text
Group 1
Box: condim 1 vs 3

Group 2
Sphere: condim 3 vs 6

Group 3
Cylinder on slope: condim 1 vs 3

Group 4
Sphere on slope: condim 4 vs 6
```

---

## 3. 全局仿真设置

模型使用：

```xml
<option
    timestep="0.002"
    gravity="0 0 -9.81"
    integrator="implicitfast"
    cone="elliptic"
    impratio="1"/>
```

其中：

```text
timestep = 0.002 s
→ 每个物理步推进 2 ms

gravity = 0 0 -9.81
→ 使用类似地球重力

integrator = implicitfast
→ 使用 implicitfast 积分器

cone = elliptic
→ 使用 elliptic friction cone

impratio = 1
→ 本实验中的 friction constraint impedance 相对设置
```

---

## 4. Friction 参数

MuJoCo 中：

```xml
friction="a b c"
```

三个参数分别表示：

```text
a
→ sliding friction

b
→ torsional friction

c
→ rolling friction
```

例如：

```xml
friction="1 0.005 0.0001"
```

表示：

```text
sliding friction = 1
torsional friction = 0.005
rolling friction = 0.0001
```

但是：

> 写出了三个 friction 参数，并不代表三种摩擦一定都会生效。

是否参与 contact model，主要还取决于：

```text
condim
```

---

## 5. `condim` 的作用

本实验使用的主要 `condim` 值：

```text
condim = 1
→ 只有 normal contact

condim = 3
→ normal + sliding friction

condim = 4
→ normal + sliding + torsional friction

condim = 6
→ normal + sliding + torsional + rolling friction
```

因此可以理解为：

```text
friction
→ 决定摩擦强度

condim
→ 决定哪些摩擦模式被纳入 contact model
```

这个实验就是为了让这个区别变得更加直观。

---

# Experiment Group 1 - Box 对照

## 6. `condim=1` 的 Box

第一个 box 使用：

```xml
friction="1 0.005 0.0001"
condim="1"
```

虽然 friction 参数已经完整写出，但 contact model 中只包含：

```text
normal contact
```

也就是说：

```text
sliding friction 并没有被启用
```

因此这个 box 在地面上更容易发生切向运动。

---

## 7. `condim=3` 的 Box

第二个 box 使用：

```xml
friction="1 0.005 0.0001"
condim="3"
```

这时 contact model 包含：

```text
normal contact
+
两个 sliding friction direction
```

因此第一个 friction 参数：

```text
friction[0]
```

真正进入接触摩擦模型。

所以相比 `condim=1` 的 box，它对滑动会有更明显的阻力。

---

## 8. 预期对比

核心区别：

```text
Box A
condim = 1
→ 没有 sliding friction mode

Box B
condim = 3
→ 启用 sliding friction
```

因此：

```text
Box A
→ 更容易滑动

Box B
→ 对滑动有更强阻力
```

这里主要改变的变量就是：

```text
condim
```

---

# Experiment Group 2 - Sphere 对照

## 9. `condim=3` 的 Sphere

第一个 sphere 使用：

```xml
friction="1 0.01 0.01"
condim="3"
```

这会启用：

```text
normal contact
+
sliding friction
```

但是不会完整加入：

```text
torsional friction
rolling friction
```

对应的 contact dimension。

---

## 10. `condim=6` 的 Sphere

第二个 sphere 使用：

```xml
friction="1 0.01 0.05"
condim="6"
```

这时会包含：

```text
normal
+
sliding
+
torsional
+
rolling
```

其中 rolling friction 特意设置得更明显：

```text
rolling friction = 0.05
```

这样更容易观察 rolling resistance 的效果。

---

## 11. 预期对比

对比关系：

```text
Sphere A
condim = 3

Sphere B
condim = 6
```

第二个 sphere 多了：

```text
torsional resistance
rolling resistance
```

尤其是 rolling friction。

因此：

```text
condim=6
```

的 sphere 应该更容易损失滚动运动。

---

# Experiment Group 3 - 斜坡上的 Cylinder

## 12. 为什么使用斜坡

斜坡可以让重力自然驱动物体运动。

重力在斜坡方向上的分量会让 cylinder 向下运动。

这样就不需要额外 actuator。

因此可以直接观察：

```text
contact friction
```

对运动的影响。

---

## 13. `condim=1` 的 Cylinder

第一个 cylinder 使用：

```xml
condim="1"
```

也就是说：

```text
只有 normal contact
```

没有 sliding friction mode。

因此它在斜坡上应该更容易向下运动。

---

## 14. `condim=3` 的 Cylinder

第二个 cylinder 使用：

```xml
condim="3"
```

这时加入：

```text
sliding friction
```

所以 cylinder 沿斜坡运动时，会受到更明显的阻力。

---

## 15. 预期对比

```text
Cylinder A
condim = 1
→ 主要只有 normal support

Cylinder B
condim = 3
→ normal + sliding friction
```

预期：

```text
condim=1
→ 更容易沿斜坡运动

condim=3
→ 运动阻力更明显
```

---

# Experiment Group 4 - 斜坡上的 Sphere

## 16. `condim=4` 的 Sphere

第一个斜坡 sphere 使用：

```xml
friction="1 0.01 0.05"
condim="4"
```

会启用：

```text
normal
+
sliding
+
torsional
```

但是：

```text
rolling friction dimension
```

还没有被加入。

---

## 17. `condim=6` 的 Sphere

第二个 sphere 使用：

```xml
friction="1 0.01 0.05"
condim="6"
```

会包含：

```text
normal
+
sliding
+
torsional
+
rolling
```

因此 rolling resistance 会真正成为 contact model 的一部分。

---

## 18. 预期对比

关键区别：

```text
condim = 4
→ 没有 rolling friction dimension

condim = 6
→ 启用 rolling friction dimension
```

两个 sphere 使用同样的 rolling friction coefficient：

```text
0.05
```

因此：

> 主要区别来自 `condim` 是否真正启用了 rolling friction。

这使得对照更有意义。

---

# Contact Priority

## 19. Floor 与 Slope 的 Priority

Floor 和 slope 使用：

```xml
priority="-1"
```

而移动物体使用：

```xml
priority="0"
```

因此：

```text
moving object priority
>
surface priority
```

这是故意这样设置的。

---

## 20. 为什么 Priority 很重要

当两个 geom 的 priority 不同时：

```text
priority 更高的 geom
```

会主导重要 contact 参数。

这些参数可能包括：

```text
friction
condim
solref
solimp
```

因此：

```text
surface priority = -1

moving object priority = 0
```

可以让：

> 每个移动物体自己的 `condim` 和 friction 设置真正成为实验变量。

这样不会被 floor 或 slope 的 contact 设置覆盖。

---

## 21. 控制变量实验设计

这个实验整体采用控制变量思路。

每一组尽量保持其他属性相近，只改变关键 contact 参数。

例如：

```text
Box
→ geometry 和 friction 基本一致
→ 只把 condim 从 1 改成 3
```

```text
Sphere
→ geometry 类似
→ condim 从 3 改成 6
```

```text
Slope Sphere
→ friction 完全一样
→ condim 从 4 改成 6
```

这样更容易把观察到的运动变化归因到某个特定 contact setting。

---

# Friction Cone

## 22. Elliptic Friction Cone

本实验使用：

```xml
cone="elliptic"
```

对于 elliptic friction cone：

```text
constraint dimension
=
condim
```

因此：

```text
condim = 1
→ 1 个 contact dimension

condim = 3
→ 3 个 contact dimensions

condim = 4
→ 4 个 contact dimensions

condim = 6
→ 6 个 contact dimensions
```

所以本实验中：

```text
condim
```

和实际 contact constraint dimension 是直接对应的。

---

## 23. 物理方向理解

对于：

```text
condim = 6
```

包含：

```text
1 个 normal direction
2 个 sliding directions
1 个 torsional direction
2 个 rolling directions
```

总共：

```text
6 个方向
```

这也解释了为什么 `condim` 是：

```text
1 → 3 → 4 → 6
```

而不是：

```text
1 → 2 → 3 → 4
```

---

# Model Independence

## 24. 移除外部 Asset 依赖

之前学习中的一个例子使用了：

```text
../asset/desert.png
```

这样的外部 skybox 文件。

当本地没有这个文件时：

```text
MuJoCo Viewer
```

无法加载模型。

因此这次实验去掉了这个外部依赖。

Floor 改为使用 MuJoCo 内置 checker texture：

```xml
builtin="checker"
```

这样整个实验更加独立。

---

## 25. 为什么这样更好

一个学习实验最好应该：

```text
容易复制
容易运行
容易检查
容易复现
```

减少不必要的外部文件依赖，可以提高 reproducibility。

---

# 实验结果与理解

## 26. 最重要的学习结果

这个实验最重要的结论是：

```text
只有 friction coefficient
是不够的
```

实际 contact behavior 很大程度上还取决于：

```text
condim
```

因为：

```text
condim
```

决定哪些 friction direction 真正存在于 contact model 中。

---

## 27. 核心关系

本实验进一步强化了下面的关系：

```text
friction
→ 某种摩擦有多强

condim
→ 某种摩擦是否被启用

priority
→ 两个 geom 接触时谁的 contact 参数占主导

cone
→ friction constraint 在数学上如何表示
```

这些参数不是独立理解的，而是需要一起看。

---

## 28. 四组对照总结

```text
Box
condim 1 vs 3
→ sliding friction

Sphere
condim 3 vs 6
→ torsional + rolling friction

Cylinder on slope
condim 1 vs 3
→ 重力作用下的 sliding resistance

Sphere on slope
condim 4 vs 6
→ rolling friction effect
```

---

## 29. 我学到的最重要一点

在做这个实验之前，很容易误以为：

```xml
friction="1 0.01 0.05"
```

就代表：

```text
三种 friction 全部生效
```

但这是不准确的。

应该理解为：

```text
friction values
+
condim
```

必须结合起来看。

例如：

```text
rolling friction coefficient 已经写了

但是 condim = 4
→ rolling friction dimension 没有启用
```

而：

```text
rolling friction coefficient 已经写了

并且 condim = 6
→ rolling friction 可以真正影响接触行为
```

这是这一部分最重要的理解之一。

---

## 30. 当前理解模型

当前阶段可以用下面这个方式记：

```text
friction
→ strength
→ 摩擦强度

condim
→ enabled friction modes
→ 启用了哪些摩擦模式

priority
→ whose contact settings are used
→ 谁的 contact 参数优先

cone
→ mathematical representation
→ 数学表示方式
```

目前不需要继续深入到底层 solver implementation。

---

## 来源

本实验基于：

```text
Albusgive/mujoco_learning
```

来源仓库：

https://github.com/Albusgive/mujoco_learning

XML 模型与实验报告是在学习过程中基于相关概念重新整理的。

本实验的目的不是复刻原始仓库内容，而是记录我对 MuJoCo contact 与 friction 行为的理解和验证过程。