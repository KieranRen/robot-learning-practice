# SIM-T02 实验报告 - 机械臂关节角目标控制

[English](sim_t02_arm_joint_targets_report.md) | [中文](sim_t02_arm_joint_targets_report_zh.md)

---

## 实验目标

这个实验复现 `Robot_knowledge_study` M2 中的第二个 MuJoCo 仿真场景。

主要目的是验证我是否能够：

- 加载多刚体机器人模型
- 理解父 body / 子 body 的层级结构
- 理解机器人 joint 的定义
- 使用 position actuator
- 从 Python 写入目标关节角
- 使用 `mj_step` 推进仿真
- 读取实际关节角和关节速度
- 读取机械臂末端位置和姿态
- 比较目标关节角与实际关节状态
- 使用 MuJoCo Viewer 观察受控运动

---

## 场景组合

T02 场景由：

```text
SIM-T01 的桌子与方块场景
+
robot.xml
```

组合而成。

T02 的 `scene.xml` 中包含：

```xml
<include file="../sim_t01_table_cube/scene.xml"/>
<include file="robot.xml"/>
```

因此完整场景包含：

- 地面
- 桌子
- 方块
- 灯光
- 相机
- 机器人主体
- 左机械臂
- 右机械臂
- actuator
- sensor
- collision 设置

本场景 timestep 为：

```text
0.001 s
```

---

## 机器人结构

机器人采用层级式 body 结构。

简化后可以理解为：

```text
openarm_body
├── 机器人主体 / 底座
├── 左机械臂
│   ├── link0
│   ├── link1
│   ├── link2
│   ├── ...
│   ├── link7
│   └── gripper
└── 右机械臂
    ├── link0
    ├── link1
    ├── ...
    ├── link7
    └── gripper
```

这种层级结构和串联机械臂的真实结构一致。

子 body 会跟随父 body 一起运动，同时如果定义了 joint，还可以产生相对于父 body 的额外运动。

---

## Default 参数模板

模型使用 `<default>` 定义可复用的参数模板。

这些模板主要用于：

- joint damping
- frictionloss
- armature
- collision 参数
- visual 参数
- actuator gain
- actuator limit

这样可以减少大量重复的 XML 代码。

核心关系是：

```text
default
→ 可复用参数模板

class
→ 选择使用哪套模板

joint / geom / actuator
→ 真正使用模板的对象
```

---

## Mesh Asset

`<asset>` 用于定义可重复使用的 mesh 资源。

例如：

```xml
<mesh name="body.obj"
      file="visual/body/openarm_body.obj"/>
```

这里只是把 mesh 文件登记进 MuJoCo。

真正让它出现在机器人上的，是后面的：

```xml
<geom type="mesh"
      mesh="body.obj"
      class="visual"/>
```

因此：

```text
asset mesh
→ 定义资源

geom type="mesh"
→ 真正使用资源
```

机器人模型同时存在：

```text
visual geometry
collision geometry
```

因此 Viewer 中看到的外观和真正参与碰撞计算的几何体可以不同。

---

## 一个 Body 中多个 Geom

一个 body 可以包含多个 geom。

这并不代表多个刚体。

而是：

```text
一个 body
+
多个几何表示
```

这些 geom 可以分别用于：

- 碰撞
- 外观显示
- 多个 mesh 共同组成复杂形状

同一个 body 下的 geom 会作为一个整体一起运动。

---

## 左机械臂的 Joint

左机械臂共有 7 个 joint：

```text
openarm_left_joint1
openarm_left_joint2
openarm_left_joint3
openarm_left_joint4
openarm_left_joint5
openarm_left_joint6
openarm_left_joint7
```

每个 joint 会定义：

- rotation axis
- joint range
- damping
- frictionloss
- armature

整个模型使用弧度：

```text
rad
```

作为角度单位。

---

## Position Actuator

左机械臂有 7 个 position actuator。

例如：

```xml
<position name="left_joint1_pos"
          joint="openarm_left_joint1"
          .../>
```

其控制关系为：

```text
Python 目标
↓
data.ctrl
↓
position actuator
↓
对应 joint
```

Position actuator 会尝试把 joint 驱动到目标角。

---

## Target 与 Actual State

这是本实验最重要的概念之一。

Python 中的：

```python
data.ctrl
```

表示：

```text
目标
```

而：

```text
qpos
```

表示：

```text
实际 joint position
```

所以：

```text
ctrl
= 我希望 joint 去哪里

qpos
= joint 实际在哪里
```

机械臂运动过程中，两者不一定完全相同。

---

## Sensor

模型定义了多种 sensor。

### Joint Position

```text
jointpos
```

读取：

```text
当前 joint angle
```

### Joint Velocity

```text
jointvel
```

读取：

```text
当前 joint angular velocity
```

### End-Effector Position

```text
framepos
```

读取：

```text
left_tool 的世界坐标
```

结果为：

```text
(x, y, z)
```

### End-Effector Orientation

```text
framequat
```

读取：

```text
left_tool 的姿态
```

结果使用四元数：

```text
(w, x, y, z)
```

---

## End-Effector Site

机器人模型中定义：

```text
left_tool
```

这个 site 位于左侧夹爪末端附近。

它不是一个新的刚体。

而是一个参考坐标系，用来测量：

- 末端位置
- 末端姿态

---

## Contact Exclusion

模型中存在：

```xml
<exclude body1="..." body2="..."/>
```

用于关闭指定 body pair 之间的碰撞检测。

主要用于：

```text
相邻 link
已经连接的结构
非常接近的部件
```

避免产生不必要的 self-collision。

---

## Python 控制程序

Python 程序使用预先定义好的 joint-space waypoint 控制左机械臂。

整体流程为：

```text
加载 scene
↓
创建 model
↓
创建 data
↓
初始化机器人
↓
定义 joint target
↓
在 waypoint 之间插值
↓
写入 data.ctrl
↓
推进仿真
↓
读取实际 joint state
↓
读取 end-effector pose
```

---

## Waypoints

程序定义了 4 组 7 关节目标姿态。

可以理解为：

```text
姿态 A
↓
姿态 B
↓
姿态 C
↓
回到姿态 A
```

每个 waypoint 中包含：

```text
7 个 joint target
```

分别对应左机械臂 7 个 joint。

---

## 时间安排

程序使用：

```text
initial hold = 5.0 s
segment duration = 4.0 s
final hold = 0.5 s
```

完整时间线：

```text
0–5 s
→ 保持姿态 A

5–9 s
→ A → B

9–13 s
→ B → C

13–17 s
→ C → A

17–17.5 s
→ 最终保持
```

总仿真时间：

```text
17.5 s
```

由于：

```text
timestep = 0.001 s
```

所以总物理步数约为：

```text
17500 steps
```

---

## 初始 Joint State

实验开始时，程序直接把 joint position 初始化到第一组 waypoint。

这属于：

```text
初始化
```

随后正常控制阶段不再直接修改：

```text
qpos
```

而是通过：

```python
data.ctrl
```

控制 actuator。

这样机械臂后续运动仍然经过完整物理仿真。

---

## 写入控制目标

每一个目标角会写入对应 actuator 的控制输入。

流程是：

```text
joint target
↓
data.ctrl
↓
position actuator
↓
joint
```

Actuator 会尝试把实际 joint position 拉向目标。

---

## Linear Interpolation

Waypoint 之间不是瞬间跳变。

而是通过线性插值平滑过渡。

简化表达：

```text
target =
start
+
alpha × (end - start)
```

其中：

```text
alpha
```

在每一段运动过程中从：

```text
0
```

逐渐增加到：

```text
1
```

因此：

```text
1.30
→ 1.29
→ 1.28
→ ...
→ 1.05
```

而不是：

```text
1.30
→ 瞬间 1.05
```

---

## Physics Simulation

程序通过：

```python
mujoco.mj_step(model, data)
```

推进仿真。

每一步：

```text
0.001 s
```

大致过程：

```text
actuator 收到目标
↓
产生控制作用
↓
joint velocity 改变
↓
joint position 改变
```

---

## Sensor Reading

程序会周期性读取：

```text
joint angles
joint velocities
left_tool position
left_tool orientation
```

终端输出中：

```text
q(rad)
→ 实际关节角

dq(rad/s)
→ 实际关节角速度

tool_xyz(m)
→ 末端位置

tool_wxyz
→ 末端姿态四元数
```

---

## Sensor Refresh

在读取部分 sensor 数据前，程序使用：

```python
mujoco.mj_forward(model, data)
```

它不会推进仿真时间。

作用是：

```text
根据当前 qpos / qvel
刷新当前派生计算
```

从而保证 sensor 数据和当前状态对应。

---

## 关键时间检查

实验检查了多个关键时刻。

### 5.000 s

机械臂仍处于第一组 waypoint。

### 9.000 s

第一段运动完成。

实际 joint configuration 已经非常接近第二组目标。

### 13.000 s

第二段运动完成。

实际 joint configuration 已经非常接近第三组目标。

### 17.000 s

机械臂已经回到最后一组 waypoint，也就是接近初始姿态。

### 17.500 s

最终保持结束。

Joint velocity 已经接近：

```text
0
```

---

## 运动中 Joint Velocity

例如：

```text
7 s
```

位于：

```text
5–9 s
```

这一段运动过程中。

所以：

```text
dq ≠ 0
```

完全正常。

这表示 joint 正在向下一组 target 运动。

---

## Target 与 Actual 对比

程序在关键时间打印：

```text
target joint configuration
```

以及：

```text
actual joint configuration
```

结果显示 position actuator 能够把机械臂驱动到非常接近目标 waypoint 的位置。

因此验证了：

```text
target
↓
ctrl
↓
actuator
↓
joint
↓
actual qpos
```

这条控制链。

---

## End-Effector Observation

随着 joint configuration 改变：

```text
joint angle 改变
↓
robot links 改变姿态
↓
left_tool position 改变
↓
left_tool orientation 改变
```

说明：

```text
joint-space motion
和
end-effector pose
```

之间存在直接关系。

本实验没有使用 inverse kinematics。

而是：

```text
直接给 joint target
↓
观察最终末端去了哪里
```

---

## 简化的核心 Python 控制

整份控制程序可以压缩成：

```python
import mujoco

model = mujoco.MjModel.from_xml_path("scene.xml")
data = mujoco.MjData(model)

target = [1.0, 0.0, 0.0, 1.2, 0.0, 0.0, -1.0]

for i, value in enumerate(target):
    data.ctrl[i] = value

for _ in range(1000):
    mujoco.mj_step(model, data)

print(data.sensor("left_joint1_angle").data)
print(data.sensor("left_tool_position").data)
```

这已经包含了最核心的控制逻辑。

---

## 简化控制流程解释

这段代码可以理解成：

```text
加载 XML
↓
创建 model
↓
创建 data
↓
定义目标 joint angle
↓
把目标写入 ctrl
↓
position actuator 接收目标
↓
mj_step 推进物理系统
↓
actual joint position 改变
↓
sensor 读取实际状态
```

其中最重要的是：

```text
target
≠
瞬间的实际状态
```

Target 只是告诉机器人：

```text
“我要你去这里”
```

而物理仿真决定：

```text
“你实际怎么运动过去”
```

---

## Viewer 检查

通过：

```bash
python -m examples.mujoco.sim_t02_arm_joint_targets --viewer
```

观察机械臂运动。

在这种模式下：

```text
Python
→ 控制仿真

Viewer
→ 显示当前仿真状态
```

通过 Viewer 可以直接观察 waypoint 之间的连续运动。

---

## Viewer Timing

完整 Python 程序还包含一部分额外 timing 代码。

在 Windows 下使用高精度 timer，使 Viewer 播放速度尽量接近真实时间。

这部分属于：

```text
工程辅助功能
```

而不是 MuJoCo 控制逻辑本身。

核心作用只是：

```text
physics step
↓
viewer sync
↓
短暂等待
↓
下一步 physics
```

---

## 主要学习收获

这个实验首次加入了主动机器人控制。

完整控制与观察链为：

```text
WAYPOINTS
↓
插值
↓
data.ctrl
↓
position actuator
↓
joint motion
↓
qpos / qvel
↓
sensor
↓
end-effector pose
↓
terminal / Viewer
```

最重要的概念包括：

```text
joint
→ 定义允许的运动

actuator
→ 驱动 joint

ctrl
→ 控制目标

qpos
→ 实际位置

qvel
→ 实际速度

sensor
→ 读取状态

site
→ 末端参考坐标系

mj_step
→ 推进物理仿真
```

---

## 与 SIM-T01 的进阶关系

SIM-T01 主要研究：

```text
gravity
↓
自由运动
↓
contact
↓
观察
```

SIM-T02 增加了主动控制：

```text
target
↓
actuator
↓
joint motion
↓
sensor feedback
```

这标志着学习从：

```text
观察一个仿真系统
```

进一步进入：

```text
主动控制一个机器人仿真系统
```

---

## 来源

本实验基于：

```text
Robot_knowledge_study
M2
SIM-T02
v0.3.0
```

来源仓库：

https://github.com/noBug01/Robot_knowledge_study

原始仓库与教学材料归对应作者所有。

本文记录的是我自己的仿真过程、代码理解、观察结果、验证与总结。