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

---

## Experiment Structure

The current directory structure is:

```text
MuJoCo/
├── README.md
├── review_model.xml
├── review_model_report.md
└── review_model_report_zh.md
```

As new MuJoCo experiments are completed, they will be added to this directory and documented here.

---

## Future Experiments

Future experiments may include topics such as:

- Joint behavior
- Revolute joints
- Slide joints
- Actuators
- Sensors
- Contact and friction
- Robot arms
- Forward kinematics
- Inverse kinematics
- Control
- More advanced rigid-body simulation

This README will be updated as M2 progresses.