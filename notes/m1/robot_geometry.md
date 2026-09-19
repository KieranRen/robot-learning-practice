# M1 — Robot Geometry: Coordinate Frames, Rotations, and Rigid Transforms

[English](robot_geometry.md) | [中文](robot_geometry_zh.md)

This note records my understanding of coordinate frames, rotation matrices, and rigid-body transformations studied in M1.

---

## 1. The Same Point Can Have Different Coordinates

For the same physical point $P$:

- $p_b$ means the coordinates of $P$ expressed in frame B.
- $p_a$ means the coordinates of the same point expressed in frame A.

For example:

$$
p_b =
\begin{bmatrix}
1\\
2\\
0
\end{bmatrix}
$$

and

$$
p_a =
\begin{bmatrix}
3\\
5\\
0
\end{bmatrix}
$$

may represent the same physical point.

The point has not moved. Only the coordinate frame used to describe it has changed.

---

## 2. Points as Column Vectors

A three-dimensional point is written mathematically as:

$$
p_b =
\begin{bmatrix}
x_b\\
y_b\\
z_b
\end{bmatrix}
$$

This is a $3\times1$ column vector.

It can be multiplied directly by a $3\times3$ rotation matrix:

$$
(3\times3)(3\times1)
\rightarrow
(3\times1)
$$

---

## 3. Rotation-Matrix Notation

The matrix $R_{ab}$ describes the orientation of frame B relative to frame A.

A useful interpretation is:

> $R_{ab}$ converts vector coordinates from frame B into frame A.

If the coordinate-frame origins coincide:

$$
p_a=R_{ab}p_b
$$

Subscript convention:

```text
R_ab
B -> A

input  = B
output = A
```

---

## 4. Columns of a Rotation Matrix

The three columns of $R_{ab}$ are the three unit axes of frame B expressed in frame A.

A compact representation is:

```math
R_{ab}
=
\begin{bmatrix}
r_1 & r_2 & r_3
\end{bmatrix}
```

where:

- $r_1$ is the $+x$ axis of B expressed in A
- $r_2$ is the $+y$ axis of B expressed in A
- $r_3$ is the $+z$ axis of B expressed in A

For example:

```math
p_b=
\begin{bmatrix}
2\\
1\\
0
\end{bmatrix}
```

means:

> 2 units along the B-frame x axis, plus 1 unit along the B-frame y axis.

Matrix multiplication forms a linear combination of the columns:

```math
R_{ab}p_b
=
2r_1+r_2
```

Therefore, $R_{ab}p_b$ expresses the same geometric displacement using the axes of frame A.

---

## 5. Standard Rotation Matrices

### Rotation about x

$$
R_x(\theta)=
\begin{bmatrix}
1&0&0\\
0&\cos\theta&-\sin\theta\\
0&\sin\theta&\cos\theta
\end{bmatrix}
$$

### Rotation about y

$$
R_y(\theta)=
\begin{bmatrix}
\cos\theta&0&\sin\theta\\
0&1&0\\
-\sin\theta&0&\cos\theta
\end{bmatrix}
$$

### Rotation about z

$$
R_z(\theta)=
\begin{bmatrix}
\cos\theta&-\sin\theta&0\\
\sin\theta&\cos\theta&0\\
0&0&1
\end{bmatrix}
$$

For:

$$
\theta=90^\circ=\frac{\pi}{2}
$$

we obtain:

$$
R_z(90^\circ)=
\begin{bmatrix}
0&-1&0\\
1&0&0\\
0&0&1
\end{bmatrix}
$$

This maps:

```text
+x -> +y
+y -> -x
+z -> +z
```

---

## 6. Right-Hand Rule

The coordinate system is right-handed:

$$
x\times y=z
$$

For positive rotation:

- point the right thumb along the positive rotation axis
- the curled fingers show the positive rotation direction

For positive rotation about $+z$, the direction from $+x$ toward $+y$ is counterclockwise when viewed from the positive z side.

---

## 7. Valid Rotation Matrices

A rigid rotation preserves vector lengths and angles.

Therefore:

$$
R^TR=I
$$

This means the columns of $R$ are orthonormal.

A useful consequence is:

$$
R^{-1}=R^T
$$

A proper rotation also requires:

$$
\det(R)=1
$$

So:

$$
\boxed{R^TR=I}
$$

and:

$$
\boxed{\det(R)=1}
$$

---

## 8. Rotation Preserves Length

For:

$$
p_a=Rp_b
$$

a valid rotation satisfies:

$$
\|p_a\|=\|p_b\|
$$

For example:

$$
p_b=
\begin{bmatrix}
2\\
1\\
0
\end{bmatrix}
$$

has length:

$$
\sqrt{2^2+1^2}=\sqrt5
$$

The rotated vector must have the same length.

---

## 9. Adding Translation

Let $t_{ab}$ represent the position of the B origin expressed in A.

Then:

$$
\boxed{
p_a=R_{ab}p_b+t_{ab}
}
$$

Here:

- $R_{ab}p_b$ converts the B-frame displacement into A coordinates.
- $t_{ab}$ adds the location of the B origin relative to A.

---

## 10. Translation Across Multiple Frames

Suppose:

- $t_{wa}$ is the A origin expressed in W.
- $t_{ab}$ is the B origin expressed in A.

They cannot be added directly.

First convert $t_{ab}$ into W coordinates:

$$
R_{wa}t_{ab}
$$

Then:

$$
\boxed{
t_{wb}=R_{wa}t_{ab}+t_{wa}
}
$$

---

## 11. Homogeneous Coordinates

The rigid-body transformation equation is:

```math
p_a=R_{ab}p_b+t_{ab}
```

This equation contains both a matrix multiplication and an addition.

To represent rotation and translation using one matrix multiplication, a 3D point is extended with an additional coordinate:

```math
\tilde p=
\begin{bmatrix}
x\\
y\\
z\\
1
\end{bmatrix}
```

The homogeneous transformation matrix is:

```math
T_{ab}
=
\begin{bmatrix}
R_{ab} & t_{ab}\\
0 & 1
\end{bmatrix}
```

More explicitly:

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

The coordinate transformation can then be written as:

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

The additional coordinate does not mean that physical space has become four-dimensional.

It is a mathematical device that allows translation to be included inside matrix multiplication.

---

## 12. Points and Direction Vectors

A point uses the homogeneous representation:

```math
\tilde p=
\begin{bmatrix}
x\\
y\\
z\\
1
\end{bmatrix}
```

A pure direction vector uses:

```math
\tilde v=
\begin{bmatrix}
v_x\\
v_y\\
v_z\\
0
\end{bmatrix}
```

Applying a rigid transform to a direction vector gives:

```math
\tilde v_a
=
T_{ab}\tilde v_b
```

which becomes:

```math
\tilde v_a
=
\begin{bmatrix}
R_{ab}v_b\\
0
\end{bmatrix}
```

Therefore:

```math
v_a=R_{ab}v_b
```

The translation term disappears because the final homogeneous coordinate of a direction vector is zero.

This matches the geometric meaning:

> Translation changes the position of a point, but does not change a pure direction.

---

## 13. Transforming Multiple Points

For:

```text
points_b.shape = (N, 3)
```

one implementation is:

```python
points_a = (R_ab @ points_b.T).T + t_ab
```

An equivalent row-storage form is:

```python
points_a = points_b @ R_ab.T + t_ab
```

---

## 14. Transform Composition

For:

```text
B -> A -> W
```

the combined transform is:

$$
\boxed{
T_{wb}=T_{wa}T_{ab}
}
$$

because:

$$
p_a=T_{ab}p_b
$$

and:

$$
p_w=T_{wa}p_a
$$

therefore:

$$
p_w=T_{wa}T_{ab}p_b
$$

The subscripts provide a useful consistency check:

$$
T_{w\cancel a}T_{\cancel a b}=T_{wb}
$$

---

## 15. Rotation and Translation Composition

For the transform chain

$$
T_{wb}=T_{wa}T_{ab}
$$

the combined rotation is:

$$
R_{wb}=R_{wa}R_{ab}
$$

The combined translation is:

$$
t_{wb}=R_{wa}t_{ab}+t_{wa}
$$

The term $t_{ab}$ is originally expressed in frame A.

Therefore it must first be converted into frame W using:

$$
R_{wa}t_{ab}
$$

before it can be added to $t_{wa}$.

---

## 16. Three-Frame Example

Suppose the origin of frame A expressed in frame W is:

```math
t_{wa}
=
\begin{bmatrix}
1\\
0\\
0
\end{bmatrix}
```

Frame A is rotated $+90^\circ$ about the z axis relative to W.

The origin of frame B expressed in frame A is:

```math
t_{ab}
=
\begin{bmatrix}
1\\
0\\
0
\end{bmatrix}
```

Frame B is rotated $-90^\circ$ about the z axis relative to A.

The point P expressed in frame B is:

```math
p_b
=
\begin{bmatrix}
1\\
0\\
0
\end{bmatrix}
```

The rotation from A to W is:

```math
R_{wa}
=
\begin{bmatrix}
0 & -1 & 0\\
1 & 0 & 0\\
0 & 0 & 1
\end{bmatrix}
```

The rotation from B to A is:

```math
R_{ab}
=
\begin{bmatrix}
0 & 1 & 0\\
-1 & 0 & 0\\
0 & 0 & 1
\end{bmatrix}
```

The combined rotation is:

```math
R_{wb}
=
R_{wa}R_{ab}
=
I
```

Now calculate the translation from B to W.

First convert $t_{ab}$ from frame A into frame W:

```math
R_{wa}t_{ab}
=
\begin{bmatrix}
0\\
1\\
0
\end{bmatrix}
```

Then:

```math
t_{wb}
=
R_{wa}t_{ab}+t_{wa}
```

so:

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

Finally:

```math
p_w
=
R_{wb}p_b+t_{wb}
```

Since $R_{wb}=I$:

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

Therefore:

```math
p_w=
\begin{bmatrix}
2\\
1\\
0
\end{bmatrix}
```

---

## 17. Inverse Transform

Start from the forward transformation:

```math
p_a
=
R_{ab}p_b+t_{ab}
```

First remove the translation:

```math
p_a-t_{ab}
=
R_{ab}p_b
```

Then multiply by the inverse rotation:

```math
p_b
=
R_{ab}^{-1}(p_a-t_{ab})
```

For a valid rotation matrix:

```math
R_{ab}^{-1}
=
R_{ab}^{T}
```

Therefore:

```math
p_b
=
R_{ab}^{T}(p_a-t_{ab})
```

The inverse rotation is:

```math
R_{ba}
=
R_{ab}^{T}
```

The inverse translation is:

```math
t_{ba}
=
-R_{ab}^{T}t_{ab}
```

Therefore the inverse homogeneous transform is:

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

The inverse translation is generally not simply $-t_{ab}$.

It must also be expressed in the new output coordinate frame.

---

## 18. Validation

Useful checks include:

### Rotation validity

$$
R^TR\approx I
$$

and:

$$
\det(R)\approx1
$$

### Length preservation

$$
\|Rp\|\approx\|p\|
$$

### Round-trip consistency

```text
B -> A -> B
```

The final point should be close to the original point.

### Independent hand calculation

Round-trip tests alone are not sufficient because two matching implementation mistakes can sometimes cancel each other.

---

## 19. Common Failure Modes

### `*` instead of `@`

Correct:

```python
R @ p
```

Incorrect for matrix multiplication:

```python
R * p
```

### Degrees instead of radians

Use:

```python
theta = np.deg2rad(90.0)
```

or:

```python
theta = np.pi / 2
```

### Unit mismatch

A factor-of-1000 error often indicates millimetres were mixed with metres.

### Shape mismatch

A batch interface may require:

```text
(N, 3)
```

so one point may need:

```python
[[x, y, z]]
```

instead of:

```python
[x, y, z]
```

### Reflection mistaken for rotation

A reflection can satisfy:

$$
R^TR=I
$$

but have:

$$
\det(R)=-1
$$

---

## 20. Main Lessons

1. A physical point may have different coordinates in different frames without moving.
2. Coordinates must always be interpreted together with their reference frame.
3. $R_{ab}$ converts coordinates from B to A.
4. The columns of $R_{ab}$ are B's axes expressed in A.
5. A valid rotation satisfies $R^TR=I$ and $\det(R)=1$.
6. Pure rotation preserves vector length.
7. Translation vectors can only be added after being expressed in the same frame.
8. A rigid transform follows $p_a=R_{ab}p_b+t_{ab}$.
9. Homogeneous coordinates combine rotation and translation into one matrix.
10. Points use homogeneous coordinate 1; directions use 0.
11. Transform chains act from right to left.
12. Frame subscripts should connect consistently.
13. The inverse rotation is the transpose.
14. The inverse translation is generally $-R^Tt$.
15. Geometry code must check frames, units, shape, numerical accuracy, and geometric invariants.