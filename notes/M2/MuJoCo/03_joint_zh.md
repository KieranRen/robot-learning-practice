# 03 - Joint 关节

[English](03_joint.md) | [中文](03_joint_zh.md)

---

## 概览

本笔记记录 MuJoCo 中与关节和刚体运动相关的基础概念。

本节内容包括：

- Joint 的作用
- Joint 类型
- `pos`
- `axis`
- `range`
- `limited`
- `damping`
- `stiffness`
- `frictionloss`
- `armature`
- `ref`
- `body`、`joint` 与 `geom` 之间的关系

---

## 1. Joint 是什么？

在 MuJoCo 中，`body` 表示一个刚体。

`joint` 决定这个 body 相对于父 body 可以如何运动。

可以这样理解：

```text
父 body
↓
joint
↓
当前 body
↓
geom / site / 子 body
```

如果一个子 body 没有 joint，那么它相对于父 body 默认是固定的。

所以：

```text
body
→ 刚体

joint
→ 定义允许的运动方式

geom
→ 定义实际几何形状
```

---

## 2. Joint 属于当前 Body

例如：

```xml
<body name="arm" pos="0 0 1">

    <joint name="shoulder"
           type="hinge"
           axis="0 1 0"/>

    <geom type="capsule"
          size="0.1 0.5"/>

</body>
```

这里的 joint 写在 `arm` body 内部。

这表示：

```text
arm
→ 相对于自己的父 body 运动
→ 运动方式由 shoulder joint 决定
```

Joint 不是一个单独放在两个 body 中间的独立物体。

更准确地说，它定义的是：

```text
当前 body 相对于父 body 的自由度
```

---

## 3. Joint 类型

MuJoCo 中常见的 joint 类型包括：

- `free`
- `ball`
- `slide`
- `hinge`

---

### `hinge`

Hinge joint 是旋转关节。

例如：

```xml
<joint type="hinge"
       axis="0 0 1"/>
```

表示：

```text
绕 z 轴旋转
```

典型应用包括：

- 机械臂旋转关节
- 车轮
- 门铰链
- 单摆

Hinge joint 有：

```text
1 个旋转自由度
```

---

### `slide`

Slide joint 是直线滑动关节。

例如：

```xml
<joint type="slide"
       axis="1 0 0"/>
```

表示：

```text
沿 x 轴方向平移
```

典型应用包括：

- 直线导轨
- 活塞
- 升降机构

Slide joint 有：

```text
1 个平移自由度
```

---

### `ball`

Ball joint 是球关节。

它允许在三维空间中进行旋转。

可以类比人体肩关节。

它具有：

```text
3 个旋转自由度
```

但不允许自由平移。

---

### `free`

Free joint 允许一个 body 在三维空间中完全自由运动。

它包括：

```text
3 个平移自由度
+
3 个旋转自由度
=
6 个自由度
```

例如：

```xml
<freejoint/>
```

适合用于：

- 自由下落物体
- 空间中自由运动的刚体
- 没有机械连接到世界的物体

---

## 4. Joint Position

`pos` 用来定义 joint 在当前 body 局部坐标系中的位置。

例如：

```xml
<joint type="hinge"
       pos="0 0 0.5"/>
```

对于 hinge joint：

```text
pos
→ 决定旋转轴经过哪里
```

旋转关节不仅需要知道：

```text
绕哪个方向转
```

还需要知道：

```text
转轴经过哪个位置
```

因此：

```text
pos
→ 决定轴的位置

axis
→ 决定轴的方向
```

---

## 5. Joint Axis

`axis` 用来定义关节的运动轴方向。

例如：

```text
axis="1 0 0"
→ x 轴

axis="0 1 0"
→ y 轴

axis="0 0 1"
→ z 轴
```

对于 hinge joint：

```text
axis
→ 旋转轴方向
```

对于 slide joint：

```text
axis
→ 平移方向
```

例如：

```xml
<joint type="hinge"
       axis="0 1 0"/>
```

表示：

```text
绕 y 轴旋转
```

而：

```xml
<joint type="slide"
       axis="0 0 1"/>
```

表示：

```text
沿 z 轴移动
```

---

## 6. Range

`range` 用来限制 joint 的运动范围。

例如：

```xml
<joint type="hinge"
       range="-90 90"/>
```

如果模型使用：

```xml
<compiler angle="degree"/>
```

那么表示：

```text
最小角度 = -90°
最大角度 = +90°
```

对于 slide joint：

```xml
<joint type="slide"
       range="0 0.5"/>
```

表示：

```text
只能在 0 m 到 0.5 m 之间移动
```

---

## 7. Limited

`limited` 用来控制是否启用 joint 的范围限制。

例如：

```xml
limited="true"
```

表示：

```text
启用 range 限制
```

而：

```xml
limited="false"
```

表示：

```text
不使用 range 限制
```

如果模型中使用：

```xml
<compiler autolimits="true"/>
```

那么当定义了 `range` 时，MuJoCo 通常可以自动判断这个 joint 需要限制。

---

## 8. Damping

`damping` 表示关节运动时的粘性阻尼。

例如：

```xml
damping="0.05"
```

可以简单理解为：

```text
运动速度越大
→ 阻尼阻力越大
```

对于平移运动，可以近似理解为：

```text
F_d = -c v
```

对于旋转运动：

```text
τ_d = -c ω
```

所以：

```text
damping 较大
→ 振动更快衰减

damping 较小
→ 运动持续更久
```

阻尼可以帮助抑制不现实的持续振荡。

---

## 9. Stiffness

`stiffness` 表示类似弹簧的恢复作用。

例如：

```xml
stiffness="10"
```

可以理解为：

```text
joint 会倾向于回到参考位置
```

类似弹簧。

对于平移：

```text
F = -k x
```

对于旋转：

```text
τ = -k(θ - θ_ref)
```

所以：

```text
stiffness 越大
→ 恢复作用越强
```

---

## 10. Friction Loss

`frictionloss` 表示 joint 内部的摩擦损失。

例如：

```xml
frictionloss="0.1"
```

它和 geom 的接触摩擦不是一回事。

可以这样区分：

```text
geom friction
→ 两个接触表面之间的摩擦

joint frictionloss
→ joint 自身内部的运动阻力
```

例如真实机器人关节中可能存在：

- 轴承摩擦
- 齿轮摩擦
- 机械接触摩擦

这些都可以通过 `frictionloss` 近似描述。

---

## 11. Armature

`armature` 表示 joint 处额外的等效惯量。

例如：

```xml
armature="0.01"
```

可以简单理解为：

```text
armature
→ joint 看到的额外惯量
```

它可以用来表示：

- 电机转子的转动惯量
- 减速器折算到关节侧的惯量

目前最重要的理解是：

```text
armature 越大
→ joint 表现得越“重”
→ 加速和减速更困难
```

---

## 12. Reference Position

`ref` 用来定义 joint 的参考位置。

例如：

```xml
ref="30"
```

如果 hinge joint 使用 degree：

```text
ref = 30°
```

这个参考值之后会用于：

- 初始姿态
- 关节弹簧
- 参考配置

---

## 13. Body、Joint 与 Geom 的关系

三个核心元素之间的关系可以总结为：

```text
body
→ 刚体 + 局部坐标系

joint
→ 定义 body 相对于父 body 如何运动

geom
→ 定义 body 的实际几何形状
```

例如：

```xml
<body name="pendulum" pos="0 0 2">

    <joint name="pivot"
           type="hinge"
           axis="0 1 0"/>

    <geom type="capsule"
          fromto="0 0 0  0 0 -1"
          size="0.08"/>

</body>
```

可以理解为：

```text
pendulum
→ 一个刚体

pivot
→ 允许 pendulum 绕 y 轴旋转

capsule
→ 定义 pendulum 的杆状几何外形
```

---

## 14. 简单单摆示例

单摆是理解 hinge joint 很好的例子。

```xml
<mujoco model="Simple Pendulum">

    <compiler angle="degree" autolimits="true"/>

    <option timestep="0.002"
            gravity="0 0 -9.81"/>

    <worldbody>

        <geom type="plane"
              size="5 5 0.1"
              rgba="0.8 0.8 0.8 1"/>

        <body name="pendulum"
              pos="0 0 2"
              euler="0 45 0">

            <joint name="pivot"
                   type="hinge"
                   pos="0 0 0"
                   axis="0 1 0"
                   range="-90 90"
                   damping="0.05"/>

            <geom type="capsule"
                  fromto="0 0 0  0 0 -1"
                  size="0.08"
                  mass="1"
                  rgba="0.8 0.2 0.2 1"/>

        </body>

    </worldbody>

</mujoco>
```

其中：

```text
type="hinge"
→ 单摆只能绕一个轴旋转
```

```text
axis="0 1 0"
→ 绕 y 轴旋转
```

```text
range="-90 90"
→ 最大运动范围为 ±90°
```

```text
damping="0.05"
→ 摆动会逐渐衰减
```

```text
euler="0 45 0"
→ 给单摆一个初始 45° 偏角
```

---

## 15. 为什么单摆需要初始偏角？

如果单摆一开始完全竖直向下：

```text
joint
  ●
  |
  |
  ● 质心
  ↓ 重力
```

重力作用线几乎正好穿过 joint。

因此：

```text
力臂 ≈ 0
→ 力矩 ≈ 0
→ 单摆不会主动开始旋转
```

如果单摆一开始倾斜：

```text
joint
  ●
   \
    \
     ● 质心
     ↓ 重力
```

重力就会对 joint 产生力矩。

基本关系为：

```text
τ = r × F
```

所以单摆会开始旋转。

这个现象说明：

```text
有重力
≠
一定会产生旋转
```

真正决定旋转的是：

```text
相对于 joint 是否产生了力矩
```

---

## 核心理解

Joint 最重要的参数可以总结为：

```text
type
→ 允许什么类型的运动

pos
→ joint 在哪里

axis
→ 沿哪个方向移动 / 绕哪个方向旋转

range
→ 最大运动范围

damping
→ 与运动速度相关的阻尼

stiffness
→ 向参考位置恢复的作用

frictionloss
→ joint 内部摩擦

armature
→ joint 处额外等效惯量

ref
→ joint 的参考位置
```

最核心的层级关系是：

```text
父 body
↓
joint
↓
当前 body
↓
geom / site / 子 body
```

---

## 来源

本学习部分基于以下上游仓库：

https://github.com/Albusgive/mujoco_learning.git

原始仓库及教学材料归对应作者所有。

本文件内容为我在学习过程中的个人整理、解释、总结与理解，并不是对上游仓库内容的直接复制。