# M1 实验报告 — 机器人几何与刚体变换

[English](robot_geometry_report.md) | [中文](robot_geometry_report_zh.md)

## 实验概述

这份报告记录 M1 机器人几何部分的实际运行与验证结果。

本次实验主要覆盖：

- 坐标系
- 旋转矩阵
- 刚体变换
- 多级变换组合
- 逆变换
- 往返验证
- 自动化测试
- 坐标系可视化

实验目的不是只记录理论公式，而是提供实际可运行、可验证的学习证据。

## 运行环境

本次实验使用项目中的 Conda 环境：

```text
robot_manipulation_learning
```

主要软件版本：

```text
Python 3.11.16
NumPy 2.4.6
pytest 8.4.2
```

参考学习材料版本：

```text
knowledge tag: v0.2.0
```

## 使用文件

本次实验主要使用：

```text
algorithms/geometry/
examples/coordinate_frames.py
tests/test_rigid_transform.py
tests/test_coordinate_frames.py
```

生成的可视化文件位于：

```text
outputs/m1/frames.svg
```

## 运行命令

运行坐标系示例：

```bash
python -m examples.coordinate_frames --output outputs/m1/frames.svg
```

运行自动化测试：

```bash
python -m pytest tests/test_rigid_transform.py tests/test_coordinate_frames.py -q
```

## 坐标变换结果

程序得到点 P 在世界坐标系 W 中的位置：

```text
p_w =
[[2. 1. 0.]]
```

这一结果与之前独立完成的三坐标系手算结果一致。

变换链为：

```text
B -> A -> W
```

组合变换满足：

```math
T_{wb}=T_{wa}T_{ab}
```

点坐标变换满足：

```math
p_w=R_{wb}p_b+t_{wb}
```

本例中：

```math
p_b=
\begin{bmatrix}
1\\
0\\
0
\end{bmatrix}
```

预期结果：

```math
p_w=
\begin{bmatrix}
2\\
1\\
0
\end{bmatrix}
```

程序的实际输出与手算结果一致。

## 中间坐标结果

程序同时输出：

```text
p_reversed =
[[ 2. -1.  0.]]
```

保留中间结果可以用于检查：

- 坐标系约定
- 变换方向
- 每一步变换是否符合预期

只得到正确的最终结果并不能完全证明所有中间步骤都正确，因此中间变量也具有验证价值。

## 往返变换验证

程序把变换后的点重新转换回 B 坐标系。

实际输出：

```text
p_b_roundtrip =
[[1. 0. 0.]]
```

原始输入：

```text
p_b =
[[1. 0. 0.]]
```

本次运行测得最大往返误差：

```text
0.000e+00 m
```

因此在本次运行的数值精度下，正向变换和逆变换能够准确恢复原始点。

概念上：

```text
B -> W -> B
```

最终应该回到原始的 B 坐标。

这一结果验证了正向变换与逆变换之间的一致性。

## 变换顺序

程序明确输出：

```text
T_wb = T_wa @ T_ab; the reversed product is not a valid B -> W frame chain.
```

这说明：

> 两个矩阵在 shape 上可以相乘，并不代表这个乘法具有正确的坐标系意义。

正确的坐标链是：

```text
B -> A -> W
```

因此：

```math
T_{wb}=T_{wa}T_{ab}
```

可以通过下标检查：

```math
T_{w\cancel a}T_{\cancel a b}=T_{wb}
```

如果反过来乘，则不再表示同一条 B 到 W 的坐标变换链。

## SVG 可视化结果

示例成功生成：

```text
outputs/m1/frames.svg
```

这张图可以帮助检查：

- 坐标轴方向
- 各坐标系原点位置
- 变换方向
- 点 P 的最终位置

但是仅仅“图看起来正确”并不足以证明实现正确。

因此还需要结合：

- 数值检查
- 手算结果
- 往返验证
- 自动化测试

共同判断。

## 自动化测试结果

测试命令实际得到：

```text
54 passed in 0.41s
```

也就是说：

```text
tests/test_rigid_transform.py
tests/test_coordinate_frames.py
```

中的 54 项自动检查在当前环境下全部通过。

## 本实验证明了什么

本实验提供了以下内容的实际运行证据：

- 旋转矩阵构造
- 坐标系转换
- 坐标系原点之间的平移
- 齐次刚体变换
- 多级变换组合
- 逆变换
- 变换顺序检查
- 往返一致性
- 数值验证
- SVG 坐标系可视化
- 使用 `pytest` 进行自动测试

## 实验反思

这次实验最重要的认识是：

> 坐标变换不能只被当作普通矩阵运算，必须始终结合坐标系的几何含义理解。

即使矩阵尺寸完全合法，也可能因为坐标系方向或变换顺序错误而得到没有正确物理意义的结果。

因此可靠的机器人几何实现需要同时检查：

- 坐标系名称与方向
- 变换方向
- 旋转是否合法
- 平移使用哪个坐标系表达
- 矩阵乘法顺序
- 数值结果
- 逆变换一致性
- 独立手算结果

把这些检查组合起来，比只看一个最终数值或一张图更加可靠。