# 学习进度记录

本文件用于持续记录机器人学习过程中的模块进度、教材来源、运行环境、验证结果与下一步计划。

它不是单纯的待办清单，而是一个长期学习轨迹，用于回答：

- 我学到了什么
- 我实际实现了什么
- 我如何验证
- 使用了哪个教材版本
- 当前进行到哪里
- 下一步准备做什么

---

## 当前教材与环境

| 项目 | 记录 |
| --- | --- |
| 教材来源 | [noBug01/Robot_knowledge_study](https://github.com/noBug01/Robot_knowledge_study) |
| 参考副本目录 | `../knowledge` |
| 当前教材版本 | `v0.2.0` |
| Conda 环境 | `robot_manipulation_learning` |
| Python | `3.11.16` |
| NumPy | `2.4.6` |
| pytest | `8.4.2` |

当某项学习任务依赖特定教材版本时，应在对应 notes 或 experiment report 中保留版本信息。

---

# 学习路线总览

## M0 — Development Workflow

**状态：已完成**

主要内容：

- Windows 本地开发环境搭建
- Conda 环境管理
- Python 环境验证
- Git 基础工作流
- GitHub private repository
- branch / commit / push / pull
- Issue 与 Pull Request
- review 与 merge
- 环境报告与可复现记录

主要成果：

- 完成首次环境验证
- 建立个人学习仓库
- 完成第一个 Issue
- 建立 feature branch
- 完成 Pull Request
- review 后 merge 到 `main`

相关记录：

- `experiments/environment_reports/`

---

## M1 — Robot Math Foundations

**状态：已完成**

M1 当前已经完成两个主要学习部分：

1. Python 与 NumPy 数值基础
2. Robot Geometry：坐标、旋转与刚体变换

---

## M1.1 — Python 与 NumPy 基础

**状态：已完成**

### 已学习内容

- Python 函数与模块
- `import`
- 类型提示
- NumPy 数组
- `shape`
- `ndim`
- `dtype`
- 索引与切片
- `None` 插入新轴
- view 与 copy
- broadcasting
- 向量长度
- `np.linalg.norm`
- `*` 与 `@`
- 物理单位管理
- 浮点误差
- `np.allclose`
- `np.testing.assert_allclose`
- `pytest`
- 输入 shape 检查
- `translate_points`

### 学习笔记

英文：

- [Python and NumPy Foundations](notes/m1/python_numpy.md)

中文：

- [Python 与 NumPy 基础](notes/m1/python_numpy_zh.md)

### 可运行代码

```text
examples/numeric_basics.py
```

### 自动测试

```text
tests/test_numeric_basics.py
```

### 实验记录

英文：

- [Numeric Basics Experiment Report](experiments/m1/numeric_basics_report.md)

中文：

- [NumPy 数值基础实验报告](experiments/m1/numeric_basics_report_zh.md)

### 当前验证结果

运行：

```bash
python -m examples.numeric_basics
```

自动测试：

```bash
python -m pytest tests/test_numeric_basics.py -q
```

实际结果：

```text
22 passed in 0.17s
```

### 主要理解

这一部分最重要的认识包括：

- 数组运算前应先理解 shape
- `(N,)`、`(1,N)` 和 `(N,1)` 含义不同
- broadcasting 能运行不代表数学意义正确
- `@` 与 `*` 必须区分
- NumPy 不会自动管理物理单位
- 浮点数通常需要使用容差比较
- 自动测试只能验证已经覆盖的条件

---

## M1.2 — Robot Geometry

**状态：已完成**

### 已学习内容

- 坐标系
- 同一个点在不同坐标系中的表达
- 列向量
- 旋转矩阵
- $R_{ab}$ 的含义
- 旋转矩阵各列的几何意义
- 绕 x、y、z 轴旋转
- 右手定则
- 正交矩阵
- determinant
- 长度保持
- 坐标系原点之间的平移
- 刚体变换
- 齐次坐标
- 点与方向向量
- 多级坐标变换
- transform composition
- inverse transform
- round-trip validation
- 坐标系可视化

### 学习笔记

英文：

- [Robot Geometry](notes/m1/robot_geometry.md)

中文：

- [机器人几何：坐标、旋转与刚体变换](notes/m1/robot_geometry_zh.md)

### 可运行代码

```text
algorithms/geometry/
examples/coordinate_frames.py
```

### 自动测试

```text
tests/test_rigid_transform.py
tests/test_coordinate_frames.py
```

### 实验记录

英文：

- [Robot Geometry Experiment Report](experiments/m1/robot_geometry_report.md)

中文：

- [机器人几何实验报告](experiments/m1/robot_geometry_report_zh.md)

### 可视化结果

```text
outputs/m1/frames.svg
```

### 当前验证结果

运行：

```bash
python -m examples.coordinate_frames --output outputs/m1/frames.svg
```

自动测试：

```bash
python -m pytest tests/test_rigid_transform.py tests/test_coordinate_frames.py -q
```

实际结果：

```text
54 passed in 0.41s
```

关键运行结果：

```text
p_w = [[2. 1. 0.]]
p_b_roundtrip = [[1. 0. 0.]]
max round-trip error = 0.000e+00 m
```

### 主要理解

这一部分最重要的认识包括：

- 同一个物理点在不同坐标系中可以有不同坐标
- 坐标必须和参考坐标系一起理解
- $R_{ab}$ 表示 B 到 A 的坐标表达转换
- 旋转矩阵的列表示坐标轴方向
- 合法旋转需要满足 $R^TR=I$ 与 $\det(R)=1$
- 平移向量必须先统一坐标系才能相加
- 刚体变换核心公式为：

```math
p_a=R_{ab}p_b+t_{ab}
```

- 齐次变换可以统一表示旋转和平移
- 多级变换顺序不能只根据矩阵 shape 判断
- 逆平移通常不是简单的 `-t`
- 往返验证、手算、测试和可视化需要结合使用

### M1.3 几何实现 — 已完成

完成了 M1 中与实现相关的部分，将前面学习的刚体变换数学对应到可复用的 NumPy 程序接口。

已学习内容：

- `rotation_z`
- `make_transform`
- `inverse_transform`
- `transform_points`
- 有限数值输入检查
- 严格的数组 shape 检查
- proper rotation matrix 合法性验证
- 浮点数容差
- `translate_points`
- 数值示例的程序结构
- 坐标系示例的程序结构
- 坐标变换组合顺序
- 逆变换一致性
- 往返验证

学习笔记：

- [Geometry Implementation](notes/m1/geometry_implementation.md)
- [几何实现](notes/m1/geometry_implementation_zh.md)

相关实现与示例：

- `algorithms/geometry/`
- `examples/numeric_basics.py`
- `examples/coordinate_frames.py`

### M1.4 测试与能力任务 — 已完成

已完成 M1 测试说明、测试代码阅读以及六项能力任务。

任务状态：

```text
PYNUM-T01  Completed
PYNUM-T02  Completed
GEOM-T01   Completed
GEOM-T02   Completed
GEOM-T03   Completed
GEOM-T04   Completed
---

### M1.5 Modern Robotics 教材阅读 — 已完成

实际阅读教材：

Kevin M. Lynch, Frank C. Park, *Modern Robotics: Mechanics, Planning, and Control*, Cambridge University Press, 2017.

本次 M1 阅读范围：

```text
Section 3.2.1 — Rotation Matrices
Section 3.3.1 — Homogeneous Transformation Matrices
```

# M1 当前成果汇总

## 学习笔记

```text
```text
notes/m1/
├── python_numpy.md
├── python_numpy_zh.md
├── robot_geometry.md
├── robot_geometry_zh.md
├── geometry_implementation.md
├── geometry_implementation_zh.md
├── modern_robotics_reading.md
└── modern_robotics_reading_zh.md
```

## 实验记录

```text
experiments/m1/
├── README.md
├── numeric_basics_report.md
├── numeric_basics_report_zh.md
├── robot_geometry_report.md
├── robot_geometry_report_zh.md
├── capability_tasks_report.md
└── capability_tasks_report_zh.md
```

## 实现与测试

```text
algorithms/geometry/
examples/numeric_basics.py
examples/coordinate_frames.py
examples/m1_solution.py
tests/test_numeric_basics.py
tests/test_rigid_transform.py
tests/test_coordinate_frames.py
tests/test_m1_solution.py
```

## 自动化验证

```text
Python / NumPy: 22 tests passed
Robot Geometry: 54 tests passed
Full repository: 107 tests passed
```

目前累计：

```text
76 tests passed
```

这里的 76 仅指上述 M1 两部分当前实际执行的测试数量，不代表整个仓库未来所有测试的固定总数。

---

## M2 - MuJoCo 仿真

状态：**进行中**

M2 当前包含两个不同上游来源的 MuJoCo 学习内容。为了保持学习来源和进度清晰，两条学习线分开记录。

---

### 来源 A - Albusgive MuJoCo Learning

来源仓库：

https://github.com/Albusgive/mujoco_learning.git

状态：**进行中**

目前已完成：

- MuJoCo 环境配置
- MJCF 基本结构
- compiler 设置
- simulation option
- timestep 与 gravity
- visual 配置
- asset 系统
- texture
- material
- mesh
- skybox
- `geom`
- 几何体类型
- mass 与 density
- friction
- collision 相关属性
- `body`
- 父子 body 层级
- 相对坐标系
- `site`
- joint 类型
- hinge joint
- joint axis
- joint range
- damping
- stiffness
- frictionloss
- armature
- 简单单摆建模
- 单摆仿真与验证

当前进度：

```text
Environment and Assets
→ 已完成

Geom, Body and Site
→ 已完成

Joint
→ 已完成

Pendulum Experiment
→ 已完成

后续 MuJoCo 内容
→ 进行中
```

### 来源 B - Robot Knowledge Study

来源仓库：

https://github.com/noBug01/Robot_knowledge_study

使用版本：

```text
v0.3.0
```

状态：**已完成**

当前该来源的 M2 内容一共包含两个场景：

```text
SIM-T01
→ 桌面与自由下落方块

SIM-T02
→ 机械臂关节角目标控制
```

#### SIM-T01 - 桌面与自由下落方块

已完成：

- M2 独立 MuJoCo 环境
- Python 3.10 环境检查
- MuJoCo 3.9.0 版本检查
- 场景 XML 阅读
- floor、table、cube、camera、light 结构
- free joint 行为
- 方块与桌面初始间隙计算
- `MjModel`
- `MjData`
- `mj_forward`
- `mj_step`
- `qpos`
- `qvel`
- `data.ncon`
- 第 0 步状态记录
- 两步连续性检查
- 200 步完整仿真
- CSV 输出
- contact observation
- 最终方块高度预测
- 100 步个人预测与验证
- `pytest` 自动测试
- 独立 MuJoCo Viewer
- Python 控制 Viewer
- Viewer 调试功能

关键结果：

```text
方块初始中心高度：
1.05 m

预测稳定中心高度：
0.80 m

实际稳定中心高度：
≈ 0.7999 m
```

核心流程：

```text
XML
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
数值与视觉验证
```

#### SIM-T02 - 机械臂关节角目标控制

已完成：

- 多 XML 文件场景结构
- XML `<include>`
- robot mesh asset
- visual mesh 与 collision mesh
- `<default>` 参数模板
- 机器人 body 层级结构
- 父 body / 子 body / 更深层 body
- 一个 body 下多个 geom
- 左臂 7 个 joint
- 右臂结构
- joint `axis`
- joint `range`
- position actuator
- actuator `ctrlrange`
- `data.ctrl`
- target 与 actual joint position
- `qpos`
- `qvel`
- `left_tool` site
- `jointpos` sensor
- `jointvel` sensor
- `framepos` sensor
- `framequat` sensor
- contact exclusion
- waypoint joint target
- 线性插值
- 使用 `qpos` 初始化姿态
- 使用 `data.ctrl` 进行正常控制
- 基于 `mj_step` 的机械臂运动
- sensor sampling
- `mj_forward` 刷新 sensor
- 末端位置读取
- 末端姿态读取
- target 与 actual 对比
- Viewer 中观察机械臂运动
- Viewer timing
- Python 控制程序整体流程理解

运动时间线验证：

```text
0–5 s
→ 保持初始姿态

5–9 s
→ Waypoint A → B

9–13 s
→ Waypoint B → C

13–17 s
→ Waypoint C → A

17–17.5 s
→ 最终保持
```

总仿真时间：

```text
17.5 s
```

在：

```text
timestep = 0.001 s
```

条件下，对应约：

```text
17500 个 physics step
```

核心控制链：

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
sensor feedback
↓
end-effector pose
```

最重要的区别：

```text
target
≠
actual state
```

其中：

```text
data.ctrl
→ 目标 actuator 输入

qpos
→ 实际 joint position
```

这一来源的 M2 内容已经全部完成。

# 学习方法

当前采用的学习流程：

```text
教材学习
    ↓
理解数学与概念
    ↓
手算 / 独立推导
    ↓
运行示例
    ↓
阅读与理解代码
    ↓
自动化测试
    ↓
记录错误与修正
    ↓
整理双语 Notes
    ↓
整理 Experiment Evidence
    ↓
Git commit / PR / merge
```

目标不是单纯完成教程，而是让每个学习模块尽量具备：

- 可理解
- 可实现
- 可运行
- 可测试
- 可复现
- 可回顾
- 可展示

---

# 当前仓库证据结构

```text
README.md
    ↓
仓库总入口与成果展示

notes/
    ↓
我理解了什么

examples/ + algorithms/
    ↓
我实际运行和实现了什么

tests/
    ↓
我如何自动验证

experiments/
    ↓
我实际观察到了什么结果

progress.md
    ↓
我整个学习过程如何持续推进
```

---

## 下一步

M1 — Robot Math Foundations 已完成。

下一阶段根据实际项目目标选择后续机器人模块，并检查对应前置知识。候选方向包括：

- robot kinematics
- simulation
- control systems
- ROS 2
- perception
- SLAM

微分、概率、优化、动力学等数学与工程知识将在后续模块需要时继续补充。

在进入下一模块之前，需要保证：

- 当前 `main` 与远程同步
- working tree clean
- 相关 notes 已更新
- experiment evidence 已保存
- 测试实际重新运行
- README / progress 链接仍然有效

---

# 维护原则

每完成一个新的学习模块，都应至少记录：

1. 教材来源与版本
2. 学习内容
3. 自己的理解
4. 可运行代码
5. 自动化测试
6. 实际执行结果
7. 实验或可视化证据
8. 错误与修正
9. Git commit
10. PR / merge

这样可以让仓库长期保持清晰，并成为真正可复查的机器人学习记录。