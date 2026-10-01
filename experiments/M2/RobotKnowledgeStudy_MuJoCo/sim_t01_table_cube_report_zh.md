# SIM-T01 实验报告 - 桌面与自由下落方块

[English](sim_t01_table_cube_report.md) | [中文](sim_t01_table_cube_report_zh.md)

---

## 实验目标

这个实验复现 `Robot_knowledge_study` M2 中的第一个 MuJoCo 仿真场景。

主要目的是验证我是否能够：

- 使用 Python 加载 MJCF 场景
- 使用 `mj_step` 推进仿真
- 读取位置和速度
- 检测接触
- 将仿真结果与简单物理预测进行比较
- 使用 MuJoCo Viewer 检查场景
- 使用自动测试验证实现结果

---

## 场景

本实验使用：

```text
simulation/mujoco/scenes/sim_t01_table_cube/scene.xml
```

场景中包含：

- 地面
- 桌子
- 一个可以自由运动的方块
- 重力
- 两个固定相机
- 灯光

方块初始位于桌面上方，并在重力作用下下落。

---

## 初始几何检查

桌面中心高度为：

```text
z = 0.725 m
```

桌面半厚度为：

```text
0.025 m
```

因此桌面上表面高度为：

```text
0.725 + 0.025
=
0.750 m
```

方块中心初始高度为：

```text
z = 1.05 m
```

方块半高为：

```text
0.05 m
```

因此方块底面初始高度为：

```text
1.05 - 0.05
=
1.00 m
```

所以方块和桌面的初始间隙为：

```text
1.00 - 0.75
=
0.25 m
```

---

## 仿真设置

场景使用：

```xml
<option timestep="0.005" gravity="0 0 -9.81"/>
```

因此：

```text
物理仿真步长 = 0.005 s
重力 = z 方向 -9.81 m/s²
```

---

## Python 仿真流程

核心 Python 流程为：

```text
加载 XML
↓
创建 MjModel
↓
创建 MjData
↓
计算初始状态
↓
记录初始状态
↓
不断执行 mj_step
↓
记录更新后的状态
```

两个最重要的对象是：

```text
MjModel
→ 模型结构和固定仿真规则

MjData
→ 当前动态仿真状态
```

---

## 读取的状态变量

本实验主要记录：

```text
仿真时间
方块 z 位置
方块 z 速度
接触点数量
```

分别来自：

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

---

## 两步验证

第一次只运行两个仿真步。

观察结果大约为：

```text
0.000 s
z = 1.0500 m
vz = 0.0000 m/s
contact = 0

0.005 s
z = 1.0498 m
vz = -0.0491 m/s
contact = 0

0.010 s
z = 1.0493 m
vz = -0.0981 m/s
contact = 0
```

这说明：

```text
时间连续增加
方块高度持续下降
向下速度绝对值逐渐增大
初始阶段没有发生接触
```

说明仿真状态是连续推进的，而不是每一步重新开始。

---

## 200 步完整仿真

完整仿真运行：

```text
200 steps
```

每一步：

```text
0.005 s
```

因此总仿真时间为：

```text
200 × 0.005
=
1.000 s
```

方块开始时自由下落，随后与桌面接触，经历轻微回弹，最后逐渐稳定。

---

## 接触观察

碰撞前：

```text
contact_count = 0
```

方块接触桌面后：

```text
contact_count > 0
```

最终稳定时：

```text
contact_count = 4
```

这个值表示当前激活的接触点数量。

它并不直接表示接触力大小。

---

## 最终高度预测

预计方块稳定后中心高度为：

```text
桌面上表面
+
方块半高
```

也就是：

```text
0.750 + 0.050
=
0.800 m
```

实际仿真结果约为：

```text
0.7999 m
```

与几何预测非常接近。

---

## 100 步个人验证

另外又进行了一个 100 步仿真，用于独立预测和验证。

预测仿真时间：

```text
100 × 0.005
=
0.500 s
```

预测最终状态：

```text
cube z ≈ 0.80 m
cube vz ≈ 0
```

实际结果：

```text
time = 0.500 s
cube_z ≈ 0.7999 m
cube_vz ≈ 0.0001 m/s
contact_count = 4
```

预测结果得到验证。

---

## 运动过程解释

整个运动过程可以概括为：

```text
方块初始位于桌面上方
↓
重力使方块向下加速
↓
方块接触桌面
↓
接触响应造成轻微回弹
↓
速度逐渐减小
↓
方块最终稳定在 z ≈ 0.80 m
```

这个实验展示了从自由运动到接触约束运动的完整过程。

---

## CSV 输出

程序可以把完整仿真状态保存为 CSV。

这样可以数值分析：

- 方块何时开始下降
- 速度如何变化
- 首次接触何时发生
- 方块如何发生轻微回弹
- 何时逐渐稳定
- 最终高度是否符合预测

CSV 提供了完整的数值时间历史，而不仅仅依赖 Viewer 动画。

---

## 自动测试

本实验运行了教材提供的 `pytest` 自动测试。

结果为：

```text
3 passed
```

说明场景和仿真行为通过了对应测试。

---

## Viewer 检查

本场景也通过 MuJoCo Viewer 进行了观察。

Viewer 用于：

- 检查桌子和方块几何结构
- 观察方块下落
- 查看接触行为
- 切换相机
- 理解独立 Viewer 与 Python 控制 Viewer 的区别

两种常用运行方式为：

```bash
python -m mujoco.viewer --mjcf=simulation/mujoco/scenes/sim_t01_table_cube/scene.xml
```

以及：

```bash
python -m examples.mujoco.sim_t01_table_cube --steps 400 --viewer
```

第一种方式：

```text
Viewer 直接加载 XML
```

第二种方式：

```text
Python 负责推进物理仿真
Viewer 负责显示当前状态
```

---

## 主要学习收获

这个实验完成了从静态 MJCF 建模到程序化 MuJoCo 仿真的过渡。

最重要的流程是：

```text
XML 场景
↓
MjModel
↓
MjData
↓
mj_step
↓
qpos / qvel / contact 更新
↓
状态读取
↓
数值和视觉验证
```

最重要的区别是：

```text
XML
→ 定义模型和物理环境

Python
→ 推进仿真并读取结果
```

---

## 来源

本实验基于：

```text
Robot_knowledge_study
M2
SIM-T01
v0.3.0
```

来源仓库：

https://github.com/noBug01/Robot_knowledge_study

原始仓库与教学材料归对应作者所有。

本文记录的是我自己的仿真过程、计算、观察、验证与理解。