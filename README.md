# Robot Learning Practice

[English](README.md) | [中文](README_zh.md)

A structured and reproducible record of my robotics learning, implementations, experiments, and technical development.

## About

This repository documents my long-term study of robotics, starting from mathematical and programming foundations and gradually extending toward larger robotics systems.

Each learning module combines:

- theory notes
- independent implementations
- automated tests
- experiments
- reproducible results
- reflections on mistakes and corrections

The goal is not only to complete tutorials, but to build a clear record of what I understand, implement, verify, and improve over time.

## Learning Source

The primary learning materials used in this repository come from multiple upstream repositories.

### M1 - Robot Math and Geometry

M1 learning materials are mainly based on:

- [Robot Knowledge Study](https://github.com/noBug01/Robot_knowledge_study.git)

This upstream repository is treated as the reference source for topics such as:

- Python and NumPy foundations
- Robot geometry
- Rigid transformations
- Geometry implementation
- Modern Robotics reading and related mathematical foundations

### M2 - MuJoCo Simulation

M2 MuJoCo learning materials are based on two upstream sources:

- [MuJoCo Learning](https://github.com/Albusgive/mujoco_learning.git)
- [Robot Knowledge Study](https://github.com/noBug01/Robot_knowledge_study)

The Albusgive source is used as the main reference for MJCF modeling and MuJoCo feature learning, including topics such as:

- MuJoCo XML / MJCF structure
- simulation configuration
- visual settings
- assets and materials
- geometries
- body hierarchy
- sites
- joints
- contact and friction
- actuator models
- lighting
- repeated model construction with `replicate`

The Robot Knowledge Study source extends this learning into Python-driven simulation, state observation, actuator control, sensor feedback, and robot-arm motion.

This repository does not aim to duplicate either upstream source. Instead, it records my own learning process, including:

- personal notes and summaries
- independent implementations
- simulation experiments
- automated tests
- reports and validation
- corrections and refinements

Whenever a specific learning task depends on a particular upstream version, the corresponding source or commit may be recorded in the relevant progress or experiment documentation.

I am sincerely grateful to the authors and contributors of the upstream repositories for generously sharing their knowledge, code, and learning materials with me.

Their contributions have been extremely helpful throughout my learning process and have given me a valuable foundation for studying robotics in a structured and practical way.

Without their sharing, this repository could not be built in its current form.

## Current Progress

| Module | Topic | Status | Learning Notes | Experiment Evidence |
|---|---|---|---|---|
| M0 | Environment setup and Git workflow | Completed | - | [Environment Reports](experiments/environment_reports/) |
| M1 | Python, NumPy, robot geometry, rigid transformations, testing, capability tasks, and Modern Robotics reading | Completed | [M1 Notes](notes/M1/) | [M1 Experiments](experiments/M1/) |
| M2 | MuJoCo simulation, MJCF modeling, contact, actuators, scene construction, and Python-driven control | In Progress | [M2 Notes](notes/README.md) | [M2 Experiments](experiments/M2/) |

### M1 Robot Math and Geometry

M1 currently includes three completed learning blocks:

#### Python and NumPy Foundations

- array shape, dimensions, and data types
- indexing and slicing
- views and copies
- broadcasting
- vector and matrix operations
- floating-point numerical checks
- automated testing with `pytest`

Learning notes:

- [English](notes/m1/python_numpy.md)
- [中文](notes/m1/python_numpy_zh.md)

Experiment evidence:

- [English](experiments/m1/numeric_basics_report.md)
- [中文](experiments/m1/numeric_basics_report_zh.md)

#### Robot Geometry and Rigid Transforms

- coordinate frames
- rotation matrices
- rigid-body transformations
- homogeneous coordinates
- transform composition
- inverse transforms
- round-trip validation
- coordinate-frame visualization

Learning notes:

- [English](notes/m1/robot_geometry.md)
- [中文](notes/m1/robot_geometry_zh.md)

Experiment evidence:

- [English](experiments/m1/robot_geometry_report.md)
- [中文](experiments/m1/robot_geometry_report_zh.md)

Generated visualization:

- [`outputs/m1/frames.svg`](outputs/m1/frames.svg)

### Geometry Implementation

The mathematical ideas above are connected to reusable NumPy implementations with explicit validation and clear interface contracts.

Topics covered:

- `rotation_z`
- `make_transform`
- `inverse_transform`
- `transform_points`
- finite numeric input validation
- strict array shape validation
- proper rotation matrix validation
- floating-point tolerance
- transform composition order
- round-trip consistency checks
- structure of the numerical and coordinate-frame examples

Learning notes:

- [English](notes/m1/geometry_implementation.md)
- [中文](notes/m1/geometry_implementation_zh.md)

### Textbook Reading

Completed the scoped M1 reading from *Modern Robotics: Mechanics, Planning, and Control*:

- Section 3.2.1 — Rotation Matrices
- Section 3.3.1 — Homogeneous Transformation Matrices

Key reinforcement and new material included:

- `SO(3)` and proper rotations
- `SE(3)` rigid transformations
- frame-subscript cancellation
- transform composition and inversion
- fixed-frame versus body-frame transform updates

Reading notes:

- [English](notes/m1/modern_robotics_reading.md)
- [中文](notes/m1/modern_robotics_reading_zh.md)

Current automated verification:

```text
Python / NumPy:    22 tests passed
Robot Geometry:    54 tests passed
Full repository:   107 tests passed
```

### M2 - MuJoCo Simulation

M2 contains MuJoCo learning from two different upstream sources.

The two learning streams are kept separate because they focus on different parts of the learning process and are progressing independently.

#### Source A - Albusgive MuJoCo Learning

Source repository:

https://github.com/Albusgive/mujoco_learning.git

This learning stream focuses mainly on MJCF modeling fundamentals, physical interaction, actuator models, and scene construction.

Completed topics so far include:

- MuJoCo XML / MJCF structure
- simulation configuration
- environment and assets
- textures, materials, meshes, and skyboxes
- `geom`
- `body`
- `site`
- body hierarchy
- relative coordinate frames
- friction and collision settings
- joint types
- hinge joints
- joint axis and range
- damping
- stiffness
- friction loss
- armature
- simple pendulum simulation
- sliding friction
- torsional friction
- rolling friction
- `friction="a b c"`
- `condim`
- elliptic friction cones
- pyramidal friction cones
- friction constraint dimensions
- contact `priority`
- contact parameter selection
- `impratio`
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
- controllable damping
- basic pneumatic / hydraulic actuator concepts
- `light`
- directional and local lighting
- ambient, diffuse, and specular lighting
- light tracking and targeting
- `replicate`
- `count`
- `offset`
- `euler`
- `sep`
- linear replication
- circular replication
- nested replication
- repeated body structures

Notes:

- [Environment and Assets](notes/M2/MuJoCo/01_environment_and_assets.md)
- [中文 - 环境配置与资源](notes/M2/MuJoCo/01_environment_and_assets_zh.md)
- [Geom, Body and Site](notes/M2/MuJoCo/02_geom_body_site.md)
- [中文 - Geom、Body 与 Site](notes/M2/MuJoCo/02_geom_body_site_zh.md)
- [Joint](notes/M2/MuJoCo/03_joint.md)
- [中文 - Joint 关节](notes/M2/MuJoCo/03_joint_zh.md)
- [Friction](notes/M2/MuJoCo/04_friction.md)
- [中文 - Friction 摩擦](notes/M2/MuJoCo/04_friction_zh.md)
- [Actuator](notes/M2/MuJoCo/05_actuator.md)
- [中文 - Actuator 执行器](notes/M2/MuJoCo/05_actuator_zh.md)
- [Light and Replicate](notes/M2/MuJoCo/06_light_and_replicate.md)
- [中文 - Light 与 Replicate](notes/M2/MuJoCo/06_light_and_replicate_zh.md)

Experiments:

- [MuJoCo Experiments Overview](experiments/M2/MuJoCo/README.md)
- [Review Model Report](experiments/M2/MuJoCo/review_model_report.md)
- [中文 - Review Model Report](experiments/M2/MuJoCo/review_model_report_zh.md)
- [Pendulum Report](experiments/M2/MuJoCo/pendulum_report.md)
- [中文 - Pendulum Report](experiments/M2/MuJoCo/pendulum_report_zh.md)

This learning stream is still in progress.

---

#### Source B - Robot Knowledge Study

Source repository:

https://github.com/noBug01/Robot_knowledge_study

Version used:

```text
v0.3.0
```

This learning stream extends MuJoCo study from XML modeling into Python-driven simulation, state observation, actuator control, and sensor feedback.

Completed topics include:

- SIM-T01 table and falling cube
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
- automated testing with `pytest`
- MuJoCo Viewer
- SIM-T02 arm joint targets
- parent-child robot body hierarchy
- default classes
- mesh assets
- position actuators
- `data.ctrl`
- target vs actual joint state
- waypoint interpolation
- joint sensors
- end-effector position
- end-effector orientation
- Python-controlled Viewer simulation

Notes:

- [SIM-T01 - Table and Falling Cube](notes/M2/RobotKnowledgeStudy_MuJoCo/01_table_cube.md)
- [中文 - SIM-T01 桌面与自由下落方块](notes/M2/RobotKnowledgeStudy_MuJoCo/01_table_cube_zh.md)
- [SIM-T02 - Arm Joint Targets](notes/M2/RobotKnowledgeStudy_MuJoCo/02_arm_joint_targets.md)
- [中文 - SIM-T02 机械臂关节角目标控制](notes/M2/RobotKnowledgeStudy_MuJoCo/02_arm_joint_targets_zh.md)

Experiments:

- [Robot Knowledge Study MuJoCo Experiments](experiments/M2/RobotKnowledgeStudy_MuJoCo/README.md)
- [SIM-T01 Experiment Report](experiments/M2/RobotKnowledgeStudy_MuJoCo/sim_t01_table_cube_report.md)
- [中文 - SIM-T01 实验报告](experiments/M2/RobotKnowledgeStudy_MuJoCo/sim_t01_table_cube_report_zh.md)
- [SIM-T02 Experiment Report](experiments/M2/RobotKnowledgeStudy_MuJoCo/sim_t02_arm_joint_targets_report.md)
- [中文 - SIM-T02 实验报告](experiments/M2/RobotKnowledgeStudy_MuJoCo/sim_t02_arm_joint_targets_report_zh.md)

The currently available M2 material from this source has been completed.

---

#### M2 Learning Progression

The two source streams currently form the following progression:

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
Python-driven simulation
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

Current status:

```text
Robot Knowledge Study
→ completed

Albusgive MuJoCo Learning
→ in progress

Overall M2
→ in progress
```

## Repository Structure

```text
robot-learning-practice/
├── notes/
│   ├── M1/
│   │   ├── python_numpy.md
│   │   ├── python_numpy_zh.md
│   │   ├── robot_geometry.md
│   │   ├── robot_geometry_zh.md
│   │   ├── geometry_implementation.md
│   │   ├── geometry_implementation_zh.md
│   │   ├── modern_robotics_reading.md
│   │   └── modern_robotics_reading_zh.md
│   │
│   └── M2/
│       ├── MuJoCo/
│       │   ├── 01_environment_and_assets.md
│       │   ├── 01_environment_and_assets_zh.md
│       │   ├── 02_geom_body_site.md
│       │   ├── 02_geom_body_site_zh.md
│       │   ├── 03_joint.md
│       │   ├── 03_joint_zh.md
│       │   ├── 04_friction.md
│       │   ├── 04_friction_zh.md
│       │   ├── 05_actuator.md
│       │   ├── 05_actuator_zh.md
│       │   ├── 06_light_and_replicate.md
│       │   └── 06_light_and_replicate_zh.md
│       │
│       └── RobotKnowledgeStudy_MuJoCo/
│           ├── 01_table_cube.md
│           ├── 01_table_cube_zh.md
│           ├── 02_arm_joint_targets.md
│           └── 02_arm_joint_targets_zh.md
│
├── experiments/
│   ├── M1/
│   │   ├── capability_tasks_report.md
│   │   ├── capability_tasks_report_zh.md
│   │   ├── numeric_basics_report.md
│   │   ├── numeric_basics_report_zh.md
│   │   ├── robot_geometry_report.md
│   │   └── robot_geometry_report_zh.md
│   │
│   └── M2/
│       ├── MuJoCo/
│       │   ├── README.md
│       │   ├── review_model.xml
│       │   ├── review_model_report.md
│       │   ├── review_model_report_zh.md
│       │   ├── pendulum.xml
│       │   ├── pendulum_report.md
│       │   └── pendulum_report_zh.md
│       │
│       └── RobotKnowledgeStudy_MuJoCo/
│           ├── README.md
│           ├── sim_t01_table_cube_report.md
│           ├── sim_t01_table_cube_report_zh.md
│           ├── sim_t02_arm_joint_targets_report.md
│           └── sim_t02_arm_joint_targets_report_zh.md
│
├── tests/
├── examples/
├── docs/
├── progress/
├── environment.yml
├── README.md
└── README_zh.md
```

The repository is organized so that learning notes and experiment evidence are separated but connected.

- `notes/` contains structured learning summaries and explanations.
- `experiments/` contains practical implementations, simulation files, and experiment reports.
- `tests/` contains automated validation.
- `examples/` contains runnable examples and demonstrations.
- `docs/` contains workflow and project documentation.
- `progress/` records milestone and learning progress.

## Learning Approach

My learning workflow is based on four steps:

1. Understand the underlying mathematics and concepts.
2. Re-implement the ideas independently.
3. Verify the implementation using tests and numerical checks.
4. Document the reasoning, mistakes, and results for future review.

The purpose of this workflow is to make each topic reproducible, explainable, and useful beyond a single tutorial or exercise.

## Reproducibility

The project uses a Conda environment defined in `environment.yml`.

Typical setup:

```bash
conda env create -f environment.yml
conda activate robot_manipulation_learning
python -m pytest
```

Runnable examples are stored in `examples/`, while automated checks are stored in `tests/`.

Where relevant, experiment outputs and environment verification records are stored under `experiments/`.

## Documentation

- [Learning Notes](notes/README.md)
- [Learning Roadmap](docs/roadmap.md)
- [Detailed Workflow](docs/workflow.md)
- [Progress Record](progress.md)

## Current Focus

The current focus is M2: MuJoCo simulation.

At this stage, I am working on:

- understanding MuJoCo XML / MJCF structure
- building simple simulation environments
- learning how `worldbody`, `body`, `geom`, `site`, and `joint` work together
- understanding parent-child body relationships and relative coordinate frames
- studying contact and friction behavior
- understanding sliding, torsional, and rolling friction
- learning how `condim`, friction cones, and contact priority affect simulation
- learning how actuators drive joints and other model elements
- comparing motor, position, velocity, and integrated-velocity control
- understanding actuator limits such as `ctrlrange`, `forcerange`, and `actrange`
- studying controllable damping and basic cylinder actuator models
- learning scene-lighting configuration
- using `replicate` to create repeated model structures efficiently
- creating simple MuJoCo experiments from scratch
- connecting simulation concepts with robotics foundations such as kinematics, dynamics, joints, actuators, sensors, and control

Completed M2 work so far includes:

- environment and asset configuration notes
- geom, body, and site notes
- joint notes
- friction notes
- actuator notes
- light and replicate notes
- a basic review simulation model
- a hinge-joint pendulum experiment
- friction comparison analysis
- actuator example analysis
- English and Chinese documentation for the current MuJoCo notes and experiments
- SIM-T01 table and falling cube
- SIM-T02 robot-arm joint target control
- Python-driven MuJoCo simulation
- state observation with `qpos` and `qvel`
- actuator control with `data.ctrl`
- sensor feedback
- end-effector position and orientation observation

The `Robot_knowledge_study` M2 material currently available in version `v0.3.0` has been completed, including both SIM-T01 and SIM-T02.

The Albusgive-based MuJoCo learning stream is still in progress and will continue to be expanded with additional modeling and simulation topics.

Therefore, overall M2 remains in progress.

## Future Directions

Planned areas include:

- robot kinematics
- control systems
- ROS 2
- perception
- SLAM
- manipulation
- simulation
- larger integrated robotics projects

As the repository grows, selected learning modules may be developed into more complete standalone projects with their own documentation, tests, and examples.

## A Note to Myself

I am still at the beginning of this journey.

There will be concepts I do not understand, code that does not work, experiments that fail, and problems that take far longer than expected. That is part of learning robotics, not evidence that I should stop.

My goal is not to appear advanced. My goal is to become capable.

I do not need to be defined by who I was before. Past hesitation, mistakes, missed opportunities, or slower beginnings do not decide what I can become. What matters is what I choose to do now, what I build now, and whether I keep moving forward from here.

So I will keep learning the mathematics, writing the code, testing my assumptions, asking better questions, and building things one step at a time.

Small progress, repeated consistently, becomes real ability.

And one day, the things that feel difficult now will become the foundations for much harder and more interesting problems.