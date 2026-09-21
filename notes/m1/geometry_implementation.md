# M1 — Geometry Implementation

[English](geometry_implementation.md) | [中文](geometry_implementation_zh.md)

This note records my understanding of how the rigid-transform mathematics from M1 is implemented as reliable Python and NumPy interfaces.

The main goal of this section is not to introduce new geometry, but to convert the mathematical ideas into reusable functions with explicit input contracts and validation.

---

## 1. From Mathematics to Software Interfaces

The main mathematical relationships studied previously are:

```math
R_z(\theta)
=
\begin{bmatrix}
\cos\theta & -\sin\theta & 0\\
\sin\theta & \cos\theta & 0\\
0 & 0 & 1
\end{bmatrix}
```

```math
p_a
=
R_{ab}p_b+t_{ab}
```

```math
T_{ab}
=
\begin{bmatrix}
R_{ab} & t_{ab}\\
0 & 1
\end{bmatrix}
```

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

The implementation exposes these ideas through four main functions:

```python
rotation_z(angle_rad)
make_transform(rotation, translation)
inverse_transform(transform)
transform_points(transform, points)
```

These functions correspond directly to the main steps used in hand calculations.

---

## 2. `rotation_z(angle_rad)`

This function creates a 3D rotation matrix for a rotation about the positive z axis.

Conceptually:

```text
angle in radians
        ↓
rotation_z(...)
        ↓
3 × 3 rotation matrix
```

For example:

```python
rotation_z(np.pi / 2)
```

represents a positive 90-degree rotation about z.

The expected matrix is:

```math
R_z\left(\frac{\pi}{2}\right)
=
\begin{bmatrix}
0 & -1 & 0\\
1 & 0 & 0\\
0 & 0 & 1
\end{bmatrix}
```

The implementation is essentially the mathematical formula translated into NumPy:

```python
c = np.cos(angle_rad)
s = np.sin(angle_rad)

R = np.array([
    [c, -s, 0.0],
    [s,  c, 0.0],
    [0.0, 0.0, 1.0]
])
```

The `_rad` suffix is important because the interface expects radians.

For example:

```python
rotation_z(np.pi / 2)
```

is correct for 90 degrees, while:

```python
rotation_z(90)
```

would be interpreted as 90 radians.

---

## 3. `make_transform(rotation, translation)`

This function combines a rotation matrix and translation vector into a homogeneous rigid transform.

Expected inputs:

```text
rotation.shape    = (3, 3)
translation.shape = (3,)
```

Output:

```text
transform.shape = (4, 4)
```

Mathematically:

```math
T
=
\begin{bmatrix}
R & t\\
0 & 1
\end{bmatrix}
```

The function therefore turns:

```text
3 × 3 rotation
+
3-element translation
```

into a single:

```text
4 × 4 homogeneous transform
```

This is useful because later operations can work with one transform object instead of handling rotation and translation separately.

---

## 4. `inverse_transform(transform)`

This function computes the inverse of a rigid transform.

For:

```math
T_{ab}
=
\begin{bmatrix}
R_{ab} & t_{ab}\\
0 & 1
\end{bmatrix}
```

the inverse is:

```math
T_{ba}
=
\begin{bmatrix}
R_{ab}^{T} & -R_{ab}^{T}t_{ab}\\
0 & 1
\end{bmatrix}
```

A general matrix inverse is not required because rigid transforms have special structure.

The important properties are:

```math
R^{-1}=R^T
```

and:

```math
t_{\text{inverse}}
=
-R^Tt
```

The inverse translation is generally not simply `-t`, because it must be expressed in the new output coordinate frame.

---

## 5. `transform_points(transform, points)`

This function applies a rigid transform to one or more points.

The interface expects:

```text
transform.shape = (4, 4)
points.shape    = (N, 3)
```

and returns:

```text
(N, 3)
```

The number of points does not change.

For example:

```python
points = np.array([
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0]
])
```

contains two 3D points, so:

```text
shape = (2, 3)
```

Even a single point is written as:

```python
[[1.0, 0.0, 0.0]]
```

rather than:

```python
[1.0, 0.0, 0.0]
```

because the interface consistently treats the input as a batch of points.

Conceptually, each point follows:

```math
p_a
=
R_{ab}p_b+t_{ab}
```

The function simply applies this same transformation to every row of the point array.

---

## 6. Why Input Validation Matters

A numerical function can execute without raising an error while still producing a result with the wrong mathematical meaning.

For this reason, the implementation checks more than just whether NumPy can perform the operation.

Important validation includes:

- expected array shape
- real numeric data
- finite values
- valid rotation matrices
- valid homogeneous-transform structure

The functions raise `ValueError` when the input violates the defined interface.

This is important because silent broadcasting or malformed transforms can otherwise create plausible-looking but incorrect results.

---

## 7. Finite Numeric Data

The helper function:

```python
_as_finite_float_array(...)
```

acts as an input-cleaning layer.

Its purpose can be summarized as:

```text
input
↓
convert to NumPy array
↓
check numeric type
↓
convert to float64
↓
reject NaN / ±inf
↓
return validated array
```

For example:

```python
[1, 2, 3]
```

may be converted into:

```python
np.array([1.0, 2.0, 3.0], dtype=np.float64)
```

Values such as:

```python
np.nan
np.inf
-np.inf
```

are rejected.

The helper function does not perform robot geometry itself. Its role is to make later numerical operations safer and more predictable.

---

## 8. Shape Validation

The implementation deliberately enforces exact interface shapes.

For example:

```text
rotation    -> (3, 3)
translation -> (3,)
points      -> (N, 3)
transform   -> (4, 4)
```

This is important because NumPy broadcasting may accept shapes that were not mathematically intended.

For example:

```text
(2, 1)
and
(2,)
```

can broadcast to:

```text
(2, 2)
```

even when that result is not meaningful for the intended operation.

Therefore the implementation does not allow NumPy to guess the intended geometry.

---

## 9. Rotation-Matrix Validation

A 3 × 3 array is not automatically a valid rotation matrix.

A proper rotation must satisfy:

```math
R^TR=I
```

and:

```math
\det(R)=1
```

The first condition checks that the axes remain orthonormal.

The second condition rejects reflections.

For example:

```math
\begin{bmatrix}
1&0&0\\
0&1&0\\
0&0&-1
\end{bmatrix}
```

is orthogonal, but:

```math
\det(R)=-1
```

so it represents a reflection rather than a proper rotation.

---

## 10. Numerical Tolerance

Floating-point calculations are not expected to match exact mathematical values bit-for-bit.

The implementation therefore uses approximate checks such as:

```python
np.allclose(...)
```

with approximately:

```text
absolute tolerance = 1e-9
relative tolerance = 0
```

For example:

```math
R^TR
```

may numerically differ from the identity matrix by a very small floating-point residual.

That should not cause a valid rotation to be rejected.

At the same time, the tolerance must remain sufficiently strict to reject genuinely invalid input.

---

## 11. `translate_points(...)`

The numerical example also contains:

```python
translate_points(points, offset)
```

This function is a simpler example of interface validation and broadcasting.

Expected shapes:

```text
points -> (N, D)
offset -> (D,)
```

The mathematical operation is simply:

```python
points_array + offset_array
```

NumPy broadcasting applies the same offset to each point.

For example:

```text
points =
[[0, 0],
 [1, 2]]

offset =
[0.5, -1]
```

produces:

```text
[[0.5, -1],
 [1.5,  1]]
```

The important implementation lesson is that the calculation itself is simple, while the surrounding input checks make the interface reliable.

---

## 12. Coordinate-Frame Example

The file:

```text
examples/coordinate_frames.py
```

combines the geometry functions into one complete coordinate-frame example.

The core calculation is approximately:

```python
T_wa = make_transform(rotation_z(np.pi / 2), [1.0, 0.0, 0.0])

T_ab = make_transform(rotation_z(-np.pi / 2), [1.0, 0.0, 0.0])

T_wb = T_wa @ T_ab

p_b = np.array([[1.0, 0.0, 0.0]])

p_w = transform_points(T_wb, p_b)

T_bw = inverse_transform(T_wb)

p_b_roundtrip = transform_points(T_bw, p_w)
```

This corresponds directly to the mathematical chain:

```text
B -> A -> W
```

and:

```math
T_{wb}
=
T_{wa}T_{ab}
```

---

## 13. Transform Order

The example also intentionally computes a reversed product:

```python
T_reversed = T_ab @ T_wa
```

The matrix multiplication is numerically valid because both matrices have compatible dimensions.

However, it does not represent the required B-to-W frame chain.

This demonstrates an important robotics principle:

> Valid matrix dimensions do not guarantee valid coordinate-frame semantics.

The correct order must follow the frame chain.

---

## 14. Round-Trip Validation

After computing:

```text
B -> W
```

the program applies the inverse transform:

```text
W -> B
```

The sequence is:

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

The result should recover the original point.

In the current example:

```text
p_b = [[1. 0. 0.]]
```

and:

```text
p_b_roundtrip = [[1. 0. 0.]]
```

with measured error:

```text
0.000e+00 m
```

This is a useful consistency check between forward and inverse transformations.

---

## 15. Structure of `coordinate_frames.py`

The file can be understood as five main parts:

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

Contains the important robot-geometry calculations.

It constructs transforms, converts the point between frames, computes the inverse, and stores the results.

### `format_report()`

Formats the calculated matrices and points for terminal output.

It does not introduce new geometry.

### `render_svg()`

Generates the SVG visualization.

Most of this function is drawing logic:

- grid lines
- coordinate axes
- arrows
- labels
- transformed points

The SVG implementation is useful for visualization but is not itself a new rigid-transform concept.

### `write_svg()`

Writes the generated SVG string to a file.

### `main()`

Coordinates the whole program:

```text
build scene
↓
print results
↓
optionally generate SVG
↓
save output
```

---

## 16. Main Lessons

The most important ideas from the geometry implementation section are:

1. The four geometry functions are direct software versions of the mathematical concepts studied earlier.
2. Reliable numerical software needs explicit input contracts.
3. Shape validation prevents unintended broadcasting.
4. `float64` provides a consistent numerical representation.
5. `NaN` and infinite values should be rejected before geometric calculations.
6. A valid rotation requires both orthogonality and determinant +1.
7. Numerical geometry requires tolerance-based comparisons.
8. `transform_points` applies the same rigid transform to a batch of points.
9. Matrix multiplication order must follow coordinate-frame semantics.
10. A numerically valid matrix product may still represent the wrong frame chain.
11. Round-trip validation is useful for checking inverse consistency.
12. Visualization supports understanding but does not replace numerical and automated verification.