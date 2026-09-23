# M1 能力任务综合报告

[English](capability_tasks_report.md) | [中文](capability_tasks_report_zh.md)

## 1. 报告目的

本报告记录 M1 Robot Math Foundations 中六项能力任务的完成情况、个人实现、测试证据、手算基准、受控失败实验和当前能力边界。

本报告只记录已经实际学习、实现和验证过的内容。

截至本报告完成时，M1 的代码、测试、数值基础、机器人几何、刚体变换和综合能力任务均已完成。

M1 指定教材阅读现已完成，因此整个 M1 状态更新为 **已完成**。

---

## 2. 学习与运行环境

个人实践仓库：

```text
robot-learning-practice
```

主要环境：

```text
Conda environment: robot_manipulation_learning
Python: 3.11.16
NumPy: 2.4.6
pytest: 8.4.2
```

主要个人实现：

```text
examples/m1_solution.py
```

主要个人测试：

```text
tests/test_m1_solution.py
```

相关参考实现：

```text
algorithms/geometry/
examples/numeric_basics.py
examples/coordinate_frames.py
```

M1 参考教材仓库版本：

```text
v0.2.0
```

本报告中的个人任务实现并未简单包装参考函数，而是针对任务要求重新实现并测试关键数值和几何操作。

---

# 3. PYNUM-T01 — 明确函数输入、输出与异常

## 目标

实现：

```python
millimeters_to_meters(values)
```

将毫米转换为米，同时明确函数的输入、输出、数据类型和异常行为。

核心计算为：

```python
array / 1000.0
```

但任务重点并不只是单位换算，而是建立明确的函数契约。

## 输入约定

接受：

- Python list
- NumPy array
- 有限实数整数或浮点数

拒绝：

- `NaN`
- `+inf`
- `-inf`
- 非实数数值类型

## 输出约定

输出：

- NumPy array
- `float64`
- 与输入保持相同 shape
- 不修改调用者原始数据

## 手算基准

输入：

```text
[0, 250, -1000] mm
```

预期：

```text
[0.0, 0.25, -1.0] m
```

## 测试证据

验证内容包括：

- 已知数值转换
- `float64` 输出
- 一维 shape 保持
- 二维 shape 保持
- 原输入不被修改
- 输出与输入不共享内存
- `NaN / ±inf` 被明确拒绝

这一任务让我进一步理解：

> 一个可靠的数值函数不仅要能够计算，还必须明确规定它接受什么、拒绝什么以及返回什么。

---

# 4. PYNUM-T02 — 数组形状先于运算

## 正确 broadcasting

使用：

```text
points.shape = (2, 3)
offset.shape = (3,)
```

执行：

```python
points + offset
```

得到：

```text
shifted.shape = (2, 3)
```

其中：

```text
points =
[[0, 0, 0],
 [1, 2, 3]]

offset =
[1, -1, 0.5]
```

结果：

```text
[[1, -1, 0.5],
 [2,  1, 3.5]]
```

这符合：

> 每个三维点加上同一个三维位移。

## 错误 shape

当：

```text
points.shape = (2, 3)
offset.shape = (3, 1)
```

NumPy 无法完成 broadcasting，因此应失败。

## 能运行但语义错误的 broadcasting

例如：

```text
(3, 1) + (3,) -> (3, 3)
```

NumPy 可以正常计算，但如果本意是两个三维向量逐坐标相加，则 `(3,3)` 的结果并不符合预期语义。

因此：

> 能够 broadcasting 不代表数学含义正确。

## `@` 与 `*`

```python
R @ p
```

表示矩阵乘法。

```python
R * p
```

表示逐元素运算并可能触发 broadcasting。

机器人旋转中的：

```math
Rp
```

应使用：

```python
R @ p
```

而不能替换成：

```python
R * p
```

## 浮点残差

计算：

```python
0.1 + 0.2 - 0.3
```

得到一个非常小但非零的浮点残差。

因此数值测试通常使用：

```python
np.testing.assert_allclose(...)
```

而不是要求浮点结果逐位完全相等。

同时，容差不能设置得过宽，否则可能掩盖真正的实现错误。

---

# 5. GEOM-T01 — 坐标系与旋转

## 坐标符号

### `R_ab`

表示 B 坐标系的方向用 A 坐标系表达。

其列向量表示 B 的单位坐标轴在 A 中的方向。

### `t_ab`

表示 B 坐标系原点的位置，用 A 坐标系表达。

### `p_b`

表示物理点 `p` 在 B 坐标系中的坐标。

### `T_ab`

表示从 B 到 A 的完整刚体坐标变换：

```math
T_{ab}
=
\begin{bmatrix}
R_{ab} & t_{ab}\\
0 & 1
\end{bmatrix}
```

其中：

```text
R_ab -> (3, 3)
t_ab -> (3,)
T_ab -> (4, 4)
```

---

## 正 90° 绕 z 轴旋转

```math
R_z(\pi/2)
=
\begin{bmatrix}
0 & -1 & 0\\
1 & 0 & 0\\
0 & 0 & 1
\end{bmatrix}
```

第一列：

```math
\begin{bmatrix}
0\\
1\\
0
\end{bmatrix}
```

表示原 +x 方向旋转后指向 +y。

第二列：

```math
\begin{bmatrix}
-1\\
0\\
0
\end{bmatrix}
```

表示原 +y 方向旋转后指向 -x。

第三列保持：

```math
\begin{bmatrix}
0\\
0\\
1
\end{bmatrix}
```

因此 z 轴不变。

---

## 手算

```math
R_z(\pi/2)
\begin{bmatrix}
2\\
1\\
0
\end{bmatrix}
=
\begin{bmatrix}
-1\\
2\\
0
\end{bmatrix}
```

旋转前：

```math
\sqrt{2^2+1^2}=\sqrt{5}
```

旋转后：

```math
\sqrt{(-1)^2+2^2}=\sqrt{5}
```

长度保持不变。

---

## 正交矩阵不一定是 proper rotation

矩阵：

```math
\begin{bmatrix}
1 & 0 & 0\\
0 & 1 & 0\\
0 & 0 & -1
\end{bmatrix}
```

满足：

```math
R^TR=I
```

但：

```math
\det(R)=-1
```

因此它表示反射，而不是右手刚体旋转。

合法 proper rotation 需要同时满足：

```math
R^TR=I
```

和：

```math
\det(R)=+1
```

---

# 6. GEOM-T02 — 从公式写实现

本任务没有直接调用参考实现中的点变换与逆变换函数，而是根据公式自行实现：

```python
apply_transform(T, points)
invert_transform(T)
```

---

## 点变换

数学公式：

```math
p_a=R_{ab}p_b+t_{ab}
```

个人代码使用 `(N,3)` 行向量批量存储点，因此：

```python
points @ R.T + t
```

等价于列向量写法：

```python
(R @ points.T).T + t
```

---

## 逆变换

对于：

```math
T=
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}
```

有：

```math
T^{-1}
=
\begin{bmatrix}
R^T&-R^Tt\\
0&1
\end{bmatrix}
```

因此个人实现直接使用：

```python
R_inv = R.T
t_inv = -R_inv @ t
```

再重新构造 4×4 齐次矩阵。

---

## 手算基准

设：

```text
R = Rz(pi/2)
t = [1, 0, 0]
p = [2, 1, 0]
```

先旋转：

```text
[2,1,0] -> [-1,2,0]
```

再平移：

```text
[-1,2,0] + [1,0,0]
=
[0,2,0]
```

因此预期：

```text
[[0,2,0]]
```

个人实现与测试结果一致。

---

## 接口验证

个人实现检查：

- `T.shape == (4,4)`
- `points.shape == (N,3)`
- 所有输入为有限实数
- 齐次矩阵底行为 `[0,0,0,1]`
- `R^TR ≈ I`
- `det(R) ≈ +1`
- 非刚体矩阵被拒绝
- 运算溢出不能静默返回无穷值

测试覆盖：

- 恒等变换
- 已知旋转和平移
- 逆变换往返
- 错误点 shape
- `NaN / inf`
- 非法刚体变换

---

# 7. GEOM-T03 — 组合顺序与失败分析

固定坐标链：

```text
B -> A -> W
```

其中：

```text
T_ab : B -> A
T_wa : A -> W
```

因此：

```math
T_{wb}=T_{wa}T_{ab}
```

下标可以检查为：

```math
T_{w\cancel a}T_{\cancel a b}=T_{wb}
```

---

## 路径 1：逐步变换

```text
p_b
↓ T_ab
p_a
↓ T_wa
p_w
```

## 路径 2：先组合

```text
T_wb = T_wa @ T_ab
```

然后：

```text
p_w = T_wb p_b
```

两条路径均得到：

```text
p_w = [2,1,0]
```

因此逐步变换与组合变换一致。

---

## 往返检查

使用：

```text
T_bw = inverse(T_wb)
```

将结果从 W 再转换回 B。

恢复结果与原始：

```text
p_b = [1,0,0]
```

一致。

最大绝对往返误差在当前 float64 米量级练习的容差范围内。

当前测试使用：

```text
rtol = 0
atol = 1e-12
```

这只是本练习中的数值验证标准，不代表真实机器人系统具有 `1e-12 m` 的物理精度。

---

## 受控失败实验

故意把：

```python
T_wa @ T_ab
```

写成：

```python
T_ab @ T_wa
```

得到：

```text
[2,-1,0]
```

而正确结果为：

```text
[2,1,0]
```

这个错误不是浮点误差。

原因是：

```text
T_ab @ T_wa
```

的 frame 下标不能形成合法的 B -> A -> W 坐标链。

因此这是：

> 坐标系约定 / 变换组合顺序错误。

这个例子说明：

> 两个矩阵能够进行数值乘法，并不意味着它们具有合法的坐标系组合语义。

---

# 8. GEOM-T04 — 综合结果与复核

## 原固定场景

参考坐标示例生成：

```text
outputs/m1/frames.svg
```

图中包含：

- W 坐标系
- A 坐标系
- B 坐标系
- 坐标轴
- 单位
- 世界坐标中的点
- 错误顺序的对照点

SVG 用于辅助理解和人工查看，但不作为个人实现正确性的唯一证据。

个人实现的数值和自动测试结果仍作为主要验证依据。

---

## 变体场景

将：

```text
t_ab = [1,0,0]
```

修改为：

```text
t_ab = [2,0,0]
```

在运行代码前先进行手算预测。

### B 原点

预测：

```text
B origin in W = [1,2,0]
```

### 点 P

对于：

```text
p_b = [1,0,0]
```

预测：

```text
p_w = [2,2,0]
```

随后使用个人实现：

```python
apply_transform(...)
```

进行验证。

自动测试结果与手算预测一致。

这说明个人实现能够处理不仅是固定参考场景，还能处理修改后的合法刚体变换输入。

---

# 9. 测试方法与测试边界

本次 M1 使用了多层验证方式：

```text
手算基准
+
单元测试
+
shape 检查
+
错误输入测试
+
几何不变量
+
逆变换往返
+
受控失败实验
+
可视化人工检查
```

不同方法承担不同作用。

例如：

- 手算用于提供独立基准
- pytest 用于自动重复验证
- 几何不变量用于检查数学结构
- round trip 用于检查正逆一致性
- 失败实验用于确认错误诊断能力
- SVG 用于辅助发现方向与空间关系问题

没有任何单独一种验证方式可以证明所有可能输入都正确。

最终从仓库根目录运行：

python -m pytest

实际结果：

107 passed in 0.51s

---

# 10. 一次实际错误与诊断

在新增 GEOM-T03 测试时，测试最初失败。

错误信息为：

```text
NameError: name 'make_transform' is not defined
```

原因不是数学公式错误，也不是 NumPy 数值错误，而是：

> `examples/m1_solution.py` 中使用了 `make_transform`，但没有在该模块中导入它。

修复方式是在正确模块中加入：

```python
from algorithms.geometry import make_transform, rotation_z
```

而不是修改测试期望值。

这个过程进一步说明：

> 测试失败时，应先根据错误信息定位失败类型，而不是为了让测试通过而修改正确答案。

---

# 11. 公式与 NumPy 的职责区别

本次实现中的数学关系由个人明确写出。

例如：

```python
point_array @ R.T + t
```

来自：

```math
p_a=Rp_b+t
```

而：

```python
-R.T @ t
```

来自刚体逆变换推导。

NumPy 本身负责：

- 数组存储
- 矩阵乘法
- broadcasting
- 转置
- determinant
- norm
- 浮点运算
- approximate comparison

NumPy 不会自动理解：

- 坐标系下标
- 变换方向
- 单位
- frame chain
- 哪一种矩阵乘法具有正确机器人语义

因此数学约定与坐标含义仍必须由实现者明确保证。

---

# 12. 当前已经验证的结论

目前已经通过实现、测试和手算支持以下结论：

- 单位转换函数具有明确输入输出契约
- 数组 shape 对 NumPy 数值语义具有决定性影响
- broadcasting 可合法运行但仍可能产生错误数学语义
- `@` 与 `*` 在机器人矩阵运算中不能互换
- 浮点比较需要合理容差
- 合法旋转需要满足正交性和 determinant +1
- 刚体旋转保持向量长度
- `(N,3)` 点集可通过 `points @ R.T + t` 批量刚体变换
- 刚体逆变换可由 `R.T` 和 `-R.T @ t` 直接构造
- 逐步变换和组合变换应产生一致结果
- 矩阵组合顺序必须符合 frame chain
- 正向与逆向变换可以通过 round-trip 检查一致性
- 非法 shape、非有限值和非法刚体矩阵应被明确拒绝
- 参考 SVG 与数值结果可互相辅助检查

---

# 13. 当前仍未覆盖的内容

本次 M1 目前没有声称覆盖：

- 任意维数的机器人刚体变换
- scaling
- shear
- affine transformation
- 非刚体变换
- 真实传感器噪声模型
- 真实机器人标定误差
- 实时控制
- 机器人动力学
- Jacobian
- motion planning
- sensor fusion

## 最终状态

M1 指定教材阅读现已完成：

```text
Modern Robotics
Section 3.2.1 — Rotation Matrices
Section 3.3.1 — Homogeneous Transformation Matrices

---
```

# 14. 当前结论

M1 的内容已经完成：

```text
Python / NumPy Foundations
Robot Geometry
Geometry Implementation
Testing and Validation
PYNUM-T01
PYNUM-T02
GEOM-T01
GEOM-T02
GEOM-T03
GEOM-T04
Textbook Reading
```

个人代码、测试、手算、失败分析和综合变体场景均已形成可复核证据。

完成教材阅读并整理真实阅读记录后，可进行 M1 最终验收并将状态更新为：

```text
Completed
```