# Learning Notes

This directory contains my structured learning notes for robotics, numerical computing, and related engineering topics.

The notes are not intended to reproduce source materials. Instead, they record my own understanding, derivations, mistakes, corrections, and summaries after completing each learning module.

## M1 — Robot Math Foundations

### Python and NumPy

- [English](m1/python_numpy.md)
- [中文](m1/python_numpy_zh.md)

Topics include:

- Python functions and modules
- NumPy arrays
- `shape`, `ndim`, and `dtype`
- indexing and slicing
- views and copies
- broadcasting
- vector length
- `*` versus `@`
- physical units
- floating-point error
- automated testing with `pytest`

### Robot Geometry

- [English](m1/robot_geometry.md)
- [中文](m1/robot_geometry_zh.md)

Topics include:

- coordinate frames
- point representations
- rotation matrices
- right-hand rule
- orthogonality and determinant checks
- rigid-body transformations
- homogeneous coordinates
- transform composition
- inverse transforms
- numerical and geometric validation

### Geometry Implementation

- [English](m1/geometry_implementation.md)
- [中文](m1/geometry_implementation_zh.md)

Topics include:

- `rotation_z`
- `make_transform`
- `inverse_transform`
- `transform_points`
- finite numeric input validation
- strict array shape validation
- proper rotation matrix checks
- floating-point tolerance
- `translate_points`
- coordinate-frame example structure
- transform composition order
- round-trip verification

### Modern Robotics Reading

- [English](m1/modern_robotics_reading.md)
- [中文](m1/modern_robotics_reading_zh.md)

Topics include:

- `SO(3)` and proper rotations
- rotation-matrix properties
- frame-subscript conventions
- `SE(3)` and homogeneous transformations
- rigid-transform inverse
- transform composition
- fixed-frame versus body-frame updates

## Purpose

These notes serve three goals:

1. Support long-term review and revision.
2. Document the reasoning behind the implementations in this repository.
3. Provide evidence of continuous and structured technical learning.

Runnable implementations are stored in `examples/`, while automated checks are stored in `tests/`.