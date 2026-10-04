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

### 3. Friction Comparison

The third MuJoCo experiment focuses on contact friction and the role of `condim`.

Files:

- [`friction_comparison.xml`](friction_comparison.xml)
- [`friction_comparison_report.md`](friction_comparison_report.md)
- [`friction_comparison_report_zh.md`](friction_comparison_report_zh.md)

The model contains four main comparison groups:

```text
Box
condim 1 vs 3

Sphere
condim 3 vs 6

Cylinder on slope
condim 1 vs 3

Sphere on slope
condim 4 vs 6
```

Main concepts reviewed:

- sliding friction
- torsional friction
- rolling friction
- `friction="a b c"`
- `condim`
- normal contact
- sliding contact directions
- torsional friction dimensions
- rolling friction dimensions
- `cone="elliptic"`
- friction constraint dimensions
- `priority`
- contact parameter selection
- `impratio`
- control-variable experiment design
- friction behavior on horizontal surfaces
- friction behavior on slopes

The experiment reinforces the relationship:

```text
friction
→ determines friction strength

condim
→ determines which friction modes are enabled

priority
→ determines which geom's contact settings dominate

cone
→ determines how friction constraints are represented
```

The floor and slopes use lower contact priority than the moving objects so that each moving object's `condim` and friction settings can be compared more clearly.

The experiment also avoids unnecessary external asset dependencies so that the model can be loaded more easily in MuJoCo Viewer.

### 4. Actuator Demo

The fourth MuJoCo experiment focuses on actuator behavior using a simple two-joint mechanism.

Files:

- [`actuator_demo.xml`](actuator_demo.xml)
- [`actuator_demo_report.md`](actuator_demo_report.md)
- [`actuator_demo_report_zh.md`](actuator_demo_report_zh.md)

The mechanism structure is:

```text
world
└── support
    └── rotary_arm
        ├── pivot joint
        ├── horizontal arm
        └── pendulum
            ├── ph joint
            ├── pendulum rod
            └── pendulum mass
```

The two joints use different actuator types:

```text
pivot
→ position actuator

ph
→ intvelocity actuator
```

Main concepts reviewed:

- actuator-to-joint connection
- `position` actuator
- `intvelocity` actuator
- `data.ctrl`
- target position
- integrated velocity command
- `kp`
- `kv`
- `ctrlrange`
- `forcerange`
- `actrange`
- `ctrllimited`
- `forcelimited`
- `actlimited`
- target vs actual joint state
- actuator output limits
- internal activation-state limits
- body hierarchy
- joint-driven motion

The position actuator demonstrates:

```text
data.ctrl
→ target angle
→ position error
→ actuator torque
→ joint motion
```

The integrated velocity actuator demonstrates:

```text
data.ctrl
→ velocity-like command
→ integration
→ internal target position
→ joint motion
```

This experiment reinforces that the physical meaning of `data.ctrl` depends on actuator type.

It also demonstrates the distinction between:

```text
ctrlrange
→ control input limit

forcerange
→ actuator force / torque output limit

actrange
→ internal actuator state limit
```

---

## Experiment Structure

The current directory structure is:

```text
MuJoCo/
├── README.md
│
├── review_model.xml
├── review_model_report.md
├── review_model_report_zh.md
│
├── pendulum.xml
├── pendulum_report.md
├── pendulum_report_zh.md
│
├── friction_comparison.xml
├── friction_comparison_report.md
├── friction_comparison_report_zh.md
│
├── actuator_demo.xml
├── actuator_demo_report.md
└── actuator_demo_report_zh.md
```

The experiments currently progress through:

```text
basic MJCF review
↓
joint motion
↓
contact and friction
↓
actuator control
```

As new MuJoCo experiments are completed, they will be added to this directory and documented here.

---

## Current Experiment Progression

The current experiment sequence follows the development of the M2 learning process.

### Review Model

```text
MJCF structure
↓
body / geom / site
↓
assets and materials
↓
basic rigid-body simulation
```

### Pendulum

```text
body
↓
hinge joint
↓
gravity
↓
torque
↓
rotational motion
```

### Friction Comparison

```text
contact
↓
friction coefficients
↓
condim
↓
friction modes
↓
priority
↓
observed contact behavior
```

### Actuator Demo

```text
joint
↓
actuator
↓
data.ctrl
↓
force / torque
↓
physical joint motion
```

Together, the current experiment progression is:

```text
model construction
↓
joint motion
↓
contact interaction
↓
actuation
```

---

## Future Experiments

Future experiments may include topics such as:

- sensors
- site-based measurements
- contact observation
- more advanced actuator control
- robot arms
- forward kinematics
- inverse kinematics
- trajectory generation
- closed-loop control
- more advanced rigid-body simulation
- larger integrated MuJoCo models

`light` and `replicate` have currently been studied mainly as MJCF modeling features rather than as standalone experiments.

A dedicated experiment may be added later if these features are used in a larger simulation task.

This README will continue to be updated as M2 progresses.