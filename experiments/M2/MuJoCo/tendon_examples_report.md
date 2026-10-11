# MuJoCo Tendon Example Analysis

[English](tendon_examples_report.md) | [中文](tendon_examples_report_zh.md)

## Overview

This report records the analysis of two tendon examples studied from the Albusgive MuJoCo learning source:

1. a Mecanum-wheel model using `fixed` tendons
2. a multi-link model using `spatial` tendons and a `muscle` actuator

The purpose of this report is to document how the example models work and how tendon transmission differs from direct joint actuation.

These examples were studied and analysed from the source material. This report does not claim that the complete original XML models were independently reconstructed or experimentally validated in this repository.

---

# 1. Example A - Fixed Tendons for a Mecanum Robot

## Model Idea

The first example uses four wheel joints:

```text
a1
b1
a2
b2
```

Instead of controlling the four joints independently, the model defines three `fixed` tendons:

```text
forward
transverse
rotate
```

This creates three virtual motion coordinates:

```text
4 physical wheel joints
↓
fixed tendon combinations
↓
3 intuitive motion channels
```

---

# 2. Wheel Structure

The wheel model uses a cylindrical wheel body with repeated angled rollers.

The rollers are created using `replicate`.

The studied structure includes approximately:

```text
16 repeated rollers
```

with an incremental rotation around the wheel:

```text
euler z ≈ 0.3925 rad
```

Since:

```text
2π / 16 ≈ 0.3927
```

the repeated rollers are distributed around the wheel circumference.

The roller orientation is approximately:

```text
±0.785398 rad
≈ ±45°
```

which is characteristic of a Mecanum-wheel arrangement.

---

# 3. Forward Tendon

The `forward` fixed tendon uses the coefficient pattern:

```text
a1  +0.25
b1  +0.25
a2  +0.25
b2  +0.25
```

Conceptually:

```text
forward
=
0.25a1
+
0.25b1
+
0.25a2
+
0.25b2
```

The sign pattern is:

```text
+ +
+ +
```

All four wheel joints contribute in the same direction.

Therefore this tendon represents the combined forward/backward motion coordinate.

---

# 4. Transverse Tendon

The `transverse` tendon uses:

```text
a1  +0.25
b1  -0.25
a2  -0.25
b2  +0.25
```

Conceptually:

```text
transverse
=
+0.25a1
-0.25b1
-0.25a2
+0.25b2
```

The sign pattern is:

```text
+ -
- +
```

Because the Mecanum rollers are mounted at opposite angles, this combination corresponds to lateral motion.

So:

```text
transverse
→ sideways motion
```

The exact positive direction depends on:

```text
wheel installation
joint-axis direction
sign conventions
```

Therefore it should not automatically be interpreted as specifically left or right without inspecting the complete model.

---

# 5. Rotate Tendon

The `rotate` tendon uses:

```text
a1  +0.25
b1  +0.25
a2  -0.25
b2  -0.25
```

Conceptually:

```text
rotate
=
+0.25a1
+0.25b1
-0.25a2
-0.25b2
```

The sign pattern is:

```text
+ +
- -
```

The two wheel groups contribute in opposite directions.

This produces a yaw-rotation coordinate.

So:

```text
rotate
→ vehicle rotation
```

Again, the exact positive rotation direction depends on the model's joint-axis conventions.

---

# 6. Why `coef="0.25"` Is Used

There are four wheel joints.

Using:

```text
0.25
```

for each equal contribution produces:

```text
0.25 × 4 = 1
```

This gives an average-like normalized combination.

However, the most important part is not the number `0.25` itself.

The most important information is:

```text
relative magnitude
+
relative sign
```

of the coefficients.

---

# 7. Velocity Actuators

The example uses velocity actuators attached to the tendons rather than directly to wheel joints.

Conceptually:

```xml
<velocity tendon="forward" .../>
<velocity tendon="transverse" .../>
<velocity tendon="rotate" .../>
```

The control chain becomes:

```text
data.ctrl
↓
velocity actuator
↓
fixed tendon
↓
multiple wheel joints
↓
vehicle motion
```

The studied actuator parameters include:

```text
kv = 30
ctrlrange = [-15, 15]
```

This means the controller operates on the tendon-level virtual coordinates.

---

# 8. Main Lesson from the Mecanum Example

Without the fixed tendons, a controller would need to reason directly about:

```text
a1
b1
a2
b2
```

With the tendon definitions, the model exposes:

```text
forward
transverse
rotate
```

This creates a much clearer high-level control interface.

The key idea is:

```text
physical joints
↓
fixed tendon
↓
virtual motion coordinate
```

---

# 9. Example B - Spatial Tendon and Muscle

The second example demonstrates `spatial` tendons.

Unlike a fixed tendon, a spatial tendon follows a geometric path through multiple sites.

The model contains several linked bodies and hinge joints.

Sites are attached to different bodies and used as tendon routing points.

---

# 10. Joint Structure

The example contains three hinge joints:

```text
joint1
joint2
joint3
```

The studied limits include approximately:

```text
joint2 range = 0 to 1.57 rad
joint3 range = 0 to 0.78 rad
```

which correspond approximately to:

```text
1.57 rad ≈ 90°
0.78 rad ≈ 45°
```

The joints rotate around:

```text
axis="0 0 1"
```

in the studied example.

---

# 11. Tendon Routing Sites

The model contains sites such as:

```text
ceiling
hook1
hook2
hook3
hook4
hook5
```

These sites act as tendon routing or attachment points.

The important relationship is:

```text
body motion
↓
site position changes
↓
spatial tendon geometry changes
↓
tendon length changes
```

---

# 12. Passive Tendon `M`

The first spatial tendon is named:

```text
M
```

Its path is:

```text
ceiling
↓
hook1
↓
hook2
↓
hook3
```

The studied parameters include:

```text
springlength = "0 0.5"
stiffness = 1000
damping = 10
width = 0.01
```

This tendon has substantial passive stiffness.

Therefore it behaves conceptually like:

```text
elastic tendon
+
damper
```

Its effect does not require an active actuator.

---

# 13. Passive Tendon Behaviour

When the linked bodies move:

```text
site geometry changes
↓
tendon length changes
```

If the tendon moves away from its spring reference length:

```text
stiffness
→ produces elastic restoring behaviour
```

If the tendon length changes rapidly:

```text
damping
→ resists the length-change velocity
```

Therefore the passive tendon can be viewed as a spring-damper transmission.

---

# 14. Active Tendon `A`

The second spatial tendon is named:

```text
A
```

Its path is:

```text
hook4
↓
hook5
```

The studied parameters include:

```text
springlength = "0 0.5"
stiffness = 0
damping = 10
width = 0.01
```

Unlike tendon `M`:

```text
stiffness = 0
```

so this tendon is not primarily acting as a passive elastic spring.

Instead, it is actively driven.

---

# 15. Muscle Actuator

The example uses a muscle actuator conceptually equivalent to:

```xml
<muscle
    name="A"
    tendon="A"
    ctrlrange="-15 15"/>
```

The most important attribute is:

```text
tendon="A"
```

This means the muscle actuator acts on the tendon rather than directly on a joint.

The transmission chain becomes:

```text
control input
↓
muscle actuator
↓
spatial tendon A
↓
hook sites
↓
bodies
↓
joint motion
```

---

# 16. Why the Spatial Tendon Can Move the Mechanism

Suppose:

```text
hook4
```

and:

```text
hook5
```

belong to different bodies.

When tension is applied through the tendon:

```text
tendon tension
↓
forces at sites
↓
forces on bodies
↓
joint torque
↓
joint motion
```

This resembles biological actuation:

```text
muscle
↓
tendon
↓
bone
↓
joint
```

---

# 17. Fixed vs Spatial Tendon

The two analysed examples demonstrate the fundamental difference.

## Fixed Tendon

```text
joint coordinates
↓
weighted mathematical combination
↓
virtual motion coordinate
```

Example:

```text
Mecanum forward / transverse / rotate
```

## Spatial Tendon

```text
sites in space
↓
geometric tendon path
↓
length and tension
↓
body forces and joint motion
```

Example:

```text
muscle-driven linked mechanism
```

---

# 18. Main Comparison

| Feature | Fixed Tendon | Spatial Tendon |
|---|---|---|
| Main representation | Joint-coordinate combination | Geometric path |
| Main child element | `joint` | `site` |
| Important parameter | `coef` | routing sites |
| Typical use | transmission / coupling | cable / muscle / tendon |
| Geometry dependent | Mostly no | Yes |
| Example studied | Mecanum robot | muscle-tendon mechanism |

---

# 19. Key Learning Outcome

The most important idea learned from these examples is that an actuator does not always need to control one joint directly.

MuJoCo can represent:

```text
actuator
↓
tendon
↓
multiple joints / bodies
```

This adds a transmission layer between control and mechanical motion.

The three concepts should be separated clearly:

```text
joint
→ defines allowed motion

tendon
→ defines transmission / coupling

actuator
→ provides active drive
```

---

## Source

This analysis is based on tendon examples from:

```text
Albusgive/mujoco_learning
```

Source repository:

https://github.com/Albusgive/mujoco_learning

The original models and teaching materials belong to the respective author(s).

This report records my own learning process and interpretation of the example models. The complete original XML examples were not independently reconstructed or claimed as original work in this repository.