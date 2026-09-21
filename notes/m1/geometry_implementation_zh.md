# M1 — 几何实现

[English](geometry_implementation.md) | [中文](geometry_implementation_zh.md)

这份笔记记录我对 M1 几何实现部分的理解。

这一部分并没有引入大量新的机器人几何数学，而是把之前学习的旋转矩阵、刚体变换、逆变换与坐标转换真正实现成可靠的 Python / NumPy 函数。

重点从“会手算”进一步转向“如何设计可靠的程序接口”。

---

## 1. 从数学公式到程序接口

前面已经学习过几个核心数学关系。

绕 z 轴旋转：

```math
R_z(\theta)
=
\begin{bmatrix}
\cos\theta & -\sin\theta & 0\\
\sin\theta & \cos\theta & 0\\
0 & 0 & 1
\end{bmatrix}
```

点的刚体变换：

```math
p_a
=
R_{ab}p_b+t_{ab}
```

齐次变换：

```math
T_{ab}
=
\begin{bmatrix}
R_{ab} & t_{ab}\\
0 & 1
\end{bmatrix}
```

逆变换：

```math
T_{ba}
=
T_{ab}^{-1}
=
\begin{bmatrix}
R_{ab}^{T} & -R_{ab}^{T}t_{ab}\\
0 & 1
\end{bmatrix}
```

代码把这些数学内容封装成四个主要函数：

```python
rotation_z(angle_rad)
make_transform(rotation, translation)
inverse_transform(transform)
transform_points(transform, points)
```

它们基本对应手算坐标变换时的几个主要步骤。

---

## 2. `rotation_z(angle_rad)`

这个函数根据角度生成绕 z 轴旋转的三维旋转矩阵。

可以理解为：

```text
输入弧度角
    ↓
rotation_z(...)
    ↓
3 × 3 旋转矩阵
```

例如：

```python
rotation_z(np.pi / 2)
```

表示绕 z 轴正方向旋转 90°。

对应：

```math
R_z\left(\frac{\pi}{2}\right)
=
\begin{bmatrix}
0 & -1 & 0\\
1 & 0 & 0\\
0 & 0 & 1
\end{bmatrix}
```

实现本质上就是把数学公式直接写成 NumPy：

```python
c = np.cos(angle_rad)
s = np.sin(angle_rad)

R = np.array([
    [c, -s, 0.0],
    [s,  c, 0.0],
    [0.0, 0.0, 1.0]
])
```

变量名中的 `_rad` 用于提醒调用者：

> 输入角度的单位是弧度。

所以：

```python
rotation_z(np.pi / 2)
```

表示 90°。

而：

```python
rotation_z(90)
```

会被程序解释成 90 弧度，并不是 90°。

---

## 3. `make_transform(rotation, translation)`

这个函数把旋转矩阵和平移向量组合成齐次刚体变换矩阵。

输入要求：

```text
rotation.shape    = (3, 3)
translation.shape = (3,)
```

输出：

```text
transform.shape = (4, 4)
```

数学上：

```math
T
=
\begin{bmatrix}
R & t\\
0 & 1
\end{bmatrix}
```

也就是说，把：

```text
3 × 3 的旋转矩阵
+
长度为 3 的平移向量
```

组合成一个：

```text
4 × 4 齐次变换矩阵
```

之后其他函数只需要处理一个 `T`，而不必每次分别传入 `R` 和 `t`。

---

## 4. `inverse_transform(transform)`

这个函数用于求刚体变换的逆。

如果：

```math
T_{ab}
=
\begin{bmatrix}
R_{ab} & t_{ab}\\
0 & 1
\end{bmatrix}
```

那么：

```math
T_{ba}
=
\begin{bmatrix}
R_{ab}^{T} & -R_{ab}^{T}t_{ab}\\
0 & 1
\end{bmatrix}
```

这里不需要使用通用矩阵求逆，因为刚体变换具有特殊结构。

核心性质：

```math
R^{-1}=R^T
```

逆平移为：

```math
t_{\text{inverse}}
=
-R^Tt
```

需要特别注意：

> 逆平移通常不是简单的 `-t`。

因为平移向量还必须使用新的输出坐标系表达。

---

## 5. `transform_points(transform, points)`

这个函数用于把一个或多个点从一个坐标系转换到另一个坐标系。

输入要求：

```text
transform.shape = (4, 4)
points.shape    = (N, 3)
```

返回：

```text
(N, 3)
```

点的数量不会发生变化。

例如：

```python
points = np.array([
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0]
])
```

表示两个三维点：

```text
shape = (2, 3)
```

即使只有一个点，也写成：

```python
[[1.0, 0.0, 0.0]]
```

而不是：

```python
[1.0, 0.0, 0.0]
```

因为这个接口始终把输入视为“一批点”。

每个点本质上执行：

```math
p_a
=
R_{ab}p_b+t_{ab}
```

`transform_points` 只是把相同的刚体变换批量应用到所有点。

---

## 6. 为什么输入检查很重要

NumPy 能完成一个运算，并不代表这个运算在数学或几何意义上一定正确。

因此实现不会只检查“能不能算”，而是主动检查接口约定。

主要检查包括：

- 数组 shape
- 是否为实数
- 数值是否有限
- 旋转矩阵是否合法
- 齐次变换结构是否合法

如果输入违反接口约定，就抛出：

```python
ValueError
```

这样可以避免错误的 broadcasting 或错误矩阵悄悄进入后续计算。

---

## 7. 有限数值检查

辅助函数：

```python
_as_finite_float_array(...)
```

主要负责清洗输入。

可以概括成：

```text
输入
↓
转换成 NumPy 数组
↓
检查是否为数值
↓
统一转换为 float64
↓
拒绝 NaN / ±inf
↓
返回合法数组
```

例如：

```python
[1, 2, 3]
```

可能被转换成：

```python
np.array([1.0, 2.0, 3.0], dtype=np.float64)
```

而：

```python
np.nan
np.inf
-np.inf
```

都会被拒绝。

这个函数本身不负责机器人几何计算，而是为后续计算提供可靠输入。

---

## 8. Shape 检查

实现会严格要求：

```text
rotation    -> (3, 3)
translation -> (3,)
points      -> (N, 3)
transform   -> (4, 4)
```

这样做是为了防止 NumPy 自动 broadcasting 掩盖输入错误。

例如：

```text
(2, 1)
```

和：

```text
(2,)
```

可以自动 broadcast 成：

```text
(2, 2)
```

虽然 NumPy 能完成计算，但这不一定符合原本的数学意义。

因此机器人几何接口不能依赖 NumPy 去猜测程序员的意图。

---

## 9. 旋转矩阵检查

一个 shape 为 `(3,3)` 的数组不一定是合法旋转矩阵。

真正的旋转必须满足：

```math
R^TR=I
```

以及：

```math
\det(R)=1
```

第一条用于保证三根坐标轴：

- 长度为 1
- 两两垂直

第二条用于排除反射。

例如：

```math
\begin{bmatrix}
1&0&0\\
0&1&0\\
0&0&-1
\end{bmatrix}
```

满足正交条件，但：

```math
\det(R)=-1
```

因此它表示反射，而不是合法旋转。

---

## 10. 数值容差

浮点数计算通常无法做到数学意义上的绝对精确。

因此实现会使用：

```python
np.allclose(...)
```

之类的近似检查。

本实现使用的数值检查大致为：

```text
绝对容差 = 1e-9
相对容差 = 0
```

例如：

```math
R^TR
```

可能因为浮点计算而和单位矩阵存在极小误差。

这不应该导致一个合法旋转矩阵被拒绝。

同时，容差也不能过大，否则真正错误的矩阵可能被错误接受。

---

## 11. `translate_points(...)`

数值示例中还有：

```python
translate_points(points, offset)
```

这是一个更简单的接口检查与 broadcasting 示例。

输入：

```text
points -> (N, D)
offset -> (D,)
```

真正的数学计算只有：

```python
points_array + offset_array
```

NumPy broadcasting 会把同一个 offset 加到每个点上。

例如：

```text
points =
[[0, 0],
 [1, 2]]

offset =
[0.5, -1]
```

结果：

```text
[[0.5, -1],
 [1.5,  1]]
```

这一段最重要的理解是：

> 数学计算本身可能非常简单，但完整函数仍然需要大量输入检查来保证接口可靠。

---

## 12. 坐标示例

文件：

```text
examples/coordinate_frames.py
```

把前面的几何函数组合成一个完整的三坐标系示例。

核心逻辑可以压缩成：

```python
T_wa = make_transform(rotation_z(np.pi / 2), [1.0, 0.0, 0.0])

T_ab = make_transform(rotation_z(-np.pi / 2), [1.0, 0.0, 0.0])

T_wb = T_wa @ T_ab

p_b = np.array([[1.0, 0.0, 0.0]])

p_w = transform_points(T_wb, p_b)

T_bw = inverse_transform(T_wb)

p_b_roundtrip = transform_points(T_bw, p_w)
```

对应坐标链：

```text
B -> A -> W
```

以及：

```math
T_{wb}
=
T_{wa}T_{ab}
```

---

## 13. 变换顺序

示例还故意计算：

```python
T_reversed = T_ab @ T_wa
```

两个矩阵都是 `(4,4)`，所以在 NumPy 中完全可以相乘。

但是它不表示正确的 B 到 W 坐标链。

这说明：

> 矩阵 shape 合法，不代表坐标系语义合法。

坐标变换必须按照正确的 frame chain 进行组合。

---

## 14. 往返验证

程序先完成：

```text
B -> W
```

然后使用逆变换完成：

```text
W -> B
```

过程为：

```text
p_b
↓
T_wb
↓
p_w
↓
T_bw
↓
p_b_roundtrip
```

本例中：

```text
p_b = [[1. 0. 0.]]
```

最终：

```text
p_b_roundtrip = [[1. 0. 0.]]
```

测得：

```text
max round-trip error = 0.000e+00 m
```

说明正向变换与逆变换之间保持一致。

---

## 15. `coordinate_frames.py` 的程序结构

整个文件可以理解为：

```text
coordinate_frames.py
│
├── build_scene()
├── format_report()
├── render_svg()
├── write_svg()
└── main()
```

### `build_scene()`

这里包含真正重要的机器人几何计算：

- 构造变换
- 组合变换
- 转换点
- 求逆
- 往返验证

### `format_report()`

负责把矩阵和点格式化成终端日志。

它本身不引入新的机器人几何内容。

### `render_svg()`

负责绘制 SVG：

- 网格
- 坐标轴
- 箭头
- 标签
- 点的位置
- W / A / B 坐标系

这一部分主要属于可视化实现，而不是新的刚体变换理论。

### `write_svg()`

负责把 SVG 保存到文件。

### `main()`

负责串联整个程序：

```text
计算场景
↓
打印结果
↓
按需要生成 SVG
↓
保存文件
```

---

## 16. 这一部分最需要长期记住的内容

1. 四个核心几何函数就是前面数学公式的软件版本。
2. 稳定的数值程序必须明确接口要求。
3. shape 检查可以防止错误 broadcasting。
4. `float64` 用于统一数值表示。
5. `NaN` 和无穷值应该在进入几何运算前被拒绝。
6. 合法旋转必须同时满足正交条件和 determinant 为 +1。
7. 浮点数几何检查必须使用合理容差。
8. `transform_points` 可以批量变换多个点。
9. 矩阵相乘顺序必须符合坐标系变换链。
10. 数值上可以相乘的矩阵不一定具有正确的坐标含义。
11. 往返验证可以检查正向与逆变换的一致性。
12. 可视化可以帮助理解，但不能代替数值验证和自动测试。