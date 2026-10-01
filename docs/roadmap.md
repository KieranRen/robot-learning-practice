# Learning Roadmap

This roadmap records the planned learning progression of this repository.  
The exact order may be adjusted according to project requirements, research needs, and progress in each stage.

## M0 — Environment and Workflow Foundations

**Status: Completed**

Main goals:

- set up the Python and Conda environment
- become familiar with Git and GitHub workflow
- learn how to work with branches, commits, pull requests, and merges
- establish the repository structure
- verify the development and testing environment

Key outcomes:

- reproducible local environment
- working GitHub workflow
- repository organization established
- basic testing workflow verified

---

## M1 — Robot Math Foundations

**Status: Completed**

Main goals:

- build practical Python and NumPy foundations
- understand vectors, matrices, and coordinate representations used in robotics
- understand rotation matrices and rigid transformations
- learn how to implement and validate basic robot geometry operations
- connect mathematical formulas with executable NumPy code
- reinforce the concepts through testing and textbook reading

Main topics:

- Python fundamentals
- NumPy arrays, shapes, broadcasting, and matrix multiplication
- vectors and coordinate frames
- rotation matrices and `SO(3)`
- homogeneous transformations and `SE(3)`
- rigid-transform composition and inverse
- fixed-frame and body-frame updates
- mathematical and numerical validation
- unit testing for geometry functions

Textbook reading:

- *Modern Robotics: Mechanics, Planning, and Control*
- Section 3.2.1 — Rotation Matrices
- Section 3.3.1 — Homogeneous Transformation Matrices

Related records:

- [M1 Learning Notes](../notes/m1/)
- [M1 Experiments](../experiments/m1/)
- [Progress Record](../progress.md)

---

## M2 - MuJoCo Simulation

**Status: In Progress**

M2 focuses on MuJoCo modeling, simulation, Python-driven control, state observation, and basic robot interaction.

The learning material currently comes from two different upstream sources. These source streams are tracked separately because they focus on different parts of MuJoCo learning and are progressing independently.

### Source A - Albusgive MuJoCo Learning

Source repository:

https://github.com/Albusgive/mujoco_learning.git

**Status: In Progress**

Main goals:

- understand MuJoCo XML / MJCF structure
- understand simulation configuration
- learn assets, textures, materials, and meshes
- understand `geom`, `body`, and `site`
- understand body hierarchy and relative coordinate frames
- learn joint types and joint parameters
- build and verify simple articulated models
- gradually expand into further MuJoCo modeling and simulation topics

Completed so far:

- environment and assets
- simulation settings
- visual configuration
- mesh and material resources
- `geom`
- `body`
- `site`
- body hierarchy
- relative coordinate relationships
- mass, density, friction, and collision properties
- joint types
- hinge joints
- joint axis and range
- damping
- stiffness
- friction loss
- armature
- simple pendulum modeling
- pendulum simulation and verification

Current state:

```text
Environment and Assets
→ Completed

Geom, Body and Site
→ Completed

Joint
→ Completed

Pendulum Experiment
→ Completed

Further MuJoCo topics
→ In Progress
```

Related records:

- [M2 Learning Notes](../notes/README.md)
- [MuJoCo Experiments](../experiments/M2/MuJoCo/)

---

### Source B - Robot Knowledge Study

Source repository:

https://github.com/noBug01/Robot_knowledge_study

Version used:

```text
v0.3.0
```

**Status: Completed**

This source introduced Python-driven MuJoCo simulation and basic robot control through two scenes.

#### SIM-T01 - Table and Falling Cube

Main topics:

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
- Python-controlled Viewer

Core workflow:

```text
XML
↓
MjModel
↓
MjData
↓
mj_step
↓
qpos / qvel / contact update
↓
observation
↓
numerical and visual verification
```

#### SIM-T02 - Arm Joint Targets

Main topics:

- hierarchical robot bodies
- parent-child body relationships
- default parameter classes
- mesh assets
- visual and collision geometry
- multiple geoms inside one body
- seven-joint robot arm
- position actuators
- `data.ctrl`
- target vs actual joint state
- waypoint interpolation
- `qpos`
- `qvel`
- joint sensors
- end-effector site
- end-effector position and orientation
- sensor feedback
- Python-controlled robot motion
- Viewer timing and synchronization

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

Key outcome:

```text
target
≠
actual state
```

Python defines the desired control target, while MuJoCo physics determines how the robot actually moves toward that target.

Related records:

- [Robot Knowledge Study Notes](../notes/M2/RobotKnowledgeStudy_MuJoCo/)
- [Robot Knowledge Study Experiments](../experiments/M2/RobotKnowledgeStudy_MuJoCo/)

---

### M2 Learning Progression

The current M2 progression is:

```text
MJCF modeling
↓
geom / body / site
↓
joint modeling
↓
basic physical simulation
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

Current status:

```text
Robot Knowledge Study
→ Completed

Albusgive MuJoCo Learning
→ In Progress

Overall M2
→ In Progress
```

---

## Next Stage

The next stage will be selected after more of the current MuJoCo learning stream is completed.

Possible future directions include:

- robot kinematics
- control
- trajectory planning
- perception
- ROS 2
- more advanced simulation
- integration of simulation with robotics software tools

The exact sequence may be adjusted according to future projects, research needs, and the remaining MuJoCo learning material.

## Next Stage

The next robotics module has not yet been fixed.

Possible directions include:

- robot kinematics
- simulation
- control
- perception
- ROS 2

The next module will be selected according to the requirements of future projects and research tasks rather than following a rigid predefined sequence.

---

## Long-Term Direction

The long-term purpose of this repository is to gradually build a practical robotics foundation that connects:

- mathematics
- programming
- robot modelling
- simulation
- control
- perception
- robotics software tools

Each stage should include, where appropriate:

1. concept learning
2. implementation
3. experiments
4. testing
5. written notes
6. reflection and progress records

The goal is not only to finish learning materials, but to build reusable knowledge and engineering skills for future robotics projects and research.