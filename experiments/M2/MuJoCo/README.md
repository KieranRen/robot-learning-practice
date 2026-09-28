# M2 - MuJoCo Experiments

## Overview

This directory contains the MuJoCo experiments completed during M2 of my Robot Learning roadmap.

The purpose of these experiments is to connect theoretical concepts with practical simulation work.

The experiments in this directory are based on concepts learned from the following upstream repository:

https://github.com/Albusgive/mujoco_learning.git

The original repository and teaching materials belong to their respective author(s).

The files in this directory record my own practice, experiments, summaries, and understanding based on the learning process.

---

## Current Experiments

### 1. Review Model

The first MuJoCo experiment combines the basic concepts learned so far into one simulation scene.

Files:

- [`review_model.xml`](review_model.xml)
- [`review_model_report.md`](review_model_report.md)
- [`review_model_report_zh.md`](review_model_report_zh.md)

Main concepts reviewed:

- Simulation configuration
- Visual settings
- Assets
- Textures
- Materials
- `worldbody`
- `body`
- `geom`
- `site`
- Parent-child body hierarchy
- Relative coordinates
- `freejoint`
- Gravity
- Mass
- Friction
- Basic collision behavior
- Sphere, box, cylinder, and capsule geometries

### 2. Pendulum

The second MuJoCo experiment focuses on joint behavior using a simple pendulum.

Files:

- [`pendulum.xml`](pendulum.xml)
- [`pendulum_report.md`](pendulum_report.md)
- [`pendulum_report_zh.md`](pendulum_report_zh.md)

Main concepts reviewed:

- `body`
- `joint`
- `geom`
- `hinge`
- joint position
- joint axis
- joint range
- damping
- initial orientation
- gravity
- center of mass
- torque
- oscillation
- constrained rotational motion

The experiment demonstrates how a hinge joint restricts a body to one rotational degree of freedom and how gravity produces torque when the pendulum starts away from its equilibrium position.

---

## Experiment Structure

The current directory structure is:

```text
MuJoCo/
├── README.md
├── review_model.xml
├── review_model_report.md
├── review_model_report_zh.md
├── pendulum.xml
├── pendulum_report.md
└── pendulum_report_zh.md
```

As new MuJoCo experiments are completed, they will be added to this directory and documented here.

---

## Future Experiments

Future experiments may include topics such as:

- Actuators
- Sensors
- Contact and friction
- Robot arms
- Forward kinematics
- Inverse kinematics
- Control
- More advanced rigid-body simulation

This README will be updated as M2 progresses.