# 单摆实验

[English](pendulum_report.md) | [中文](pendulum_report_zh.md)

---

## 概览

这个实验使用 MuJoCo 中的 hinge joint 构建了一个简单单摆。

主要目的是把 M2 中学习到的 joint 概念和实际仿真联系起来。

本实验重点包括：

- `body`
- `joint`
- `geom`
- `hinge`
- `axis`
- `range`
- `damping`
- 重力
- 初始姿态
- 重力产生的力矩

仿真文件为：

```text
pendulum.xml
```

---

## 1. 实验结构

模型中包括：

- 一个地面平面
- 一个 pendulum body
- 一个 hinge joint
- 一个表示摆杆的 capsule geom

简化后的层级结构为：

```text
worldbody
├── ground
└── pendulum body
    ├── hinge joint
    └── capsule geom
```

---

## 2. Pendulum Body

单摆 body 定义为：

```xml
<body name="pendulum"
      pos="0 0 2"
      euler="0 45 0">
```

其中：

```text
pos="0 0 2"
```

表示这个 body 的局部坐标系原点位于世界坐标：

```text
x = 0
y = 0
z = 2
```

而：

```text
euler="0 45 0"
```

表示给单摆一个 45° 的初始倾斜角。

这个初始倾斜非常重要，因为它使重力能够对 joint 产生力矩。

---

## 3. Hinge Joint

Joint 定义为：

```xml
<joint name="pivot"
       type="hinge"
       pos="0 0 0"
       axis="0 1 0"
       range="-90 90"
       damping="0.05"/>
```

主要参数可以这样理解：

```text
type="hinge"
→ 只允许绕一个轴旋转
```

```text
pos="0 0 0"
→ joint 位于 pendulum body 的局部原点
```

```text
axis="0 1 0"
→ 绕 y 轴旋转
```

```text
range="-90 90"
→ 旋转范围限制为 ±90°
```

```text
damping="0.05"
→ 摆动会逐渐衰减
```

---

## 4. Pendulum Geometry

单摆的杆使用 capsule 表示：

```xml
<geom type="capsule"
      fromto="0 0 0  0 0 -1"
      size="0.08"
      mass="1"
      rgba="0.8 0.2 0.2 1"/>
```

`fromto` 定义了摆杆的两个端点：

```text
点 A = (0, 0, 0)
点 B = (0, 0, -1)
```

因此摆杆从 joint 所在位置向下延伸。

Capsule 的半径为：

```text
0.08 m
```

质量为：

```text
1 kg
```

---

## 5. 为什么单摆会运动

重力沿 z 轴负方向作用：

```xml
gravity="0 0 -9.81"
```

当单摆处于倾斜状态时，它的质心不在 hinge joint 的正下方。

因此重力会对 joint 产生力矩。

基本关系为：

```text
τ = r × F
```

其中：

```text
τ
→ 力矩

r
→ 从 joint 指向质心的位置向量

F
→ 重力
```

因为重力作用线没有直接穿过 joint，所以会产生转矩。

这个转矩会使单摆开始旋转。

---

## 6. 为什么一开始竖直时不会动

当单摆一开始完全竖直向下：

```text
joint
  ●
  |
  |
  ● 质心
  ↓ 重力
```

重力作用线几乎直接通过 joint。

因此：

```text
力臂 ≈ 0
```

所以：

```text
力矩 ≈ 0
```

单摆就会保持静止。

这个现象说明了一个重要的力学概念：

```text
有重力
并不意味着
一定会发生旋转
```

真正决定是否旋转的是：

```text
相对于 joint 是否存在力矩
```

---

## 7. Damping 的作用

Joint 中设置了：

```xml
damping="0.05"
```

Damping 表示对 joint 运动的阻尼。

可以简单理解为：

```text
角速度越大
→ 阻尼阻力越大
```

旋转阻尼可以近似理解为：

```text
τ_d = -cω
```

其中：

```text
c
→ 阻尼系数

ω
→ 角速度
```

因此单摆的运动过程大致是：

```text
开始摆动
↓
不断损失能量
↓
摆动幅度逐渐减小
```

如果没有 damping，理想情况下单摆会持续摆动更长时间。

---

## 8. Joint Range

实验使用：

```xml
range="-90 90"
```

同时：

```xml
<compiler angle="degree" autolimits="true"/>
```

所以 hinge joint 的运动范围为：

```text
-90° ≤ angle ≤ 90°
```

这样可以防止单摆无限制地绕一整圈旋转。

---

## 9. 本实验复习的概念

本实验复习了：

```text
body
→ 刚体和局部坐标系

joint
→ 定义 body 可以如何运动

geom
→ 定义实际几何形状
```

同时复习了 joint 的主要参数：

```text
type
pos
axis
range
damping
```

并将这些参数和下面的物理概念联系起来：

```text
gravity
initial orientation
center of mass
torque
oscillation
```

---

## 10. 运行实验

首先激活 MuJoCo 环境：

```bash
conda activate mujoco_env
```

进入保存 `pendulum.xml` 的文件夹。

然后运行：

```bash
python -m mujoco.viewer --mjcf pendulum.xml
```

Viewer 打开后开始仿真。

单摆应该会：

```text
从倾斜位置开始
↓
受到重力作用加速
↓
经过最低点
↓
摆向另一侧
↓
由于 damping 的存在，摆幅逐渐减小
```

---

## 核心理解

这个实验最重要的关系是：

```text
joint
→ 定义允许的运动

gravity
→ 产生力

力的作用线与 joint 存在偏移
→ 产生力矩

力矩
→ 产生旋转运动
```

Hinge joint 只有一个旋转自由度，所以单摆只能围绕指定轴进行旋转。

这个实验把下面三部分连接起来：

```text
MuJoCo joint 配置
+
刚体力学
+
物理仿真
```

---

## 来源

本实验基于以下上游仓库中学习到的 joint 相关内容：

https://github.com/Albusgive/mujoco_learning.git

原始仓库及教学材料归对应作者所有。

本实验文件与报告内容为我在学习过程中的个人实践、整理与理解，并不是对上游仓库内容的直接复制。