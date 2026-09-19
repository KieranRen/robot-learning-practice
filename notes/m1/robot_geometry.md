# M1 — Robot Geometry: Coordinate Frames, Rotations, and Rigid Transforms

[English](robot_geometry.md) | [中文](robot_geometry_zh.md)

This note records my understanding of the coordinate-frame and rigid-body transformation concepts studied in M1. The focus is on the geometric meaning behind the equations, not only on memorizing matrix formulas.

---

## 1. The Same Point Can Have Different Coordinates

A physical point does not change its position simply because a different coordinate frame is used to describe it.

For the same point \(P\):

\[
p_b
\]

means the coordinates of \(P\) expressed in frame \(B\), while

\[
p_a
\]

means the coordinates of the same physical point expressed in frame \(A\).

For example:

\[
p_b =
\begin{bmatrix}
1\\
2\\
0
\end{bmatrix}
\]

and

\[
p_a =
\begin{bmatrix}
3\\
5\\
0
\end{bmatrix}
\]

may describe the same point using two different origins and axis directions.

A coordinate vector must therefore always be interpreted together with its reference frame.

---

## 2. Points as Column Vectors

A three-dimensional point is written mathematically as a \(3 \times 1\) column vector:

\[
p_b =
\begin{bmatrix}
x_b\\
y_b\\
z_b
\end{bmatrix}
\]

The three values describe how far the point lies along the \(x\), \(y\), and \(z\) axes of frame \(B\).

The column-vector form is convenient because it can be multiplied directly by a \(3 \times 3\) rotation matrix:

\[
(3 \times 3)(3 \times 1)
\rightarrow
(3 \times 1)
\]

---

## 3. Rotation-Matrix Notation

The matrix

\[
R_{ab}
\]

describes the orientation of frame \(B\) relative to frame \(A\).

A useful interpretation is:

> \(R_{ab}\) converts a vector expressed in frame \(B\) into the same vector expressed in frame \(A\).

Therefore:

\[
p_a = R_{ab}p_b
\]

when the two coordinate-frame origins coincide.

The subscript convention is:

```text
R_ab
B -> A

input frame  = B
output frame = A
```

---

## 4. Columns of a Rotation Matrix

The three columns of \(R_{ab}\) are the three unit axes of frame \(B\), expressed in frame \(A\).

If

\[
R_{ab}
=
\begin{bmatrix}
| & | & |\\
r_1 & r_2 & r_3\\
| & | & |
\end{bmatrix}
\]

then:

- \(r_1\) is the \(+x\) axis of \(B\) expressed in \(A\)
- \(r_2\) is the \(+y\) axis of \(B\) expressed in \(A\)
- \(r_3\) is the \(+z\) axis of \(B\) expressed in \(A\)

This explains why multiplying a rotation matrix by a coordinate vector forms a linear combination of its columns.

For example:

\[
p_b =
\begin{bmatrix}
2\\
1\\
0
\end{bmatrix}
\]

means:

> 2 units along the \(B\)-frame x axis, plus 1 unit along the \(B\)-frame y axis.

Then

\[
R_{ab}p_b
\]

expresses the same geometric displacement using the axes of frame \(A\).

---

## 5. Rotation About the Coordinate Axes

Using the right-hand rule, the standard rotation matrices are:

### Rotation about the x axis

\[
R_x(\theta)=
\begin{bmatrix}
1&0&0\\
0&\cos\theta&-\sin\theta\\
0&\sin\theta&\cos\theta
\end{bmatrix}
\]

### Rotation about the y axis

\[
R_y(\theta)=
\begin{bmatrix}
\cos\theta&0&\sin\theta\\
0&1&0\\
-\sin\theta&0&\cos\theta
\end{bmatrix}
\]

### Rotation about the z axis

\[
R_z(\theta)=
\begin{bmatrix}
\cos\theta&-\sin\theta&0\\
\sin\theta&\cos\theta&0\\
0&0&1
\end{bmatrix}
\]

For example, with

\[
\theta=90^\circ=\frac{\pi}{2}
\]

we obtain:

\[
R_z(90^\circ)=
\begin{bmatrix}
0&-1&0\\
1&0&0\\
0&0&1
\end{bmatrix}
\]

This maps:

```text
+x -> +y
+y -> -x
+z -> +z
```

The z axis remains unchanged because the rotation is about the z axis.

---

## 6. Right-Hand Rule

The coordinate frames used here are right-handed.

The axis relationship is:

\[
x \times y = z
\]

For a positive rotation about an axis:

- point the right-hand thumb along the positive axis direction
- the curled fingers indicate the positive rotation direction

For a positive rotation around \(+z\), viewed from the positive z side toward the origin, rotation from \(+x\) toward \(+y\) is counterclockwise.

---

## 7. Properties of a Valid Rotation Matrix

A rigid rotation must preserve lengths and angles.

Therefore the columns of a rotation matrix must:

- each have unit length
- be mutually perpendicular

This gives:

\[
R^T R = I
\]

Such a matrix is orthogonal.

An important consequence is:

\[
R^{-1}=R^T
\]

However, orthogonality alone is not sufficient for a proper rotation.

A reflection matrix can also satisfy:

\[
R^T R=I
\]

Therefore a proper 3D rotation must also satisfy:

\[
\det(R)=+1
\]

So a valid rotation matrix satisfies:

\[
\boxed{R^TR=I}
\]

and

\[
\boxed{\det(R)=1}
\]

The first condition checks orthonormality, while the second excludes reflections.

---

## 8. Rotation Preserves Vector Length

A pure rotation changes direction but does not change vector length.

If:

\[
p_a=Rp_b
\]

then:

\[
\|p_a\|=\|p_b\|
\]

For example:

\[
p_b=
\begin{bmatrix}
2\\
1\\
0
\end{bmatrix}
\]

has length:

\[
\sqrt{2^2+1^2}=\sqrt{5}
\]

After a valid rotation, the transformed vector must still have length \(\sqrt{5}\).

This provides a useful numerical check for rotation implementations.

---

## 9. Adding Translation Between Coordinate Origins

If the origins of frames \(A\) and \(B\) are not the same, rotation alone is not enough.

Let:

\[
t_{ab}
\]

represent the position of the origin of frame \(B\), expressed in frame \(A\).

Then the complete coordinate transformation is:

\[
\boxed{
p_a = R_{ab}p_b+t_{ab}
}
\]

The two terms have different meanings:

\[
R_{ab}p_b
\]

converts the displacement from the B origin to the point into A-frame coordinates.

Then:

\[
t_{ab}
\]

adds the displacement from the A origin to the B origin.

Both terms must be expressed in the same coordinate frame before they can be added.

---

## 10. Why Translation Must Sometimes Be Rotated First

Suppose:

\[
t_{wa}
\]

is the position of the A origin in frame W, while

\[
t_{ab}
\]

is the position of the B origin in frame A.

They cannot be added directly because they are expressed in different frames.

First convert \(t_{ab}\) into W coordinates:

\[
R_{wa}t_{ab}
\]

Then:

\[
\boxed{
t_{wb}=R_{wa}t_{ab}+t_{wa}
}
\]

This is one of the most important ideas in multi-frame problems:

> Vectors can only be added directly when they are expressed in the same coordinate frame.

---

## 11. Homogeneous Coordinates

A rigid transform contains both rotation and translation:

\[
p_a=R_{ab}p_b+t_{ab}
\]

To represent both operations using one matrix multiplication, a 3D point is extended with an additional coordinate:

\[
\tilde p=
\begin{bmatrix}
x\\
y\\
z\\
1
\end{bmatrix}
\]

The homogeneous transformation matrix is:

\[
T_{ab}
=
\begin{bmatrix}
R_{ab}&t_{ab}\\
0&1
\end{bmatrix}
\]

or explicitly:

\[
T_{ab}
=
\begin{bmatrix}
r_{11}&r_{12}&r_{13}&t_x\\
r_{21}&r_{22}&r_{23}&t_y\\
r_{31}&r_{32}&r_{33}&t_z\\
0&0&0&1
\end{bmatrix}
\]

Then:

\[
\boxed{
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
}
\]

The extra coordinate does not mean that physical space has become four-dimensional. It is a mathematical device that allows translation to be included inside matrix multiplication.

---

## 12. Points and Direction Vectors in Homogeneous Form

A point uses:

\[
\begin{bmatrix}
x\\
y\\
z\\
1
\end{bmatrix}
\]

so translation contributes to the result.

A pure direction vector uses:

\[
\begin{bmatrix}
v_x\\
v_y\\
v_z\\
0
\end{bmatrix}
\]

Then:

\[
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}
\begin{bmatrix}
v\\
0
\end{bmatrix}
=
\begin{bmatrix}
Rv\\
0
\end{bmatrix}
\]

The translation disappears because it is multiplied by zero.

This matches the physical interpretation:

> A point has a position and is affected by translation. A direction has no origin position, so translation does not change it.

---

## 13. Transforming Multiple Points in NumPy

Mathematically, a point is often treated as a column vector.

In NumPy, however, a batch of points is commonly stored with one point per row:

```text
points_b.shape = (N, 3)
```

One implementation is:

```python
points_a = (R_ab @ points_b.T).T + t_ab
```

The steps are:

```text
(N, 3)
   |
 transpose
   v
(3, N)
   |
 R_ab @ ...
   v
(3, N)
   |
 transpose
   v
(N, 3)
   |
 + t_ab through broadcasting
   v
(N, 3)
```

The equivalent row-storage expression is:

```python
points_a = points_b @ R_ab.T + t_ab
```

The mathematical convention and the array-storage convention should be understood separately.

---

## 14. Composing Multiple Coordinate Transforms

For three frames \(W\), \(A\), and \(B\):

```text
B -> A -> W
```

the combined transform is:

\[
\boxed{
T_{wb}=T_{wa}T_{ab}
}
\]

The rightmost transformation acts first.

For a point in B:

\[
p_a=T_{ab}p_b
\]

then:

\[
p_w=T_{wa}p_a
\]

Substituting gives:

\[
p_w=T_{wa}T_{ab}p_b
\]

therefore:

\[
T_{wb}=T_{wa}T_{ab}
\]

The subscripts provide a useful consistency check:

\[
T_{w\cancel a}T_{\cancel a b}
=
T_{wb}
\]

If the intermediate frame labels do not match, the multiplication does not represent the intended transformation chain even if the matrix dimensions happen to be compatible.

---

## 15. Composition of Rotation and Translation

For:

\[
T_{wb}=T_{wa}T_{ab}
\]

the rotation part is:

\[
\boxed{
R_{wb}=R_{wa}R_{ab}
}
\]

and the translation part is:

\[
\boxed{
t_{wb}=R_{wa}t_{ab}+t_{wa}
}
\]

The second formula is especially important because \(t_{ab}\) is originally expressed in frame A, so it must be converted into W coordinates before it can be added to \(t_{wa}\).

---

## 16. Worked Three-Frame Example

Suppose:

\[
t_{wa}=
\begin{bmatrix}
1\\
0\\
0
\end{bmatrix}
\]

and A is rotated \(+90^\circ\) about z relative to W.

Also:

\[
t_{ab}=
\begin{bmatrix}
1\\
0\\
0
\end{bmatrix}
\]

and B is rotated \(-90^\circ\) about z relative to A.

Finally:

\[
p_b=
\begin{bmatrix}
1\\
0\\
0
\end{bmatrix}
\]

The rotation matrices are:

\[
R_{wa}
=
\begin{bmatrix}
0&-1&0\\
1&0&0\\
0&0&1
\end{bmatrix}
\]

and:

\[
R_{ab}
=
\begin{bmatrix}
0&1&0\\
-1&0&0\\
0&0&1
\end{bmatrix}
\]

Therefore:

\[
R_{wb}=R_{wa}R_{ab}=I
\]

For the translation:

\[
R_{wa}t_{ab}
=
\begin{bmatrix}
0\\
1\\
0
\end{bmatrix}
\]

so:

\[
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
\]

Finally:

\[
p_w=R_{wb}p_b+t_{wb}
\]

which gives:

\[
\boxed{
p_w=
\begin{bmatrix}
2\\
1\\
0
\end{bmatrix}
}
\]

---

## 17. Inverse Transform

The forward transformation is:

\[
p_a=R_{ab}p_b+t_{ab}
\]

To solve for \(p_b\), first remove the translation:

\[
p_a-t_{ab}=R_{ab}p_b
\]

Then multiply by the inverse rotation:

\[
p_b=R_{ab}^{-1}(p_a-t_{ab})
\]

Since:

\[
R^{-1}=R^T
\]

for a valid rotation matrix:

\[
\boxed{
p_b=R_{ab}^T(p_a-t_{ab})
}
\]

The inverse rotation is therefore:

\[
\boxed{
R_{ba}=R_{ab}^T
}
\]

The inverse translation is:

\[
\boxed{
t_{ba}=-R_{ab}^Tt_{ab}
}
\]

Thus:

\[
\boxed{
T_{ba}
=
T_{ab}^{-1}
=
\begin{bmatrix}
R_{ab}^T&-R_{ab}^Tt_{ab}\\
0&1
\end{bmatrix}
}
\]

The inverse translation is generally not simply \(-t_{ab}\), because it must be expressed in the new output coordinate frame.

---

## 18. Numerical and Structural Checks

A coordinate transformation implementation should not only be checked by visual inspection.

Useful checks include:

### Rotation validity

\[
R^TR \approx I
\]

and:

\[
\det(R)\approx1
\]

### Length preservation

For a pure rotation:

\[
\|Rp\|\approx\|p\|
\]

### Round-trip consistency

Transform a point forward and then apply the inverse:

```text
B -> A -> B
```

The final point should be numerically close to the original point.

### Independent hand calculation

Round-trip testing alone is not sufficient, because two consistent implementation mistakes can sometimes cancel each other.

An independent hand-computed example provides a separate reference.

---

## 19. Common Failure Modes

### Using `*` instead of `@`

If a matrix-vector operation unexpectedly returns shape `(3, 3)`, check whether elementwise multiplication was used accidentally.

Correct:

```python
R @ p
```

Incorrect for matrix multiplication:

```python
R * p
```

### Using degrees directly in `sin` and `cos`

NumPy trigonometric functions expect radians.

Use:

```python
theta = np.deg2rad(90.0)
```

or:

```python
theta = np.pi / 2
```

### Mixing millimetres and metres

A result that differs by a factor of 1000 often indicates a unit-conversion problem.

### Confusing `(3,)` and `(1, 3)`

Interfaces may intentionally require batches of points with shape:

```text
(N, 3)
```

so a single point may need to be written as:

```python
[[x, y, z]]
```

instead of:

```python
[x, y, z]
```

### Accepting a reflection as a rotation

A matrix can satisfy:

\[
R^TR=I
\]

while still having:

\[
\det(R)=-1
\]

Therefore determinant checking is also required.

---

## 20. Main Lessons

The most important ideas I want to retain from this section are:

1. A physical point can have different coordinate values in different frames without moving.
2. Coordinate values must always be interpreted together with their reference frame.
3. \(R_{ab}\) converts vector coordinates from frame B to frame A.
4. The columns of \(R_{ab}\) are the B-frame unit axes expressed in A.
5. A valid rotation matrix satisfies \(R^TR=I\) and \(\det(R)=1\).
6. Pure rotation preserves vector length.
7. Translation vectors can only be added when they are expressed in the same coordinate frame.
8. A rigid transform follows \(p_a=R_{ab}p_b+t_{ab}\).
9. Homogeneous coordinates allow rotation and translation to be represented in one matrix.
10. Points use homogeneous coordinate 1, while pure direction vectors use 0.
11. Transform chains compose from right to left.
12. The frame subscripts should connect consistently when transforms are multiplied.
13. The inverse rotation is the transpose of the original rotation.
14. The inverse translation is generally \(-R^Tt\), not simply \(-t\).
15. Correct robotics geometry requires checking frame meaning, units, shape, numerical accuracy, and geometric invariants together.