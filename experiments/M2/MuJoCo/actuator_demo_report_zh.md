# Actuator 执行器示例实验

[English](actuator_demo_report.md) | [中文](actuator_demo_report_zh.md)

---

## 1. 实验目的

本实验用于巩固 Albusgive MuJoCo 学习来源中关于 actuator 的相关内容。

主要目标包括：

- 理解 actuator 如何连接到 joint
- 理解不同 actuator 类型如何解释 `data.ctrl`
- 区分 `position` 与 `intvelocity`
- 理解 `ctrlrange`
- 理解 `forcerange`
- 理解 `actrange`
- 理解 actuator control 与 joint motion 之间的关系

本实验最核心的问题是：

> 当 actuator 类型不同时，`data.ctrl` 的含义是如何变化的？

---

## 2. 模型文件

实验模型保存在：

```text
experiments/M2/MuJoCo/actuator_demo.xml
```

模型中有两个可运动 joint：

```text
pivot
ph
```

并分别使用两种不同 actuator：

```text
pivot
→ position actuator

ph
→ intvelocity actuator
```

---

# 机械结构

## 3. Body 层级结构

模型结构为：

```text
world
└── support
    └── rotary_arm
        ├── pivot joint
        ├── horizontal arm
        └── pendulum
            ├── ph joint
            ├── pendulum rod
            └── pendulum mass
```

这个层级结构很重要，因为：

```text
support
→ 固定底座

rotary_arm
→ support 的子 body

pendulum
→ rotary_arm 的子 body
```

因此父 body 发生运动时，子 body 的整体位置和姿态也会受到影响。

---

## 4. Fixed Support

支撑结构：

```xml
<body name="support" pos="0 0 0.1">
```

内部包含一个 cylinder geom。

`support` 本身没有 joint，因此：

```text
support
→ 相对于 world 固定
```

它相当于整个机构的底座。

---

## 5. Rotary Arm

`support` 内部包含：

```xml
<body name="rotary_arm" pos="0 0 0.51">
```

这个 body 中有：

```xml
<joint
    name="pivot"
    type="hinge"
    axis="0 0 1"/>
```

因此：

```text
pivot
→ hinge joint
→ 绕 z 轴旋转
```

水平杆属于 `rotary_arm`。

所以：

```text
pivot 转动
→ horizontal arm 绕 z 轴转动
```

---

## 6. Pendulum

水平杆末端有：

```xml
<body name="pendulum" pos="0.2 0 0">
```

这个 body 中包含：

```xml
<joint
    name="ph"
    type="hinge"
    axis="1 0 0"/>
```

因此：

```text
ph
→ hinge joint
→ 绕 x 轴旋转
```

pendulum rod 和末端质量都属于这个 body。

所以：

```text
ph 转动
→ pendulum 绕 x 轴摆动
```

---

# Actuator 结构

## 7. Actuator 容器

模型使用：

```xml
<actuator>
    ...
</actuator>
```

在这个容器中定义两个 actuator。

最重要的关系是：

```text
actuator
→ 引用某个 joint
→ 驱动这个 joint
```

---

# Position Actuator

## 8. Pivot 的 Position Actuator

第一个 actuator：

```xml
<position
    name="pivot_position"
    joint="pivot"
    kp="2"
    kv="0.1"
    ctrllimited="true"
    ctrlrange="-3.14 3.14"
    forcelimited="true"
    forcerange="-5 5"/>
```

它控制：

```text
joint="pivot"
```

因此它负责控制水平杆的旋转位置。

---

## 9. `data.ctrl` 的含义

对于 position actuator：

```text
data.ctrl
→ target position
```

对于这个 hinge joint：

```text
data.ctrl
→ target angle
```

例如：

```python
data.ctrl[0] = 1.0
```

可以理解为：

```text
pivot 目标角度
=
1.0 rad
```

但这并不代表 joint 会瞬间变成 1 rad。

---

## 10. Position Control 的过程

Actuator 会比较：

```text
target position
和
actual position
```

可以近似写成：

```text
position error
=
ctrl - qpos
```

然后 actuator 根据误差产生 torque。

可以粗略理解成：

```text
torque
≈
kp × (target - position)
-
kv × velocity
```

完整过程：

```text
data.ctrl
↓
target angle
↓
position error
↓
actuator torque
↓
pivot joint 加速
↓
qvel 改变
↓
qpos 改变
```

---

## 11. `kp`

参数：

```xml
kp="2"
```

控制 position feedback 的强度。

可以理解为：

```text
位置误差越大
→ 修正 torque 越大
```

通常：

```text
kp 更大
→ 反应更强
→ 更快拉向目标
→ 控制更“硬”
```

---

## 12. `kv`

参数：

```xml
kv="0.1"
```

提供速度相关阻尼。

它主要帮助减少：

```text
overshoot
oscillation
过快运动
```

可以这样记：

```text
kp
→ 把 joint 拉向目标

kv
→ 防止 joint 晃得太厉害
```

---

# 控制输入限制

## 13. `ctrlrange`

这个 actuator 使用：

```xml
ctrllimited="true"
ctrlrange="-3.14 3.14"
```

表示允许的 control input 被限制为：

```text
[-3.14, 3.14]
```

由于这里是 position-controlled hinge：

```text
ctrlrange
→ 允许的目标角度范围
```

大约就是：

```text
-π 到 +π rad
```

---

## 14. `ctrlrange` 与 Joint Range

`ctrlrange` 并不是：

```text
joint 的物理运动范围
```

它表示：

```text
actuator 允许接收的输入范围
```

区别是：

```text
joint range
→ joint 物理上能运动到哪里

ctrlrange
→ actuator 的 target command 能给到哪里
```

这两个参数可能有关，但不是同一个概念。

---

# 输出力 / 力矩限制

## 15. `forcerange`

Actuator 还使用：

```xml
forcelimited="true"
forcerange="-5 5"
```

它限制 actuator 最终输出。

由于这里控制的是 hinge joint，所以主要可以理解为：

```text
torque limit
```

因此：

```text
forcerange = [-5, 5]
```

表示 actuator 输出不能超过大约：

```text
+5 N·m
```

也不能低于：

```text
-5 N·m
```

---

## 16. Force Limiting 示例

假设 position controller 算出：

```text
required torque = +8
```

但是：

```text
forcerange = [-5, 5]
```

那么最终输出只能是：

```text
+5
```

同理：

```text
calculated torque = -7
```

最终会被限制为：

```text
-5
```

所以：

```text
forcerange
→ actuator output saturation
```

---

## 17. 为什么需要 `forcerange`

如果没有输出限制：

```text
大位置误差
+
大 kp
```

可能导致非常大的 torque。

使用：

```text
forcerange
```

可以让 actuator 更接近真实硬件。

例如：

```text
真实电机
机器人关节
有限扭矩执行器
```

都不可能输出无限大的 torque。

---

# Intvelocity Actuator

## 18. Pendulum 的 Intvelocity Actuator

第二个 actuator：

```xml
<intvelocity
    name="ph_intvelocity"
    joint="ph"
    kp="100"
    kv="2"
    actlimited="true"
    actrange="-2 2"/>
```

它控制：

```text
joint="ph"
```

也就是 pendulum 的 hinge joint。

---

## 19. `data.ctrl` 在 Intvelocity 中的含义

对于 `intvelocity`：

```text
data.ctrl
```

不是直接表示 target position。

同时它也不是普通 velocity actuator 那样直接表示：

```text
target velocity
```

而是：

```text
ctrl
→ velocity-like command
↓
integration
↓
internal target position
↓
position-like control
```

---

## 20. Integrated Target

假设：

```text
ctrl = 0.5 rad/s
```

并持续：

```text
2 s
```

那么内部 target position 大约变化：

```text
0.5 × 2
=
1.0 rad
```

内部 target 大约变成：

```text
0 s
→ 0 rad

1 s
→ 0.5 rad

2 s
→ 1.0 rad
```

所以 intvelocity 实际上是在：

> 按指定速度移动一个内部 position target。

---

## 21. 为什么叫 `intvelocity`

这个名字可以理解成：

```text
integrated velocity
```

因为 velocity-like command 会随时间积分。

基本关系：

```text
position change
=
velocity × time
```

所以：

```text
velocity-like input
↓
integration
↓
position target
```

---

# Activation Limit

## 22. `actrange`

Intvelocity actuator 使用：

```xml
actlimited="true"
actrange="-2 2"
```

这个参数限制它的内部 activation state。

对于 intvelocity 来说，这个内部状态和：

```text
integrated target position
```

密切相关。

---

## 23. 为什么需要 `actrange`

假设：

```text
ctrl = 1
```

持续很长时间。

内部 target 会不断增加：

```text
1 s
→ +1

2 s
→ +2

3 s
→ +3

4 s
→ +4
```

一直继续。

这通常不是我们希望看到的。

所以：

```text
actrange="-2 2"
```

可以防止内部积分状态无限增大。

内部状态会被限制在大约：

```text
[-2, 2]
```

---

## 24. `ctrlrange`、`forcerange` 与 `actrange`

这三个 range 限制的是完全不同的东西：

```text
ctrlrange
→ actuator 输入命令

forcerange
→ actuator 最终输出 force / torque

actrange
→ actuator 内部 activation state
```

这一点非常重要。

它们分别作用在 actuator 的不同阶段。

---

# Position 与 Intvelocity 对比

## 25. Position Actuator

Position actuator 接收：

```text
desired position
```

例如：

```text
ctrl = 1.0
```

表示：

```text
去 1.0 rad
```

---

## 26. Intvelocity Actuator

Intvelocity 接收：

```text
velocity-like command
```

例如：

```text
ctrl = 0.5
```

大约表示：

```text
让内部 target position 以 0.5 rad/s 的速度移动
```

然后 joint 再去追踪这个内部位置目标。

---

## 27. 核心区别

最简单的记法：

```text
position
→ “去这个位置”

intvelocity
→ “让内部位置目标按这个速度移动”
```

这是本实验最重要的概念之一。

---

# 与普通 Velocity Actuator 的关系

## 28. Velocity Actuator

普通 velocity actuator 可以理解成：

```text
ctrl
→ target velocity

qvel
→ actual velocity
```

然后 controller 去减小：

```text
ctrl - qvel
```

---

## 29. Velocity 与 Intvelocity

区别是：

```text
velocity
→ 直接追踪速度

intvelocity
→ 先对 velocity command 积分
→ 再追踪内部 position target
```

所以：

```text
velocity
→ speed control

intvelocity
→ moving-position-target control
```

---

# 与 Python Control 的关系

## 30. Control Array

MuJoCo 中通常通过：

```python
data.ctrl
```

给 actuator 输入命令。

本模型有两个 actuator：

```text
data.ctrl[0]
→ pivot_position

data.ctrl[1]
→ ph_intvelocity
```

具体顺序取决于 actuator 在 XML 中声明的顺序。

---

## 31. 示例理解

例如：

```python
data.ctrl[0] = 1.0
data.ctrl[1] = 0.5
```

可以理解成：

```text
pivot_position
→ 让 pivot 向 1.0 rad 运动

ph_intvelocity
→ 让 ph 的内部 target
   以约 0.5 rad/s 的速度移动
```

所以：

> 同一个 `data.ctrl` 数组里的不同元素，可以具有不同的物理意义。

---

## 32. 关于 `data.ctrl` 的重要理解

这个实验强化了一个非常重要的概念：

> `data.ctrl` 本身没有一个固定不变的物理意义。

它的含义取决于 actuator 类型。

例如：

```text
motor
→ force / torque-like command

position
→ position target

velocity
→ velocity target

intvelocity
→ integrated velocity command
```

因此在阅读或编写 MuJoCo 控制代码时：

```text
先看 actuator 类型
再解释 ctrl
```

非常重要。

---

# 机械系统的真实响应

## 33. 为什么 `ctrl` 和实际运动不是一回事

即使使用 position actuator：

```text
ctrl = 1 rad
```

也不代表：

```text
qpos 立即变成 1 rad
```

Actuator 仍然需要：

```text
产生 torque
↓
让 joint 加速
↓
改变 qvel
↓
最终改变 qpos
```

实际运动还受到：

- inertia
- gravity
- damping
- friction
- actuator gain
- force limit
- timestep

等因素影响。

所以 MuJoCo 始终是在做：

```text
physics simulation
```

而不是直接把 joint position 强行改成目标值。

---

## 34. Target 与 Actual State

核心关系：

```text
target
↓
controller
↓
force / torque
↓
physics
↓
actual state
```

所以：

```text
target state
≠
每一时刻的 actual state
```

这和之前 Robot Knowledge Study 的机械臂控制实验中观察到的现象是一致的。

---

# Model Independence

## 35. 移除外部依赖

原始学习例子中包含一些外部或当前实验不需要的 asset 相关设置。

如果对应文件缺失，可能导致：

```text
MuJoCo Viewer
```

无法加载模型。

因此本实验中：

```text
external skybox dependency
→ 删除

unused mesh-related default
→ 删除
```

Floor 改成使用：

```xml
builtin="checker"
```

的内置纹理。

这样模型更加独立。

---

## 36. 为什么简化模型更适合学习

本实验只保留 actuator 学习真正需要的部分：

```text
body hierarchy
joint
geom
position actuator
intvelocity actuator
actuator limits
```

把无关结构删掉之后：

```text
actuator
→ joint
→ body motion
```

之间的关系更容易观察和理解。

---

# 实验结果

## 37. 最重要的学习结果

本实验最重要的结论是：

> Actuator 类型决定 control input 应该如何解释。

对于两个 joint：

```text
pivot
→ position actuator
→ ctrl = target angle

ph
→ intvelocity actuator
→ ctrl = velocity-like input
→ 被积分成 target position
```

因此：

```text
同一个 data.ctrl 数组
```

内部不同元素可以代表不同物理量。

---

## 38. Range 参数总结

本实验也进一步巩固了：

```text
ctrlrange
→ 限制 command input

forcerange
→ 限制 actuator output

actrange
→ 限制 actuator internal state
```

这三个参数不能混淆。

---

## 39. Actuator Control Chain

整体控制链：

```text
Python
↓
data.ctrl
↓
actuator
↓
joint
↓
force / torque
↓
body motion
↓
qpos / qvel
```

其中 actuator 内部具体发生什么：

```text
取决于 actuator type
```

---

## 40. 我学到的内容

这个实验最重要的思维模型是：

```text
joint
→ 决定“怎么能动”

actuator
→ 决定“怎么驱动它动”
```

不同 actuator：

```text
motor
→ “用这么大的力 / 力矩推”

position
→ “去这个位置”

velocity
→ “按这个速度运动”

intvelocity
→ “让内部目标位置按这个速度移动”
```

对于限制参数：

```text
ctrlrange
→ 输入限制

forcerange
→ 输出限制

actrange
→ 内部状态限制
```

这些概念为后续更复杂的机器人控制实验打下了基础。

---

## 来源

本实验基于：

```text
Albusgive/mujoco_learning
```

来源仓库：

https://github.com/Albusgive/mujoco_learning

模型在学习过程中进行了简化和重新整理，使其更加专注于 actuator 行为以及 actuator limit。

本报告记录的是我对相关示例的个人理解、代码分析与学习总结，而不是对原始材料的直接复制。