# 03 - Joint

[English](03_joint.md) | [中文](03_joint_zh.md)

---

## Overview

This note records the MuJoCo concepts related to joints and body motion.

Topics covered:

- What a joint does
- Joint types
- `pos`
- `axis`
- `range`
- `limited`
- `damping`
- `stiffness`
- `frictionloss`
- `armature`
- `ref`
- Relationship between `body`, `joint`, and `geom`

---

## 1. What Is a Joint?

In MuJoCo, a `body` represents a rigid body.

A `joint` determines how that body is allowed to move relative to its parent body.

A useful mental model is:

```text
parent body
↓
joint
↓
current body
↓
geom / site / child body
```

Without a joint, a child body is fixed relative to its parent.

So:

```text
body
→ rigid body

joint
→ defines allowed motion

geom
→ defines physical shape
```

---

## 2. Joint Belongs to the Current Body

Consider:

```xml
<body name="arm" pos="0 0 1">

    <joint name="shoulder"
           type="hinge"
           axis="0 1 0"/>

    <geom type="capsule"
          size="0.1 0.5"/>

</body>
```

The joint is written inside the `arm` body.

This means:

```text
arm
→ moves relative to its parent
→ according to the shoulder joint
```

The joint does not exist as an independent object between two bodies.

Instead, it defines the degrees of freedom of the current body relative to its parent.

---

## 3. Joint Types

Common MuJoCo joint types include:

- `free`
- `ball`
- `slide`
- `hinge`

---

### `hinge`

A hinge joint allows rotation around one axis.

Example:

```xml
<joint type="hinge"
       axis="0 0 1"/>
```

This means:

```text
rotation around the z-axis
```

Typical examples include:

- Robot arm revolute joints
- Wheels
- Door hinges
- Pendulums

A hinge joint has:

```text
1 rotational degree of freedom
```

---

### `slide`

A slide joint allows translation along one axis.

Example:

```xml
<joint type="slide"
       axis="1 0 0"/>
```

This means:

```text
translation along the x-axis
```

Typical examples include:

- Linear rails
- Pistons
- Lifting mechanisms

A slide joint has:

```text
1 translational degree of freedom
```

---

### `ball`

A ball joint allows rotation in three dimensions.

It is similar to a human shoulder joint.

It has:

```text
3 rotational degrees of freedom
```

It does not allow free translation.

---

### `free`

A free joint allows a body to move freely in 3D.

It has:

```text
3 translational DOF
+
3 rotational DOF
=
6 DOF
```

Example:

```xml
<freejoint/>
```

This is useful for objects such as:

- Falling objects
- Free-floating rigid bodies
- Objects not mechanically attached to the world

---

## 4. Joint Position

The `pos` attribute defines the position of the joint in the current body's local coordinate frame.

Example:

```xml
<joint type="hinge"
       pos="0 0 0.5"/>
```

For a hinge joint:

```text
pos
→ defines where the rotation axis passes through
```

This is important because rotation depends not only on the axis direction, but also on the location of the axis.

---

## 5. Joint Axis

The `axis` attribute defines the motion axis.

Examples:

```text
axis="1 0 0"
→ x-axis

axis="0 1 0"
→ y-axis

axis="0 0 1"
→ z-axis
```

For a hinge joint:

```text
axis
→ rotation axis
```

For a slide joint:

```text
axis
→ translation direction
```

Example:

```xml
<joint type="hinge"
       axis="0 1 0"/>
```

means:

```text
rotate around the y-axis
```

Example:

```xml
<joint type="slide"
       axis="0 0 1"/>
```

means:

```text
move along the z-axis
```

---

## 6. Range

The `range` attribute limits joint motion.

Example:

```xml
<joint type="hinge"
       range="-90 90"/>
```

If the model uses:

```xml
<compiler angle="degree"/>
```

this means:

```text
minimum angle = -90°
maximum angle = +90°
```

For a slide joint:

```xml
<joint type="slide"
       range="0 0.5"/>
```

means:

```text
translation is limited between 0 m and 0.5 m
```

---

## 7. Limited

The `limited` attribute determines whether a joint range is enforced.

Example:

```xml
limited="true"
```

means:

```text
joint range is active
```

while:

```xml
limited="false"
```

means:

```text
joint is not limited by range
```

If the model uses:

```xml
<compiler autolimits="true"/>
```

MuJoCo can often infer that a joint is limited when a `range` is defined.

---

## 8. Damping

The `damping` attribute represents viscous resistance to joint motion.

Example:

```xml
damping="0.05"
```

A simple physical interpretation is:

```text
higher velocity
→ larger damping resistance
```

For translational motion, it can be approximately understood as:

```text
F_d = -c v
```

For rotational motion:

```text
τ_d = -c ω
```

So:

```text
larger damping
→ oscillations decay faster

smaller damping
→ motion continues longer
```

This is useful for suppressing unrealistic oscillation.

---

## 9. Stiffness

The `stiffness` attribute introduces spring-like behavior.

Example:

```xml
stiffness="10"
```

A simplified interpretation is:

```text
the joint tends to return toward a reference position
```

This behavior is similar to a spring.

For translation:

```text
F = -k x
```

For rotation:

```text
τ = -k(θ - θ_ref)
```

So:

```text
larger stiffness
→ stronger restoring effect
```

---

## 10. Friction Loss

The `frictionloss` attribute represents internal friction in the joint.

Example:

```xml
frictionloss="0.1"
```

This is different from geom contact friction.

The distinction is:

```text
geom friction
→ friction between contacting surfaces

joint frictionloss
→ resistance inside the joint itself
```

For example, a real robot joint may have friction due to bearings, gears, or mechanical contact.

---

## 11. Armature

The `armature` attribute represents additional effective inertia at the joint.

Example:

```xml
armature="0.01"
```

A useful interpretation is:

```text
armature
→ extra effective inertia seen at the joint
```

This can represent effects such as:

- Motor rotor inertia
- Gearbox reflected inertia

At this stage, the important idea is that larger armature makes the joint behave as if it has more inertia.

---

## 12. Reference Position

The `ref` attribute defines a reference joint position.

Example:

```xml
ref="30"
```

For a hinge joint using degree units, this may represent a 30° reference configuration.

The reference value becomes useful in topics such as:

- Initial configuration
- Joint springs
- Reference posture

---

## 13. Body, Joint, and Geom Relationship

The relationship between the main elements can be summarized as:

```text
body
→ rigid body + local coordinate frame

joint
→ defines how the body moves relative to its parent

geom
→ defines the body's physical shape
```

Example:

```xml
<body name="pendulum" pos="0 0 2">

    <joint name="pivot"
           type="hinge"
           axis="0 1 0"/>

    <geom type="capsule"
          fromto="0 0 0  0 0 -1"
          size="0.08"/>

</body>
```

This means:

```text
pendulum
→ rigid body

pivot
→ allows pendulum to rotate around the y-axis

capsule
→ gives the pendulum its visible and physical rod shape
```

---

## 14. Simple Pendulum Example

A simple pendulum is a useful example for understanding a hinge joint.

```xml
<mujoco model="Simple Pendulum">

    <compiler angle="degree" autolimits="true"/>

    <option timestep="0.002"
            gravity="0 0 -9.81"/>

    <worldbody>

        <geom type="plane"
              size="5 5 0.1"
              rgba="0.8 0.8 0.8 1"/>

        <body name="pendulum"
              pos="0 0 2"
              euler="0 45 0">

            <joint name="pivot"
                   type="hinge"
                   pos="0 0 0"
                   axis="0 1 0"
                   range="-90 90"
                   damping="0.05"/>

            <geom type="capsule"
                  fromto="0 0 0  0 0 -1"
                  size="0.08"
                  mass="1"
                  rgba="0.8 0.2 0.2 1"/>

        </body>

    </worldbody>

</mujoco>
```

Important parts:

```text
type="hinge"
→ the pendulum can rotate around one axis
```

```text
axis="0 1 0"
→ rotation occurs around the y-axis
```

```text
range="-90 90"
→ rotation is limited to ±90°
```

```text
damping="0.05"
→ oscillation gradually decreases
```

```text
euler="0 45 0"
→ gives the pendulum an initial tilted configuration
```

---

## 15. Why the Pendulum Must Start Tilted

If the pendulum starts perfectly vertical:

```text
joint
  ●
  |
  |
  ● center of mass
  ↓ gravity
```

the gravity force line passes through the joint axis.

Therefore:

```text
moment arm ≈ 0
→ torque ≈ 0
→ the pendulum does not start moving
```

If the pendulum starts tilted:

```text
joint
  ●
   \
    \
     ● center of mass
     ↓ gravity
```

gravity creates a moment about the joint.

The basic idea is:

```text
τ = r × F
```

So the pendulum begins to rotate.

This demonstrates an important principle:

```text
having gravity does not automatically cause rotation

rotation requires torque about the joint
```

---

## Key Understanding

The most important joint concepts are:

```text
type
→ what kind of motion is allowed

pos
→ where the joint is located

axis
→ which direction the joint moves or rotates around

range
→ how far the joint is allowed to move

damping
→ resistance proportional to motion

stiffness
→ restoring effect toward a reference position

frictionloss
→ internal joint friction

armature
→ additional effective joint inertia

ref
→ reference joint configuration
```

The core relationship is:

```text
parent body
↓
joint
↓
current body
↓
geom / site / child body
```

---

## Source

This learning section is based on the following upstream repository:

https://github.com/Albusgive/mujoco_learning.git

The original repository and teaching materials belong to their respective author(s).

The notes above are my own summaries, explanations, and understanding based on the learning process.