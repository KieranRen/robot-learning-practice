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

M2 MuJoCo learning materials are based on:

- [MuJoCo Learning](https://github.com/Albusgive/mujoco_learning.git)

This upstream repository is used as the reference source for topics such as:

- MuJoCo XML / MJCF structure
- Simulation configuration
- Visual settings
- Assets and materials
- Geometries
- Body hierarchy
- Sites
- Basic simulation experiments

This repository does not aim to duplicate either upstream source. Instead, it records my own learning process, including:

- Personal notes and summaries
- Independent implementations
- Simulation experiments
- Automated tests
- Reports and validation
- Corrections and refinements

Whenever a specific learning task depends on a particular upstream version, the corresponding source or commit may be recorded in the relevant progress or experiment documentation.

I am sincerely grateful to the authors and contributors of the upstream repositories for generously sharing their knowledge, code, and learning materials with me.

Their contributions have been extremely helpful throughout my learning process and have given me a valuable foundation for studying robotics in a structured and practical way.

Without their sharing, this repository cannot be built in this currrent way.

## Current Progress

| Module | Topic | Status | Learning Notes | Experiment Evidence |
|---|---|---|---|---|
| M0 | Environment setup and Git workflow | Completed | - | [Environment Reports](experiments/environment_reports/) |
| M1 | Python, NumPy, robot geometry, rigid transformations, testing, capability tasks, and Modern Robotics reading | Completed | [M1 Notes](notes/M1/) | [M1 Experiments](experiments/M1/) |
| M2 | MuJoCo simulation and MJCF modeling | In Progress | [M2 MuJoCo Notes](notes/M2/MuJoCo/) | [M2 MuJoCo Experiments](experiments/M2/MuJoCo/) |

### M1 Highlights

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

### M2 MuJoCo Simulation

M2 focuses on building practical robot simulation experience with MuJoCo and MJCF.

Current learning includes:

- MuJoCo XML / MJCF structure
- Simulation configuration
- `timestep`, gravity, integrators, and solvers
- Visual settings
- Assets, textures, materials, meshes, and skyboxes
- Geometry definitions with `geom`
- `body` hierarchy and relative coordinate frames
- `site` markers
- Joint types and constrained body motion
- `hinge`, `slide`, `ball`, and `free` joints
- Joint position, axis, range, damping, stiffness, friction loss, and armature
- Basic contact and friction concepts
- Simple MuJoCo simulation experiments

Learning notes:

- [Environment and Assets](notes/M2/MuJoCo/01_environment_and_assets.md)
- [中文 - 环境配置与资源](notes/M2/MuJoCo/01_environment_and_assets_zh.md)
- [Geom, Body and Site](notes/M2/MuJoCo/02_geom_body_site.md)
- [中文 - Geom、Body 与 Site](notes/M2/MuJoCo/02_geom_body_site_zh.md)
- [Joint](notes/M2/MuJoCo/03_joint.md)
- [中文 - Joint 关节](notes/M2/MuJoCo/03_joint_zh.md)

Experiment evidence:

- [MuJoCo Experiments Overview](experiments/M2/MuJoCo/README.md)
- [Review Model](experiments/M2/MuJoCo/review_model.xml)
- [Review Model Report](experiments/M2/MuJoCo/review_model_report.md)
- [中文 - Review Model Report](experiments/M2/MuJoCo/review_model_report_zh.md)
- [Pendulum](experiments/M2/MuJoCo/pendulum.xml)
- [Pendulum Report](experiments/M2/MuJoCo/pendulum_report.md)
- [中文 - Pendulum Report](experiments/M2/MuJoCo/pendulum_report_zh.md)

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
│       └── MuJoCo/
│           ├── README.md
│           ├── 01_environment_and_assets.md
│           ├── 01_environment_and_assets_zh.md
│           ├── 02_geom_body_site.md
│           ├── 02_geom_body_site_zh.md
│           ├── 03_joint.md
│           └── 03_joint_zh.md
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
│       └── MuJoCo/
│           ├── README.md
│           ├── review_model.xml
│           ├── review_model_report.md
│           ├── review_model_report_zh.md
│           ├── pendulum.xml
│           ├── pendulum_report.md
│           └── pendulum_report_zh.md
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

Runnable examples are stored in examples/, while automated checks are stored in tests/.
Where relevant, experiment outputs and environment verification records are stored under experiments/.

## Documentation

- [Learning Notes](notes/README.md)
- [Learning Roadmap](docs/roadmap.md)
- [Detailed Workflow](docs/workflow.md)
- [Progress Record](progress.md)

## Current Focus

The current focus is M2: MuJoCo simulation.

At this stage, I am working on:

- Understanding MuJoCo XML / MJCF structure
- Building simple simulation environments
- Learning how `worldbody`, `body`, `geom`, and `site` work together
- Understanding parent-child body relationships and relative coordinates
- Practicing basic geometry, materials, gravity, contact, and friction
- Creating simple MuJoCo experiments from scratch
- Connecting simulation concepts with robotics foundations such as kinematics, dynamics, joints, actuators, sensors, and control

Completed M2 work so far includes:

- Environment and asset configuration notes
- Geom, body, and site notes
- Joint notes
- A basic review simulation model
- A hinge-joint pendulum experiment
- English and Chinese documentation for notes and experiments

M2 is still in progress and will continue to expand as more MuJoCo and robotics concepts are introduced.

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
