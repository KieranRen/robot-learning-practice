# RobotKnowledgeStudy MuJoCo Experiments

This folder contains my MuJoCo experiments based on the M2 material from:

```text
Robot_knowledge_study
v0.3.0
```

Source repository:

https://github.com/noBug01/Robot_knowledge_study

The experiments here document my own learning process, verification, observations, and understanding based on the original materials.

---

## Experiment 1 - SIM-T01 Table and Falling Cube

This experiment introduces the basic Python-driven MuJoCo simulation workflow.

Files:

- [English Report](sim_t01_table_cube_report.md)
- [中文实验报告](sim_t01_table_cube_report_zh.md)

Main topics:

- loading an MJCF model with Python
- `MjModel`
- `MjData`
- `mj_step`
- `mj_forward`
- `qpos`
- `qvel`
- contact detection
- `data.ncon`
- CSV output
- prediction and numerical verification
- MuJoCo Viewer
- automated testing with `pytest`

Main workflow:

```text
XML scene
↓
MjModel
↓
MjData
↓
mj_step
↓
position / velocity / contact change
↓
observation
↓
numerical and visual verification
```

The experiment verifies that a freely falling cube reaches the table and settles at the expected height.

---

## Experiment 2 - SIM-T02 Arm Joint Targets

This experiment extends the simulation workflow from passive physical observation to active robot control.

Files:

- [English Report](sim_t02_arm_joint_targets_report.md)
- [中文实验报告](sim_t02_arm_joint_targets_report_zh.md)

Main topics:

- hierarchical robot bodies
- parent and child bodies
- default parameter classes
- mesh assets
- visual and collision geometry
- multiple geoms inside one body
- seven-joint robot arm
- position actuators
- `data.ctrl`
- target vs actual joint state
- `qpos`
- `qvel`
- joint sensors
- end-effector site
- end-effector position and orientation
- waypoint motion
- linear interpolation
- Viewer-controlled robot motion

Main control chain:

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

The experiment verifies that the left robot arm can follow predefined joint-space waypoints while Python observes both joint states and end-effector motion.

---

## Progression Between the Two Experiments

The two experiments represent a clear progression.

### SIM-T01

```text
physical model
↓
natural motion
↓
contact
↓
observation
```

The system is not actively controlled.

Python mainly advances the simulation and reads the result.

### SIM-T02

```text
control target
↓
actuator
↓
joint motion
↓
sensor feedback
```

Python actively controls the simulated robot.

This introduces the transition from:

```text
simulation observation
```

to:

```text
robot control and feedback
```

---

## Key Learning Progression

The main development across these experiments is:

```text
MJCF modeling
↓
Python simulation
↓
state observation
↓
active actuator control
↓
sensor feedback
↓
end-effector observation
```

These two experiments form the complete MuJoCo M2 content currently covered by the `Robot_knowledge_study` source.

---

## Repository Organization

This experiment folder is intentionally kept separate from the MuJoCo material based on other upstream repositories.

The goal is to preserve a clear relationship between:

```text
learning source
↓
notes
↓
experiments
↓
personal understanding
```

---

## Acknowledgement

I am sincerely grateful to the authors and contributors of `Robot_knowledge_study` for openly sharing their code, explanations, and learning materials.

Their work provided valuable guidance for learning MuJoCo simulation, Python-based simulation control, and basic robot-state observation in a structured and reproducible way.