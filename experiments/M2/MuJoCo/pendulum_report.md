# Pendulum Experiment

[English](pendulum_report.md) | [中文](pendulum_report_zh.md)

---

## Overview

This experiment demonstrates a simple MuJoCo pendulum using a hinge joint.

The main purpose is to connect the joint concepts learned in M2 with an actual simulation.

The experiment focuses on:

- `body`
- `joint`
- `geom`
- `hinge`
- `axis`
- `range`
- `damping`
- Gravity
- Initial orientation
- Torque caused by gravity

The simulation file is:

```text
pendulum.xml
```

---

## 1. Experiment Structure

The model contains:

- A ground plane
- A pendulum body
- A hinge joint
- A capsule geom representing the pendulum rod

The simplified hierarchy is:

```text
worldbody
├── ground
└── pendulum body
    ├── hinge joint
    └── capsule geom
```

---

## 2. Pendulum Body

The pendulum body is defined as:

```xml
<body name="pendulum"
      pos="0 0 2"
      euler="0 45 0">
```

The position:

```text
pos="0 0 2"
```

places the pendulum body at:

```text
x = 0
y = 0
z = 2
```

relative to the world frame.

The initial orientation:

```text
euler="0 45 0"
```

tilts the pendulum by 45 degrees.

This initial tilt is important because it allows gravity to generate a torque about the joint.

---

## 3. Hinge Joint

The joint is defined as:

```xml
<joint name="pivot"
       type="hinge"
       pos="0 0 0"
       axis="0 1 0"
       range="-90 90"
       damping="0.05"/>
```

The main settings are:

```text
type="hinge"
→ allows rotation around one axis
```

```text
pos="0 0 0"
→ places the joint at the local origin of the pendulum body
```

```text
axis="0 1 0"
→ rotation occurs around the y-axis
```

```text
range="-90 90"
→ limits the rotation to ±90 degrees
```

```text
damping="0.05"
→ gradually reduces oscillation
```

---

## 4. Pendulum Geometry

The pendulum rod is represented by a capsule:

```xml
<geom type="capsule"
      fromto="0 0 0  0 0 -1"
      size="0.08"
      mass="1"
      rgba="0.8 0.2 0.2 1"/>
```

The `fromto` attribute defines the rod between:

```text
Point A = (0, 0, 0)
Point B = (0, 0, -1)
```

So the pendulum extends downward from the joint.

The capsule radius is:

```text
0.08 m
```

and the mass is:

```text
1 kg
```

---

## 5. Why the Pendulum Moves

Gravity acts in the negative z direction:

```xml
gravity="0 0 -9.81"
```

If the pendulum starts tilted, its center of mass is not directly below the hinge axis.

Therefore gravity produces a torque about the joint.

The basic idea is:

```text
τ = r × F
```

where:

```text
τ
→ torque

r
→ position vector from the joint to the center of mass

F
→ gravitational force
```

Because the force does not act directly through the joint axis, a moment is generated.

This causes the pendulum to rotate.

---

## 6. Why the Vertical Pendulum Did Not Move

When the pendulum was initially vertical:

```text
joint
  ●
  |
  |
  ● center of mass
  ↓ gravity
```

the gravitational force acted almost directly through the joint axis.

Therefore:

```text
moment arm ≈ 0
```

and:

```text
torque ≈ 0
```

So the pendulum remained stationary.

This demonstrates an important mechanics principle:

```text
gravity alone does not guarantee rotation

rotation requires torque about the joint
```

---

## 7. Effect of Damping

The joint uses:

```xml
damping="0.05"
```

Damping creates resistance to joint motion.

A simple interpretation is:

```text
higher angular velocity
→ larger damping resistance
```

The rotational damping effect can be approximately understood as:

```text
τ_d = -cω
```

where:

```text
c
→ damping coefficient

ω
→ angular velocity
```

As a result:

```text
the pendulum oscillates
↓
energy is gradually dissipated
↓
the oscillation amplitude decreases
```

Without damping, the pendulum would continue oscillating for much longer in an ideal simulation.

---

## 8. Joint Range

The experiment uses:

```xml
range="-90 90"
```

with:

```xml
<compiler angle="degree" autolimits="true"/>
```

Therefore the hinge joint is limited to:

```text
-90° ≤ angle ≤ 90°
```

This prevents the pendulum from rotating freely through a full circle.

---

## 9. Concepts Reviewed

This experiment reviews:

```text
body
→ rigid body and local coordinate frame

joint
→ defines how the body can move

geom
→ defines the physical shape
```

It also reviews the following joint parameters:

```text
type
pos
axis
range
damping
```

and connects them with:

```text
gravity
initial orientation
center of mass
torque
oscillation
```

---

## 10. Running the Experiment

Activate the MuJoCo environment:

```bash
conda activate mujoco_env
```

Go to the folder containing the experiment file.

Then run:

```bash
python -m mujoco.viewer --mjcf pendulum.xml
```

After the viewer opens, start the simulation.

The pendulum should:

```text
start from a tilted position
↓
accelerate under gravity
↓
pass through the lowest point
↓
swing to the opposite side
↓
gradually lose amplitude because of damping
```

---

## Key Understanding

The most important idea from this experiment is:

```text
joint
→ defines allowed motion

gravity
→ produces force

offset between joint and force line
→ produces torque

torque
→ produces rotational motion
```

The hinge joint allows only one rotational degree of freedom, so the pendulum motion is constrained to rotation around the selected axis.

This experiment provides a simple connection between:

```text
MuJoCo joint configuration
+
rigid-body mechanics
+
physical simulation
```

---

## Source

This experiment is based on joint concepts learned from the following upstream repository:

https://github.com/Albusgive/mujoco_learning.git

The original repository and teaching materials belong to their respective author(s).

The simulation file and report here are my own practice, organization, and understanding based on the learning process.