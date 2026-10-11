# MuJoCo Sensor 综合示例分析

[English](sensor_example_report.md) | [中文](sensor_example_report_zh.md)

## 概览

本报告记录的是 Albusgive MuJoCo 学习来源中的一个综合 sensor 示例。

这个示例在同一个模型中展示了多种 sensor，包括：

- camera observation
- IMU 类 sensing
- `subtreelinvel`
- `framepos`
- `force`
- `torque`
- `jointpos`
- `jointvel`
- `ballquat`
- `ballangvel`

同时模型中还包含：

- 一个 free body
- 一个固定 support
- 一个 hinge joint
- 一个 ball joint
- 一个 position actuator
- 多个 sensor 安装 site

这个例子的目的不是构建一个完整机器人。

它更像是：

> 一个用于集中演示不同 MuJoCo sensor 如何连接到不同模型元素上的综合示例。

---

# 1. 整体模型结构

整个模型可以大致分成几个相互独立的演示部分：

```text
world
├── floor
├── external camera
├── free body B
│   ├── freejoint
│   ├── IMU site
│   └── body-mounted camera
│
├── force / torque demo
│   └── up_box
│       └── force_torque site
│
└── joint sensor demo
    └── support
        └── rotay_am
            ├── pivot hinge joint
            ├── horizontal link
            └── pendulum
                ├── ph ball joint
                ├── vertical link
                └── sphere mass
```

所以这个 XML 其实是把几种不同 sensing situation 放进同一个文件里。

---

# 2. 基础仿真设置

示例使用了常见的 compiler 设置：

```xml
<compiler
    angle="radian"
    meshdir="meshes"
    autolimits="true"/>
```

表示：

```text
angle
→ 使用 radian

meshdir
→ 默认 mesh 目录

autolimits
→ 当定义 range 时自动启用相关 limit
```

仿真设置中包括：

```text
timestep = 0.002
gravity = 0 0 -9.81
integrator = implicitfast
```

因此：

```text
一个 simulation step
→ 0.002 s
```

对应大约：

```text
500 steps per second
```

---

# 3. Asset 部分

这个例子定义了一些视觉资源：

```text
texture
material
mesh
```

其中 checker texture / material 用于地面。

还定义了一个 tetrahedron mesh。

但在这次分析的 sensor 逻辑中，这个 mesh 并不是核心。

所以它主要属于：

```text
model resource setup
```

而不是 sensor 演示本身。

---

# 4. Floor 和 Light

`worldbody` 中包含：

```text
floor geom
directional light
```

它们的作用分别是：

```text
floor
→ 地面

light
→ 场景渲染
```

它们不是 sensor。

只是为了给整个示例提供基本环境。

---

# 5. 外部 Camera `c2`

模型中有一个放在 body `B` 外部的 camera。

概念上类似：

```xml
<camera
    name="c2"
    pos="1 0 1"
    mode="targetbody"
    target="B"
    fovy="54.225"/>
```

重要参数：

```text
name="c2"
→ camera 名字

pos
→ camera 位置

mode="targetbody"
→ camera 朝向指定 body

target="B"
→ 目标 body 是 B

fovy
→ vertical field of view
```

所以这个 camera 可以理解成：

```text
外部观察者
↓
始终看向 body B
```

---

# 6. Free Body `B`

模型中有：

```xml
<body name="B" pos="0 0 0">
    <freejoint/>
    <site name="imu"/>
    ...
</body>
```

最关键的是：

```xml
<freejoint/>
```

这意味着 body `B` 具有完整的空间自由度：

```text
3 translational DOF
+
3 rotational DOF
=
6 DOF
```

所以 B 可以：

```text
沿 x / y / z 移动
+
进行三维旋转
```

---

# 7. IMU Site

在 body `B` 中：

```xml
<site name="imu"/>
```

定义了一个 sensor reference location。

这个 site 可以理解成：

```text
sensor mounting point
+
sensor coordinate frame
```

它可以被：

```text
framequat
accelerometer
gyro
```

等 sensor 使用。

---

# 8. Body-Mounted Camera `c1`

body `B` 内部还有一个 camera。

概念上类似：

```xml
<camera
    name="c1"
    mode="fixed"
    fovy="54.225"
    euler="1.57 0 0"/>
```

由于这个 camera：

```text
属于 body B
+
mode="fixed"
```

所以：

```text
B 动
↓
camera c1 也跟着动
```

因此两个 camera 可以对比：

```text
c2
→ 外部观察 B

c1
→ 安装在 B 上，跟着 B 一起运动
```

---

# 9. IMU 类 Sensor

示例中有一些 IMU 相关 sensor，有些通过 XML comment 暂时关闭。

包括：

```xml
<framequat
    name="orientation"
    objtype="site"
    objname="imu"/>

<gyro
    name="base_ang_vel"
    site="imu"/>

<accelerometer
    name="accel"
    site="imu"/>
```

它们分别提供：

```text
framequat
→ orientation

gyro
→ angular velocity

accelerometer
→ acceleration
```

所以可以理解成：

```text
IMU-style sensing
≈
orientation
+
angular velocity
+
acceleration
```

---

# 10. `subtreelinvel`

示例中一个启用的 sensor 是：

```xml
<subtreelinvel
    name="base_lin_vel"
    body="B"/>
```

它读取的是：

> 以 body `B` 为 root 的整个 subtree 的 center of mass linear velocity。

概念上：

```text
body B
+
B 的所有 descendants
↓
整体 subtree COM
↓
linear velocity
```

由于这个示例里的 B 结构比较简单，所以这里可以近似理解成：

```text
free body B 整体的线速度
```

---

# 11. `framepos`

示例中还有一个可能被注释掉的：

```xml
<framepos
    name="base_pos"
    objtype="body"
    objname="B"/>
```

它测量：

```text
body B 的 position
```

由于没有指定 reference：

```text
base_pos
→ B 相对于 world frame 的位置
```

输出：

```text
x
y
z
```

---

# 12. Force / Torque 示例结构

模型中还有一组：

```text
parent body
└── up_box
    ├── force_torque site
    └── box geom
```

概念上类似：

```xml
<body pos="0 0 1">
    <geom type="box" .../>

    <body name="up_box" pos="0 0 .02">
        <site name="force_torque"/>
        <geom type="box" .../>
    </body>
</body>
```

其中：

```text
force_torque
```

这个 site 作为 force 和 torque sensor 的 measurement frame。

---

# 13. Force Sensor

示例定义：

```xml
<force
    name="force"
    site="force_torque"/>
```

它测量三维力：

```text
Fx
Fy
Fz
```

可以理解：

```text
force
→ 在该 sensor site 处测得的作用力
```

---

# 14. Torque Sensor

同时还有：

```xml
<torque
    name="torque"
    site="force_torque"/>
```

输出：

```text
Tx
Ty
Tz
```

所以：

```text
force
+
torque
```

组合后得到：

```text
3 个 force components
+
3 个 torque components
=
6 维 force/torque information
```

这就类似真实机器人里的：

```text
6-axis force/torque sensor
```

---

# 15. Joint Sensor 示例结构

Joint sensor 这一部分采用嵌套 body：

```text
world
└── support
    └── rotay_am
        └── pendulum
```

这里非常重要的一点是：

> child body 的 `pos` 是相对于 parent body 定义的。

---

# 16. `support` Body

最外层：

```xml
<body name="support" pos="1 0 0.1">
```

里面有一个 cylinder geom。

由于 `support` 没有 joint：

```text
support
→ 固定在 world
```

所以它相当于固定底座。

---

# 17. Support Geometry

support 的 geom 使用：

```text
type="cylinder"
```

大致参数：

```text
radius = 0.05
half-length = 0.5
```

所以完整高度大约：

```text
1.0
```

示例中它的 mass 设置得比较大。

不过由于这个 body 本身固定，所以这里最重要的概念只是：

```text
support
→ stable base
```

---

# 18. `rotay_am` Body

在 `support` 里面：

```xml
<body name="rotay_am" pos="0 0 0.51">
```

这个：

```text
0 0 0.51
```

是相对于 support 的坐标。

它把旋转臂放到 support 顶部附近。

---

# 19. `pivot` Hinge Joint

在 `rotay_am` 中：

```xml
<joint
    type="hinge"
    name="pivot"
    pos="0 0 0"
    axis="0 0 1"
    damping="0.001"
    frictionloss="0.0"
    stiffness="0.5"/>
```

各参数可以理解：

```text
type="hinge"
→ 1 rotational DOF

name="pivot"
→ joint 名字

axis="0 0 1"
→ 绕 z 轴旋转

damping
→ 与速度相关的阻尼

frictionloss
→ 额外关节摩擦损失

stiffness
→ 弹性恢复作用
```

所以：

```text
pivot
→ 让水平臂在 xy 平面内转动
```

---

# 20. Horizontal Link

`rotay_am` 中有一个 capsule：

```xml
<geom
    type="capsule"
    fromto="0 0 0 0.2 0 0"
    size="0.01"
    .../>
```

表示：

```text
沿 +x 方向
延伸约 0.2
```

然后：

```xml
<body name="pendulum" pos="0.2 0 0">
```

正好把 pendulum 放在：

```text
水平杆末端
```

---

# 21. `pendulum` Body

子 body：

```xml
<body name="pendulum" pos="0.2 0 0">
```

属于 `rotay_am`。

因此：

```text
rotay_am 动
↓
pendulum 的 parent frame 也跟着动
```

然后 pendulum 还可以通过自己的 joint：

```text
相对于 parent 再运动
```

---

# 22. `ph` Ball Joint

pendulum 内：

```xml
<joint
    type="ball"
    name="ph"
    pos="0 0 0"
    damping="0.001"
    frictionloss="0.0"/>
```

Ball joint 有：

```text
3 rotational DOF
```

和 hinge 不同：

```text
hinge
→ 只绕一个轴

ball
→ 可以进行三维旋转
```

所以不需要一个单独的：

```xml
axis="..."
```

---

# 23. Ball Joint State

对于 ball joint：

```text
position state
→ quaternion
→ 4 个值

velocity state
→ angular velocity
→ 3 个值
```

所以 MuJoCo 专门提供：

```text
ballquat
ballangvel
```

读取它的状态。

---

# 24. Pendulum Link

pendulum 中还有一根垂直 capsule：

```xml
<geom
    type="capsule"
    fromto="0 0 0 0 0 -0.3"
    size="0.01"
    .../>
```

表示：

```text
从 ball joint
沿 -z 方向
延伸约 0.3
```

---

# 25. Pendulum End Mass

同一个 body 里还有一个 sphere：

```xml
<geom
    type="sphere"
    pos="0 0 -0.3"
    size="0.03"
    .../>
```

它刚好位于 pendulum 底部。

因此结构：

```text
ball joint
↓
vertical link
↓
sphere end mass
```

---

# 26. 一个 Body 可以有多个 Geom

pendulum body 同时包含：

```text
capsule
+
sphere
```

它们不是两个独立 body。

而是：

```text
同一个 rigid body
上的两个 geom
```

所以：

```text
capsule
+
sphere
↓
作为一个整体一起运动
```

这再次强调：

```text
body
→ rigid body

geom
→ 附着在 body 上的 shape
```

---

# 27. Parent-Child Motion

Body 层级：

```text
support
↓
rotay_am
↓
pendulum
```

如果：

```text
pivot
```

旋转：

```text
rotay_am 转动
↓
pendulum 的 parent frame 也随之改变
```

然后：

```text
ph ball joint
```

还可以额外产生 relative rotation。

所以：

```text
child motion
=
parent motion
+
joint-relative motion
```

这就是串联机构的基本运动逻辑。

---

# 28. Joint Position Sensor

示例定义：

```xml
<jointpos
    name="pivot_p"
    joint="pivot"/>
```

因为 `pivot` 是 hinge joint：

```text
pivot_p
→ 一个 joint angle
```

它对应：

```python
data.qpos
```

里的相关 joint coordinate。

---

# 29. Joint Velocity Sensor

示例还定义：

```xml
<jointvel
    name="pivot_v"
    joint="pivot"/>
```

因为 pivot 是 hinge joint：

```text
pivot_v
→ 一个 angular velocity
```

对应：

```python
data.qvel
```

里的相关状态。

---

# 30. Ball Quaternion Sensor

示例可以启用：

```xml
<ballquat
    name="ballquat"
    joint="ph"/>
```

它读取：

```text
ball joint orientation
```

输出：

```text
quaternion
→ 4 个值
```

---

# 31. Ball Angular Velocity Sensor

还可以启用：

```xml
<ballangvel
    name="ballangvel"
    joint="ph"/>
```

它读取：

```text
ball joint angular velocity
```

输出：

```text
ωx
ωy
ωz
```

---

# 32. Position Actuator

模型中还有：

```xml
<position
    kp="2"
    kv="0.1"
    name="pivot"
    joint="pivot"
    ctrlrange="-3.14 3.14"
    forcerange="-5 5"/>
```

表示：

```text
actuator type
→ position servo

controlled joint
→ pivot

ctrl
→ target joint position

forcerange
→ 最终 actuator 输出力 / 力矩限制
```

控制逻辑可以简化理解成：

```text
target position
↓
position error
↓
actuator torque
↓
pivot motion
```

---

# 33. Actuator 和 Sensor 同时出现

这个例子同时展示了机器人系统的两边。

Actuator：

```text
data.ctrl
↓
actuator
↓
joint motion
```

Sensor：

```text
joint / body state
↓
sensor
↓
measurement
```

组合：

```text
controller
↓
actuator
↓
robot motion
↓
sensor
↓
controller
```

这就是：

```text
feedback control
```

的基本结构。

---

# 34. Sensor Output 存在哪里

XML 中定义 sensor 后：

```text
不会自动打印数据
```

MuJoCo 会把启用的 sensor output 存入：

```python
data.sensordata
```

所以：

```text
simulation step
↓
state 改变
↓
sensor value 更新
↓
data.sensordata
```

---

# 35. 使用 Python 读取 Sensor

最简单可以写：

```python
import mujoco

model = mujoco.MjModel.from_xml_path("model.xml")
data = mujoco.MjData(model)

for _ in range(1000):
    mujoco.mj_step(model, data)
    print(data.sensordata)
```

关键流程：

```text
mj_step
↓
更新 simulation state
↓
更新 sensor output
↓
Python 读取 sensordata
```

---

# 36. 为什么 `data.sensordata` 里会有很多值

因为不同 sensor 输出维度不同。

例如：

```text
jointpos
→ 1

jointvel
→ 1

force
→ 3

torque
→ 3

framepos
→ 3

framequat
→ 4

ballquat
→ 4

ballangvel
→ 3
```

所以：

```python
data.sensordata
```

实际上就是：

```text
所有 active sensor output
按顺序组合成的一个数组
```

---

# 37. 大型模型里为什么要使用 Sensor Name

如果模型很小，可以直接查看：

```python
data.sensordata
```

但模型一大，就不适合一直记：

```text
第 0 个值是什么
第 1 个值是什么
第 2 个值是什么
```

更好的思路：

```text
sensor name
↓
sensor ID
↓
sensor data address
↓
读取 data.sensordata 中对应部分
```

这样代码会更加清晰。

---

# 38. 这个例子展示了哪些 Sensor 类型

可以分成几类。

## Body / Frame Observation

```text
framepos
framequat
subtreelinvel
```

---

## IMU 类 Observation

```text
framequat
gyro
accelerometer
```

---

## Joint State

```text
jointpos
jointvel
ballquat
ballangvel
```

---

## Mechanical Interaction

```text
force
torque
```

---

## Visual Observation

```text
camera
```

---

# 39. 这个例子最重要的学习成果

不同对象适合不同 sensor。

例如：

```text
hinge joint
→ jointpos / jointvel

ball joint
→ ballquat / ballangvel

body / site frame
→ frame sensor

IMU mounting point
→ framequat + accelerometer + gyro

mechanical connection
→ force + torque
```

所以选择 sensor 时，本质上是在问两个问题：

```text
我要观察哪个 object？
+
我要测什么 physical quantity？
```

---

# 40. 最终理解

完整的数据和控制流程可以写成：

```text
XML
↓
定义 body / joint / site / camera / actuator / sensor
↓
MjModel
↓
MjData
↓
mj_step
↓
physical state 改变
↓
sensor output 更新
↓
data.sensordata
↓
Python
↓
display / save / analyse / control
```

这个综合例子把之前学过的很多 MuJoCo 概念连接到了一起：

```text
body hierarchy
joint
site
camera
actuator
sensor
qpos
qvel
sensordata
Python control
```

所以它不仅是在学习 sensor，也是在把前面的 MuJoCo 基础知识逐渐连接成一个完整的机器人仿真工作流。

---

## 来源

本示例分析基于：

```text
Albusgive/mujoco_learning
```

来源仓库：

https://github.com/Albusgive/mujoco_learning

原始模型与教学材料归对应作者所有。

本报告记录的是我在学习过程中对该示例的结构分析、代码解读与个人理解。