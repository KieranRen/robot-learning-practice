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

M2 contains MuJoCo learning materials from two different upstream sources.

To keep the learning process clear and traceable, notes from the two sources are organized separately.

---

### Source A - Albusgive MuJoCo Learning

Source repository:

https://github.com/Albusgive/mujoco_learning.git

This part focuses mainly on MJCF modeling fundamentals, physical interaction, actuator models, and scene construction.

#### Environment and Assets

- [English](M2/MuJoCo/01_environment_and_assets.md)
- [中文](M2/MuJoCo/01_environment_and_assets_zh.md)

Topics include:

- MuJoCo XML / MJCF structure
- compiler settings
- simulation options
- gravity
- timestep
- integrators and solvers
- visual configuration
- assets
- textures
- materials
- meshes
- skyboxes

#### Geom, Body and Site

- [English](M2/MuJoCo/02_geom_body_site.md)
- [中文](M2/MuJoCo/02_geom_body_site_zh.md)

Topics include:

- geom
- geometry types
- body hierarchy
- relative coordinate frames
- multiple geoms inside one body
- site markers
- friction
- collision filtering
- mass and density

#### Joint

- [English](M2/MuJoCo/03_joint.md)
- [中文](M2/MuJoCo/03_joint_zh.md)

Topics include:

- joint types
- hinge joints
- joint axis
- joint range
- damping
- stiffness
- friction loss
- armature
- simple pendulum modeling

#### Friction

- [English](M2/MuJoCo/04_friction.md)
- [中文](M2/MuJoCo/04_friction_zh.md)

Topics include:

- sliding friction
- torsional friction
- rolling friction
- `friction="a b c"`
- `condim`
- `cone="elliptic"`
- `cone="pyramidal"`
- friction constraint dimensions
- internal friction expansion
- `priority`
- contact parameter selection
- `impratio`
- box, sphere, and slope comparison experiments

#### Actuator

- [English](M2/MuJoCo/05_actuator.md)
- [中文](M2/MuJoCo/05_actuator_zh.md)

Topics include:

- actuator fundamentals
- `general`
- `motor`
- `position`
- `velocity`
- `intvelocity`
- `damper`
- `cylinder`
- `data.ctrl`
- `ctrlrange`
- `forcerange`
- `actrange`
- `gear`
- `kp`
- `kv`
- `timeconst`
- `inheritrange`
- target position vs actual joint state
- force / torque control
- velocity control
- integrated velocity control
- controllable damping
- pneumatic / hydraulic cylinder concepts

Core actuator chain:

```text
data.ctrl
↓
actuator
↓
joint / tendon / site
↓
body motion
```

#### Light and Replicate

- [English](M2/MuJoCo/06_light_and_replicate.md)
- [中文](M2/MuJoCo/06_light_and_replicate_zh.md)

Topics include:

- light position and direction
- directional lights
- ambient lighting
- diffuse lighting
- specular highlights
- shadows
- attenuation
- spotlight parameters
- light tracking modes
- `replicate`
- `count`
- `offset`
- `euler`
- `sep`
- linear patterns
- circular patterns
- nested replication
- repeated body structures
- automatic naming of replicated elements

Core distinction:

```text
light
→ visualization / rendering

replicate
→ repeated model construction
```

---

### Source B - Robot Knowledge Study

Source repository:

https://github.com/noBug01/Robot_knowledge_study

Version used:

```text
v0.3.0
```

This part extends MuJoCo learning from XML modeling into Python-driven simulation, state observation, and basic robot control.

#### SIM-T01 - Table and Falling Cube

- [English](M2/RobotKnowledgeStudy_MuJoCo/01_table_cube.md)
- [中文](M2/RobotKnowledgeStudy_MuJoCo/01_table_cube_zh.md)

Topics include:

- loading MJCF with Python
- `MjModel`
- `MjData`
- `mj_step`
- `mj_forward`
- `qpos`
- `qvel`
- contact observation
- `data.ncon`
- CSV output
- numerical prediction and verification
- Viewer
- automated testing

Core workflow:

```text
XML scene
↓
MjModel
↓
MjData
↓
mj_step
↓
state changes
↓
observation
↓
numerical / visual verification
```

#### SIM-T02 - Arm Joint Targets

- [English](M2/RobotKnowledgeStudy_MuJoCo/02_arm_joint_targets.md)
- [中文](M2/RobotKnowledgeStudy_MuJoCo/02_arm_joint_targets_zh.md)

Topics include:

- parent-child body hierarchy
- default classes
- mesh assets
- multiple geoms inside one body
- seven-joint robot arm
- position actuators
- `data.ctrl`
- target vs actual joint position
- `qpos`
- `qvel`
- joint sensors
- end-effector site
- end-effector position and orientation
- waypoint motion
- interpolation
- Viewer-based controlled motion

Core control chain:

```text
WAYPOINTS
↓
interpolation
↓
data.ctrl
↓
position actuator
↓
joint motion
↓
qpos / qvel
↓
sensor feedback
↓
end-effector pose
```

---

### M2 Learning Progression

The two source streams cover different parts of the MuJoCo learning process.

```text
Albusgive source
↓
MJCF structure
↓
geom / body / site
↓
joint modeling
↓
contact and friction
↓
actuator models
↓
light and repeated scene construction

Robot Knowledge Study source
↓
Python simulation
↓
state observation
↓
actuator control
↓
sensor feedback
↓
end-effector observation
```

Together, the current M2 learning progression is:

```text
MJCF modeling
↓
rigid-body structure
↓
joint motion
↓
contact and friction
↓
actuation
↓
scene construction
↓
Python-driven simulation
↓
state observation
↓
active joint control
↓
sensor feedback
```

---

### Current M2 Status

M2 is still in progress because it contains material from two different upstream sources.

#### Robot Knowledge Study

The currently available M2 material from `Robot_knowledge_study` has been completed.

Completed topics include:

- SIM-T01 table and falling cube
- Python-based MuJoCo simulation
- `MjModel` and `MjData`
- `mj_step` and `mj_forward`
- state observation with `qpos` and `qvel`
- contact observation
- CSV output
- automated testing
- SIM-T02 arm joint targets
- position actuators
- `data.ctrl`
- waypoint-based joint control
- sensor feedback
- end-effector position and orientation
- Python-controlled Viewer simulation

#### Albusgive MuJoCo Learning

The MuJoCo learning material based on the Albusgive source is still in progress.

Completed topics so far include:

- environment and assets
- geom, body, and site
- joint modeling
- pendulum simulation
- friction
- `condim`
- elliptic and pyramidal friction cones
- contact priority
- actuator fundamentals
- motor actuator
- position actuator
- velocity actuator
- integrated velocity actuator
- damper actuator
- cylinder actuator
- actuator limits and control parameters
- light
- replicate
- linear and circular replication
- nested replication

More topics from this source will continue to be added as the learning progresses.

Therefore:

```text
Robot Knowledge Study
→ completed

Albusgive MuJoCo Learning
→ in progress

Overall M2
→ in progress
```

## Purpose

These notes serve three goals:

1. Support long-term review and revision.
2. Document the reasoning behind the implementations in this repository.
3. Provide evidence of continuous and structured technical learning.

Runnable implementations are stored in `examples/`, while automated checks are stored in `tests/`.