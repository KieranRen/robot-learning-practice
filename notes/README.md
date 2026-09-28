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

## M2 - MuJoCo Simulation

M2 focuses on robot simulation with MuJoCo and MJCF.

The goal of this stage is to gradually connect simulation with core robotics concepts such as rigid-body modeling, joints, contact, friction, actuators, sensors, kinematics, dynamics, and control.

### Environment and Assets

- [English](M2/MuJoCo/01_environment_and_assets.md)
- [中文](M2/MuJoCo/01_environment_and_assets_zh.md)

Topics include:

- MuJoCo XML / MJCF root structure
- compiler settings
- simulation timestep
- gravity
- numerical integrators
- constraint solvers
- solver iterations and tolerance
- visual configuration
- lighting and RGBA colors
- `asset`
- textures
- materials
- meshes
- height fields
- skyboxes
- built-in and external resources

### Geom, Body and Site

- [English](M2/MuJoCo/02_geom_body_site.md)
- [中文](M2/MuJoCo/02_geom_body_site_zh.md)

Topics include:

- `geom`
- geometry types
- `size`
- `pos`
- `rgba`
- materials
- mass and density
- friction
- `condim`
- collision filtering with `contype` and `conaffinity`
- `fromto`
- `worldbody`
- rigid-body hierarchy
- parent-child coordinate relationships
- relative coordinate frames
- multiple geoms inside one body
- `site` markers

### Joint

- [English](M2/MuJoCo/03_joint.md)
- [中文](M2/MuJoCo/03_joint_zh.md)

Topics include:

- role of joints in MuJoCo
- relationship between parent body, joint, and child body
- `free`, `ball`, `slide`, and `hinge` joints
- joint position
- joint axis
- joint range
- joint limits
- damping
- stiffness
- joint friction loss
- armature
- reference position
- hinge-joint pendulum example
- torque caused by gravity
- relationship between joint motion and rigid-body mechanics

### Current M2 Understanding

The main MuJoCo structure studied so far can be summarized as:

```text
<mujoco>
│
├── compiler
│   └── how MuJoCo interprets model settings
│
├── option
│   └── how the physics simulation runs
│
├── visual
│   └── how the simulation is rendered
│
├── asset
│   └── reusable simulation resources
│
└── worldbody
    └── physical simulation world
        │
        └── body
            ├── joint
            ├── geom
            ├── site
            └── child body
```

A useful conceptual relationship is:

```text
body
→ rigid body + local coordinate frame

joint
→ defines how a body can move relative to its parent

geom
→ defines physical geometry and contact shape

site
→ defines an auxiliary reference marker
```

M2 has also started connecting MuJoCo configuration with physical concepts such as:

- gravity
- mass
- friction
- damping
- rigid-body hierarchy
- relative coordinate frames
- torque
- constrained motion

### Source Repository

The MuJoCo learning materials in M2 are based on:

https://github.com/Albusgive/mujoco_learning.git

The original repository and teaching materials belong to their respective author(s).

These notes record my own summaries, explanations, experiments, and understanding based on the learning process.

M2 is currently in progress.

Future topics will include:

- friction
- more detailed contact modeling
- actuators
- sensors
- robot kinematics
- robot dynamics
- control
- more advanced MuJoCo simulation

## Purpose

These notes serve three goals:

1. Support long-term review and revision.
2. Document the reasoning behind the implementations in this repository.
3. Provide evidence of continuous and structured technical learning.

Runnable implementations are stored in `examples/`, while automated checks are stored in `tests/`.