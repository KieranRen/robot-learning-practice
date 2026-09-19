# M1 Experiment Report — Robot Geometry and Rigid Transforms

[English](robot_geometry_report.md) | [中文](robot_geometry_report_zh.md)

## Overview

This report records the execution and verification of the M1 robot geometry examples.

The experiment covers:

- coordinate frames
- rotation matrices
- rigid-body transformations
- transform composition
- inverse transforms
- round-trip verification
- automated testing
- coordinate-frame visualization

The purpose is to provide executable evidence that the mathematical concepts studied in M1 can be implemented and validated numerically.

## Environment

The experiment was executed using the project Conda environment:

```text
robot_manipulation_learning
```

Relevant software versions:

```text
Python 3.11.16
NumPy 2.4.6
pytest 8.4.2
```

Reference learning material:

```text
knowledge tag: v0.2.0
```

## Files

The main files used in this experiment are:

```text
algorithms/geometry/
examples/coordinate_frames.py
tests/test_rigid_transform.py
tests/test_coordinate_frames.py
```

The generated visualization is stored at:

```text
outputs/m1/frames.svg
```

## Commands

The coordinate-frame example was executed with:

```bash
python -m examples.coordinate_frames --output outputs/m1/frames.svg
```

The automated tests were executed with:

```bash
python -m pytest tests/test_rigid_transform.py tests/test_coordinate_frames.py -q
```

## Coordinate Transformation Result

The experiment produced the world-frame coordinate:

```text
p_w =
[[2. 1. 0.]]
```

This agrees with the independent hand calculation from the three-frame example.

The transformation chain is:

```text
B -> A -> W
```

with the combined transform:

```math
T_{wb}=T_{wa}T_{ab}
```

The point transformation follows:

```math
p_w=R_{wb}p_b+t_{wb}
```

For this example:

```math
p_b=
\begin{bmatrix}
1\\
0\\
0
\end{bmatrix}
```

and the expected result is:

```math
p_w=
\begin{bmatrix}
2\\
1\\
0
\end{bmatrix}
```

The program output matches this result.

## Intermediate Coordinate

The example also reports the intermediate coordinate:

```text
p_reversed =
[[ 2. -1.  0.]]
```

This provides an additional value for checking the coordinate-frame convention and transformation direction.

Intermediate values are useful because a correct final answer alone does not guarantee that every transformation step is implemented correctly.

## Round-Trip Verification

The transformed point was converted back into frame B.

Observed result:

```text
p_b_roundtrip =
[[1. 0. 0.]]
```

The original point was:

```text
p_b =
[[1. 0. 0.]]
```

The measured maximum round-trip error was:

```text
0.000e+00 m
```

Therefore the forward and inverse transformations returned exactly to the original point within the numerical precision observed in this run.

Conceptually:

```text
B -> W -> B
```

should recover the original coordinates.

This verifies consistency between the forward transform and its inverse.

## Transform Order

The example explicitly reports:

```text
T_wb = T_wa @ T_ab; the reversed product is not a valid B -> W frame chain.
```

This demonstrates that matrix dimensions alone do not determine whether a transform composition is meaningful.

The valid coordinate-frame chain is:

```text
B -> A -> W
```

therefore:

```math
T_{wb}=T_{wa}T_{ab}
```

The intermediate frame labels connect:

```math
T_{w\cancel a}T_{\cancel a b}=T_{wb}
```

Reversing the multiplication order does not represent the same coordinate transformation.

## Generated Visualization

The example successfully generated:

```text
outputs/m1/frames.svg
```

The SVG provides a visual representation of the coordinate frames and point configuration used in the experiment.

The visualization is useful for checking:

- coordinate-axis orientation
- frame origins
- transformation direction
- the location of the transformed point

However, visual agreement alone is not sufficient evidence of correctness. Numerical checks and automated tests are also required.

## Automated Test Result

The test command produced:

```text
54 passed in 0.41s
```

All 54 tests in:

```text
tests/test_rigid_transform.py
tests/test_coordinate_frames.py
```

passed in the current environment.

These tests provide automated checks for the implemented rigid-transform and coordinate-frame behavior.

## What This Experiment Demonstrates

This experiment provides executable evidence of:

- rotation-matrix construction
- coordinate-frame conversion
- translation between frame origins
- homogeneous rigid transforms
- transform composition
- inverse transformation
- correct transformation order
- round-trip consistency
- numerical validation
- SVG-based visualization
- automated testing with `pytest`

## Key Reflection

The most important lesson from this experiment is that coordinate transformations cannot be treated as ordinary matrix operations without considering their geometric meaning.

A calculation can have valid matrix dimensions while still representing the wrong frame relationship.

Reliable robot geometry therefore requires checking:

- coordinate-frame labels
- transformation direction
- rotation validity
- translation representation
- multiplication order
- numerical results
- inverse consistency
- independent hand calculations

Combining these checks provides much stronger evidence than relying on a single numerical result or visualization.