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

## 学习资料来源

本仓库当前主要学习资料来自以下上游仓库：

- [noBug01/Robot_knowledge_study](https://github.com/noBug01/Robot_knowledge_study)

本仓库并不以复制上游教材内容为目标，而是记录我自己的学习过程，包括：

- 个人笔记与总结
- 独立代码实现
- 测试与数值验证
- 实验记录
- 错误、修正与反思
- 基于所学内容进一步完成的小项目与扩展

上游仓库作为主要参考资料，本仓库则作为个人学习、实践、记录与开发空间。

当某项学习任务依赖特定教材版本时，会在对应的进度记录或实验报告中记录具体版本或 commit。

## 当前进度

| 模块 | 内容 | 状态 | 学习笔记 | 实验证据 |
| --- | --- | --- | --- | --- |
| M0 | 开发环境与 Git 工作流 | 已完成 | — | [环境报告](experiments/environment_reports/) |
| M1 | Python、NumPy、坐标系、刚体变换与几何实现 | 进行中 | [M1 笔记](notes/m1/) | [M1 实验](experiments/m1/) |

### M1 当前成果

M1 目前已经完成两个主要学习部分。

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

当前自动化验证结果：

```text
Python / NumPy：    22 项测试通过
Robot Geometry：    54 项测试通过
```

## 仓库结构

```text
robot-learning-practice/
├── notes/          # 个人学习笔记与总结
├── examples/       # 可运行示例与独立实现
├── tests/          # 自动化测试
├── experiments/    # 实验报告与可复现记录
├── docs/           # 路线图、工作流和项目文档
├── progress.md     # 持续更新的学习进度
├── environment.yml # 可复现 Python 环境
└── README.md
```

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

## 当前学习重点

目前正在进行 M1，主要包括：

- Python 与 NumPy 基础
- 数组 shape、索引、切片与广播
- 向量与矩阵运算
- 数值精度与浮点误差检查
- 坐标系
- 旋转矩阵
- 刚体变换
- 变换组合
- 逆变换
- 使用 `pytest` 进行自动化测试

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

