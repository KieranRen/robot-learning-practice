# Modern Robotics — M1 教材阅读记录

[English](modern_robotics_reading.md) | [中文](modern_robotics_reading_zh.md)

## 阅读来源

Kevin M. Lynch, Frank C. Park, *Modern Robotics: Mechanics, Planning, and Control*, Cambridge University Press, 2017.

本次使用 May 2017 preprint，并按照 M1 的静态机器人几何学习范围进行阅读。

## 阅读范围

本次 M1 实际阅读：

- Section 3.2.1 — Rotation Matrices
- Section 3.3.1 — Homogeneous Transformation Matrices

本次没有继续学习角速度、twists、exponential coordinates 等后续内容，因为它们不属于当前 M1 的最小完成范围。

---

## 1. Rotation Matrices

### 旋转矩阵的约束

三维旋转矩阵：

```math
R \in SO(3)
```

必须满足：

```math
R^T R = I
```

以及：

```math
\det(R) = +1
```

`R^T R = I` 表示矩阵列向量互相正交且长度为 1。

仅满足正交性还不够。例如：

```math
\begin{bmatrix}
1 & 0 & 0\\
0 & 1 & 0\\
0 & 0 & -1
\end{bmatrix}
```

虽然满足：

```math
R^T R = I
```

但 determinant 为 `-1`，表示反射而不是 proper rotation。

### 逆旋转

对于：

```math
R \in SO(3)
```

有：

```math
R^{-1} = R^T
```

这与个人实现中使用 transpose 构造逆旋转一致。

### 组合

两个旋转矩阵相乘仍是旋转矩阵。

矩阵乘法满足结合律，但通常不满足交换律：

```math
R_1 R_2 \neq R_2 R_1
```

### 长度保持

若：

```math
y = Rx
```

则：

```math
\|y\| = \|x\|
```

因此合法刚体旋转不会改变向量长度。

### 坐标系下标

`R_ab` 表示 frame B 的 orientation 用 frame A 表达。

旋转矩阵的列对应 B 的三个单位坐标轴在 A 中的方向。

坐标变换：

```math
R_{ab} p_b = p_a
```

表示同一个几何对象从 B 坐标表达转换为 A 坐标表达。

组合满足：

```math
R_{ab} R_{bc} = R_{ac}
```

可以使用下标消去规则检查 frame chain。

---

## 2. Homogeneous Transformation Matrices

刚体位姿将旋转和平移组合为：

```math
T =
\begin{bmatrix}
R & p\\
0 & 1
\end{bmatrix}
```

其中：

- `R` 是 3×3 rotation matrix
- `p` 是 3×1 translation
- `T` 是 4×4 homogeneous transformation matrix

合法三维刚体变换属于：

```math
SE(3)
```

### 齐次坐标

三维点可以写成：

```math
\begin{bmatrix}
x\\
1
\end{bmatrix}
```

于是：

```math
T
\begin{bmatrix}
x\\
1
\end{bmatrix}
=
\begin{bmatrix}
Rx+p\\
1
\end{bmatrix}
```

这样旋转和平移可以统一为一次矩阵运算。

### 逆变换

对于：

```math
T =
\begin{bmatrix}
R & p\\
0 & 1
\end{bmatrix}
```

逆变换为：

```math
T^{-1}
=
\begin{bmatrix}
R^T & -R^T p\\
0 & 1
\end{bmatrix}
```

这与个人实现：

```python
R_inv = R.T
t_inv = -R_inv @ t
```

完全一致。

### 变换组合

Transformation matrices 一般不满足交换律。

Frame chain：

```math
T_{ab} T_{bc} = T_{ac}
```

与前面 M1 中使用的：

```math
T_{wa} T_{ab} = T_{wb}
```

具有相同的下标消去逻辑。

### 刚体不变量

Rigid transformation 保持：

- 两点距离
- 两向量夹角

因此不会产生 scaling、shear 或其他非刚体形变。

---

## 3. Fixed-Frame 与 Body-Frame 变换

这是本次教材阅读相对于前面 M1 实现最重要的新补充。

设当前刚体姿态为：

```math
T_{sb}
```

### 左乘

```math
T_{\text{new}} = \Delta T\, T_{sb}
```

表示增量变换 `ΔT` 在 fixed / space frame 中解释。

即：

> 按世界坐标系定义的方向进行旋转或平移。

### 右乘

```math
T_{\text{new}} = T_{sb}\, \Delta T
```

表示增量变换 `ΔT` 在当前 body frame 中解释。

即：

> 按机器人自身坐标系定义的方向进行旋转或平移。

一个直观例子：

若机器人已经绕世界 z 轴旋转 90°，此时增量平移为：

```text
[1, 0, 0]
```

左乘表示沿世界 +x 移动。

右乘表示沿机器人自身 +x 移动；由于机器人自身 +x 此时指向世界 +y，因此世界坐标中的实际位移是 +y。

因此：

> 左乘可以理解为“按地图坐标动”，右乘可以理解为“按机器人自身坐标动”。

---

## 4. 与 M1 能力任务的对应

### GEOM-T01

教材进一步确认：

- rotation matrix 的列表示坐标轴方向
- `R^T R = I`
- `det(R) = +1`
- rotation preserves vector length

### GEOM-T02

教材正式给出：

```math
p_a = R_{ab}p_b + t_{ab}
```

以及：

```math
T^{-1}
=
\begin{bmatrix}
R^T & -R^Tt\\
0 & 1
\end{bmatrix}
```

与个人实现一致。

### GEOM-T03

教材明确说明：

- transformation composition generally does not commute
- frame chain 可以通过下标消去检查
- `T_ab T_bc = T_ac`

这与受控失败实验中错误交换矩阵顺序的结果一致。

### GEOM-T04

教材中的多坐标系机器人例子展示了实际系统中如何通过已知 frame transforms 组合和求逆，得到目标 frame 之间的关系。

这说明 M1 中的 W、A、B 坐标系练习是更复杂机器人 frame graph 的基础形式。

---

## 5. 阅读后的主要新认识

M1 前面的实现和测试已经覆盖了本节大部分核心数学。

本次教材阅读最重要的新补充是：

> 同一个增量变换放在当前位姿左侧或右侧，代表增量分别在 fixed frame 或 body frame 中解释。

即：

```text
ΔT @ T_old
= fixed-frame update

T_old @ ΔT
= body-frame update
```

这一区别将在后续机器人运动学、机械臂姿态更新和移动机器人运动中反复出现。

---

## 6. M1 教材阅读结论

本次 M1 指定教材阅读已完成。

实际覆盖：

```text
Modern Robotics
Section 3.2.1 — Rotation Matrices
Section 3.3.1 — Homogeneous Transformation Matrices
```

阅读内容已经与：

```text
GEOM-T01
GEOM-T02
GEOM-T03
GEOM-T04
```

逐项核对。

至此，M1 要求的教材阅读、个人实现、自动测试、手算验证、失败分析与综合能力任务均已完成。