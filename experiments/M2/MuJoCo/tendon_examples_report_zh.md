# MuJoCo Tendon 示例分析

[English](tendon_examples_report.md) | [中文](tendon_examples_report_zh.md)

## 概览

本报告记录了 Albusgive MuJoCo 学习来源中的两个 tendon 示例分析：

1. 使用 `fixed` tendon 的 Mecanum 轮模型
2. 使用 `spatial` tendon 与 `muscle` actuator 的多连杆模型

这份报告的目的，是记录两个示例的工作原理，以及 tendon 传动与直接 joint 驱动之间的区别。

这些示例来自原始学习材料并进行了详细分析。

本报告不声称已经在本仓库中完整重新构建并独立验证原始 XML 模型。

---

# 1. 示例 A - Mecanum 机器人的 Fixed Tendon

## 模型思路

第一个示例有四个主要 wheel joint：

```text
a1
b1
a2
b2
```

模型没有直接独立控制四个 joint，而是定义了三个 `fixed` tendon：

```text
forward
transverse
rotate
```

这样就把：

```text
4 个真实 wheel joint
↓
fixed tendon 组合
↓
3 个直观运动通道
```

---

# 2. Wheel 结构

这个 Mecanum wheel 模型使用 cylinder 作为主要轮体，并在轮子周围重复生成倾斜 roller。

Roller 使用：

```text
replicate
```

创建。

学习到的结构中大约有：

```text
16 个重复 roller
```

每次绕轮子增加的旋转角约为：

```text
euler z ≈ 0.3925 rad
```

因为：

```text
2π / 16 ≈ 0.3927
```

所以这些 roller 会比较均匀地分布在轮子圆周上。

Roller 自身倾斜角大约为：

```text
±0.785398 rad
≈ ±45°
```

这正是典型的 Mecanum wheel roller 布置方式。

---

# 3. Forward Tendon

`forward` fixed tendon 的系数关系：

```text
a1  +0.25
b1  +0.25
a2  +0.25
b2  +0.25
```

可以表示成：

```text
forward
=
0.25a1
+
0.25b1
+
0.25a2
+
0.25b2
```

符号模式：

```text
+ +
+ +
```

四个 wheel joint 都同方向贡献。

因此这个 tendon 表示：

```text
forward / backward
```

也就是前后移动的组合坐标。

---

# 4. Transverse Tendon

`transverse` tendon 的系数关系：

```text
a1  +0.25
b1  -0.25
a2  -0.25
b2  +0.25
```

可以表示为：

```text
transverse
=
+0.25a1
-0.25b1
-0.25a2
+0.25b2
```

符号模式：

```text
+ -
- +
```

因为 Mecanum roller 的安装方向不同，这样的 wheel 组合可以形成横向运动。

所以：

```text
transverse
→ sideways motion
```

具体正方向到底对应左移还是右移，需要结合：

```text
wheel installation
joint axis
sign convention
```

判断。

因此不能只通过这里的正负号，就直接断定某一方向一定是左或右。

---

# 5. Rotate Tendon

`rotate` tendon 的系数关系：

```text
a1  +0.25
b1  +0.25
a2  -0.25
b2  -0.25
```

可以表示为：

```text
rotate
=
+0.25a1
+0.25b1
-0.25a2
-0.25b2
```

符号模式：

```text
+ +
- -
```

两组 wheel 产生相反方向的贡献。

因此会形成：

```text
yaw rotation
```

也就是车辆自身旋转。

具体正方向是：

```text
clockwise
或
counter-clockwise
```

同样取决于完整模型中的 joint axis 和 wheel orientation。

---

# 6. 为什么使用 `coef="0.25"`

模型中有四个 wheel joint。

如果每个 joint 的贡献都是：

```text
0.25
```

那么：

```text
0.25 × 4 = 1
```

所以可以理解成一种：

```text
average-like
normalized combination
```

不过真正重要的并不是：

```text
0.25
```

这个数字本身。

更加重要的是：

```text
relative magnitude
+
relative sign
```

也就是每个 joint 之间的相对权重和方向。

---

# 7. Velocity Actuator

示例中 actuator 不是直接控制 wheel joint，而是直接控制 tendon。

概念上类似：

```xml
<velocity tendon="forward" .../>
<velocity tendon="transverse" .../>
<velocity tendon="rotate" .../>
```

因此控制链变成：

```text
data.ctrl
↓
velocity actuator
↓
fixed tendon
↓
多个 wheel joint
↓
vehicle motion
```

学习材料中的 actuator 参数包括：

```text
kv = 30
ctrlrange = [-15, 15]
```

这意味着控制器是在：

```text
tendon-level virtual coordinate
```

上进行控制。

---

# 8. Mecanum 示例最重要的意义

如果没有 fixed tendon，控制器可能需要自己分别考虑：

```text
a1
b1
a2
b2
```

也就是四个 wheel joint 应该分别如何运动。

加入 fixed tendon 后，可以将这些 joint 组合成：

```text
forward
transverse
rotate
```

所以控制层可以直接考虑：

```text
前后
横向
旋转
```

这比直接处理四个 wheel joint 更直观。

最重要的概念：

```text
physical joints
↓
fixed tendon
↓
virtual motion coordinate
```

---

# 9. 示例 B - Spatial Tendon + Muscle

第二个示例展示的是：

```text
spatial tendon
```

和 fixed tendon 不同，spatial tendon 不是 joint coordinate 的数学组合。

它真正沿着多个：

```text
site
```

在空间中形成几何路径。

模型由多个相互连接的 body 和 hinge joint 组成。

不同 body 上放置 site，再通过 site 构建 tendon routing。

---

# 10. Joint 结构

示例中包含三个 hinge joint：

```text
joint1
joint2
joint3
```

学习到的关节范围中包括：

```text
joint2 range = 0 to 1.57 rad
joint3 range = 0 to 0.78 rad
```

大约对应：

```text
1.57 rad ≈ 90°
0.78 rad ≈ 45°
```

这些 joint 在该示例中使用：

```text
axis="0 0 1"
```

也就是绕 z 轴旋转。

---

# 11. Tendon Routing Site

模型中有多个 site：

```text
ceiling
hook1
hook2
hook3
hook4
hook5
```

这些 site 用来作为：

```text
tendon attachment point
tendon guide point
```

最重要的关系是：

```text
body motion
↓
site position 改变
↓
spatial tendon geometry 改变
↓
tendon length 改变
```

---

# 12. 被动 Tendon `M`

第一条 spatial tendon 名为：

```text
M
```

它的路径：

```text
ceiling
↓
hook1
↓
hook2
↓
hook3
```

学习到的主要参数：

```text
springlength = "0 0.5"
stiffness = 1000
damping = 10
width = 0.01
```

这条 tendon 具有比较大的：

```text
stiffness
```

所以可以理解成：

```text
elastic tendon
+
damper
```

也就是：

> 带弹性和阻尼的被动 tendon。

它不需要 actuator，也可以产生弹性和阻尼作用。

---

# 13. 被动 Tendon 的行为

当模型中的 body 运动时：

```text
site position 改变
↓
tendon length 改变
```

如果 tendon 偏离 spring reference length：

```text
stiffness
↓
产生恢复作用
```

如果 tendon 长度快速变化：

```text
damping
↓
抵抗长度变化速度
```

所以：

```text
M
```

可以近似理解成：

```text
spring
+
damper
```

构成的 tendon transmission。

---

# 14. 主动 Tendon `A`

第二条 spatial tendon 名为：

```text
A
```

它的路径：

```text
hook4
↓
hook5
```

主要参数：

```text
springlength = "0 0.5"
stiffness = 0
damping = 10
width = 0.01
```

和 `M` 最大的区别：

```text
stiffness = 0
```

所以它本身没有明显的被动弹簧作用。

它主要通过 actuator 主动驱动。

---

# 15. Muscle Actuator

示例中使用：

```xml
<muscle
    name="A"
    tendon="A"
    ctrlrange="-15 15"/>
```

最重要的是：

```xml
tendon="A"
```

这说明 muscle actuator 并不是直接控制：

```text
joint
```

而是直接作用于：

```text
spatial tendon A
```

因此控制链是：

```text
control input
↓
muscle actuator
↓
spatial tendon A
↓
hook sites
↓
body
↓
joint motion
```

---

# 16. Spatial Tendon 为什么能带动机构

假设：

```text
hook4
```

和：

```text
hook5
```

分别属于不同 body。

当 tendon 产生 tension 时：

```text
tendon tension
↓
site 上产生作用力
↓
body 受到力
↓
对 joint 形成 torque
↓
joint motion
```

这和真实生物系统非常类似：

```text
muscle
↓
tendon
↓
bone
↓
joint
```

---

# 17. Fixed 和 Spatial 的根本区别

两个例子体现出了两种 tendon 的根本差异。

## Fixed Tendon

```text
joint coordinate
↓
weighted mathematical combination
↓
virtual motion coordinate
```

典型例子：

```text
Mecanum
→ forward
→ transverse
→ rotate
```

---

## Spatial Tendon

```text
sites in space
↓
geometric tendon path
↓
length / tension
↓
body force
↓
joint motion
```

典型例子：

```text
muscle-driven linked mechanism
```

---

# 18. 两种 Tendon 对比

| 特点 | Fixed Tendon | Spatial Tendon |
|---|---|---|
| 本质 | Joint coordinate 组合 | 空间几何路径 |
| 主要子元素 | `joint` | `site` |
| 关键参数 | `coef` | routing site |
| 常见用途 | transmission / coupling | cable / tendon / muscle |
| 是否依赖几何位置 | 主要不依赖 | 强烈依赖 |
| 学习示例 | Mecanum robot | muscle-tendon mechanism |

---

# 19. 这两个例子最大的学习成果

这两个模型最重要的地方，是让我理解了：

> actuator 并不一定要直接控制一个 joint。

MuJoCo 还可以实现：

```text
actuator
↓
tendon
↓
multiple joints / bodies
```

这样 actuator 和 joint 之间就增加了一层：

```text
transmission
```

需要清楚区分三个概念：

```text
joint
→ 定义机构允许怎样运动

tendon
→ 定义力和运动怎样传递 / 耦合

actuator
→ 提供主动驱动力
```

---

## 来源

本示例分析基于：

```text
Albusgive/mujoco_learning
```

来源仓库：

https://github.com/Albusgive/mujoco_learning

原始模型和教学材料归对应作者所有。

本报告记录的是我在学习过程中对原始示例的理解、结构分析与总结。

本仓库没有声称这些完整 XML 模型是自行原创，也没有声称已经在本仓库中完整重新构建并独立验证这些原始示例。