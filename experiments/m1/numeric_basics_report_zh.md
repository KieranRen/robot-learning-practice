# M1 实验报告 — Python 与 NumPy 数值基础

[English](numeric_basics_report.md) | [中文](numeric_basics_report_zh.md)

## 实验概述

这份报告记录 M1 Python 与 NumPy 数值基础示例的实际运行与验证结果。

本实验的目标是验证：

- 数值示例能够在当前开发环境中正确运行
- NumPy 的 shape、broadcasting、矩阵运算和浮点误差行为符合预期
- 对应自动化测试能够全部通过

## 运行环境

本次实验使用项目 Conda 环境：

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

本次实验使用：

```text
examples/numeric_basics.py
tests/test_numeric_basics.py
```

## 运行命令

运行数值示例：

```bash
python -m examples.numeric_basics
```

运行自动化测试：

```bash
python -m pytest tests/test_numeric_basics.py -q
```

## 1. 数组操作

实际输出：

```text
ARRAY | points shape=(2, 2) dtype=float64
ARRAY | offset shape=(2,); translated (m)=[[0.5, -1.0], [1.5, 1.0]]
ARRAY | after view edit: source=[9.0, 2.0, 3.0] copy=[1.0, 2.0]
```

这部分验证了：

- 点集 shape 为 `(2,2)`
- 偏移向量 shape 为 `(2,)`
- broadcasting 会把同一个偏移应用到每一个点
- 普通切片可能共享原数组数据
- `.copy()` 可以创建独立副本

平移计算为：

```text
[0.0, 0.0] + [0.5, -1.0] = [0.5, -1.0]

[1.0, 2.0] + [0.5, -1.0] = [1.5, 1.0]
```

## 2. 向量长度

实际输出：

```text
VECTOR | components (m)=[3.0, 4.0] squares (m^2)=[9.0, 16.0]
VECTOR | squared length=25.0 m^2; length=5.0 m
```

数学计算：

```math
3^2+4^2=25
```

因此：

```math
\sqrt{25}=5
```

这验证了向量 `[3,4]` 的欧几里得长度为 5。

## 3. 矩阵运算

实际输出：

```text
MATRIX | A @ v=[11.0, 4.0]
MATRIX | A * v=[[3.0, 8.0], [0.0, 4.0]]
```

这展示了：

```python
A @ v
```

和：

```python
A * v
```

之间的区别。

`@` 表示矩阵乘法，而 `*` 表示逐元素乘法，并可能伴随 broadcasting。

矩阵乘法结果：

```math
\begin{bmatrix}
1 & 2\\
0 & 1
\end{bmatrix}
\begin{bmatrix}
3\\
4
\end{bmatrix}
=
\begin{bmatrix}
11\\
4
\end{bmatrix}
```

## 4. 浮点误差与错误检查

实际输出：

```text
ERROR | equal elementwise=[False, True]
ERROR | max absolute residual=5.551e-17
ERROR | allclose(rtol=0, atol=1e-12)=True
ERROR | accidental (2, 1) - (2,) shape=(2, 2)
ERROR | expected rejection: offset must have shape (2,)
```

第一项说明直接使用严格相等比较浮点数可能失败。

例如：

```python
0.1 + 0.2 == 0.3
```

在计算机内部并不一定为 `True`。

本次实验观察到的最大残差约为：

```text
5.551e-17
```

这个误差非常小。

使用：

```python
np.allclose(...)
```

并设置合理容差后，结果为：

```text
True
```

另外：

```text
(2,1) - (2,)
```

会被 NumPy 自动广播成：

```text
(2,2)
```

虽然这个运算在 NumPy 规则下合法，但不一定符合原本的数学含义。

因此函数接口需要主动检查 shape。

## 自动化测试结果

测试命令实际得到：

```text
22 passed in 0.17s
```

说明 `tests/test_numeric_basics.py` 中的 22 项自动检查全部通过。

测试通过说明已经覆盖到的条件符合预期，但不能证明所有可能的 bug 或物理建模问题都不存在。

## 本实验证明了什么

本实验提供了以下内容的实际运行证据：

- NumPy 数组 shape 与 dtype
- 索引、切片、view 与 copy
- broadcasting
- 向量长度
- 矩阵乘法
- 逐元素乘法
- 浮点误差比较
- shape 输入检查
- 使用 `pytest` 进行自动测试

## 实验反思

本实验最重要的认识是：

> 数值代码“能够运行”并不代表它在数学或物理意义上一定正确。

在机器人代码中，必须同时关注：

- 数组 shape
- 坐标含义
- 物理单位
- 数学运算类型
- 数值容差
- 函数接口约定

因此，数值程序需要同时通过数学推理和自动化测试进行验证。