# Robot Learning Practice

[English](README.md) | [中文](README_zh.md)

一个结构化、可复现的机器人学习记录，包含学习笔记、代码实现、实验、验证以及持续的技术积累。

## 关于本仓库

这个仓库记录我长期学习机器人的过程。

学习从数学、编程和机器人基础开始，并逐步扩展到更完整、更复杂的机器人系统。

每一个学习模块都会尽可能包含：

- 理论笔记
- 独立实现
- 自动化测试
- 实验
- 可复现结果
- 对错误与修正过程的记录

目标不仅仅是完成教程，而是建立一个清晰的长期记录，展示：

```text
我理解了什么
我实现了什么
我验证了什么
我在哪里犯过错误
我又是如何改进的
```

---

## 学习来源

本仓库使用多个上游仓库作为主要学习材料来源。

### M1 - Robot Math and Geometry

M1 的主要学习来源是：

- [Robot Knowledge Study](https://github.com/noBug01/Robot_knowledge_study.git)

这个上游仓库主要作为以下内容的学习参考：

- Python 与 NumPy 基础
- Robot Geometry
- Rigid Transformations
- Geometry Implementation
- Modern Robotics 阅读及相关数学基础

---

### M2 - MuJoCo Simulation

M2 的 MuJoCo 学习目前来自两个不同的上游来源：

- [MuJoCo Learning](https://github.com/Albusgive/mujoco_learning.git)
- [Robot Knowledge Study](https://github.com/noBug01/Robot_knowledge_study)

其中，Albusgive 来源主要用于系统学习 MJCF 建模与 MuJoCo 功能，包括：

- MuJoCo XML / MJCF 结构
- simulation configuration
- visual settings
- assets 与 materials
- geometries
- body hierarchy
- sites
- joints
- contact 与 friction
- actuator models
- lighting
- 使用 `replicate` 构建重复模型结构
- tendon transmission 与 joint coupling
- sensor modeling 与 observation

Robot Knowledge Study 来源则进一步把 MuJoCo 学习扩展到：

- Python 驱动仿真
- state observation
- actuator control
- sensor feedback
- robot-arm motion

本仓库并不是为了复制这些上游仓库。

这里记录的是我自己的学习过程，包括：

- 个人学习笔记与总结
- 独立实现
- simulation experiments
- automated tests
- reports 与 validation
- corrections 与 refinements

当某个学习任务依赖特定版本或 commit 时，会在对应的 progress 或 experiment 文档中记录其来源信息。

非常感谢这些上游仓库作者与贡献者无私分享知识、代码与学习材料。

这些内容为我系统学习机器人提供了非常重要的基础。

如果没有这些作者的分享，这个仓库也无法以现在的形式建立起来。

---

## 当前进度

| Module | Topic | Status | Learning Notes | Experiment Evidence |
|---|---|---|---|---|
| M0 | 环境配置与 Git 工作流 | Completed | - | [Environment Reports](experiments/environment_reports/) |
| M1 | Python、NumPy、机器人几何、刚体变换、测试、能力任务与 Modern Robotics 阅读 | Completed | [M1 Notes](notes/M1/) | [M1 Experiments](experiments/M1/) |
| M2 | MuJoCo 仿真、MJCF 建模、接触、执行器、tendon、sensor、场景构建与 Python 控制 | In Progress | [M2 Notes](notes/README.md) | [M2 Experiments](experiments/M2/) |

---

# M1 - Robot Math and Geometry

M1 目前包含三个已经完成的主要学习模块。

## Python 与 NumPy 基础

学习内容包括：

- array shape、dimensions 与 data types
- indexing 与 slicing
- views 与 copies
- broadcasting
- vector 与 matrix operations
- floating-point numerical checks
- 使用 `pytest` 进行 automated testing

学习笔记：

- [English](notes/m1/python_numpy.md)
- [中文](notes/m1/python_numpy_zh.md)

实验记录：

- [English](experiments/m1/numeric_basics_report.md)
- [中文](experiments/m1/numeric_basics_report_zh.md)

---

## Robot Geometry 与 Rigid Transforms

学习内容包括：

- coordinate frames
- rotation matrices
- rigid-body transformations
- homogeneous coordinates
- transform composition
- inverse transforms
- round-trip validation
- coordinate-frame visualization

学习笔记：

- [English](notes/m1/robot_geometry.md)
- [中文](notes/m1/robot_geometry_zh.md)

实验记录：

- [English](experiments/m1/robot_geometry_report.md)
- [中文](experiments/m1/robot_geometry_report_zh.md)

生成的可视化：

- [`outputs/m1/frames.svg`](outputs/m1/frames.svg)

---

## Geometry Implementation

前面的数学概念进一步被整理成可重复使用的 NumPy 实现，并加入明确的输入验证和接口约束。

主要包括：

- `rotation_z`
- `make_transform`
- `inverse_transform`
- `transform_points`
- finite numeric input validation
- strict array shape validation
- proper rotation matrix validation
- floating-point tolerance
- transform composition order
- round-trip consistency checks
- numerical 与 coordinate-frame examples 的结构

学习笔记：

- [English](notes/m1/geometry_implementation.md)
- [中文](notes/m1/geometry_implementation_zh.md)

---

## 教材阅读

M1 阶段完成了 *Modern Robotics: Mechanics, Planning, and Control* 中当前规划的阅读内容：

- Section 3.2.1 — Rotation Matrices
- Section 3.3.1 — Homogeneous Transformation Matrices

主要强化和新增理解包括：

- `SO(3)` 与 proper rotations
- `SE(3)` rigid transformations
- frame-subscript cancellation
- transform composition 与 inversion
- fixed-frame 与 body-frame transform updates

阅读笔记：

- [English](notes/m1/modern_robotics_reading.md)
- [中文](notes/m1/modern_robotics_reading_zh.md)

当前 automated verification：

```text
Python / NumPy:    22 tests passed
Robot Geometry:    54 tests passed
Full repository:   107 tests passed
```

---

# M2 - MuJoCo Simulation

M2 目前包含两个不同来源的 MuJoCo 学习流。

这两个来源会持续保持分开，因为它们关注的重点不同，并且学习进度也是独立推进的。

---

## Source A - Albusgive MuJoCo Learning

来源仓库：

```text
https://github.com/Albusgive/mujoco_learning.git
```

这一学习流目前主要用于学习：

```text
MJCF modeling fundamentals
physical interaction
actuator models
tendon transmission
sensor modeling
scene construction
```

当前已经学习的内容包括：

- MuJoCo XML / MJCF structure
- simulation configuration
- environment and assets
- textures、materials、meshes 与 skyboxes
- `geom`
- `body`
- `site`
- body hierarchy
- relative coordinate frames
- friction 与 collision settings
- joint types
- hinge joints
- joint axis 与 range
- damping
- stiffness
- friction loss
- armature
- simple pendulum simulation
- sliding friction
- torsional friction
- rolling friction
- `friction="a b c"`
- `condim`
- elliptic friction cones
- pyramidal friction cones
- friction constraint dimensions
- contact `priority`
- contact parameter selection
- `impratio`
- actuator fundamentals
- `general`
- `motor`
- `position`
- `velocity`
- `intvelocity`
- `damper`
- `cylinder`
- `data.ctrl`
- `ctrlrange`
- `forcerange`
- `actrange`
- `gear`
- `kp`
- `kv`
- `timeconst`
- `inheritrange`
- target position 与 actual joint state
- controllable damping
- basic pneumatic / hydraulic actuator concepts
- `light`
- directional 与 local lighting
- ambient、diffuse 与 specular lighting
- light tracking 与 targeting
- `replicate`
- `count`
- `offset`
- `euler`
- `sep`
- linear replication
- circular replication
- nested replication
- repeated body structures
- tendon fundamentals
- `spatial` tendon
- `fixed` tendon
- tendon routing through sites
- tendon `coef`
- tendon `springlength`
- tendon `stiffness`
- tendon `damping`
- tendon-based actuation
- muscle actuator on tendons
- Mecanum fixed-tendon transmission
- camera fundamentals
- IMU-style sensing
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
- `framelinvel`
- `frameangvel`
- `framelinacc`
- `frameangacc`
- relative frame sensing
- subtree sensing
- `data.sensordata`

---

## Source A 学习笔记

- [Environment and Assets](notes/M2/MuJoCo/01_environment_and_assets.md)
- [中文 - 环境配置与资源](notes/M2/MuJoCo/01_environment_and_assets_zh.md)
- [Geom, Body and Site](notes/M2/MuJoCo/02_geom_body_site.md)
- [中文 - Geom、Body 与 Site](notes/M2/MuJoCo/02_geom_body_site_zh.md)
- [Joint](notes/M2/MuJoCo/03_joint.md)
- [中文 - Joint 关节](notes/M2/MuJoCo/03_joint_zh.md)
- [Friction](notes/M2/MuJoCo/04_friction.md)
- [中文 - Friction 摩擦](notes/M2/MuJoCo/04_friction_zh.md)
- [Actuator](notes/M2/MuJoCo/05_actuator.md)
- [中文 - Actuator 执行器](notes/M2/MuJoCo/05_actuator_zh.md)
- [Light and Replicate](notes/M2/MuJoCo/06_light_and_replicate.md)
- [中文 - Light 与 Replicate](notes/M2/MuJoCo/06_light_and_replicate_zh.md)
- [Tendon](notes/M2/MuJoCo/07_tendon.md)
- [中文 - Tendon 肌腱 / 传动结构](notes/M2/MuJoCo/07_tendon_zh.md)
- [Sensor](notes/M2/MuJoCo/08_sensor.md)
- [中文 - Sensor 传感器](notes/M2/MuJoCo/08_sensor_zh.md)

---

## Source A 实验与示例分析

- [MuJoCo Experiments Overview](experiments/M2/MuJoCo/README.md)
- [Review Model Report](experiments/M2/MuJoCo/review_model_report.md)
- [中文 - Review Model Report](experiments/M2/MuJoCo/review_model_report_zh.md)
- [Pendulum Report](experiments/M2/MuJoCo/pendulum_report.md)
- [中文 - Pendulum Report](experiments/M2/MuJoCo/pendulum_report_zh.md)
- [Friction Comparison Report](experiments/M2/MuJoCo/friction_comparison_report.md)
- [中文 - Friction Comparison Report](experiments/M2/MuJoCo/friction_comparison_report_zh.md)
- [Actuator Demo Report](experiments/M2/MuJoCo/actuator_demo_report.md)
- [中文 - Actuator Demo Report](experiments/M2/MuJoCo/actuator_demo_report_zh.md)
- [Tendon Example Analysis](experiments/M2/MuJoCo/tendon_examples_report.md)
- [中文 - Tendon 示例分析](experiments/M2/MuJoCo/tendon_examples_report_zh.md)
- [Sensor Example Analysis](experiments/M2/MuJoCo/sensor_example_report.md)
- [中文 - Sensor 综合示例分析](experiments/M2/MuJoCo/sensor_example_report_zh.md)

这一学习流当前仍然：

```text
In Progress
```

---

# Source B - Robot Knowledge Study

来源仓库：

```text
https://github.com/noBug01/Robot_knowledge_study
```

学习版本：

```text
v0.3.0
```

这一学习流将 MuJoCo 学习从 XML 建模进一步扩展到：

```text
Python-driven simulation
state observation
actuator control
sensor feedback
```

当前已经完成：

- SIM-T01 table and falling cube
- 使用 Python 加载 MJCF
- `MjModel`
- `MjData`
- `mj_step`
- `mj_forward`
- `qpos`
- `qvel`
- contact observation
- `data.ncon`
- CSV output
- numerical prediction 与 verification
- 使用 `pytest` 进行 automated testing
- MuJoCo Viewer
- SIM-T02 arm joint targets
- parent-child robot body hierarchy
- default classes
- mesh assets
- position actuators
- `data.ctrl`
- target 与 actual joint state
- waypoint interpolation
- joint sensors
- end-effector position
- end-effector orientation
- Python-controlled Viewer simulation

---

## Source B 学习笔记

- [SIM-T01 - Table and Falling Cube](notes/M2/RobotKnowledgeStudy_MuJoCo/01_table_cube.md)
- [中文 - SIM-T01 桌面与自由下落方块](notes/M2/RobotKnowledgeStudy_MuJoCo/01_table_cube_zh.md)
- [SIM-T02 - Arm Joint Targets](notes/M2/RobotKnowledgeStudy_MuJoCo/02_arm_joint_targets.md)
- [中文 - SIM-T02 机械臂关节角目标控制](notes/M2/RobotKnowledgeStudy_MuJoCo/02_arm_joint_targets_zh.md)

---

## Source B 实验记录

- [Robot Knowledge Study MuJoCo Experiments](experiments/M2/RobotKnowledgeStudy_MuJoCo/README.md)
- [SIM-T01 Experiment Report](experiments/M2/RobotKnowledgeStudy_MuJoCo/sim_t01_table_cube_report.md)
- [中文 - SIM-T01 实验报告](experiments/M2/RobotKnowledgeStudy_MuJoCo/sim_t01_table_cube_report_zh.md)
- [SIM-T02 Experiment Report](experiments/M2/RobotKnowledgeStudy_MuJoCo/sim_t02_arm_joint_targets_report.md)
- [中文 - SIM-T02 实验报告](experiments/M2/RobotKnowledgeStudy_MuJoCo/sim_t02_arm_joint_targets_report_zh.md)

当前 `v0.3.0` 中可用的 M2 内容已经完成。

---

# M2 学习进展结构

目前两个来源分别形成了以下学习路径：

```text
Albusgive source
↓
MJCF structure
↓
geom / body / site
↓
joint modeling
↓
contact and friction
↓
actuator models
↓
light and repeated scene construction
↓
tendon transmission
↓
sensor modeling and observation

Robot Knowledge Study source
↓
Python-driven simulation
↓
state observation
↓
actuator control
↓
sensor feedback
↓
end-effector observation
```

综合来看，目前 M2 的学习路径已经逐渐形成：

```text
MJCF modeling
↓
rigid-body structure
↓
joint motion
↓
contact and friction
↓
actuation
↓
scene construction
↓
tendon transmission
↓
sensor modeling
↓
Python-driven simulation
↓
state observation
↓
active joint control
↓
sensor feedback
```

当前状态：

```text
Robot Knowledge Study
→ Completed

Albusgive MuJoCo Learning
→ In Progress

Overall M2
→ In Progress
```

---

# 仓库结构

```text
robot-learning-practice/
├── notes/
│   ├── M1/
│   │   ├── python_numpy.md
│   │   ├── python_numpy_zh.md
│   │   ├── robot_geometry.md
│   │   ├── robot_geometry_zh.md
│   │   ├── geometry_implementation.md
│   │   ├── geometry_implementation_zh.md
│   │   ├── modern_robotics_reading.md
│   │   └── modern_robotics_reading_zh.md
│   │
│   └── M2/
│       ├── MuJoCo/
│       │   ├── 01_environment_and_assets.md
│       │   ├── 01_environment_and_assets_zh.md
│       │   ├── 02_geom_body_site.md
│       │   ├── 02_geom_body_site_zh.md
│       │   ├── 03_joint.md
│       │   ├── 03_joint_zh.md
│       │   ├── 04_friction.md
│       │   ├── 04_friction_zh.md
│       │   ├── 05_actuator.md
│       │   ├── 05_actuator_zh.md
│       │   ├── 06_light_and_replicate.md
│       │   ├── 06_light_and_replicate_zh.md
│       │   ├── 07_tendon.md
│       │   ├── 07_tendon_zh.md
│       │   ├── 08_sensor.md
│       │   └── 08_sensor_zh.md
│       │
│       └── RobotKnowledgeStudy_MuJoCo/
│           ├── 01_table_cube.md
│           ├── 01_table_cube_zh.md
│           ├── 02_arm_joint_targets.md
│           └── 02_arm_joint_targets_zh.md
│
├── experiments/
│   ├── M1/
│   │   ├── capability_tasks_report.md
│   │   ├── capability_tasks_report_zh.md
│   │   ├── numeric_basics_report.md
│   │   ├── numeric_basics_report_zh.md
│   │   ├── robot_geometry_report.md
│   │   └── robot_geometry_report_zh.md
│   │
│   └── M2/
│       ├── MuJoCo/
│       │   ├── README.md
│       │   ├── review_model.xml
│       │   ├── review_model_report.md
│       │   ├── review_model_report_zh.md
│       │   ├── pendulum.xml
│       │   ├── pendulum_report.md
│       │   ├── pendulum_report_zh.md
│       │   ├── friction_comparison.xml
│       │   ├── friction_comparison_report.md
│       │   ├── friction_comparison_report_zh.md
│       │   ├── actuator_demo.xml
│       │   ├── actuator_demo_report.md
│       │   ├── actuator_demo_report_zh.md
│       │   ├── tendon_examples_report.md
│       │   ├── tendon_examples_report_zh.md
│       │   ├── sensor_example_report.md
│       │   └── sensor_example_report_zh.md
│       │
│       └── RobotKnowledgeStudy_MuJoCo/
│           ├── README.md
│           ├── sim_t01_table_cube_report.md
│           ├── sim_t01_table_cube_report_zh.md
│           ├── sim_t02_arm_joint_targets_report.md
│           └── sim_t02_arm_joint_targets_report_zh.md
│
├── tests/
├── examples/
├── docs/
├── progress/
├── environment.yml
├── README.md
└── README_zh.md
```

整个仓库会尽量保持：

```text
Notes
→ 学习总结与概念理解

Experiments
→ 实际实现、模型、实验与验证

Tests
→ 自动化验证

Examples
→ 可运行示例

Docs
→ 工作流与项目文档

Progress
→ 学习里程碑记录
```

---

# 学习方法

当前学习流程主要分为四步：

1. 理解背后的数学和概念。
2. 尽可能独立重新实现。
3. 使用测试与数值检查验证实现。
4. 记录推理过程、错误、修正与最终结果。

这个流程的目的，是让每一个学习主题都尽可能做到：

```text
可复现
可解释
可验证
可长期回顾
```

而不是只完成一次教程后就结束。

---

# 可复现性

项目使用：

```text
environment.yml
```

定义 Conda 环境。

典型配置：

```bash
conda env create -f environment.yml
conda activate robot_manipulation_learning
python -m pytest
```

可运行示例存放在：

```text
examples/
```

自动化测试存放在：

```text
tests/
```

相关实验输出与环境验证记录存放在：

```text
experiments/
```

---

# 文档导航

- [Learning Notes](notes/README.md)
- [Learning Roadmap](docs/roadmap.md)
- [Detailed Workflow](docs/workflow.md)
- [Progress Record](progress.md)

---

# 当前重点

目前主要学习重点是：

```text
M2 - MuJoCo Simulation
```

当前正在学习和强化：

- 理解 MuJoCo XML / MJCF structure
- 构建简单 simulation environment
- 理解 `worldbody`、`body`、`geom`、`site` 和 `joint` 如何配合
- 理解 parent-child body hierarchy 与 relative coordinate frames
- 学习 contact 与 friction behaviour
- 理解 sliding、torsional 与 rolling friction
- 学习 `condim`、friction cone 与 contact priority
- 理解 actuator 如何驱动 joint 和其他模型元素
- 对比 motor、position、velocity 和 integrated-velocity control
- 理解 `ctrlrange`、`forcerange` 与 `actrange`
- 学习 controllable damping 与 basic cylinder actuator
- 学习 scene lighting
- 使用 `replicate` 高效创建重复模型结构
- 理解 `spatial` 与 `fixed` tendon
- 学习 site-based tendon routing
- 理解 joint coupling 与 `coef`
- 学习 tendon-driven actuation
- 学习 muscle actuator 基础概念
- 学习 camera 与 IMU-style sensing
- 学习 joint、ball-joint、frame、subtree、rangefinder、force 和 torque sensor
- 理解 sensor output 如何存储在 `data.sensordata`
- 从零构建简单 MuJoCo experiments
- 将 simulation concepts 与 kinematics、dynamics、joint、actuator、transmission、sensor 和 control 联系起来

---

# 当前已经完成的 M2 工作

包括：

- environment and asset configuration notes
- geom、body 与 site notes
- joint notes
- friction notes
- actuator notes
- light 与 replicate notes
- tendon notes
- sensor notes
- basic review simulation model
- hinge-joint pendulum experiment
- friction comparison analysis
- actuator example analysis
- fixed 与 spatial tendon example analysis
- IMU、joint、frame、force/torque、ball-joint sensor example analysis
- 当前 MuJoCo notes 与 experiments 的中英双语文档
- SIM-T01 table and falling cube
- SIM-T02 robot-arm joint target control
- Python-driven MuJoCo simulation
- 使用 `qpos` 与 `qvel` 进行 state observation
- 使用 `data.ctrl` 进行 actuator control
- sensor feedback
- end-effector position 与 orientation observation

最近 Albusgive MuJoCo 学习进一步扩展到了：

```text
transmission
+
sensing
```

具体包括：

- `spatial` 与 `fixed` tendon
- site-based tendon routing
- 使用 `coef` 进行 joint coupling
- muscle-driven tendon actuation
- Mecanum virtual motion coordinates
- 使用 `framequat`、`accelerometer` 与 `gyro` 构建 IMU-style sensing
- joint 与 ball-joint sensors
- rangefinder sensing
- force 与 torque sensing
- global 与 relative frame sensors
- subtree sensing
- sensor output through `data.sensordata`

当前：

```text
Robot Knowledge Study v0.3.0 M2
→ SIM-T01 与 SIM-T02 已完成

Albusgive MuJoCo Learning
→ 仍在继续

Overall M2
→ 仍然是 In Progress
```

---

# 未来方向

之后计划继续学习：

- robot kinematics
- control systems
- ROS 2
- perception
- SLAM
- manipulation
- simulation
- larger integrated robotics projects

随着仓库不断扩展，一些学习模块可能会进一步发展成：

```text
更完整的独立项目
+
更完整的 documentation
+
tests
+
examples
```

---

# 写给自己的话

我现在仍然只是刚刚开始这段学习过程。以后一定还会遇到很多看不懂的概念，写不出来的代码，运行失败的实验，花很久才能解决的问题。

这些都是学习机器人过程的一部分，而不是应该停下来的理由。

我的目标不是看起来很厉害，而是真正变得有能力。

我不需要被过去的自己定义。以前的犹豫、错误、错过的机会，或者比别人更慢的起点，都不能决定以后能做到什么。

真正重要的是，我现在选择做什么，我现在学习什么，以及我是否愿意继续向前。

所以我会继续学习数学，继续写代码，继续做实验，继续提出更好的问题，也继续一点一点构建真正属于自己的能力。

终有一天，现在觉得困难的东西，会成为以后解决更困难、更复杂问题时必要的基础。