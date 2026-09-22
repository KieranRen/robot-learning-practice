# M1 Capability Tasks Report

[English](capability_tasks_report.md) | [中文](capability_tasks_report_zh.md)

## 1. Purpose

This report records the completion of the six M1 Robot Math Foundations capability tasks, including personal implementations, automated tests, hand-computed baselines, controlled failure analysis, and integrated verification.

Only material that has actually been studied, implemented, and tested is recorded here.

At the time of this report, the numerical foundations, robot geometry, rigid-transform implementation, testing, and all six capability tasks have been completed.

The assigned textbook reading remains outstanding, so M1 is still **In Progress**.

---

## 2. Environment and Evidence

Personal practice repository:

```text
robot-learning-practice
```

Environment:

```text
Conda environment: robot_manipulation_learning
Python: 3.11.16
NumPy: 2.4.6
pytest: 8.4.2
```

Personal implementation:

```text
examples/m1_solution.py
```

Personal tests:

```text
tests/test_m1_solution.py
```

Related reference implementation:

```text
algorithms/geometry/
examples/numeric_basics.py
examples/coordinate_frames.py
```

M1 reference repository version:

```text
v0.2.0
```

The personal capability-task implementation does not simply wrap the reference point-transform and inverse-transform functions. The required numerical and rigid-transform operations were independently implemented and tested.

---

# 3. PYNUM-T01 — Explicit Inputs, Outputs, and Exceptions

## Goal

Implement:

```python
millimeters_to_meters(values)
```

to convert millimeters to meters while defining a clear function contract.

The core numerical operation is:

```python
array / 1000.0
```

but the main purpose of the task is to define reliable input, output, and error behavior.

## Input Contract

Accepted inputs include:

- Python lists
- NumPy arrays
- finite real integer or floating-point values

Rejected inputs include:

- `NaN`
- `+inf`
- `-inf`
- non-real numeric data

## Output Contract

The function returns:

- a NumPy array
- `float64` data
- the same shape as the input
- a result that does not modify the caller's original array

## Hand-Computed Baseline

Input:

```text
[0, 250, -1000] mm
```

Expected output:

```text
[0.0, 0.25, -1.0] m
```

## Verification

Tests check:

- known numerical conversion
- `float64` output
- one-dimensional shape preservation
- two-dimensional shape preservation
- caller data is not modified
- output does not share storage with the input
- `NaN` and infinities are rejected

The main lesson is:

> A reliable numerical function needs an explicit contract, not only a correct formula.

---

# 4. PYNUM-T02 — Array Shape Before Arithmetic

## Correct Broadcasting

For:

```text
points.shape = (2, 3)
offset.shape = (3,)
```

the operation:

```python
points + offset
```

produces:

```text
(2, 3)
```

and correctly applies the same three-dimensional offset to every point.

Example:

```text
points =
[[0, 0, 0],
 [1, 2, 3]]

offset =
[1, -1, 0.5]
```

produces:

```text
[[1, -1, 0.5],
 [2,  1, 3.5]]
```

## Invalid Shape

For:

```text
(2, 3) + (3, 1)
```

NumPy cannot broadcast the arrays, so the operation fails.

## Broadcastable but Semantically Wrong

For example:

```text
(3, 1) + (3,) -> (3, 3)
```

is numerically valid NumPy broadcasting.

However, if the intended operation is addition of two three-dimensional vectors, the resulting `(3,3)` array has the wrong mathematical meaning.

Therefore:

> Broadcast compatibility does not guarantee semantic correctness.

## Matrix vs Elementwise Multiplication

```python
R @ p
```

represents matrix multiplication.

```python
R * p
```

represents elementwise multiplication with possible broadcasting.

A robot rotation written mathematically as:

```math
Rp
```

must therefore use:

```python
R @ p
```

rather than `R * p`.

## Floating-Point Residuals

The calculation:

```python
0.1 + 0.2 - 0.3
```

produces a very small non-zero residual because decimal values such as `0.1` cannot generally be represented exactly in binary floating point.

Numerical tests therefore use tolerance-based comparison such as:

```python
np.testing.assert_allclose(...)
```

The tolerance must still remain sufficiently strict to avoid hiding genuine implementation errors.

---

# 5. GEOM-T01 — Coordinate Frames and Rotations

## Frame Notation

### `R_ab`

`R_ab` represents the orientation of frame B expressed in frame A.

Its columns describe the unit axes of B expressed in A.

### `t_ab`

`t_ab` represents the origin of frame B expressed in frame A.

### `p_b`

`p_b` represents the coordinates of physical point `p` expressed in frame B.

### `T_ab`

`T_ab` represents the complete rigid transform from B coordinates to A coordinates:

```math
T_{ab}
=
\begin{bmatrix}
R_{ab} & t_{ab}\\
0 & 1
\end{bmatrix}
```

with:

```text
R_ab -> (3, 3)
t_ab -> (3,)
T_ab -> (4, 4)
```

## Positive 90-Degree Rotation About z

```math
R_z(\pi/2)
=
\begin{bmatrix}
0 & -1 & 0\\
1 & 0 & 0\\
0 & 0 & 1
\end{bmatrix}
```

The first column shows that the original +x direction maps to +y.

The second column shows that the original +y direction maps to -x.

The third column shows that the z direction is unchanged.

## Hand Calculation

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

Before rotation:

```math
\sqrt{2^2+1^2}=\sqrt{5}
```

After rotation:

```math
\sqrt{(-1)^2+2^2}=\sqrt{5}
```

so length is preserved.

## Orthogonal Does Not Always Mean Proper Rotation

The matrix:

```math
\operatorname{diag}(1,1,-1)
```

satisfies:

```math
R^TR=I
```

but:

```math
\det(R)=-1
```

so it represents a reflection rather than a proper right-handed rotation.

A proper rotation requires both:

```math
R^TR=I
```

and:

```math
\det(R)=+1
```

---

# 6. GEOM-T02 — Implementing the Formulas

Two functions were implemented independently:

```python
apply_transform(T, points)
invert_transform(T)
```

## Point Transformation

The mathematical formula is:

```math
p_a=R_{ab}p_b+t_{ab}
```

The personal implementation stores a batch of points as rows with shape `(N,3)`, so the corresponding NumPy expression is:

```python
points @ R.T + t
```

which is equivalent to:

```python
(R @ points.T).T + t
```

## Inverse Transform

For:

```math
T=
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}
```

the inverse is:

```math
T^{-1}
=
\begin{bmatrix}
R^T&-R^Tt\\
0&1
\end{bmatrix}
```

The implementation therefore uses:

```python
R_inv = R.T
t_inv = -R_inv @ t
```

before reconstructing the 4×4 homogeneous transform.

## Hand-Computed Baseline

Given:

```text
R = Rz(pi/2)
t = [1, 0, 0]
p = [2, 1, 0]
```

rotation gives:

```text
[2,1,0] -> [-1,2,0]
```

and translation gives:

```text
[-1,2,0] + [1,0,0]
=
[0,2,0]
```

The implementation matches the expected result:

```text
[[0,2,0]]
```

## Interface Validation

The implementation checks:

- `T.shape == (4,4)`
- `points.shape == (N,3)`
- finite real-valued inputs
- homogeneous bottom row `[0,0,0,1]`
- `R.T @ R ≈ I`
- `det(R) ≈ +1`
- invalid rigid transforms are rejected
- arithmetic overflow cannot silently produce infinity

Tests cover:

- identity transform
- known rotation and translation
- inverse round trip
- invalid point shapes
- non-finite values
- invalid rigid transforms

---

# 7. GEOM-T03 — Composition Order and Failure Analysis

The fixed frame chain is:

```text
B -> A -> W
```

with:

```text
T_ab : B -> A
T_wa : A -> W
```

Therefore:

```math
T_{wb}=T_{wa}T_{ab}
```

The frame subscripts can be checked as:

```math
T_{w\cancel a}T_{\cancel a b}=T_{wb}
```

## Stepwise Path

```text
p_b
↓ T_ab
p_a
↓ T_wa
p_w
```

## Composed Path

First:

```text
T_wb = T_wa @ T_ab
```

then transform `p_b` once.

Both paths produce:

```text
p_w = [2,1,0]
```

so the stepwise and composed transformations agree.

## Round Trip

The inverse transform:

```text
T_bw = inverse(T_wb)
```

returns the transformed point to:

```text
p_b = [1,0,0]
```

within the selected numerical tolerance.

The current exercise uses:

```text
rtol = 0
atol = 1e-12
```

for meter-scale `float64` calculations.

This numerical tolerance is not a claim that a physical robot system has `1e-12 m` accuracy.

## Controlled Failure

The correct composition:

```python
T_wa @ T_ab
```

was intentionally replaced by:

```python
T_ab @ T_wa
```

The incorrect result is:

```text
[2,-1,0]
```

instead of:

```text
[2,1,0]
```

This is not a floating-point residual.

The failure occurs because the frame subscripts do not form the required B-to-A-to-W chain.

Therefore the error is classified as a:

> coordinate-frame / transform-composition error.

This demonstrates that matrices being numerically multipliable does not imply valid frame semantics.

---

# 8. GEOM-T04 — Integrated Verification

## Original Fixed Scene

The reference coordinate-frame example generates:

```text
outputs/m1/frames.svg
```

showing:

- frames W, A, and B
- coordinate axes
- units
- the world-coordinate point
- the reversed-order comparison point

The visualization supports human interpretation but is not treated as the sole proof of correctness.

Personal numerical results and automated tests remain independent evidence.

## Modified Scene

The original:

```text
t_ab = [1,0,0]
```

was changed to:

```text
t_ab = [2,0,0]
```

Before running the implementation, the modified result was predicted by hand.

Expected B origin in W:

```text
[1,2,0]
```

For:

```text
p_b = [1,0,0]
```

the expected world coordinate is:

```text
[2,2,0]
```

The personal `apply_transform(...)` implementation was then used to verify the prediction.

The automated test matched both hand-computed results.

---

# 9. Validation Strategy and Boundaries

M1 uses multiple forms of evidence:

```text
hand calculations
+
unit tests
+
shape checks
+
invalid-input tests
+
geometric invariants
+
inverse round trips
+
controlled failure cases
+
visual inspection
```

Each method checks different failure modes.

For example:

- hand calculations provide an independent baseline
- pytest provides repeatable automated verification
- invariants check mathematical structure
- round trips check forward/inverse consistency
- controlled failures test diagnostic reasoning
- SVG visualization supports spatial interpretation

No single method proves correctness for every possible input.

Final repository-wide verification was run from the repository root:

python -m pytest

Observed result:

107 passed in 0.51s

---

# 10. One Real Failure and Its Diagnosis

While adding the GEOM-T03 tests, the new tests initially failed with:

```text
NameError: name 'make_transform' is not defined
```

The problem was not the transform mathematics or NumPy arithmetic.

`transform_chain_example()` used `make_transform`, but the symbol had not been imported into `examples/m1_solution.py`.

The fix was to add the required import in the implementation module rather than changing the expected test result.

This demonstrated an important debugging principle:

> Diagnose the failure category before changing the implementation or the test expectation.

---

# 11. Mathematical Formulas vs NumPy

The geometry relationships were explicitly chosen and implemented.

For example:

```python
point_array @ R.T + t
```

comes from:

```math
p_a=Rp_b+t
```

and:

```python
-R.T @ t
```

comes from the rigid-transform inverse derivation.

NumPy provides:

- array storage
- matrix multiplication
- broadcasting
- transpose
- determinant
- norms
- floating-point arithmetic
- approximate numerical comparison

NumPy does not automatically understand:

- coordinate-frame subscripts
- transform direction
- physical units
- frame chains
- which mathematically valid array operation has the intended robotics meaning

Those semantics must be maintained by the implementation.

---

# 12. Conclusions Supported by Current Evidence

The current implementation, hand calculations, and tests support the following conclusions:

- the unit-conversion function has an explicit numerical contract
- array shape strongly affects NumPy semantics
- valid broadcasting can still be semantically incorrect
- `@` and `*` are not interchangeable in robot matrix operations
- floating-point comparisons require appropriate tolerances
- proper rotations require orthogonality and determinant +1
- rigid rotations preserve vector length
- `(N,3)` point batches can be transformed using `points @ R.T + t`
- rigid-transform inverses can be constructed from `R.T` and `-R.T @ t`
- stepwise and composed transforms agree for the tested frame chain
- transform order must follow frame semantics
- forward/inverse consistency can be checked with a round trip
- invalid shapes, non-finite data, and invalid rigid transforms should be rejected explicitly
- the reference SVG and numerical results can be used as complementary evidence

---

# 13. Current Scope Limitations

This M1 work does not claim support for:

- arbitrary-dimensional robot rigid transforms
- scaling
- shear
- general affine transforms
- non-rigid transformations
- physical sensor-noise models
- real robot calibration error
- real-time control
- robot dynamics
- Jacobians
- motion planning
- sensor fusion

The assigned M1 textbook reading is also still outstanding.

Therefore the overall M1 status remains:

```text
In Progress
```

with only:

```text
Textbook Reading
```

remaining.

---

# 14. Current Status

The following M1 areas are complete:

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
```

The personal implementation, automated tests, hand calculations, controlled failure analysis, and modified-scene verification now provide reproducible evidence.

After the assigned textbook reading is completed and documented, M1 can undergo final review and be updated to:

```text
Completed
```