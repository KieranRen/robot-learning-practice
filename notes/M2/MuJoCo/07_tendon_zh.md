# MuJoCo Tendon 肌腱 / 传动结构

[English](07_tendon.md) | [中文](07_tendon_zh.md)

## 概览

本笔记整理的是 Albusgive MuJoCo 学习来源中关于 `tendon` 的内容。

主要包括：

- tendon 基本概念
- `spatial` tendon
- `fixed` tendon
- 基于 site 的 tendon 路径
- joint 组合
- `coef`
- `range`
- `frictionloss`
- `springlength`
- `stiffness`
- `damping`
- tendon 可视化
- tendon 与 actuator 的关系
- Mecanum 轮 fixed tendon 示例
- spatial tendon + muscle 示例

最重要的关系是：

```text
joint
→ 决定 body 可以怎么动

tendon
→ 建立传动 / 耦合关系

actuator
→ 提供主动驱动力
```

因此 actuator 可以直接作用于 joint：

```text
actuator
↓
joint
↓
body motion
```

也可以通过 tendon：

```text
actuator
↓
tendon
↓
joint(s) / body structure
↓
motion
```

---

# 1. Tendon 是什么

MuJoCo 中的 tendon 可以把多个模型部件之间的运动或受力关系连接起来。

它可以用来模拟或描述：

- 绳索
- 钢丝
- 皮带
- 生物肌腱
- 多关节传动
- 关节耦合

正常情况下，一个 actuator 可以单独控制一个 joint。

例如：

```text
actuator 1
→ joint 1

actuator 2
→ joint 2
```

但使用 tendon 后可以变成：

```text
一个 actuator
↓
一个 tendon
↓
多个 joint / body
```

所以 tendon 可以理解成：

> 机器人机构中的传动或耦合层。

---

# 2. Tendon 的两种主要类型

MuJoCo 中主要有两种 tendon：

```text
spatial
fixed
```

两者代表完全不同的概念。

```text
spatial
→ 空间中的几何路径

fixed
→ joint coordinate 的数学组合
```

最简单的记忆方式：

```text
spatial
→ 看 site

fixed
→ 看 joint
```

---

# Part I - Spatial Tendon

## 3. Spatial Tendon

`spatial tendon` 可以理解成：

> 一根真实经过多个空间点的绳索 / 肌腱。

它的路径通常由多个 `site` 定义。

例如：

```xml
<tendon>
    <spatial name="T">
        <site site="s1"/>
        <site site="s2"/>
        <site site="s3"/>
    </spatial>
</tendon>
```

表示 tendon 的路径：

```text
s1
↓
s2
↓
s3
```

所以 spatial tendon 的几何形状会随着这些 site 的位置改变而改变。

---

# 4. Site 为什么重要

在 spatial tendon 中，site 可以作为：

```text
attachment point
guide point
hook point
```

也就是：

> tendon 的固定点、挂点或导向点。

例如：

```xml
<site name="hook1"/>
<site name="hook2"/>
<site name="hook3"/>
```

再写：

```xml
<spatial name="T">
    <site site="hook1"/>
    <site site="hook2"/>
    <site site="hook3"/>
</spatial>
```

就代表：

```text
tendon 从 hook1
↓
经过 hook2
↓
再到 hook3
```

由于这些 site 属于不同 body：

```text
body motion
↓
site position 改变
↓
tendon path 改变
↓
tendon length 改变
↓
tendon force 可能改变
```

这就是 spatial tendon 的核心。

---

# 5. Spatial Tendon 的物理意义

Spatial tendon 非常适合模拟：

- cable-driven robot
- tendon-driven robot
- biological tendon
- pulley-like routing
- 拉索机构
- 绳索传动

它的 tendon length 是根据：

```text
site 在空间中的实际位置
```

计算出来的。

这和 fixed tendon 完全不同。

---

# 6. `range`

Tendon 可以设置：

```xml
range="a b"
```

表示允许的 tendon length 范围。

例如：

```xml
range="0.2 0.5"
```

可以理解成：

```text
tendon 允许长度
→ 0.2 ~ 0.5
```

可以和 joint range 对比：

```text
joint range
→ joint coordinate 范围

tendon range
→ tendon length 范围
```

通常还需要配合相应的 limit 设置，range 才会成为真正的约束。

---

# 7. `frictionloss`

Tendon 可以设置：

```xml
frictionloss="..."
```

表示 tendon 自身的摩擦损失。

可以理解成：

```text
tendon 想改变长度
↓
frictionloss
↓
产生阻力
```

当前阶段知道它是：

> tendon 层面的摩擦阻力

即可。

---

# 8. `width`

Spatial tendon 可以设置：

```xml
width="0.003"
```

主要用于 Viewer 可视化。

```text
width 大
→ tendon 看起来更粗

width 小
→ tendon 看起来更细
```

需要注意：

> `width` 主要是显示参数，不要直接把它理解成真实绳索的物理截面积。

---

# 9. `rgba`

例如：

```xml
rgba="1 0 0 1"
```

表示 tendon 在 Viewer 中显示为红色。

所以：

```text
rgba
→ 控制 tendon 显示颜色
```

主要也是可视化参数。

---

# 10. `stiffness`

Tendon 可以具有弹簧性质。

参数：

```xml
stiffness="..."
```

决定 tendon 对长度变化的抵抗强度。

可以粗略理解：

```text
F ≈ k ΔL
```

其中：

```text
k
→ stiffness

ΔL
→ tendon 当前长度相对于参考长度的偏差
```

因此：

```text
stiffness 大
→ tendon 更硬
→ 不容易改变长度

stiffness 小
→ tendon 更软
```

---

# 11. `springlength`

参数：

```xml
springlength="..."
```

表示 tendon 作为弹簧工作时的参考长度 / 自然长度。

可以简单记：

```text
springlength
→ 弹簧自然长度

stiffness
→ 弹簧有多硬
```

两者一起决定 tendon 的弹性行为。

---

# 12. `damping`

参数：

```xml
damping="..."
```

表示 tendon 对长度变化速度的阻尼。

可以粗略理解：

```text
damping force
≈
-c × tendon length velocity
```

所以：

```text
stiffness
→ 抵抗长度偏移

damping
→ 抵抗长度变化速度
```

也就是类似：

```text
spring
+
damper
```

系统。

---

# 13. 被动 Spatial Tendon 示例

学习中的第一个 spatial tendon：

```xml
<spatial
    name="M"
    springlength="0 0.5"
    stiffness="1000"
    damping="10"
    width="0.01"
    rgba="1 0 0 1">

    <site site="ceiling"/>
    <site site="hook1"/>
    <site site="hook2"/>
    <site site="hook3"/>

</spatial>
```

它的路径是：

```text
ceiling
↓
hook1
↓
hook2
↓
hook3
```

其中：

```text
stiffness = 1000
damping = 10
```

所以这条 tendon 有比较强的：

```text
弹性恢复作用
+
阻尼作用
```

可以把它理解成：

> 一条被动弹性肌腱 / 弹性拉索。

---

# 14. 主动 Spatial Tendon 示例

第二条 tendon：

```xml
<spatial
    name="A"
    springlength="0 0.5"
    stiffness="0"
    damping="10"
    width="0.01"
    rgba="1 0 0 1">

    <site site="hook4"/>
    <site site="hook5"/>

</spatial>
```

它的路径：

```text
hook4
↓
hook5
```

这里：

```text
stiffness = 0
```

表示：

> 它本身不作为一个明显的被动弹簧工作。

它主要通过后面的 actuator 主动驱动。

---

# 15. Muscle Actuator 驱动 Tendon

示例中：

```xml
<actuator>
    <muscle
        name="A"
        tendon="A"
        ctrlrange="-15 15"/>
</actuator>
```

最关键的是：

```xml
tendon="A"
```

也就是说：

```text
muscle actuator
```

不是直接控制某个：

```text
joint
```

而是控制：

```text
tendon A
```

所以控制链：

```text
muscle actuator
↓
tendon A
↓
site
↓
body
↓
joint motion
```

---

# 16. 为什么拉 Tendon 会让 Joint 转动

假设：

```text
hook4
→ 属于 body 2

hook5
→ 属于 body 3
```

当 tendon A 产生 tension：

```text
hook4 和 hook5
↓
趋向靠近
```

由于它们属于不同 body：

```text
site force
↓
body force
↓
产生 joint torque
↓
joint rotation
```

这就是 tendon-driven robot 的基本工作原理。

---

# 17. 和真实肌肉的关系

真实人体中：

```text
muscle contraction
↓
tendon tension
↓
拉动骨骼
↓
joint rotation
```

MuJoCo 中也是类似：

```text
muscle actuator
↓
spatial tendon
↓
body / site
↓
joint motion
```

所以 spatial tendon 非常适合模拟：

```text
muscle-tendon system
```

---

# Part II - Fixed Tendon

## 18. Fixed Tendon

`fixed tendon` 与 spatial tendon 完全不同。

它不定义真实的空间绳索路径。

而是：

> 把多个 joint coordinate 按一定系数组合起来。

例如：

```xml
<tendon>
    <fixed name="T">
        <joint joint="joint1" coef="1"/>
        <joint joint="joint2" coef="2"/>
    </fixed>
</tendon>
```

可以粗略理解成：

```text
T
=
1 × q1
+
2 × q2
```

其中：

```text
q1
→ joint1 coordinate

q2
→ joint2 coordinate
```

所以 fixed tendon 可以看成：

> 一个由多个真实 joint 组合出来的虚拟 coordinate。

---

# 19. `coef`

参数：

```xml
coef="..."
```

决定每个 joint 在 fixed tendon 中的贡献。

例如：

```text
coef = 1
→ 正常贡献

coef = 2
→ 两倍贡献

coef = -1
→ 反方向贡献
```

最重要的是：

```text
正负号
```

因为正负号决定不同 joint 是：

```text
同方向贡献
还是
反方向贡献
```

---

# 20. Fixed Tendon 可以理解成虚拟运动轴

假设有：

```text
joint1
joint2
joint3
joint4
```

通过 fixed tendon 可以组合成：

```text
virtual coordinate
```

所以：

```text
多个真实 joint
↓
fixed tendon
↓
一个虚拟运动方向
```

然后 actuator 可以直接控制这个 tendon。

---

# 21. Mecanum 轮示例

学习中的 Mecanum 示例有四个主要 wheel joint：

```text
a1
b1
a2
b2
```

然后使用三个 fixed tendon：

```text
forward
transverse
rotate
```

所以：

```text
4 个真实轮子 joint
↓
3 个 fixed tendon
↓
3 个直观控制通道
```

也就是：

```text
前后移动
横向移动
旋转
```

---

# 22. Forward Tendon

代码：

```xml
<fixed name="forward">
    <joint joint="a1" coef="0.25"/>
    <joint joint="b1" coef="0.25"/>
    <joint joint="a2" coef="0.25"/>
    <joint joint="b2" coef="0.25"/>
</fixed>
```

可以写成：

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

四个 coef：

```text
全部同号
```

所以：

```text
+   +
+   +
```

表示四个 wheel joint 同方向贡献。

因此对应：

```text
forward / backward
```

运动模式。

---

# 23. 为什么使用 `0.25`

因为有四个 wheel joint：

```text
0.25 × 4 = 1
```

可以理解成一种：

```text
normalized / average-like combination
```

当前阶段不需要认为一定必须是 0.25。

真正重要的是：

> 四个 coef 的相对大小和符号关系。

---

# 24. Transverse Tendon

代码：

```xml
<fixed name="transverse">
    <joint joint="a1" coef="0.25"/>
    <joint joint="b1" coef="-0.25"/>
    <joint joint="a2" coef="-0.25"/>
    <joint joint="b2" coef="0.25"/>
</fixed>
```

数学关系：

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
+   -
-   +
```

由于 Mecanum wheel roller 具有不同的安装角度：

```text
前后方向力分量
→ 大量抵消

横向力分量
→ 相互叠加
```

于是车辆产生：

```text
sideways motion
```

也就是横向移动。

---

# 25. Rotate Tendon

代码：

```xml
<fixed name="rotate">
    <joint joint="a1" coef="0.25"/>
    <joint joint="b1" coef="0.25"/>
    <joint joint="a2" coef="-0.25"/>
    <joint joint="b2" coef="-0.25"/>
</fixed>
```

数学关系：

```text
rotate
=
+0.25a1
+0.25b1
-0.25a2
-0.25b2
```

符号：

```text
+   +
-   -
```

也就是一组 wheel 正方向贡献，另一组反方向贡献。

这样会形成：

```text
yaw torque
```

所以车辆可以旋转。

---

# 26. Mecanum Tendon 对比

可以总结成：

| Tendon | a1 | b1 | a2 | b2 | 主要效果 |
|---|---:|---:|---:|---:|---|
| `forward` | + | + | + | + | 前后移动 |
| `transverse` | + | - | - | + | 横向移动 |
| `rotate` | + | + | - | - | 旋转 |

具体正方向对应：

```text
前 / 后
左 / 右
顺时针 / 逆时针
```

还要结合：

```text
joint axis
wheel orientation
```

判断。

当前最重要的是：

```text
相对符号组合
```

---

# 27. Actuator 控制 Fixed Tendon

示例：

```xml
<actuator>
    <velocity
        tendon="forward"
        name="forward"
        kv="30"
        ctrlrange="-15 15"/>

    <velocity
        tendon="transverse"
        name="transverse"
        kv="30"
        ctrlrange="-15 15"/>

    <velocity
        tendon="rotate"
        name="rotate"
        kv="30"
        ctrlrange="-15 15"/>
</actuator>
```

这里非常重要：

```xml
tendon="..."
```

而不是：

```xml
joint="..."
```

所以控制关系变成：

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

---

# 28. 为什么 Fixed Tendon 很方便

如果没有 fixed tendon：

```text
controller
```

可能需要自己计算：

```text
a1 = ?
b1 = ?
a2 = ?
b2 = ?
```

然后分别控制四个 wheel。

使用 fixed tendon 后：

```text
a1
b1
a2
b2
↓
组合成
↓
forward
transverse
rotate
```

控制层只需要考虑：

```text
前后
横移
旋转
```

所以控制接口会更加直观。

---

# 29. Spatial 与 Fixed 对比

| 特点 | Spatial Tendon | Fixed Tendon |
|---|---|---|
| 本质 | 空间中的绳索路径 | joint coordinate 的数学组合 |
| 主要使用 | `site` | `joint` |
| 是否依赖几何位置 | 是 | 主要不是 |
| Tendon length 来源 | site 空间路径 | joint coordinate + coef |
| 典型用途 | 拉索、肌腱、绳索 | 关节耦合、传动 |
| 关键参数 | site、stiffness、damping | joint、coef |

最简单记忆：

```text
spatial
→ 真正走空间路线

fixed
→ joint 数学组合
```

---

# 30. Tendon、Joint、Actuator 的区别

这三个概念必须区分。

## Joint

```text
决定 body 允许怎样相对运动
```

例如：

```text
hinge
→ 1 个 rotational DOF
```

---

## Tendon

```text
建立 transmission / coupling
```

例如：

```text
spatial
→ cable path

fixed
→ joint combination
```

---

## Actuator

```text
提供主动驱动力
```

所以：

```text
joint
→ 怎么能动

tendon
→ 力和运动怎么传递 / 耦合

actuator
→ 谁来主动驱动
```

---

# 31. 核心理解

最重要的关系：

```text
spatial tendon
→ 基于 site 的空间路径
→ body 运动会改变 tendon length
```

```text
fixed tendon
→ 多个 joint coordinate 的线性组合
→ coef 决定贡献大小和方向
```

```text
actuator
→ 可以驱动 tendon
→ tendon 再影响一个或多个 joint / body
```

---

# 32. 当前阶段需要记住什么

最重要的是：

```text
spatial
→ 跟 site 走

fixed
→ 把 joint 组合起来

coef
→ joint 的贡献大小与方向

stiffness
→ tendon 弹性刚度

springlength
→ tendon 弹簧参考长度

damping
→ 抵抗 tendon length 变化速度

actuator tendon="..."
→ actuator 控制 tendon
```

两个典型例子：

```text
Mecanum wheel
→ fixed tendon
→ joint coupling
```

```text
muscle-driven mechanism
→ spatial tendon
→ geometric cable force transmission
```

---

## 来源

本笔记基于：

```text
Albusgive/mujoco_learning
```

来源仓库：

https://github.com/Albusgive/mujoco_learning

原始仓库与教学材料归对应作者所有。

本文记录的是我在学习过程中的个人理解、例子分析、代码解读与总结。