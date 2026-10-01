# SIM-T02 - 机械臂关节角目标控制

[English](02_arm_joint_targets.md) | [中文](02_arm_joint_targets_zh.md)

---

## 概览

这个场景在 SIM-T01 的基础上进一步加入了：

- 多关节机械臂
- Actuator 执行器
- Sensor 传感器
- 关节目标角
- Python 控制输入
- 末端位姿读取
- Waypoint 轨迹
- Viewer 中的受控运动

本场景主要学习：

- MJCF 中父 body / 子 body 的层级结构
- `<default>` 的参数模板作用
- `<asset>` 中 mesh 的定义与使用
- 一个 body 中多个 geom 的意义
- Joint 的定义和范围
- Position actuator 的作用
- Joint sensor 与末端 sensor
- `data.ctrl` 作为控制目标
- 目标关节角与实际关节角的区别
- Waypoint 之间的插值
- Python 如何主动控制机械臂
- Python 如何读取实际状态和末端位姿

整个场景最核心的控制链为：

```text
目标关节角
↓
data.ctrl
↓
position actuator
↓
joint 运动
↓
qpos / qvel 改变
↓
sensor 读取实际状态
```

---

## 1. 场景是如何组合起来的

T02 的 `scene.xml` 并没有把所有内容都写在一个文件中。

它通过：

```xml
<include file="../sim_t01_table_cube/scene.xml"/>
<include file="robot.xml"/>
```

把多个 XML 文件组合起来。

最终场景可以理解成：

```text
SIM-T01 scene
├── 地面
├── 桌子
├── 方块
├── 灯光
└── 相机

+

robot.xml
├── 机器人主体
├── 左机械臂
├── 右机械臂
├── actuator
├── sensor
└── contact 设置
```

T02 还重新设置了：

```xml
<option timestep="0.001"/>
```

因此仿真步长变成：

```text
0.001 s
```

---

## 2. Robot XML 的整体结构

`robot.xml` 主要包含：

```text
default
asset
worldbody
actuator
sensor
contact
```

简化后的机器人层级大概是：

```text
openarm_body
├── 机器人主体 / 底座
├── 左机械臂
│   ├── left link 0
│   ├── left link 1
│   ├── ...
│   ├── left link 7
│   └── left gripper
└── 右机械臂
    ├── right link 0
    ├── right link 1
    ├── ...
    ├── right link 7
    └── right gripper
```

---

## 3. 父 Body 与子 Body

机械臂采用层层嵌套的 body 结构。

例如：

```text
父 body
└── 子 body
    └── 孙 body
        └── 下一层 body
```

这正好对应串联机械臂的物理结构：

```text
肩部
↓
上臂
↓
肘部
↓
前臂
↓
手腕
↓
夹爪
```

子 body 会继承父 body 的整体运动，同时自己的 joint 还能增加相对于父 body 的运动。

因此：

```text
子 body 的世界运动
=
父 body 的运动
+
子 body 自己的相对 joint 运动
```

---

## 4. 为什么一个 Body 下面可以有多个 Geom

一个 body 可以包含多个 geom。

例如：

```xml
<body name="link">
    <geom .../>
    <geom .../>
    <geom .../>
</body>
```

这并不代表有三个刚体。

真正含义是：

```text
一个刚体
+
多个几何表示
```

这些 geom 可以分别用于：

```text
collision geom
→ 用于碰撞计算

visual geom
→ 用于外观显示

多个 visual geom
→ 共同组成复杂外形
```

同一个 body 下的所有 geom 会作为一个刚体一起运动。

---

## 5. Default 参数模板

`<default>` 用来定义可重复使用的参数模板。

例如：

```xml
<default class="motor_DM8009">
    <joint .../>
</default>
```

后面的 joint 可以写：

```xml
<joint class="motor_DM8009" .../>
```

从而自动继承这套参数。

Default 中可以预先定义：

- joint damping
- frictionloss
- armature
- joint type
- collision 参数
- visual 参数
- actuator gain
- actuator limit

可以这样理解：

```text
default
→ 参数模板

class
→ 选择哪套模板

joint / geom / actuator
→ 真正使用模板的对象
```

---

## 6. Asset 中的 Mesh

`<asset>` 负责定义可复用的 3D mesh 资源。

例如：

```xml
<mesh name="body.obj"
      file="visual/body/openarm_body.obj"/>
```

这里只是把这个模型资源登记进 MuJoCo。

并不会立刻让它出现在场景中。

后面需要通过：

```xml
<geom type="mesh"
      mesh="body.obj"
      class="visual"/>
```

真正使用这个 mesh。

因此关系是：

```text
asset 中的 mesh
→ 定义资源

geom type="mesh"
→ 真正使用这个资源
```

模型中可以看到多组：

```text
visual/body
visual/arm
visual/gripper

collision/arm
collision/gripper
```

---

## 7. Visual Mesh 与 Collision Mesh

机器人同一个 link 通常可以同时拥有：

```text
visual mesh
→ 用于 Viewer 显示

collision mesh
→ 用于物理碰撞计算
```

Visual mesh 可以更精细、更好看。

Collision mesh 通常更简单，更适合快速稳定地进行碰撞计算。

所以：

```text
Viewer 里看到的外观
≠
MuJoCo 真正用于碰撞的形状一定完全相同
```

例如机器人底盘和轮子可能已经被做进一个大的 visual mesh 里。

因此：

```text
看见轮子
≠
一定存在独立 wheel body / wheel joint
```

---

## 8. 左机械臂的 7 个 Joint

左机械臂共有 7 个旋转关节：

```text
openarm_left_joint1
openarm_left_joint2
...
openarm_left_joint7
```

每个 joint 会定义：

```text
axis
range
damping
frictionloss
armature
```

XML 中使用：

```xml
<compiler angle="radian" .../>
```

因此 joint range 和目标角单位都是：

```text
rad
```

核心理解：

```text
joint
→ 定义一个 body 相对于父 body 可以如何运动
```

---

## 9. 右机械臂

右机械臂的写法和左机械臂基本相同：

```text
body
→ joint
→ geom
→ child body
```

只是：

- 名字不同
- 部分位置与姿态是镜像关系
- 某些 joint axis 可能不同

本场景的主动控制主要集中在左机械臂。

---

## 10. Position Actuator

模型给左机械臂定义了 7 个 position actuator。

例如：

```xml
<position name="left_joint1_pos"
          joint="openarm_left_joint1"
          .../>
```

表示：

```text
这个 actuator
控制
openarm_left_joint1
```

控制关系为：

```text
Python 目标值
↓
data.ctrl
↓
position actuator
↓
joint 运动
```

Position actuator 的作用是：

> 尝试把 joint 拉向某个目标角度。

它并不是直接把 joint 瞬间设到目标角。

---

## 11. `range / ctrlrange / ctrl / qpos`

这四个概念必须区分。

### Joint Range

```text
range
```

表示：

> 这个 joint 物理上允许运动到哪里。

### Control Range

```text
ctrlrange
```

表示：

> actuator 允许接受什么范围的目标值。

### Control Input

```python
data.ctrl
```

表示：

> 当前发送给 actuator 的目标。

### Actual Joint Position

```python
qpos
```

表示：

> 当前 joint 实际所在的位置。

因此：

```text
data.ctrl
= 目标

qpos
= 实际
```

两者在运动过程中不一定完全相同。

---

## 12. 末端 Site

模型中定义：

```xml
<site name="left_tool" .../>
```

这个 site 位于左侧夹爪末端。

Site：

```text
不是刚体
不增加质量
不直接参与控制
```

它更像是一个：

```text
参考点 / 参考坐标系
```

这里用于表示：

```text
机械臂末端
```

---

## 13. Sensor

模型定义了多种传感器。

### Joint Position Sensor

```xml
<jointpos .../>
```

读取：

```text
当前关节角
```

### Joint Velocity Sensor

```xml
<jointvel .../>
```

读取：

```text
当前关节角速度
```

### End-Effector Position Sensor

```xml
<framepos .../>
```

读取：

```text
left_tool 在世界坐标系中的位置
```

返回：

```text
(x, y, z)
```

### End-Effector Orientation Sensor

```xml
<framequat .../>
```

读取：

```text
left_tool 的姿态
```

返回四元数：

```text
(w, x, y, z)
```

---

## 14. Contact Exclusion

`<contact>` 中存在类似：

```xml
<exclude body1="..." body2="..."/>
```

它表示：

> 这两个 body 之间不进行碰撞检测。

主要用于：

```text
相邻机械臂 link
彼此非常接近的结构
已经物理连接在一起的部件
```

这样可以减少无意义碰撞和不稳定接触。

所以：

```text
contact exclude
→ 碰撞过滤
```

不是在创建新的碰撞。

---

## 15. Python 仿真结构

T02 的 Python 程序开始加入主动控制。

整体流程：

```text
加载 XML
↓
创建 model
↓
创建 data
↓
初始化机械臂
↓
定义 waypoint
↓
写入 data.ctrl
↓
mj_step 推进
↓
读取实际 joint 与 sensor
↓
打印结果 / Viewer 显示
```

---

## 16. Scene Path

程序首先找到：

```text
simulation/mujoco/scenes/sim_t02_arm_joint_targets/scene.xml
```

这个路径随后交给：

```python
mujoco.MjModel.from_xml_path(...)
```

加载完整场景。

---

## 17. WAYPOINTS_RAD

程序定义了多个 7 关节目标姿态：

```python
WAYPOINTS_RAD = (
    (...7 values...),
    (...7 values...),
    (...7 values...),
    (...7 values...),
)
```

每组分别对应：

```text
joint1
joint2
joint3
joint4
joint5
joint6
joint7
```

整体动作可以理解为：

```text
姿态 A
↓
姿态 B
↓
姿态 C
↓
回到姿态 A
```

---

## 18. 时间安排

程序设置：

```text
INITIAL_HOLD_SECONDS = 5.0
SECONDS_PER_SEGMENT = 4.0
FINAL_HOLD_SECONDS = 0.5
```

所以时间线为：

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

总时间：

```text
17.5 s
```

由于：

```text
timestep = 0.001 s
```

所以总步数约为：

```text
17.5 / 0.001
=
17500 steps
```

---

## 19. 自动生成 Joint / Actuator / Sensor 名字

程序使用：

```python
ARM_JOINTS
ARM_ACTUATORS
ANGLE_SENSORS
VELOCITY_SENSORS
```

自动生成：

```text
openarm_left_joint1
...
openarm_left_joint7
```

以及：

```text
left_joint1_pos
...
left_joint7_pos
```

这样就不用重复手写 7 次。

---

## 20. SensorReading

程序定义：

```python
class SensorReading(NamedTuple):
    ...
```

用于把传感器数据打包。

每次读取中包含：

```text
7 个关节角
7 个关节角速度
末端位置
末端姿态四元数
```

这样不同函数之间传递数据更清晰。

---

## 21. 读取 Sensor

程序通过：

```python
data.sensor(name).data
```

读取传感器。

包括：

```text
joint angle
joint velocity
left_tool position
left_tool orientation
```

整体关系：

```text
XML 声明 sensor
↓
MuJoCo 计算 sensor 数据
↓
Python 读取 sensor
```

---

## 22. 初始关节状态

程序开始时会直接设置：

```text
qpos
```

让机械臂一开始就在第一组 waypoint。

这是初始化阶段。

之后正常控制时，不再直接修改：

```text
qpos
```

而改为修改：

```python
data.ctrl
```

因此：

```text
初始化
→ 可以直接设置 qpos

正常控制
→ 使用 ctrl
→ 由 actuator 驱动
```

---

## 23. 写入控制目标

程序把目标角写到：

```python
data.ctrl
```

每个 actuator 接收一个目标角。

流程为：

```text
WAYPOINT
↓
data.ctrl
↓
position actuator
↓
joint
```

Actuator 会尝试减小：

```text
目标角
和
实际角
```

之间的差值。

---

## 24. Target 与 Actual 的区别

Target 并不会瞬间变成实际 joint angle。

真实过程是：

```text
target
↓
actuator 产生控制作用
↓
joint 加速
↓
qvel 改变
↓
qpos 改变
```

实际运动还会受到：

- 质量
- 惯性
- 重力
- damping
- friction
- actuator gain
- force limit
- timestep

等因素影响。

因此：

```text
ctrl
≠
每一时刻的 qpos
```

---

## 25. Linear Interpolation

Waypoint 之间不是瞬间跳变。

程序使用插值：

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

从：

```text
0
```

逐渐变化到：

```text
1
```

例如：

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
→ 瞬间变成 1.05
```

这样机械臂运动会更平滑。

---

## 26. Physics Step

更新目标后，程序调用：

```python
mujoco.mj_step(model, data)
```

每次推进：

```text
0.001 s
```

在每一步中：

```text
actuator 施加控制
↓
计算 joint acceleration
↓
qvel 改变
↓
qpos 改变
```

---

## 27. Sensor Refresh

在读取特定 sensor 数据前，程序会调用：

```python
mujoco.mj_forward(model, data)
```

它不会推进时间。

只是：

```text
根据当前 qpos / qvel
重新计算当前派生结果和 sensor
```

这样 sensor 数据就能和当前状态对齐。

---

## 28. Sensor Sampling

程序大约每：

```text
1 s
```

读取一次 sensor。

这样不需要每：

```text
0.001 s
```

都打印。

终端输出包括：

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

## 29. 关键时间验证

运行结果中检查了几个关键时间。

### 5.000 s

仍处于初始姿态。

### 9.000 s

第一段运动结束，到达第二组 waypoint。

### 13.000 s

第二段结束，到达第三组 waypoint。

### 17.000 s

已经回到最后一组目标姿态。

### 17.500 s

最终保持结束，joint velocity 基本接近：

```text
0
```

---

## 30. 为什么运动中 dq 不为 0

例如：

```text
7 s
```

位于：

```text
5–9 s
```

这一段 waypoint transition 中。

所以机械臂正在运动。

因此：

```text
dq ≠ 0
```

是正常的。

---

## 31. End-Effector Motion

随着 7 个 joint angle 改变：

```text
机械臂 link 姿态改变
↓
left_tool 位置改变
↓
left_tool 姿态改变
```

因此：

```text
joint configuration
↓
robot geometry
↓
end-effector pose
```

本场景没有做 inverse kinematics。

只是：

> 直接给 joint target，然后观察末端最终去了哪里。

---

## 32. Viewer

可以使用：

```bash
python -m examples.mujoco.sim_t02_arm_joint_targets --viewer
```

此时：

```text
Python 负责控制和 mj_step
Viewer 负责显示
```

程序通过：

```python
viewer.sync()
```

把当前仿真状态同步到窗口。

---

## 33. Viewer Timing

Python 程序中还存在一大段 Viewer timing 代码。

它的目的是：

> 让 Viewer 播放速度尽量接近真实时间。

在 Windows 上，程序通过系统 API 建立高精度 timer。

这部分主要属于：

```text
工程实现
```

而不是：

```text
MuJoCo 控制核心
```

当前阶段只需要理解：

```text
physics step
↓
viewer.sync
↓
程序等待一点真实时间
↓
画面不会瞬间跑完
```

---

## 34. 核心 Python 控制流程

完整的教学程序还包含很多额外功能，例如：

- Viewer timing
- 命令行参数
- 输出格式
- Windows 平台兼容
- 高精度定时器
- 数据打印辅助函数

但是 MuJoCo 真正最核心的控制逻辑可以缩减成下面这样：

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

这段简化代码已经包含了 Python 控制 MuJoCo 机器人的核心逻辑。

### 第 1 步 - 导入 MuJoCo

```python
import mujoco
```

作用是导入 MuJoCo Python 库。

之后程序才能：

- 读取 MJCF/XML
- 创建 simulation state
- 推进物理仿真
- 访问 joint
- 访问 actuator
- 访问 sensor

---

### 第 2 步 - 加载 XML 模型

```python
model = mujoco.MjModel.from_xml_path("scene.xml")
```

这一步读取 XML，并建立 MuJoCo model。

`model` 中主要包含比较固定的信息，例如：

```text
body
joint
geom
actuator
sensor
mass
gravity
timestep
joint range
actuator setting
```

可以把它理解成：

```text
model
=
整个仿真系统的结构和规则
```

---

### 第 3 步 - 创建仿真状态

```python
data = mujoco.MjData(model)
```

`MjData` 保存当前仿真的动态状态。

它会随着仿真不断变化。

例如：

```text
simulation time
joint position
joint velocity
control input
contact
sensor value
```

所以可以记：

```text
model
→ 系统是什么

data
→ 系统现在正在做什么
```

---

### 第 4 步 - 定义目标关节角

```python
target = [1.0, 0.0, 0.0, 1.2, 0.0, 0.0, -1.0]
```

左机械臂有 7 个受控关节。

所以这 7 个数分别对应：

```text
joint1 → 1.0 rad
joint2 → 0.0 rad
joint3 → 0.0 rad
joint4 → 1.2 rad
joint5 → 0.0 rad
joint6 → 0.0 rad
joint7 → -1.0 rad
```

这些数字代表：

```text
目标角
```

不是：

```text
当前实际角
```

---

### 第 5 步 - 把目标写入 Actuator

```python
for i, value in enumerate(target):
    data.ctrl[i] = value
```

`enumerate(target)` 会依次得到：

```text
i = 0, value = 1.0
i = 1, value = 0.0
i = 2, value = 0.0
...
i = 6, value = -1.0
```

然后：

```python
data.ctrl[i] = value
```

就相当于：

```text
ctrl[0]
→ actuator 1 的目标

ctrl[1]
→ actuator 2 的目标

...

ctrl[6]
→ actuator 7 的目标
```

因为 XML 中使用的是 position actuator，所以这些 control value 可以理解为：

```text
目标 joint position
```

整个关系是：

```text
target
↓
data.ctrl
↓
position actuator
↓
对应 joint
```

注意：

> 这时只是“告诉 actuator 想去哪”，joint 还没有瞬间到达目标。

---

### 第 6 步 - 推进物理仿真

```python
for _ in range(1000):
    mujoco.mj_step(model, data)
```

这一段才是真正让机器人动起来。

每调用一次：

```python
mujoco.mj_step(model, data)
```

仿真就推进一个 timestep。

如果：

```text
timestep = 0.001 s
```

那么：

```text
1000 steps × 0.001 s
=
1.0 s
```

仿真时间。

每一步内部大概经历：

```text
目标角
↓
position actuator 比较目标与实际差值
↓
actuator 产生控制作用
↓
joint acceleration 产生
↓
joint velocity 改变
↓
joint position 改变
```

然后下一步继续重复。

所以实际 joint angle 会逐渐靠近目标角。

---

### 第 7 步 - Target 与 Actual State 的区别

这是最重要的概念之一：

```text
data.ctrl
=
我希望 joint 去哪里

qpos
=
joint 现在实际上在哪里
```

不是：

```text
ctrl = 1.0
→ joint 立刻等于 1.0
```

而是：

```text
ctrl = 1.0
↓
actuator 开始驱动
↓
不断 mj_step
↓
joint 逐渐运动
↓
qpos 慢慢靠近 1.0
```

实际运动会受到：

- mass
- inertia
- gravity
- damping
- friction
- actuator gain
- force limit
- timestep

影响。

因此：

```text
target
和
actual
```

在运动过程中可以存在差异。

---

### 第 8 步 - 读取实际关节角

```python
print(data.sensor("left_joint1_angle").data)
```

XML 中已经定义了：

```xml
<jointpos
    name="left_joint1_angle"
    joint="openarm_left_joint1"/>
```

所以 Python 可以直接：

```python
data.sensor("left_joint1_angle").data
```

读取这个 sensor。

它返回：

```text
joint1 当前实际角度
```

因此可以比较：

```text
data.ctrl
→ 我要求的目标

sensor joint angle
→ 实际做到的结果
```

---

### 第 9 步 - 读取末端位置

```python
print(data.sensor("left_tool_position").data)
```

XML 中定义了：

```xml
<framepos
    name="left_tool_position"
    objtype="site"
    objname="left_tool"/>
```

所以这个 sensor 会返回：

```text
[x, y, z]
```

表示：

```text
left_tool 当前在世界坐标系中的位置
```

这体现了机器人学中非常重要的关系：

```text
joint angle 改变
↓
link configuration 改变
↓
end-effector position 改变
```

---

### 简化后的完整控制链

所以这段最小程序可以理解为：

```text
加载 XML
↓
创建 model
↓
创建 data
↓
定义 7 个目标角
↓
写入 data.ctrl
↓
actuator 接收目标
↓
mj_step 不断推进物理仿真
↓
joint 实际 qpos / qvel 发生变化
↓
sensor 读取真实结果
↓
Python 得到反馈
```

还可以进一步压缩成：

```text
target
↓
ctrl
↓
actuator
↓
joint
↓
mj_step
↓
actual state
↓
sensor
```

这就是 SIM-T02 最重要的 Python 控制流程。

---

## 35. 完整控制与反馈关系

整个 T02 的控制过程可以整理成：

```text
WAYPOINTS_RAD
↓
线性插值
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

这是整个 SIM-T02 最核心的逻辑。

---

## 36. 当前阶段必须掌握的内容

本场景最重要的概念是：

```text
joint
→ 定义怎么动

actuator
→ 驱动 joint

ctrl
→ 给 actuator 的目标输入

qpos
→ 实际 joint position

qvel
→ 实际 joint velocity

sensor
→ 读取仿真状态

site
→ 末端参考点

mj_step
→ 推进物理仿真

mj_forward
→ 刷新当前状态的派生计算
```

整份 Python 文件还有很多：

- argparse
- Viewer timing
- ctypes
- Windows API
- 输出格式
- contextmanager

这些属于工程辅助部分。

当前阶段不需要掌握到底层实现。

真正应该掌握的是：

```text
ctrl
→ actuator
→ joint
→ mj_step
→ qpos / qvel
→ sensor
```

---

## 37. 核心理解

SIM-T02 相比 SIM-T01 的最大变化是：

```text
SIM-T01
XML
→ physics
→ 观察自然运动
```

变成：

```text
SIM-T02
XML
→ Python 给目标
→ actuator
→ joint 运动
→ sensor feedback
```

最重要的区别是：

```text
target
≠
actual state
```

Python 负责提出：

```text
“我希望机器人去哪里”
```

而 MuJoCo 物理仿真负责决定：

```text
“机器人实际如何运动过去”
```

这标志着学习从单纯的物理仿真，进入了基础机器人控制与状态反馈。

---

## 来源

本笔记基于以下 M2 `SIM-T02` 学习材料：

```text
Robot_knowledge_study
v0.3.0
```

来源仓库：

https://github.com/noBug01/Robot_knowledge_study

原始仓库与教学材料归对应作者所有。

本文记录的是我在学习过程中的个人理解、代码解读、仿真验证与总结，并不是对原始教材内容的直接复制。