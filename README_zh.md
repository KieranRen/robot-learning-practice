# 机器人学习实践

[English](README.md) | [中文](README_zh.md)

这是一个用于长期记录机器人学习、代码实现、实验验证与技术成长的结构化仓库。

## 关于本仓库

本仓库用于记录我从数学与编程基础开始，逐步学习机器人相关知识的全过程。

每个学习模块尽量包含：

- 理论笔记
- 独立实现
- 自动化测试
- 实验记录
- 可复现结果
- 对错误、修正与理解过程的总结

目标不仅是完成教程，而是持续记录我真正理解、实现、验证和改进了什么。

## 学习来源

本仓库使用的主要学习资料来自多个不同的上游仓库。

### M1 - 机器人数学与几何基础

M1 的学习内容主要基于：

- [Robot Knowledge Study](https://github.com/noBug01/Robot_knowledge_study.git)

这个上游仓库主要作为以下内容的参考来源：

- Python 与 NumPy 基础
- 机器人几何
- 刚体变换
- 几何实现
- Modern Robotics 阅读
- 相关机器人数学基础

### M2 - MuJoCo 仿真

M2 中的 MuJoCo 学习内容主要基于：

- [MuJoCo Learning](https://github.com/Albusgive/mujoco_learning.git)

这个上游仓库主要作为以下内容的参考来源：

- MuJoCo XML / MJCF 结构
- 仿真环境配置
- 视觉设置
- Asset 与 Material
- Geom 几何体
- Body 层级结构
- Site 标记点
- 基础仿真实验

本仓库并不是对这些上游仓库内容的直接复制，而是用于记录我自己的学习过程，包括：

- 个人学习笔记与总结
- 独立实现
- 仿真实验
- 自动化测试
- 实验报告与验证
- 错误修正与持续完善

当某个具体学习任务依赖特定上游版本时，对应的来源或 commit 信息会记录在相关进度或实验文档中。

非常感谢这些上游仓库的作者和贡献者愿意公开分享他们的知识、代码与学习资料。

这些内容在我的学习过程中提供了非常有价值的帮助，也为我以更加系统、更加实践性的方式学习机器人相关内容打下了重要基础。

如果没有他们的无私分享，本仓库也不会以当前这种方式建立起来。

## 当前进度

| 模块 | 主题 | 状态 | 学习笔记 | 实验证明 |
|---|---|---|---|---|
| M0 | 环境配置与 Git 工作流 | 已完成 | - | [环境报告](experiments/environment_reports/) |
| M1 | Python、NumPy、机器人几何、刚体变换、测试、能力任务与 Modern Robotics 阅读 | 已完成 | [M1 笔记](notes/M1/) | [M1 实验](experiments/M1/) |
| M2 | MuJoCo 仿真与 MJCF 建模 | 进行中 | [M2 MuJoCo 笔记](notes/M2/MuJoCo/) | [M2 MuJoCo 实验](experiments/M2/MuJoCo/) |

### M1 当前成果

M1 目前已经完成三个主要学习部分。

#### Python 与 NumPy 基础

包括：

- 数组 shape、维度与数据类型
- 索引与切片
- view 与 copy
- broadcasting
- 向量与矩阵运算
- 浮点误差检查
- 使用 `pytest` 进行自动测试

学习笔记：

- [English](notes/m1/python_numpy.md)
- [中文](notes/m1/python_numpy_zh.md)

实验证据：

- [English](experiments/m1/numeric_basics_report.md)
- [中文](experiments/m1/numeric_basics_report_zh.md)

#### 机器人几何与刚体变换

包括：

- 坐标系
- 旋转矩阵
- 刚体变换
- 齐次坐标
- 多级变换组合
- 逆变换
- 往返验证
- 坐标系可视化

学习笔记：

- [English](notes/m1/robot_geometry.md)
- [中文](notes/m1/robot_geometry_zh.md)

实验证据：

- [English](experiments/m1/robot_geometry_report.md)
- [中文](experiments/m1/robot_geometry_report_zh.md)

生成的可视化：

- [`outputs/m1/frames.svg`](outputs/m1/frames.svg)

### 几何实现

前面的数学概念已经进一步对应到可复用的 NumPy 实现，并通过明确的输入约定和验证逻辑提高可靠性。

已学习内容：

- `rotation_z`
- `make_transform`
- `inverse_transform`
- `transform_points`
- 有限数值输入检查
- 严格的数组 shape 检查
- proper rotation matrix 合法性验证
- 浮点数容差
- 坐标变换组合顺序
- 往返一致性检查
- 数值示例与坐标系示例的程序结构

学习笔记：

- [English](notes/m1/geometry_implementation.md)
- [中文](notes/m1/geometry_implementation_zh.md)

### 教材阅读

已完成 M1 指定范围的 *Modern Robotics: Mechanics, Planning, and Control* 阅读：

- Section 3.2.1 — Rotation Matrices
- Section 3.3.1 — Homogeneous Transformation Matrices

主要核对并补充：

- `SO(3)` 与 proper rotation
- `SE(3)` 齐次刚体变换
- 坐标系下标消去规则
- 变换组合与逆变换
- fixed-frame 与 body-frame 的左乘 / 右乘更新

阅读笔记：

- [English](notes/m1/modern_robotics_reading.md)
- [中文](notes/m1/modern_robotics_reading_zh.md)

当前自动化验证结果：

```text
Python / NumPy：    22 项测试通过
Robot Geometry：    54 项测试通过
Full repository:    107 项测试通过
```

### M2 - MuJoCo 仿真

M2 的 MuJoCo 学习内容来自两个不同的上游仓库。

为了保持学习来源清晰、内容可追踪，这两条学习线会分开整理，因为它们关注的内容不同，学习进度也彼此独立。

#### 来源 A - Albusgive MuJoCo Learning

来源仓库：

https://github.com/Albusgive/mujoco_learning.git

这一条学习线主要集中在 MJCF 建模基础。

目前已经完成的内容包括：

- MuJoCo XML / MJCF 结构
- 仿真参数配置
- Environment 与 Asset
- Texture、Material、Mesh 与 Skybox
- `geom`
- `body`
- `site`
- body 层级结构
- 相对坐标系
- friction 与 collision 设置
- joint 类型
- hinge joint
- joint axis 与 range
- damping
- stiffness
- frictionloss
- armature
- 简单单摆仿真

学习笔记：

- [Environment and Assets](notes/M2/MuJoCo/01_environment_and_assets.md)
- [中文 - 环境配置与资源](notes/M2/MuJoCo/01_environment_and_assets_zh.md)
- [Geom, Body and Site](notes/M2/MuJoCo/02_geom_body_site.md)
- [中文 - Geom、Body 与 Site](notes/M2/MuJoCo/02_geom_body_site_zh.md)
- [Joint](notes/M2/MuJoCo/03_joint.md)
- [中文 - Joint 关节](notes/M2/MuJoCo/03_joint_zh.md)

实验：

- [MuJoCo Experiments Overview](experiments/M2/MuJoCo/README.md)
- [Review Model Report](experiments/M2/MuJoCo/review_model_report.md)
- [中文 - Review Model Report](experiments/M2/MuJoCo/review_model_report_zh.md)
- [Pendulum Report](experiments/M2/MuJoCo/pendulum_report.md)
- [中文 - Pendulum Report](experiments/M2/MuJoCo/pendulum_report_zh.md)

这一条学习线目前仍在继续。

---

#### 来源 B - Robot Knowledge Study

来源仓库：

https://github.com/noBug01/Robot_knowledge_study

使用版本：

```text
v0.3.0
```

这一条学习线把 MuJoCo 学习从 XML 建模进一步扩展到 Python 驱动仿真、状态读取、执行器控制与传感器反馈。

已经完成的内容包括：

- SIM-T01 桌面与自由下落方块
- 使用 Python 加载 MJCF
- `MjModel`
- `MjData`
- `mj_step`
- `mj_forward`
- `qpos`
- `qvel`
- 接触状态观察
- `data.ncon`
- CSV 输出
- 数值预测与验证
- 使用 `pytest` 自动测试
- MuJoCo Viewer
- SIM-T02 机械臂关节角目标控制
- 父 body / 子 body 层级结构
- default 参数模板
- mesh asset
- position actuator
- `data.ctrl`
- target 与 actual joint state
- waypoint 插值
- joint sensor
- 末端位置
- 末端姿态
- Python 控制下的 Viewer 仿真

学习笔记：

- [SIM-T01 - Table and Falling Cube](notes/M2/RobotKnowledgeStudy_MuJoCo/01_table_cube.md)
- [中文 - SIM-T01 桌面与自由下落方块](notes/M2/RobotKnowledgeStudy_MuJoCo/01_table_cube_zh.md)
- [SIM-T02 - Arm Joint Targets](notes/M2/RobotKnowledgeStudy_MuJoCo/02_arm_joint_targets.md)
- [中文 - SIM-T02 机械臂关节角目标控制](notes/M2/RobotKnowledgeStudy_MuJoCo/02_arm_joint_targets_zh.md)

实验：

- [Robot Knowledge Study MuJoCo Experiments](experiments/M2/RobotKnowledgeStudy_MuJoCo/README.md)
- [SIM-T01 Experiment Report](experiments/M2/RobotKnowledgeStudy_MuJoCo/sim_t01_table_cube_report.md)
- [中文 - SIM-T01 实验报告](experiments/M2/RobotKnowledgeStudy_MuJoCo/sim_t01_table_cube_report_zh.md)
- [SIM-T02 Experiment Report](experiments/M2/RobotKnowledgeStudy_MuJoCo/sim_t02_arm_joint_targets_report.md)
- [中文 - SIM-T02 实验报告](experiments/M2/RobotKnowledgeStudy_MuJoCo/sim_t02_arm_joint_targets_report_zh.md)

目前 `Robot_knowledge_study` 提供的 M2 内容已经全部完成。

---

#### M2 学习进展

目前两条学习线共同形成了下面这条学习路径：

```text
MJCF 建模
↓
geom / body / site
↓
joint 建模
↓
基础物理仿真
↓
Python 驱动仿真
↓
状态读取
↓
actuator 控制
↓
sensor feedback
↓
end-effector observation
```

当前状态：

```text
Robot Knowledge Study
→ 已完成

Albusgive MuJoCo Learning
→ 进行中

M2 整体
→ 进行中
```

## 仓库结构

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
│       │   └── 03_joint_zh.md
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
│       │   └── pendulum_report_zh.md
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

仓库整体按照“学习笔记”和“实验验证”分开组织，同时保持两者之间的对应关系。

- `notes/`：存放结构化学习笔记与知识总结
- `experiments/`：存放实际实现、仿真文件与实验报告
- `tests/`：存放自动化测试与验证
- `examples/`：存放可运行示例
- `docs/`：存放工作流与项目文档
- `progress/`：记录阶段进度与学习里程碑

## 学习方式

我的学习流程主要分为四步：

1. 理解背后的数学与核心概念。
2. 尝试独立重新实现。
3. 使用测试与数值检查验证实现。
4. 记录推理过程、错误、修正和结果，方便未来复习。

希望每个学习主题都尽量做到可复现、可解释，并能够进一步用于后续项目。

## 可复现环境

项目使用 `environment.yml` 定义 Conda 环境。

典型使用方式：

```bash
conda env create -f environment.yml
conda activate robot_manipulation_learning
python -m pytest
```

可运行示例存放在 `examples/`，自动化测试存放在 `tests/`。

实验输出与环境验证记录会按需要保存在 `experiments/`。

## 文档入口

- [学习笔记](notes/README.md)
- [学习路线图](docs/roadmap.md)
- [详细工作流](docs/workflow.md)
- [学习进度记录](progress.md)

## 当前重点

目前的学习重点是 M2：MuJoCo 仿真。

这一阶段正在进行的内容包括：

- 理解 MuJoCo XML / MJCF 的基本结构
- 搭建简单的仿真环境
- 理解 `worldbody`、`body`、`geom` 与 `site` 之间的关系
- 理解父子 body 的层级关系与相对坐标
- 练习基础几何体、材质、重力、接触与摩擦
- 从零开始创建简单的 MuJoCo 仿真实验
- 将仿真知识逐步与机器人学中的运动学、动力学、关节、执行器、传感器和控制联系起来

目前已经完成的 M2 内容包括：

- 环境配置与 Asset 资源相关笔记
- Geom、Body 与 Site 相关笔记
- Joint 关节相关笔记
- 一个基础综合复习仿真模型
- 一个基于 hinge joint 的单摆实验
- Notes 与 Experiments 的中英文双语文档

后续会随着 MuJoCo 和机器人学内容的深入，继续加入：

- Actuator
- Sensor
- Contact
- Robot kinematics
- Robot dynamics
- Control
- More advanced simulation experiments

`Robot_knowledge_study` 来源的 M2 内容已经完成，包括 SIM-T01 和 SIM-T02 两个场景。

基于 Albusgive 来源的 MuJoCo 学习仍在继续，后续会继续加入更多建模与仿真相关内容。

## 后续方向

计划逐步学习和扩展：

- 机器人运动学
- 控制系统
- ROS 2
- 机器人感知
- SLAM
- 机器人操作与抓取
- 仿真
- 更完整的综合机器人项目

随着仓库逐渐成熟，部分学习模块也会进一步发展成具有独立文档、测试和示例的完整小项目。

## 写给自己的话

我现在仍然只是刚刚开启对机器人的探索之路。

以后一定还会遇到看不懂的概念、跑不通的代码、失败的实验，以及花很久都解决不了的问题。这些都不是我应该停下来的理由，而本来就是学习机器人这件事的一部分。

我的目标不是“看起来很厉害”，而是真正变得有能力。

我不需要被过去的自己定义。曾经的犹豫、错误、错过的机会，或者起步得比别人慢，都不能决定我以后会成为怎样的人。真正重要的是现在的我选择做什么、现在开始积累什么，以及从这一刻起是否继续向前。

所以继续学数学，继续写代码，继续验证自己的假设，继续提出更好的问题，也继续一点一点把东西做出来。

持续重复的小进步，最终会变成真正的能力。

而今天觉得困难的东西，终有一天会成为我解决更高级，更复杂问题时最普通的基础。

