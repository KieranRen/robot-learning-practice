# MuJoCo Sensors 传感器

[English](08_sensor.md) | [中文](08_sensor_zh.md)

## 概览

本笔记整理的是 Albusgive MuJoCo 学习来源中关于 sensor 的内容。

主要包括：

- camera 相关观察方式
- IMU 类传感器
- `framequat`
- `accelerometer`
- `gyro`
- `jointpos`
- `jointvel`
- `rangefinder`
- `force`
- `torque`
- `ballquat`
- `ballangvel`
- `framepos`
- `framequat`
- `framelinvel`
- `frameangvel`
- `framelinacc`
- `frameangacc`
- subtree 相关 sensor
- 一个综合 sensor 示例

最核心的逻辑是：

```text
MuJoCo simulation
↓
body / joint / site 状态
↓
sensor 定义
↓
sensor measurement
↓
Python 读取 data.sensordata
```

XML 里的 sensor 负责定义：

```text
测什么
在哪里测
相对于谁测
```

Python 通常负责：

```text
显示
保存
画图
控制
验证
```

---

# 1. MuJoCo 中的 Sensor Data

在 XML 中定义 sensor，并不会自动把数据打印到终端。

例如：

```xml
<sensor>
    <jointpos name="pivot_p" joint="pivot"/>
    <jointvel name="pivot_v" joint="pivot"/>
</sensor>
```

这只是告诉 MuJoCo：

```text
我要读取 pivot 的位置
我要读取 pivot 的速度
```

仿真运行以后，MuJoCo 会计算这些 sensor 的输出，并把结果存入：

```python
data.sensordata
```

所以整体流程：

```text
XML 定义 sensor
↓
simulation 运行
↓
MuJoCo 计算 sensor output
↓
data.sensordata
↓
Python 读取
```

然后 Python 可以：

```text
print 到终端
保存 CSV
画图
做反馈控制
```

---

# 2. Camera

Camera 本身不是 `<sensor>` 标签，但它是机器人仿真中非常重要的观察组件。

Camera 可以定义：

- 位置
- 姿态
- tracking mode
- target body
- field of view
- camera intrinsics

例如：

```xml
<camera
    name="c2"
    pos="1 0 1"
    mode="targetbody"
    target="B"
    fovy="54.225"/>
```

这个 camera 可以理解成：

```text
放在指定位置
↓
始终观察 body B
↓
camera 朝向会跟着 B 调整
```

---

# 3. Camera Mode

常见 camera mode：

```text
fixed
track
trackcom
targetbody
targetbodycom
```

可以先这样理解：

```text
fixed
→ camera 固定在 parent body 上

targetbody
→ camera 始终朝向指定 body

track
→ camera 跟随某个对象

trackcom
→ 跟随 center of mass

targetbodycom
→ 朝向 body 的 center of mass
```

---

# 4. Camera 的 Field of View

最直接的参数：

```xml
fovy="..."
```

表示：

```text
vertical field of view
```

单位是 degree。

可以简单理解：

```text
fovy 小
→ 视野窄
→ 看起来更像放大

fovy 大
→ 视野宽
```

---

# 5. Camera Intrinsics

MuJoCo 也可以定义更接近真实相机的内部参数。

例如：

```text
focal
focalpixel
sensorsize
resolution
principal
principalpixel
```

可以理解为：

```text
focal
→ 物理单位下的焦距

focalpixel
→ 像素单位下的焦距

sensorsize
→ 传感器物理尺寸

resolution
→ 图像分辨率

principal
→ 物理单位下的主点位置

principalpixel
→ 像素单位下的主点位置
```

当前阶段使用：

```text
fovy
```

往往更简单直接。

---

# 6. MuJoCo 中的 IMU

MuJoCo 不需要一个单独叫：

```text
IMU
```

的 sensor。

通常是组合多个 sensor 来获得类似 IMU 的信息。

常见组合：

```text
framequat
+
accelerometer
+
gyro
```

也就是：

```text
IMU
≈
orientation
+
linear acceleration
+
angular velocity
```

---

# 7. IMU Site

通常先用一个 site 指定 IMU 的安装位置。

例如：

```xml
<site
    name="imu"
    type="box"
    size="0.02 0.02 0.02"/>
```

这个 site 可以理解成：

```text
IMU 的安装位置
+
IMU 的局部坐标系
```

然后后面的 sensor 都可以绑定：

```xml
site="imu"
```

---

# 8. `framequat`

例如：

```xml
<framequat
    name="orientation"
    objtype="site"
    objname="imu"/>
```

表示：

```text
读取 imu 这个 site 的姿态
```

输出为：

```text
quaternion
```

也就是四元数。

可以理解：

```text
framequat
→ 这个坐标系现在朝什么方向
```

---

# 9. `accelerometer`

例如：

```xml
<accelerometer
    name="accel"
    site="imu"/>
```

表示：

```text
读取 imu site 处的加速度
```

输出为三维向量。

概念上：

```text
accelerometer
→ 这个位置当前的线性加速度
```

---

# 10. `gyro`

例如：

```xml
<gyro
    name="base_ang_vel"
    site="imu"/>
```

表示：

```text
读取 imu site 的角速度
```

输出：

```text
ωx
ωy
ωz
```

可以理解：

```text
gyro
→ 这个 sensor frame 当前转得多快
```

---

# 11. IMU 总结

典型结构：

```text
site "imu"
↓
framequat
→ orientation

accelerometer
→ acceleration

gyro
→ angular velocity
```

所以和真实机器人中的 IMU 思路非常接近。

---

# 12. `jointpos`

例如：

```xml
<jointpos
    name="pivot_p"
    joint="pivot"/>
```

表示：

```text
读取 pivot joint 的 position
```

对于 hinge joint：

```text
jointpos
→ joint angle
```

对于 slide joint：

```text
jointpos
→ translational position
```

对应的是：

```python
data.qpos
```

中的相关 joint state。

所以可以理解：

```text
jointpos
≈
对某个 joint position 的结构化 sensor 接口
```

---

# 13. `jointvel`

例如：

```xml
<jointvel
    name="pivot_v"
    joint="pivot"/>
```

表示：

```text
读取 joint velocity
```

对于 hinge joint：

```text
jointvel
→ angular velocity
```

对于 slide joint：

```text
jointvel
→ linear velocity
```

对应：

```python
data.qvel
```

中的相关数据。

---

# 14. `jointpos` 和 `jointvel`

最简单的区别：

```text
jointpos
→ joint 现在在哪里

jointvel
→ joint 现在动多快
```

对于 hinge joint：

```text
jointpos
→ rad

jointvel
→ rad/s
```

---

# 15. 直接读取 State 和 Sensor 的区别

MuJoCo 里也可以直接读取：

```python
data.qpos
data.qvel
```

它们属于：

```text
底层系统状态数组
```

而：

```text
jointpos
jointvel
```

更像：

```text
已经命名好的 sensor measurement
```

所以：

```text
qpos / qvel
→ 底层状态

jointpos / jointvel
→ 更结构化的 sensor 接口
```

---

# 16. `rangefinder`

Rangefinder 用来测距离。

例如：

```xml
<rangefinder site="rf"/>
```

它依赖 site 来确定：

```text
ray 起点
+
ray 方向
```

基本逻辑：

```text
site
↓
发出 ray
↓
ray 与 geom 相交
↓
返回距离
```

本质上就是：

```text
ray casting
```

---

# 17. 为什么 Rangefinder 要绑定 Site

测距至少要知道：

```text
从哪里发射
朝哪个方向发射
```

site 正好包含：

```text
position
orientation
```

因此：

```xml
<rangefinder site="rf"/>
```

可以理解成：

```text
从 rf 这个 site 出发
↓
沿 site 的方向发出 ray
↓
测量遇到目标的距离
```

---

# 18. 单线 Rangefinder

一个 rangefinder：

```text
一个 site
↓
一条 ray
↓
一个距离值
```

所以它类似：

```text
single-beam lidar
```

或者简单的 laser distance sensor。

---

# 19. 构建 LiDAR

如果创建很多不同方向的 site：

```text
site 1
site 2
site 3
...
```

并给每个 site 配：

```text
rangefinder
```

就可以得到：

```text
很多 ray
↓
很多 distance samples
↓
类似 point cloud
```

这时候之前学过的：

```text
replicate
```

就可以帮助批量创建 sensor pattern。

---

# 20. Rangefinder 的性能问题

Rangefinder 数量越多：

```text
ray 数越多
↓
碰撞检测 / 求交计算越多
↓
计算量越大
```

所以：

```text
physics simulation
```

可以高频运行，

而：

```text
lidar update
```

不一定需要同样高频。

例如：

```text
physics
→ 500 Hz

lidar
→ 10 Hz / 20 Hz
```

这是实际机器人仿真中很重要的工程思维。

---

# 21. `force`

例如：

```xml
<force
    name="force"
    site="force_torque"/>
```

表示：

```text
在指定 site 上测量力
```

输出：

```text
Fx
Fy
Fz
```

也就是三维 force vector。

---

# 22. `torque`

例如：

```xml
<torque
    name="torque"
    site="force_torque"/>
```

表示：

```text
测量 torque
```

输出：

```text
Tx
Ty
Tz
```

也就是三维 torque vector。

---

# 23. Force / Torque Sensor

把：

```text
force
+
torque
```

放在一起：

```text
3 个 force 分量
+
3 个 torque 分量
=
6 维 measurement
```

这就非常接近真实机器人中的：

```text
6-axis force/torque sensor
```

典型用途：

```text
机械臂 wrist sensor
gripper force
机器人脚底受力
contact measurement
```

---

# 24. 为什么 Force / Torque 使用 Site

site 可以提供：

```text
measurement location
+
measurement coordinate frame
```

所以：

```text
force
torque
```

可以根据该 site 对应的测量坐标系来理解。

---

# 25. Ball Joint Sensor

Ball joint 有：

```text
3 rotational DOF
```

所以不像 hinge：

```text
一个角度就够
```

MuJoCo 提供：

```text
ballquat
ballangvel
```

来读取 ball joint 状态。

---

# 26. `ballquat`

例如：

```xml
<ballquat
    name="ballquat"
    joint="ph"/>
```

表示：

```text
读取 ph 这个 ball joint 的 orientation
```

输出：

```text
quaternion
```

即四个值。

---

# 27. `ballangvel`

例如：

```xml
<ballangvel
    name="ballangvel"
    joint="ph"/>
```

表示：

```text
读取 ball joint angular velocity
```

输出：

```text
ωx
ωy
ωz
```

所以：

```text
ballquat
→ orientation

ballangvel
→ angular velocity
```

---

# 28. 为什么 Ball Joint Orientation 是 4 个值

Ball joint 有：

```text
3 rotational DOF
```

但是姿态使用：

```text
quaternion
```

表示。

quaternion 有：

```text
w
x
y
z
```

四个分量。

但它满足：

```text
||q|| = 1
```

所以虽然有 4 个数，本质上仍然只有：

```text
3 个 independent rotational DOF
```

---

# 29. Hinge 与 Ball Joint Sensor 对比

| Joint 类型 | Position Sensor | Velocity Sensor |
|---|---|---|
| Hinge | `jointpos` | `jointvel` |
| Slide | `jointpos` | `jointvel` |
| Ball | `ballquat` | `ballangvel` |

---

# 30. Frame 系列 Sensor

MuJoCo 里还有一组：

```text
frame...
```

系列 sensor。

包括：

```text
framepos
framequat
framelinvel
frameangvel
framelinacc
frameangacc
```

这些不是只读取一个 joint。

而是：

> 读取某个对象 frame 的运动状态。

---

# 31. `framepos`

例如：

```xml
<framepos
    name="base_pos"
    objtype="body"
    objname="B"/>
```

表示：

```text
读取 body B 的位置
```

输出：

```text
x
y
z
```

如果没有设置 reference：

```text
可以理解成相对于 world frame
```

---

# 32. `framequat`

例如：

```xml
<framequat
    name="base_quat"
    objtype="body"
    objname="B"/>
```

表示：

```text
读取 B 的 orientation
```

输出：

```text
quaternion
```

所以：

```text
framepos
+
framequat
```

组合起来就是：

```text
position
+
orientation
=
pose
```

---

# 33. `framelinvel`

表示：

```text
frame linear velocity
```

输出：

```text
vx
vy
vz
```

可以理解：

```text
这个 frame 平移得多快
```

---

# 34. `frameangvel`

表示：

```text
frame angular velocity
```

输出：

```text
ωx
ωy
ωz
```

可以理解：

```text
这个 frame 转得多快
```

---

# 35. `framelinacc`

表示：

```text
frame linear acceleration
```

输出：

```text
ax
ay
az
```

可以理解：

```text
linear velocity 改变得多快
```

---

# 36. `frameangacc`

表示：

```text
frame angular acceleration
```

输出：

```text
αx
αy
αz
```

可以理解：

```text
angular velocity 改变得多快
```

---

# 37. 相对 Frame Sensor

Frame sensor 还可以使用：

```text
reftype
refname
```

来指定 reference frame。

例如：

```xml
<framepos
    objtype="site"
    objname="end_effector"
    reftype="body"
    refname="base"/>
```

表示：

```text
测量 end_effector
相对于 base
的位置
```

而不是：

```text
相对于 world
```

---

# 38. `obj` 和 `ref` 怎么理解

可以记成：

```text
objtype + objname
→ 我要观察谁

reftype + refname
→ 我站在哪个 frame 看它
```

这和机器人学里的：

```text
world frame
base frame
tool frame
```

完全对应。

---

# 39. Frame Sensor 与机器人运动学

假设：

```text
world
└── base
    └── arm
        └── end_effector
```

如果读取：

```text
end_effector relative to world
```

得到：

```text
global pose
```

如果读取：

```text
end_effector relative to base
```

得到：

```text
robot base frame 下的 end-effector pose
```

这和之前学习的：

```text
coordinate transformation
relative frame
```

直接联系起来。

---

# 40. Subtree Sensor

学习材料还介绍了：

```text
subtreecom
subtreelinvel
subtreeangmom
```

这里的：

```text
subtree
```

表示：

```text
某个 body
+
它下面所有 child body
```

---

# 41. `subtreecom`

表示：

```text
整个 body subtree 的 center of mass
```

例如：

```text
upper_arm
└── forearm
    └── hand
```

如果选：

```text
upper_arm
```

那么：

```text
subtreecom
```

不是只计算 upper_arm。

而是：

```text
upper_arm
+
forearm
+
hand
```

整体的 COM。

---

# 42. `subtreelinvel`

表示：

```text
subtree center of mass 的 linear velocity
```

也就是：

```text
整个 subtree 的综合质心移动速度
```

---

# 43. `subtreeangmom`

表示：

```text
subtree angular momentum
```

可以理解：

```text
整个 body subtree 的整体旋转动量
```

---

# 44. 综合 Sensor 示例

学习中的综合 XML 同时放入了多个 sensor demo。

包括：

```text
free body B
force/torque structure
hinge joint
ball joint
camera
actuator
multiple sensors
```

它的目的不是：

```text
做一个完整真实机器人
```

而是：

> 用一个模型同时演示多种 sensor。

---

# 45. Free Body `B`

例如：

```xml
<body name="B" pos="0 0 0">
    <freejoint/>
    <site name="imu"/>
    ...
</body>
```

`freejoint` 表示：

```text
3 translational DOF
+
3 rotational DOF
```

所以 B 可以在空间中自由运动。

内部：

```xml
<site name="imu"/>
```

可以用来安装：

```text
framequat
accelerometer
gyro
```

等 sensor。

---

# 46. 两个 Camera

示例中有两个 camera。

一个使用：

```text
mode="targetbody"
target="B"
```

它相当于：

```text
外部 camera
→ 始终观察 B
```

另一个 camera 放在 B 内部：

```text
mode="fixed"
```

所以：

```text
camera 跟着 B 一起运动
```

可以对比：

```text
external camera
→ 从外部观察 B

body-mounted camera
→ 固定在 B 上
```

---

# 47. Force / Torque Demo

示例里有：

```text
parent body
└── up_box
    ├── force_torque site
    └── geom
```

然后：

```xml
<force name="force" site="force_torque"/>
<torque name="torque" site="force_torque"/>
```

用于演示：

```text
3D force
+
3D torque
```

---

# 48. Hinge Joint Demo

示例中：

```xml
<joint
    type="hinge"
    name="pivot"
    axis="0 0 1"
    .../>
```

表示：

```text
pivot 是 1 DOF hinge joint
```

对应 sensor：

```xml
<jointpos name="pivot_p" joint="pivot"/>
<jointvel name="pivot_v" joint="pivot"/>
```

所以：

```text
pivot_p
→ pivot angle

pivot_v
→ pivot angular velocity
```

---

# 49. Ball Joint Demo

另一个 joint：

```xml
<joint
    type="ball"
    name="ph"
    .../>
```

表示：

```text
pendulum 可以进行 3 DOF rotation
```

对应：

```xml
<ballquat
    name="ballquat"
    joint="ph"/>

<ballangvel
    name="ballangvel"
    joint="ph"/>
```

得到：

```text
ball joint orientation
+
ball joint angular velocity
```

---

# 50. 综合例子的 Body 层级

整体大致是：

```text
world
└── support
    └── rotay_am
        ├── pivot hinge joint
        ├── horizontal capsule
        └── pendulum
            ├── ph ball joint
            ├── vertical capsule
            └── sphere mass
```

---

# 51. `support`

最外层：

```xml
<body name="support" pos="1 0 0.1">
```

它没有 joint。

所以：

```text
support
→ 固定在 world 上
```

里面有一个 cylinder geom，作为固定支撑。

---

# 52. `rotay_am`

子 body：

```xml
<body name="rotay_am" pos="0 0 0.51">
```

这个位置是：

```text
相对于 support
```

内部：

```xml
<joint
    type="hinge"
    name="pivot"
    axis="0 0 1"
    .../>
```

因此：

```text
rotay_am
→ 可以绕 z 轴旋转
```

---

# 53. Horizontal Capsule

例如：

```xml
<geom
    type="capsule"
    fromto="0 0 0 0.2 0 0"
    size="0.01"
    .../>
```

表示一根：

```text
沿 +x 方向
长度约 0.2
```

的水平杆。

然后：

```xml
<body name="pendulum" pos="0.2 0 0">
```

刚好把 pendulum 放在：

```text
水平杆末端
```

---

# 54. `pendulum`

Pendulum 内部：

```xml
<joint
    type="ball"
    name="ph"
    .../>
```

表示：

```text
pendulum 相对于 parent
可以做 3 DOF rotation
```

内部的 capsule：

```xml
fromto="0 0 0 0 0 -0.3"
```

表示：

```text
沿 -z 方向向下延伸
```

末端 sphere：

```xml
pos="0 0 -0.3"
```

作为：

```text
末端质量
```

---

# 55. 一个 Body 可以有多个 Geom

Pendulum body 中同时有：

```text
capsule
+
sphere
```

这两个不是：

```text
两个独立刚体
```

而是：

```text
同一个 body 的两个 geom
```

所以：

```text
capsule
+
sphere
↓
作为一个刚体一起运动
```

要牢记：

```text
body
→ rigid body

geom
→ body 的 shape
```

---

# 56. Parent-Child Motion

如果：

```text
pivot
```

旋转：

```text
rotay_am
→ 跟着转
```

因为：

```text
pendulum
```

是它的 child body：

```text
pendulum 的 parent frame
→ 也会跟着移动
```

然后：

```text
ph ball joint
```

还可以再产生：

```text
relative rotation
```

所以 child 最终运动：

```text
parent motion
+
child joint relative motion
```

这就是串联机构的基本思想。

---

# 57. 综合例子中的 Actuator

示例里还有：

```xml
<position
    kp="2"
    kv="0.1"
    name="pivot"
    joint="pivot"
    ctrlrange="-3.14 3.14"
    forcerange="-5 5"/>
```

这是之前学过的 position actuator。

控制关系：

```text
data.ctrl
↓
position actuator
↓
pivot joint
↓
rotary arm motion
```

---

# 58. Sensor 与 Actuator 的关系

Actuator：

```text
control input
↓
actuator
↓
改变 joint / body state
```

Sensor：

```text
joint / body state
↓
sensor
↓
measurement
```

组合起来：

```text
control
↓
robot motion
↓
sensor feedback
↓
controller
↓
new control
```

这就是：

```text
feedback control
```

的基础。

---

# 59. 不同 Sensor 输出长度

不同 sensor 输出的数据维度不同。

| Sensor | 常见输出长度 |
|---|---:|
| `jointpos` | 1 |
| `jointvel` | 1 |
| `force` | 3 |
| `torque` | 3 |
| `gyro` | 3 |
| `accelerometer` | 3 |
| `framepos` | 3 |
| `framequat` | 4 |
| `ballquat` | 4 |
| `ballangvel` | 3 |

因此：

```python
data.sensordata
```

本质上就是：

```text
所有启用 sensor 输出
按顺序拼成的数组
```

---

# 60. Python 中读取 Sensor

最简单的 Python：

```python
import mujoco

model = mujoco.MjModel.from_xml_path("model.xml")
data = mujoco.MjData(model)

for _ in range(1000):
    mujoco.mj_step(model, data)
    print(data.sensordata)
```

其中：

```python
mujoco.mj_step(model, data)
```

会：

```text
推进 simulation
+
更新 sensor data
```

然后：

```python
data.sensordata
```

就是当前的 sensor 输出。

---

# 61. 为什么 Sensor Name 很重要

当 sensor 很多时，不应该长期依靠：

```text
第 0 个值是什么
第 1 个值是什么
第 2 个值是什么
```

更好的思路：

```text
sensor name
↓
找到 sensor ID
↓
找到 sensordata address
↓
读取对应区间
```

这样大型模型更清晰。

---

# 62. Sensor 分类

目前学过的 sensor 可以分为几组。

## Joint State Sensor

```text
jointpos
jointvel
ballquat
ballangvel
```

用于读取：

```text
joint state
```

---

## Frame State Sensor

```text
framepos
framequat
framelinvel
frameangvel
framelinacc
frameangacc
```

用于读取：

```text
body / site / geom / camera frame state
```

---

## IMU 类 Sensor

```text
framequat
accelerometer
gyro
```

组合起来可以近似：

```text
IMU
```

---

## Interaction Sensor

```text
force
torque
```

读取：

```text
mechanical interaction
```

---

## Distance Sensor

```text
rangefinder
```

读取：

```text
ray-based distance
```

---

## Subtree Sensor

```text
subtreecom
subtreelinvel
subtreeangmom
```

读取：

```text
body subtree 的整体状态
```

---

# 63. 核心理解

最重要的数据流：

```text
simulation state
↓
sensor definition
↓
measurement
↓
data.sensordata
↓
Python
```

XML 主要负责：

```text
测什么
在哪里测
相对于哪个 frame 测
```

Python 主要负责：

```text
拿到数据以后怎么办
```

例如：

```text
display
save
analyse
control
verify
```

---

# 64. 当前阶段需要记住什么

最重要的对应关系：

```text
site
→ 经常用来定义 sensor location 和 coordinate frame

jointpos
→ joint position

jointvel
→ joint velocity

ballquat
→ ball joint orientation

ballangvel
→ ball joint angular velocity

accelerometer
→ acceleration

gyro
→ angular velocity

force
→ 3D force

torque
→ 3D torque

rangefinder
→ ray-based distance

framepos
→ frame position

framequat
→ frame orientation

framelinvel
→ frame linear velocity

frameangvel
→ frame angular velocity

framelinacc
→ frame linear acceleration

frameangacc
→ frame angular acceleration

subtreecom
→ subtree center of mass
```

更大的整体关系：

```text
actuator
→ 改变机器人状态

sensor
→ 观察机器人状态

Python
→ 把 sensing 和 control 连接起来
```

这就是机器人反馈控制的基础。

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