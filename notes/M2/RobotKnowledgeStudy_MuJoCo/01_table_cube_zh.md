# SIM-T01 - 桌面与自由下落方块

[English](01_table_cube.md) | [中文](01_table_cube_zh.md)

---

## 概览

这个场景通过一个简单的“桌子 + 方块”模型，介绍了 MuJoCo 的基础仿真流程。

本场景主要学习：

- MJCF XML 如何定义几何体和物理属性
- Python 如何加载 XML 模型
- `MjModel` 和 `MjData` 分别承担什么作用
- 仿真如何通过 `mj_step` 一步一步推进
- 如何读取位置、速度和接触信息
- 如何通过数值结果和 Viewer 检查仿真行为

场景中包含：

- 地面
- 桌子
- 一个自由下落的方块
- 两个固定相机
- 灯光

方块在重力作用下下落，与桌面接触，最后逐渐稳定。

---

## 1. 场景结构

主要 XML 结构可以概括为：

```text
mujoco
├── option
└── worldbody
    ├── light
    ├── camera: front_view
    ├── camera: top_view
    ├── floor geom
    ├── table top geom
    ├── 四个 table-leg geom
    └── cube body
        ├── freejoint
        └── cube geom
```

这个结构体现了一个重要的 MuJoCo 规则：

```text
直接写在 worldbody 下面的 geom
→ 固定在世界中

body + joint
→ 可以运动的刚体
```

---

## 2. 仿真设置

场景中使用：

```xml
<option timestep="0.005" gravity="0 0 -9.81"/>
```

表示：

```text
timestep = 0.005 s
gravity = (0, 0, -9.81) m/s²
```

每调用一次：

```python
mujoco.mj_step(model, data)
```

仿真时间就前进：

```text
0.005 s
```

---

## 3. 桌面几何

桌面通过 box geom 定义：

```xml
<geom name="table_top"
      type="box"
      pos="0 0 0.725"
      size="0.5 0.35 0.025"/>
```

MuJoCo 中 box 的 `size` 表示半尺寸。

因此桌面的完整尺寸为：

```text
长 = 1.00 m
宽 = 0.70 m
厚 = 0.05 m
```

桌面中心高度为：

```text
z = 0.725 m
```

所以桌面上表面高度为：

```text
0.725 + 0.025 = 0.750 m
```

---

## 4. 方块定义

方块定义为：

```xml
<body name="cube" pos="0 0 1.05">
    <freejoint name="cube_free"/>
    <geom name="cube_geom"
          type="box"
          size="0.05 0.05 0.05"
          mass="0.1"/>
</body>
```

方块 body 的初始中心高度：

```text
z = 1.05 m
```

方块半高：

```text
0.05 m
```

因此方块底面初始高度为：

```text
1.05 - 0.05 = 1.00 m
```

方块与桌面的初始间隙为：

```text
1.00 - 0.75 = 0.25 m
```

---

## 5. Free Joint 的作用

方块包含：

```xml
<freejoint name="cube_free"/>
```

Free joint 给予方块：

```text
3 个平移自由度
+
3 个旋转自由度
```

因此方块不是固定的，可以在重力作用下自由下落。

核心关系为：

```text
body
→ 刚体

freejoint
→ 允许刚体自由运动

geom
→ 定义形状、质量、外观和碰撞几何
```

---

## 6. Model 与仿真状态

Python 使用：

```python
model = mujoco.MjModel.from_xml_path(...)
data = mujoco.MjData(model)
```

加载模型。

这两个对象作用不同：

```text
model
→ 模型结构和固定的仿真规则

data
→ 当前时刻的仿真状态
```

`model` 中包含例如：

```text
几何结构
质量
重力
关节
timestep
```

而 `data` 中保存：

```text
当前时间
位置
速度
接触
控制输入
传感器数据
```

---

## 7. 初始状态

正式推进仿真前，程序先执行：

```python
mujoco.mj_forward(model, data)
```

它会计算当前状态下的派生结果，但不会推进仿真时间。

随后记录初始状态：

```python
samples = [observe(data)]
```

于是产生第 0 步记录：

```text
time = 0.000 s
```

因为这条记录发生在循环之前，所以：

```text
200 个仿真步
+
1 条初始记录
=
201 条记录
```

---

## 8. 仿真如何推进

每一次循环按下面顺序执行：

```python
mujoco.mj_step(model, data)
mujoco.mj_forward(model, data)
samples.append(observe(data))
```

作用分别为：

```text
mj_step
→ 推进一个物理步长

mj_forward
→ 重新计算当前状态下的派生结果
→ 不推进时间

observe
→ 记录当前状态
```

整个过程中始终复用同一个 `data` 对象。

仿真并不会在每一步重新从初始状态开始。

---

## 9. 读取哪些状态

程序记录四个主要数值：

```text
time_s
cube_z_m
cube_vz_m_s
contact_count
```

分别对应：

```python
data.time
```

```python
data.joint("cube_free").qpos[2]
```

```python
data.joint("cube_free").qvel[2]
```

```python
data.ncon
```

对于 free joint：

```text
qpos[0] = x
qpos[1] = y
qpos[2] = z
```

剩余 4 个 `qpos` 值表示四元数姿态。

Free joint 的 `qvel` 包含：

```text
3 个平移速度
+
3 个角速度
```

所以：

```text
qvel[2]
```

就是方块沿 z 方向的速度。

---

## 10. 前两步验证

程序先运行两步，用来验证状态是否连续变化。

典型输出：

```text
time_s cube_z_m cube_vz_m_s contact_count

0.000  1.0500   0.0000    0
0.005  1.0498  -0.0491    0
0.010  1.0493  -0.0981    0
```

说明：

```text
时间持续增加
方块高度持续下降
竖直速度越来越负
接触数仍然为 0
```

说明方块正在重力作用下加速下落。

---

## 11. 完整 200 步仿真

运行：

```text
200 steps
```

且：

```text
timestep = 0.005 s
```

所以总仿真时间为：

```text
200 × 0.005 = 1.000 s
```

方块开始时自由下落。

当与桌面接触后：

```text
contact_count
从 0 变为正数
```

随后方块会经历轻微的接触响应，最后逐渐稳定。

---

## 12. 最终高度预测

桌面上表面高度：

```text
0.75 m
```

方块半高：

```text
0.05 m
```

所以方块稳定后，中心高度预计为：

```text
0.75 + 0.05 = 0.80 m
```

实际仿真结果约为：

```text
0.7999 m
```

与几何预测非常接近。

---

## 13. Contact Count

程序使用：

```python
data.ncon
```

查看当前激活的接触点数量。

典型情况：

```text
方块在空中
→ contact_count = 0

方块落在桌面上
→ contact_count > 0
```

本场景中，方块稳定后得到：

```text
contact_count = 4
```

它表示检测到的接触点数量。

它并不直接表示接触力大小。

---

## 14. 100 步预测实验

为了验证理解，又额外运行了 100 步。

因为：

```text
100 × 0.005 = 0.500 s
```

所以预期最终仿真时间为：

```text
0.500 s
```

预测稳定状态：

```text
cube_z ≈ 0.80 m
cube_vz ≈ 0
```

实际结果约为：

```text
time = 0.500 s
cube_z = 0.7999 m
cube_vz = 0.0001 m/s
contact_count = 4
```

与预测一致。

---

## 15. CSV 输出

程序可以把每一步状态保存到 CSV。

这样可以分析：

- 方块何时开始下落
- 首次接触发生在什么时候
- 竖直速度如何变化
- 方块什么时候逐渐静止
- 最终高度是否符合预测

CSV 提供的是完整的数值时间历史，而不仅仅是动画效果。

---

## 16. 自动测试

本场景使用 `pytest` 进行自动测试。

自动测试用于验证模型结构和基本仿真行为。

实际运行结果为：

```text
3 passed
```

说明本场景的自动测试全部通过。

---

## 17. Viewer

本场景也可以使用 MuJoCo Viewer 进行观察。

主要有两种方式。

### 独立 Viewer

直接打开 XML：

```bash
python -m mujoco.viewer --mjcf=simulation/mujoco/scenes/sim_t01_table_cube/scene.xml
```

适合：

- 暂停 / 继续
- Reset
- 切换 Camera
- 检查几何结构
- 查看接触点与接触力
- 手动探索场景

### Python 控制 Viewer

Python 脚本也可以启动被动 Viewer：

```bash
python -m examples.mujoco.sim_t01_table_cube --steps 400 --viewer
```

此时：

```text
Python 负责 mj_step
Viewer 负责显示当前状态
```

---

## 18. Viewer 作为调试工具

常用 Viewer 功能包括：

```text
F2
→ 查看仿真信息

C
→ 显示接触点

F
→ 显示接触力

W
→ Wireframe

T
→ Transparent

[ / ]
→ 在固定相机之间切换

Esc
→ 回到自由相机
```

因此 Viewer 不只是用于看动画。

它也可以用于检查和验证仿真行为。

---

## 19. 核心理解

整个仿真流程可以总结为：

```text
XML 定义物理场景
↓
MjModel 加载模型
↓
MjData 保存当前状态
↓
mj_step 推进物理仿真
↓
qpos / qvel / contact 发生变化
↓
observe 记录状态
↓
CSV 与 Viewer 提供数值和视觉验证
```

最重要的概念区别是：

```text
XML
→ 定义场景中有什么，以及物理规则是什么

Python
→ 决定如何推进仿真，以及如何读取结果
```

这个场景标志着学习从静态 MJCF 建模进入程序化 MuJoCo 仿真。

---

## 来源

本笔记基于以下 M2 `SIM-T01` 学习材料：

```text
Robot_knowledge_study
v0.3.0
```

来源仓库：

https://github.com/noBug01/Robot_knowledge_study

原始仓库与教学材料归对应作者所有。

本文记录的是我在学习过程中的个人理解、计算、仿真验证与总结，并不是对原始教材内容的直接复制。