# MuJoCo Actuator 执行器

[English](05_actuator.md) | [中文](05_actuator_zh.md)

---

## 概览

本笔记整理的是 Albusgive MuJoCo 学习来源中关于 `actuator` 的内容。

主要包括：

- actuator 基本概念
- actuator 与 joint 的关系
- `general`
- `motor`
- `position`
- `velocity`
- `intvelocity`
- `damper`
- `cylinder`
- `ctrlrange`
- `forcerange`
- `actrange`
- `gear`
- `kp`
- `kv`
- `timeconst`
- `inheritrange`
- actuator 的简化控制流程
- 一个双关节 actuator 示例

最重要的关系是：

```text
joint
→ 决定 body 可以怎么动

actuator
→ 决定 joint 怎么被驱动
```

从 Python 的角度看：

```text
data.ctrl
↓
actuator
↓
joint
↓
body 运动
```

---

## 1. Actuator 容器

MuJoCo 的 actuator 都定义在：

```xml
<actuator>
    ...
</actuator>
```

中。

同一个 `<actuator>` 容器里可以同时放不同类型的 actuator。

常见类型包括：

```text
general
motor
position
velocity
intvelocity
damper
cylinder
muscle
adhesion
plugin
```

当前阶段最重要的是：

```text
motor
position
velocity
intvelocity
```

而：

```text
damper
cylinder
```

属于更偏物理装置模拟的 actuator。

---

## 2. `general` Actuator

`general` 是最灵活、最底层的 actuator 形式。

很多其他 actuator 都可以理解成：

> 对 `general` 的常用参数进行了预设。

常见底层参数包括：

```text
dyntype
→ actuator 内部动态类型

gaintype
→ control input 如何被放大或映射

biastype
→ 如何产生额外偏置项

dynprm
→ dynamics 参数

gainprm
→ gain 参数

biasprm
→ bias 参数
```

当前阶段不需要记住这些数组的具体排列。

只需要理解：

```text
general
→ 最通用、最底层

motor / position / velocity / ...
→ 更容易使用的预设形式
```

---

## 3. Actuator 作用到哪里

Actuator 必须知道自己作用在哪个对象上。

常见目标包括：

```text
joint
tendon
site
```

例如：

```xml
<position joint="joint1"/>
```

表示：

```text
这个 actuator 控制 joint1
```

目前学习中的大部分 actuator 都是直接控制 joint。

---

## 4. `ctrlrange`

`ctrlrange` 定义 actuator 允许接受的 control input 范围。

例如：

```xml
<position
    joint="joint1"
    ctrllimited="true"
    ctrlrange="-1 1"/>
```

表示：

```text
data.ctrl
```

应限制在：

```text
[-1, 1]
```

范围内。

需要区分：

```text
joint range
→ joint 物理上能运动到哪里

ctrlrange
→ actuator 输入允许给多大
```

这两个不是同一个概念。

---

## 5. `forcerange`

`forcerange` 限制 actuator 最终能够施加的力或力矩。

例如：

```xml
<position
    joint="pivot"
    forcerange="-5 5"/>
```

如果控制的是 hinge joint，可以把它理解成：

```text
actuator torque
被限制在
[-5, 5] N·m 左右
```

例如：

```text
理论计算力矩 = +8
forcerange = [-5, 5]

最终输出
→ +5
```

同理：

```text
理论计算力矩 = -7

最终输出
→ -5
```

因此：

```text
ctrlrange
→ 限制“命令输入”

forcerange
→ 限制“最终输出力 / 力矩”
```

---

## 6. `actrange`

某些 actuator 会有内部 activation state。

`actrange` 用来限制这个内部状态。

它对包含以下行为的 actuator 特别重要：

```text
积分
滤波
内部 activation dynamics
```

例如 `intvelocity` 会把速度命令积分成一个内部目标位置。

如果完全不限制，这个内部目标可能不断累积。

---

## 7. `gear`

`gear` 决定 actuator 输出如何映射到目标对象。

对于简单 joint actuator，可以近似理解为：

```text
actuator output
× gear
↓
joint force / torque
```

所以一般来说：

```text
gear 更大
→ 同样 actuator output 下作用更强
```

但 `gear` 实际上可以表示更复杂的多维传动关系，所以精确含义要结合具体 actuator 配置理解。

---

# Motor Actuator

## 8. `motor`

`motor` actuator 直接提供力或力矩。

如果作用在 hinge joint：

```text
motor
→ torque control
```

如果作用在 translational joint：

```text
motor
→ force control
```

例如：

```xml
<motor
    name="Torque"
    joint="joint"/>
```

如果 Python 中：

```python
data.ctrl[0] = 0.5
```

这并不是：

```text
目标角 = 0.5 rad
```

而是：

```text
给 actuator 一个控制输入
↓
经过 gain / gear 映射
↓
产生力或力矩
```

---

## 9. Motor 与 Position 的区别

这是非常重要的区别。

### Motor

```text
control input
→ “推多大”
```

### Position

```text
control input
→ “去哪里”
```

例如：

```text
motor ctrl = 1
→ 给正方向驱动力 / 力矩

position ctrl = 1
→ 尽量把 joint 拉到 1 rad
```

使用 motor 时，最终 joint 会转到哪里，取决于：

- mass
- inertia
- gravity
- damping
- friction
- gear
- 控制输入持续时间

Motor 本身不会自动帮你决定最终位置。

---

## 10. Motor 是 General Actuator 的一种预设

`motor` 可以理解成一套简化的 `general actuator` 参数配置。

其典型特征可以概括为：

```text
dyntype = none
gaintype = fixed
biastype = none
```

也就是：

```text
没有额外 activation dynamics
固定 gain
没有额外 bias
```

控制链可以理解为：

```text
data.ctrl
↓
fixed gain
↓
gear mapping
↓
joint force / torque
```

---

# Position Actuator

## 11. `position`

`position actuator` 控制目标 joint position。

例如：

```xml
<position
    joint="joint"
    name="pos"
    kp="2"
    kv="0.1"/>
```

如果：

```python
data.ctrl[0] = 1.0
```

并且控制的是 hinge joint，可以理解成：

```text
目标角度
=
1.0 rad
```

Joint 不会瞬间变成 1.0 rad。

Actuator 会根据位置误差产生力或力矩，让 joint 逐渐靠近目标。

---

## 12. Position Error

最核心的位置误差是：

```text
目标位置
-
实际位置
```

也就是近似：

```text
error
=
ctrl - qpos
```

Position actuator 会根据这个误差产生控制作用。

可以粗略理解成：

```text
force / torque
≈
kp × (target - position)
-
kv × velocity
```

---

## 13. `kp`

`kp` 是位置反馈增益。

可以理解为：

```text
位置误差越大
↓
控制作用越强
```

一般来说：

```text
kp 大
→ 拉向目标更强
→ 响应更快
→ 控制更“硬”
```

而：

```text
kp 小
→ 控制更柔
→ 收敛更慢
```

如果 `kp` 过大，可能出现：

```text
overshoot
oscillation
数值不稳定
```

---

## 14. Position Control 中的 `kv`

在 position actuator 中：

```text
kv
→ 速度相关阻尼
```

它主要用于抵抗过快运动，降低振荡。

可以记成：

```text
kp
→ 负责“把 joint 拉过去”

kv
→ 负责“别来回晃”
```

所以 position actuator 很像：

```text
弹簧
+
阻尼器
```

---

## 15. 为什么 `ctrl` 和 `qpos` 不一样

对于 position actuator：

```text
data.ctrl
→ 目标位置

qpos
→ 实际位置
```

完整过程是：

```text
ctrl target
↓
计算 position error
↓
actuator 产生 torque
↓
joint acceleration
↓
qvel 改变
↓
qpos 改变
```

因此：

```text
ctrl
≠
每一时刻的 qpos
```

这也解释了之前机械臂实验里 target 和 actual state 为什么不一定完全一样。

---

## 16. `timeconst`

Position actuator 可以通过 `timeconst` 增加内部平滑动态。

可以简单理解为：

```text
timeconst = 0
→ target 立即变化

timeconst > 0
→ target 更平滑地变化
```

比如外部命令：

```text
0 → 1
```

内部可能变成：

```text
0
→ 0.2
→ 0.5
→ 0.75
→ 0.9
→ 1
```

而不是瞬间跳变。

---

## 17. `inheritrange`

`inheritrange` 可以根据 joint range 自动生成 actuator 的 `ctrlrange`。

假设：

```text
joint range = [-2, 2]
```

如果：

```text
inheritrange = 1
```

那么：

```text
ctrlrange = [-2, 2]
```

如果：

```text
inheritrange = 0.5
```

则控制范围缩小：

```text
[-1, 1]
```

如果：

```text
inheritrange = 1.5
```

则控制范围扩大：

```text
[-3, 3]
```

所以：

```text
< 1
→ 更窄、更严格

= 1
→ 和 joint range 一样

> 1
→ 更宽
```

并且控制范围仍以原 joint range 的中点为中心。

---

# Velocity Actuator

## 18. `velocity`

`velocity actuator` 控制目标速度。

例如：

```xml
<velocity
    joint="joint1"
    kv="5"/>
```

如果 Python 中：

```python
data.ctrl[0] = 1.0
```

对于 hinge joint，可以理解成：

```text
目标角速度
=
1 rad/s
```

不是：

```text
目标角度 = 1 rad
```

---

## 19. Velocity Error

Velocity actuator 会比较：

```text
目标速度
和
实际速度
```

也就是近似：

```text
velocity error
=
ctrl - qvel
```

可以粗略理解为：

```text
force / torque
≈
kv × (target velocity - actual velocity)
```

所以 actuator 会不断加速或减速 joint，使：

```text
qvel
```

逐渐靠近目标速度。

---

## 20. Velocity Control 中的 `kv`

在 velocity actuator 中：

```text
kv
→ 速度误差反馈增益
```

一般：

```text
kv 大
→ 对速度误差反应更强

kv 小
→ 速度追踪更柔和
```

这和 position actuator 中 `kv` 主要作为阻尼项的角色略有不同。

---

# Integrated Velocity Actuator

## 21. `intvelocity`

`intvelocity` 输入看起来像速度命令，但不会直接把它当作速度目标。

而是：

```text
速度命令
↓
积分
↓
内部目标位置
↓
position-like servo
↓
joint 运动
```

这是它和普通 velocity actuator 最大的区别。

---

## 22. 积分目标示例

假设：

```text
ctrl = 0.5 rad/s
```

持续：

```text
2 s
```

那么内部目标位置大约变化：

```text
0.5 × 2
=
1.0 rad
```

所以内部 target 会随时间变化：

```text
0 s
→ 0 rad

1 s
→ 0.5 rad

2 s
→ 1.0 rad

3 s
→ 1.5 rad
```

然后 joint 去追这个不断移动的目标位置。

---

## 23. `dyntype="integrator"`

`intvelocity` 的核心内部机制就是积分。

可以理解为：

```text
内部目标变化率
=
ctrl
```

所以：

```text
ctrl > 0
→ 内部目标不断增加

ctrl = 0
→ 内部目标保持

ctrl < 0
→ 内部目标不断减小
```

因此它需要一个内部 activation state。

---

## 24. 为什么 `intvelocity` 需要 `actrange`

由于内部状态一直积分，如果不限制：

```text
ctrl = 1
```

持续很长时间，就可能让内部目标不断变大。

所以可以设置：

```xml
actrange="-2 2"
```

限制内部 activation / integrated target。

这样可以防止积分目标无限累积。

---

## 25. Velocity 与 Intvelocity 对比

可以这样记：

```text
velocity
→ 直接追踪目标速度

intvelocity
→ 先把速度命令积分成内部位置目标
→ 再追踪这个位置目标
```

一句话：

```text
velocity
→ “按这个速度运动”

intvelocity
→ “让内部目标位置按这个速度移动”
```

---

# Damper Actuator

## 26. `damper`

`damper actuator` 会产生与运动方向相反的阻力。

可以粗略写成：

```text
F
=
-kv × velocity × control
```

所以：

```text
速度越大
→ 阻力越大
```

负号表示：

> 阻力始终和运动方向相反。

---

## 27. Damper 示例

假设：

```text
velocity = +2
kv = 3
ctrl = 0.5
```

那么：

```text
F
=
-3 × 2 × 0.5
=
-3
```

阻力方向与正向运动相反。

如果：

```text
velocity = -2
```

则：

```text
F
=
-3 × (-2) × 0.5
=
+3
```

仍然是反向阻碍运动。

---

## 28. Damper 与 Joint Damping

Joint 自己可以有：

```xml
damping="..."
```

但两者区别是：

```text
joint damping
→ joint 自带的固定阻尼

damper actuator
→ 可以通过 ctrl 调节强弱的阻尼器
```

因此 damper actuator 可以理解成：

> 可控阻尼装置。

---

## 29. 强阻尼与 Integrator

强烈的速度相关阻尼可能让数值求解更困难。

因此一些 damper actuator 示例会使用：

```text
implicit
implicitfast
```

积分器。

当前阶段只需要记：

```text
强阻尼
→ implicit 系列积分器通常更稳定
```

---

# Cylinder Actuator

## 30. `cylinder`

`cylinder actuator` 用于模拟气缸或液压缸。

基本物理关系是：

```text
压力
×
活塞面积
↓
产生线性推力
```

所以常见参数包括：

```text
area
diameter
timeconst
bias
```

---

## 31. `area`

`area` 表示有效活塞面积。

一般：

```text
面积越大
↓
同样输入下产生的力越大
```

可以简单理解为：

```text
Force
≈
Pressure × Area
```

---

## 32. `diameter`

除了直接指定 `area`，也可以指定活塞直径。

然后根据：

```text
A = πd² / 4
```

得到面积。

所以：

```text
area
→ 直接指定面积

diameter
→ 指定直径，再换算面积
```

---

## 33. Cylinder 中的 `timeconst`

真实气缸和液压缸不会瞬间达到新输出。

`timeconst` 用来表示这种响应延迟。

可以理解为：

```text
timeconst 小
→ 响应更快

timeconst 大
→ 响应更慢
```

因此控制输入突然变化后，实际 actuator output 可以逐渐变化。

---

## 34. 同时使用多种 Actuator

同一个 `<actuator>` 容器里可以同时存在不同控制类型。

例如：

```xml
<actuator>
    <position
        joint="rfd"
        name="rfdp"
        kp="2"
        kv="0.1"/>

    <motor
        joint="rfa"
        name="rfav"/>
</actuator>
```

表示：

```text
joint rfd
→ 使用 position actuator

joint rfa
→ 使用 motor actuator
```

所以同一个机器人不同 joint 可以使用不同控制策略。

---

# 示例 - 双关节机构

## 35. 机构结构

Actuator 示例中使用了一个简单机构：

```text
world
└── support
    └── rotay_am
        ├── pivot joint
        ├── horizontal arm
        └── pendulum
            ├── ph joint
            ├── pendulum rod
            └── end mass
```

两个可运动 joint 是：

```text
pivot
→ 绕 z 轴的 hinge

ph
→ 绕 x 轴的 hinge
```

---

## 36. Pivot 的 Position Actuator

第一个 actuator：

```xml
<position
    kp="2"
    kv="0.1"
    name="pivot"
    joint="pivot"
    ctrlrange="-3.14 3.14"
    forcerange="-5 5"/>
```

控制：

```text
joint="pivot"
```

因此：

```text
data.ctrl
→ pivot 的目标角度
```

其中：

```text
kp
→ position feedback

kv
→ velocity damping
```

输入目标范围：

```text
[-3.14, 3.14] rad
```

最终输出力矩限制：

```text
[-5, 5]
```

---

## 37. Pivot 控制链

完整过程：

```text
目标 pivot angle
↓
data.ctrl
↓
position actuator
↓
position error
↓
control torque
↓
pivot hinge
↓
horizontal arm 旋转
```

---

## 38. Pendulum 的 Intvelocity Actuator

第二个 actuator：

```xml
<intvelocity
    name="ph"
    joint="ph"
    kp="100"
    kv="2"
    actrange="-2 2"/>
```

控制：

```text
joint="ph"
```

其输入是一个 velocity-like command。

核心过程：

```text
ctrl velocity command
↓
integrator
↓
internal target position
↓
position-like control
↓
ph joint
↓
pendulum 运动
```

内部 activation state 被：

```text
actrange="-2 2"
```

限制，防止无限积分。

---

## 39. 一个模型使用两种不同控制方式

这个例子同时演示了：

```text
pivot
→ position actuator
→ 直接给目标角度

ph
→ intvelocity actuator
→ 速度命令先积分成内部位置目标
```

说明：

```text
同一个机械系统
可以对不同 joint
使用不同 actuator 类型
```

---

## 40. 核心对比

目前学到的 actuator 可以总结为：

```text
motor
→ “给这么大的力 / 力矩”

position
→ “去这个位置”

velocity
→ “保持这个速度”

intvelocity
→ “让内部目标位置按这个速度移动”

damper
→ “用可控阻尼抵抗运动”

cylinder
→ “模拟气缸 / 液压缸线性驱动”
```

---

## 41. 核心理解

最重要的控制链：

```text
Python
↓
data.ctrl
↓
actuator
↓
joint / tendon / site
↓
物理运动
```

但是：

> `data.ctrl` 的物理意义并不是固定不变的。

它取决于 actuator 类型。

例如：

```text
motor
→ 力 / 力矩命令

position
→ 位置目标

velocity
→ 速度目标

intvelocity
→ 被积分的速度命令
```

---

## 42. 当前阶段需要记住什么

最重要的 actuator 类型：

```text
motor
→ 直接 force / torque control

position
→ target position control

velocity
→ target velocity control

intvelocity
→ integrated velocity command

damper
→ controllable damping

cylinder
→ pneumatic / hydraulic actuator model
```

重要限制参数：

```text
ctrlrange
→ 控制输入范围

forcerange
→ 最终 actuator force / torque 范围

actrange
→ actuator 内部 activation state 范围
```

Position servo 中最重要的参数：

```text
kp
→ 位置反馈强度

kv
→ 速度阻尼
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