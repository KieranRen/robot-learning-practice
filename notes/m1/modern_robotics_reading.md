# Modern Robotics — M1 Reading Notes

[English](modern_robotics_reading.md) | [中文](modern_robotics_reading_zh.md)

## Reading Source

Kevin M. Lynch and Frank C. Park, *Modern Robotics: Mechanics, Planning, and Control*, Cambridge University Press, 2017.

This M1 reading used the May 2017 preprint and focused on the static robot-geometry material required for the current module.

## Reading Scope

The following sections were read for M1:

- Section 3.2.1 — Rotation Matrices
- Section 3.3.1 — Homogeneous Transformation Matrices

Angular velocity, twists, exponential coordinates, and later dynamic topics were not included because they are outside the current M1 completion scope.

---

## 1. Rotation Matrices

### Rotation-Matrix Constraints

A three-dimensional rotation matrix

```math
R \in SO(3)
```

must satisfy

```math
R^T R = I
```

and

```math
\det(R) = +1.
```

The condition `R^T R = I` means that the columns of `R` are mutually orthogonal unit vectors.

Orthogonality alone is not sufficient. For example,

```math
\begin{bmatrix}
1 & 0 & 0\\
0 & 1 & 0\\
0 & 0 & -1
\end{bmatrix}
```

satisfies

```math
R^T R = I,
```

but has determinant `-1`, so it represents a reflection rather than a proper rotation.

### Inverse Rotation

For

```math
R \in SO(3),
```

the inverse is

```math
R^{-1} = R^T.
```

This directly matches the use of the transpose when constructing inverse rotations in the personal implementation.

### Composition

The product of two rotation matrices is also a rotation matrix.

Rotation-matrix multiplication is associative but generally not commutative:

```math
R_1R_2 \neq R_2R_1.
```

### Length Preservation

If

```math
y = Rx,
```

then

```math
\|y\| = \|x\|.
```

Therefore, a valid rigid rotation does not change vector length.

### Frame-Subscript Convention

`R_ab` represents the orientation of frame B expressed in frame A.

The columns of `R_ab` are the unit axes of B expressed in A.

Coordinate conversion follows

```math
R_{ab}p_b = p_a,
```

meaning that the same geometric object is re-expressed from frame B coordinates into frame A coordinates.

Rotation composition follows

```math
R_{ab}R_{bc}=R_{ac}.
```

The intermediate frame subscript can therefore be used as a consistency check for a frame chain.

---

## 2. Homogeneous Transformation Matrices

A rigid-body pose combines rotation and translation in the matrix

```math
T=
\begin{bmatrix}
R & p\\
0 & 1
\end{bmatrix}.
```

Here:

- `R` is a 3×3 rotation matrix,
- `p` is a 3×1 translation vector,
- `T` is a 4×4 homogeneous transformation matrix.

Valid three-dimensional rigid transformations belong to

```math
SE(3).
```

### Homogeneous Coordinates

A three-dimensional point can be represented as

```math
\begin{bmatrix}
x\\
1
\end{bmatrix}.
```

Then

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
\end{bmatrix}.
```

This allows rotation and translation to be represented by one matrix operation.

### Inverse Transform

For

```math
T=
\begin{bmatrix}
R & p\\
0 & 1
\end{bmatrix},
```

the inverse is

```math
T^{-1}
=
\begin{bmatrix}
R^T & -R^Tp\\
0 & 1
\end{bmatrix}.
```

This matches the personal implementation:

```python
R_inv = R.T
t_inv = -R_inv @ t
```

### Transform Composition

Transformation matrices are generally not commutative.

A valid frame chain follows

```math
T_{ab}T_{bc}=T_{ac},
```

which is the same subscript-cancellation rule used earlier in M1:

```math
T_{wa}T_{ab}=T_{wb}.
```

### Rigid-Body Invariants

A rigid transformation preserves:

- distances between points,
- angles between vectors.

It therefore does not introduce scaling, shear, or other non-rigid deformation.

---

## 3. Fixed-Frame and Body-Frame Updates

This was the most important new concept added by the textbook reading.

Let the current body pose be

```math
T_{sb}.
```

### Premultiplication

```math
T_{\text{new}}=\Delta T\,T_{sb}
```

means that the incremental transform `ΔT` is interpreted in the fixed or space frame.

In practical terms:

> The motion is defined using world-frame directions and axes.

### Postmultiplication

```math
T_{\text{new}}=T_{sb}\,\Delta T
```

means that the incremental transform `ΔT` is interpreted in the current body frame.

In practical terms:

> The motion is defined using the robot's own current directions and axes.

For example, suppose a robot has already rotated 90 degrees about the world z-axis, and an incremental translation is

```text
[1, 0, 0]
```

Premultiplication interprets this as motion along world +x.

Postmultiplication interprets it as motion along the robot's own +x. Since the robot's +x axis now points along world +y, the actual world-frame displacement is along +y.

A useful summary is:

```text
ΔT @ T_old
= fixed-frame update

T_old @ ΔT
= body-frame update
```

or, more intuitively:

> Premultiply: move according to the map frame.  
> Postmultiply: move according to the robot's own frame.

---

## 4. Connection to the M1 Capability Tasks

### GEOM-T01

The textbook reinforced:

- rotation-matrix columns represent coordinate-axis directions,
- `R^T R = I`,
- `det(R) = +1`,
- rigid rotation preserves vector length.

### GEOM-T02

The textbook formally supports the rigid-transform relationship

```math
p_a = R_{ab}p_b+t_{ab}
```

and the inverse

```math
T^{-1}
=
\begin{bmatrix}
R^T & -R^Tt\\
0 & 1
\end{bmatrix}.
```

These agree with the personal implementation.

### GEOM-T03

The textbook confirms that:

- transformation composition is generally noncommutative,
- frame chains can be checked through subscript cancellation,
- `T_ab T_bc = T_ac`.

This matches the controlled failure experiment in which reversing the transform order produced an incorrect result.

### GEOM-T04

The multi-frame robotics example in the textbook demonstrates how real robotic systems combine and invert known frame transformations to recover an unknown target transformation.

This shows how the W–A–B examples used in M1 extend naturally to larger robot frame chains.

---

## 5. Main New Insight from the Reading

Most of the mathematical content in these sections had already been implemented and tested during M1.

The main new conceptual addition was the distinction between fixed-frame and body-frame updates:

```text
ΔT @ T_old
→ fixed-frame update

T_old @ ΔT
→ body-frame update
```

This distinction will be important in later work involving robot kinematics, manipulator pose updates, and mobile-robot motion.

---

## 6. Reading Completion

The assigned M1 textbook reading is complete.

Actual reading coverage:

```text
Modern Robotics
Section 3.2.1 — Rotation Matrices
Section 3.3.1 — Homogeneous Transformation Matrices
```

The reading was checked against:

```text
GEOM-T01
GEOM-T02
GEOM-T03
GEOM-T04
```

With this reading complete, the M1 requirements for textbook study, personal implementation, automated testing, hand calculations, controlled failure analysis, and integrated capability tasks have all been completed.