# M1 — 机器人几何：坐标、旋转与刚体变换

[English](robot_geometry.md) | [中文](robot_geometry_zh.md)

这份笔记记录我在 M1 中对坐标系、旋转矩阵和刚体变换的理解。重点不是单纯记忆矩阵公式，而是理解每个公式背后的几何意义。

---

## 1. 同一个点可以有不同坐标

对于同一个物理点 $P$：

- $p_b$ 表示 P 在 B 坐标系中的坐标。
- $p_a$ 表示同一个 P 在 A 坐标系中的坐标。

例如：

$$
p_b=
\begin{bmatrix}
1\\
2\\
0
\end{bmatrix}
$$

和：

$$
p_a=
\begin{bmatrix}
3\\
5\\
0
\end{bmatrix}
$$

完全可能表示同一个物理点。

点没有移动，只是描述它的坐标系发生了变化。

---

## 2. 点为什么写成列向量

三维点通常写成：

$$
p_b=
\begin{bmatrix}
x_b\\
y_b\\
z_b
\end{bmatrix}
$$

这是一个 $3\times1$ 列向量。

它可以直接和 $3\times3$ 旋转矩阵相乘：

$$
(3\times3)(3\times1)
\rightarrow
(3\times1)
$$

---

## 3. 旋转矩阵记号

$R_{ab}$ 表示 B 相对于 A 的方向关系。

可以理解为：

> $R_{ab}$ 把“在 B 中表达的向量”转换成“在 A 中表达的同一个向量”。

如果两个坐标系原点重合：

$$
p_a=R_{ab}p_b
$$

下标规则：

```text
R_ab
B -> A

输入 = B
输出 = A
```

---

## 4. 旋转矩阵每一列的意义

$R_{ab}$ 的三列分别表示 B 坐标系的三根单位轴在 A 坐标系中的方向。

可以简写为：

```math
R_{ab}
=
\begin{bmatrix}
r_1 & r_2 & r_3
\end{bmatrix}
```

其中：

- $r_1$：B 的 $+x$ 轴在 A 中的方向
- $r_2$：B 的 $+y$ 轴在 A 中的方向
- $r_3$：B 的 $+z$ 轴在 A 中的方向

例如：

```math
p_b
=
\begin{bmatrix}
2\\
1\\
0
\end{bmatrix}
```

表示：

> 沿 B 的 x 轴走 2 个单位，再沿 B 的 y 轴走 1 个单位。

矩阵乘法实际上是在对旋转矩阵的列进行线性组合：

```math
R_{ab}p_b
=
2r_1+r_2
```

因此，$R_{ab}p_b$ 表示把同一段几何位移重新使用 A 坐标系的轴进行表达。

---

## 5. 绕 x、y、z 轴的标准旋转矩阵

### 绕 x 轴

$$
R_x(\theta)=
\begin{bmatrix}
1&0&0\\
0&\cos\theta&-\sin\theta\\
0&\sin\theta&\cos\theta
\end{bmatrix}
$$

### 绕 y 轴

$$
R_y(\theta)=
\begin{bmatrix}
\cos\theta&0&\sin\theta\\
0&1&0\\
-\sin\theta&0&\cos\theta
\end{bmatrix}
$$

### 绕 z 轴

$$
R_z(\theta)=
\begin{bmatrix}
\cos\theta&-\sin\theta&0\\
\sin\theta&\cos\theta&0\\
0&0&1
\end{bmatrix}
$$

例如：

$$
\theta=90^\circ=\frac{\pi}{2}
$$

得到：

$$
R_z(90^\circ)=
\begin{bmatrix}
0&-1&0\\
1&0&0\\
0&0&1
\end{bmatrix}
$$

对应：

```text
+x -> +y
+y -> -x
+z -> +z
```

---

## 6. 右手定则

右手坐标系满足：

$$
x\times y=z
$$

判断正旋转方向时：

- 右手拇指指向旋转轴正方向
- 四指弯曲方向就是正旋转方向

绕 $+z$ 正旋转时，从正 z 方向看向原点：

> $+x$ 到 $+y$ 是逆时针。

---

## 7. 合法旋转矩阵的条件

真正的旋转必须保持长度和夹角。

因此：

$$
R^TR=I
$$

这说明旋转矩阵的三列是互相垂直的单位向量。

同时：

$$
R^{-1}=R^T
$$

但仅仅满足正交条件还不够。

合法旋转还需要：

$$
\det(R)=1
$$

所以：

$$
\boxed{R^TR=I}
$$

以及：

$$
\boxed{\det(R)=1}
$$

---

## 8. 旋转不会改变长度

如果：

$$
p_a=Rp_b
$$

那么合法旋转满足：

$$
\|p_a\|=\|p_b\|
$$

例如：

$$
p_b=
\begin{bmatrix}
2\\
1\\
0
\end{bmatrix}
$$

长度为：

$$
\sqrt{2^2+1^2}=\sqrt5
$$

旋转后仍然应该是 $\sqrt5$。

---

## 9. 加入坐标系原点之间的平移

定义 $t_{ab}$：

> B 原点在 A 坐标系中的位置。

完整变换：

$$
\boxed{
p_a=R_{ab}p_b+t_{ab}
}
$$

其中：

- $R_{ab}p_b$：把 B 原点到 P 的位移转换到 A 中表达
- $t_{ab}$：A 原点到 B 原点的位置

---

## 10. 多级平移为什么不能直接相加

$t_{wa}$ 表示：

> A 原点在 W 中的位置。

$t_{ab}$ 表示：

> B 原点在 A 中的位置。

二者不能直接相加。

必须先：

$$
R_{wa}t_{ab}
$$

把 $t_{ab}$ 转换到 W 中。

然后：

$$
\boxed{
t_{wb}=R_{wa}t_{ab}+t_{wa}
}
$$

核心原则：

> 两个向量只有在同一坐标系中表达后才能直接相加。

---

## 11. 齐次坐标

刚体变换公式为：

```math
p_a
=
R_{ab}p_b+t_{ab}
```

这个公式同时包含矩阵乘法和平移加法。

为了把旋转和平移统一成一次矩阵乘法，可以给三维点增加一个额外坐标：

```math
\tilde p
=
\begin{bmatrix}
x\\
y\\
z\\
1
\end{bmatrix}
```

然后构造齐次变换矩阵：

```math
T_{ab}
=
\begin{bmatrix}
R_{ab} & t_{ab}\\
0 & 1
\end{bmatrix}
```

完整展开为：

```math
T_{ab}
=
\begin{bmatrix}
r_{11} & r_{12} & r_{13} & t_x\\
r_{21} & r_{22} & r_{23} & t_y\\
r_{31} & r_{32} & r_{33} & t_z\\
0 & 0 & 0 & 1
\end{bmatrix}
```

这样坐标变换可以统一写成：

```math
\begin{bmatrix}
p_a\\
1
\end{bmatrix}
=
T_{ab}
\begin{bmatrix}
p_b\\
1
\end{bmatrix}
```

最后增加的这一维并不表示现实物理空间真的变成了四维。

它只是一个数学表示技巧，用于把平移也包含进矩阵乘法。

---

## 12. 点和方向向量为什么不同

一个点的齐次表示为：

```math
\tilde p
=
\begin{bmatrix}
x\\
y\\
z\\
1
\end{bmatrix}
```

而一个纯方向向量表示为：

```math
\tilde v
=
\begin{bmatrix}
v_x\\
v_y\\
v_z\\
0
\end{bmatrix}
```

对方向向量应用刚体变换：

```math
\tilde v_a
=
T_{ab}\tilde v_b
```

结果为：

```math
\tilde v_a
=
\begin{bmatrix}
R_{ab}v_b\\
0
\end{bmatrix}
```

因此：

```math
v_a
=
R_{ab}v_b
```

由于方向向量最后一个齐次坐标是 0，所以平移项不会参与计算。

这符合几何意义：

> 平移会改变点的位置，但不会改变一个纯方向。

---

## 13. NumPy 中批量变换多个点

如果：

```text
points_b.shape = (N, 3)
```

可以写：

```python
points_a = (R_ab @ points_b.T).T + t_ab
```

也可以写：

```python
points_a = points_b @ R_ab.T + t_ab
```

这里需要区分：

- 数学上通常把点写成列向量
- NumPy 批量数据通常每一行存一个点

---

## 14. 多级坐标变换组合

对于：

```text
B -> A -> W
```

总变换：

$$
\boxed{
T_{wb}=T_{wa}T_{ab}
}
$$

因为：

$$
p_a=T_{ab}p_b
$$

以及：

$$
p_w=T_{wa}p_a
$$

所以：

$$
p_w=T_{wa}T_{ab}p_b
$$

下标可以辅助检查：

$$
T_{w\cancel a}T_{\cancel a b}=T_{wb}
$$

---

## 15. 旋转和平移组合

对于：

$$
T_{wb}=T_{wa}T_{ab}
$$

组合后的旋转为：

$$
R_{wb}=R_{wa}R_{ab}
$$

组合后的平移为：

$$
t_{wb}=R_{wa}t_{ab}+t_{wa}
$$

这里的 $t_{ab}$ 原本是在 A 坐标系中表达的。

因此必须先通过：

$$
R_{wa}t_{ab}
$$

把它转换成 W 坐标系中的表达，才能和 $t_{wa}$ 相加。

---

## 16. 三坐标系例题

已知 A 原点在 W 中的位置：

```math
t_{wa}
=
\begin{bmatrix}
1\\
0\\
0
\end{bmatrix}
```

A 相对 W 绕 z 轴旋转 $+90^\circ$。

B 原点在 A 中的位置：

```math
t_{ab}
=
\begin{bmatrix}
1\\
0\\
0
\end{bmatrix}
```

B 相对 A 绕 z 轴旋转 $-90^\circ$。

点 P 在 B 中的坐标：

```math
p_b
=
\begin{bmatrix}
1\\
0\\
0
\end{bmatrix}
```

A 到 W 的旋转矩阵：

```math
R_{wa}
=
\begin{bmatrix}
0 & -1 & 0\\
1 & 0 & 0\\
0 & 0 & 1
\end{bmatrix}
```

B 到 A 的旋转矩阵：

```math
R_{ab}
=
\begin{bmatrix}
0 & 1 & 0\\
-1 & 0 & 0\\
0 & 0 & 1
\end{bmatrix}
```

总旋转为：

```math
R_{wb}
=
R_{wa}R_{ab}
=
I
```

接下来计算 B 原点在 W 中的位置。

首先把 $t_{ab}$ 从 A 坐标系转换到 W 坐标系：

```math
R_{wa}t_{ab}
=
\begin{bmatrix}
0\\
1\\
0
\end{bmatrix}
```

然后：

```math
t_{wb}
=
R_{wa}t_{ab}+t_{wa}
```

因此：

```math
t_{wb}
=
\begin{bmatrix}
0\\
1\\
0
\end{bmatrix}
+
\begin{bmatrix}
1\\
0\\
0
\end{bmatrix}
=
\begin{bmatrix}
1\\
1\\
0
\end{bmatrix}
```

最后计算 P 在 W 中的位置：

```math
p_w
=
R_{wb}p_b+t_{wb}
```

因为 $R_{wb}=I$：

```math
p_w
=
\begin{bmatrix}
1\\
0\\
0
\end{bmatrix}
+
\begin{bmatrix}
1\\
1\\
0
\end{bmatrix}
=
\begin{bmatrix}
2\\
1\\
0
\end{bmatrix}
```

因此：

```math
p_w
=
\begin{bmatrix}
2\\
1\\
0
\end{bmatrix}
```

---

## 17. 逆变换

从正向变换开始：

```math
p_a
=
R_{ab}p_b+t_{ab}
```

首先去掉平移：

```math
p_a-t_{ab}
=
R_{ab}p_b
```

然后乘旋转矩阵的逆：

```math
p_b
=
R_{ab}^{-1}(p_a-t_{ab})
```

对于合法旋转矩阵：

```math
R_{ab}^{-1}
=
R_{ab}^{T}
```

所以：

```math
p_b
=
R_{ab}^{T}(p_a-t_{ab})
```

逆旋转为：

```math
R_{ba}
=
R_{ab}^{T}
```

逆平移为：

```math
t_{ba}
=
-R_{ab}^{T}t_{ab}
```

因此完整逆齐次变换为：

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

需要特别注意：

> 逆变换中的平移通常不是简单的 $-t_{ab}$。

因为它还必须使用新的输出坐标系进行表达。

---

## 18. 如何验证结果

### 旋转矩阵合法性

$$
R^TR\approx I
$$

并且：

$$
\det(R)\approx1
$$

### 长度保持

$$
\|Rp\|\approx\|p\|
$$

### 往返检查

```text
B -> A -> B
```

最后应该回到原始点附近。

### 独立手算

不能只做往返测试，因为两个一致的错误可能互相抵消。

---

## 19. 常见错误

### 把 `@` 写成 `*`

正确：

```python
R @ p
```

错误：

```python
R * p
```

### 把角度直接传给 `sin` / `cos`

NumPy 使用弧度：

```python
theta = np.deg2rad(90.0)
```

或者：

```python
theta = np.pi / 2
```

### 米和毫米混用

差 1000 倍时优先检查单位。

### `(3,)` 与 `(1,3)` 混淆

单点可能需要：

```python
[[x, y, z]]
```

而不是：

```python
[x, y, z]
```

### 把反射当成旋转

即使：

$$
R^TR=I
$$

仍然需要检查：

$$
\det(R)=1
$$

---

## 20. 这一部分最需要长期记住的内容

1. 同一个物理点在不同坐标系中可以有不同坐标。
2. 坐标必须与参考坐标系一起理解。
3. $R_{ab}$ 把 B 中的坐标表达转换成 A 中的表达。
4. $R_{ab}$ 的三列表示 B 的三根单位轴在 A 中的方向。
5. 合法旋转满足 $R^TR=I$ 和 $\det(R)=1$。
6. 纯旋转不改变向量长度。
7. 位移向量必须先统一坐标系才能相加。
8. 刚体变换核心公式是 $p_a=R_{ab}p_b+t_{ab}$。
9. 齐次坐标把旋转和平移统一为一次矩阵乘法。
10. 点的齐次末位为 1，方向向量为 0。
11. 多级变换从右往左作用。
12. 下标必须正确连接。
13. 旋转矩阵的逆等于转置。
14. 逆平移通常是 $-R^Tt$。
15. 坐标变换代码要同时检查坐标系、单位、shape、数值误差和几何性质。