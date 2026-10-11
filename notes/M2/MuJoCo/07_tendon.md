# MuJoCo Tendon

[English](07_tendon.md) | [中文](07_tendon_zh.md)

---

## Overview

This note summarizes the tendon concepts studied from the Albusgive MuJoCo learning source.

The main topics are:

- tendon fundamentals
- `spatial` tendon
- `fixed` tendon
- site-based tendon paths
- joint combinations
- `coef`
- `range`
- `frictionloss`
- `springlength`
- `stiffness`
- `damping`
- tendon visualization
- tendon-driven actuators
- Mecanum wheel fixed-tendon example
- spatial tendon and muscle example

The most important idea is:

```text
joint
→ defines how one body can move

tendon
→ creates a transmission / coupling relationship

actuator
→ provides active driving force
```

An actuator can therefore act directly on a joint:

```text
actuator
↓
joint
↓
body motion
```

or through a tendon:

```text
actuator
↓
tendon
↓
joint(s) / body structure
↓
motion
```

---

# 1. What Is a Tendon?

A tendon in MuJoCo can be used to connect or combine motion across multiple parts of a model.

It can represent concepts similar to:

- ropes
- cables
- belts
- biological tendons
- coupled joint transmissions

Instead of controlling every joint independently, a tendon can define a combined transmission relationship.

For example:

```text
one actuator
↓
one tendon
↓
multiple joints
```

This is useful when several joints or bodies should behave as part of one coordinated mechanism.

---

# 2. Two Main Tendon Types

MuJoCo provides two main tendon types:

```text
spatial
fixed
```

They represent very different ideas.

```text
spatial
→ geometric tendon path through space

fixed
→ mathematical combination of joint coordinates
```

A useful memory aid is:

```text
spatial
→ follows sites

fixed
→ combines joints
```

---

# Part I - Spatial Tendon

## 3. Spatial Tendon

A `spatial` tendon behaves like a rope or cable passing through a sequence of points in space.

The path is usually defined using `site` elements.

Example:

```xml
<tendon>
    <spatial name="T">
        <site site="s1"/>
        <site site="s2"/>
        <site site="s3"/>
    </spatial>
</tendon>
```

This defines a tendon path:

```text
s1
↓
s2
↓
s3
```

The tendon geometry changes when those sites move.

---

# 4. Why Sites Are Important

A site can act as a tendon attachment point or guide point.

For example:

```xml
<site name="hook1"/>
<site name="hook2"/>
<site name="hook3"/>
```

Then:

```xml
<spatial name="T">
    <site site="hook1"/>
    <site site="hook2"/>
    <site site="hook3"/>
</spatial>
```

means:

```text
the tendon passes through hook1
then hook2
then hook3
```

Because the sites belong to bodies, body motion changes site position.

Therefore:

```text
body motion
↓
site positions change
↓
tendon path changes
↓
tendon length changes
↓
tendon force may change
```

This is the core idea of a spatial tendon.

---

# 5. Spatial Tendon as a Physical Cable

A spatial tendon can be understood as a geometric transmission element.

It is especially suitable for:

- cable-driven robots
- tendon-driven mechanisms
- biological muscle-tendon models
- pulley-like routing
- flexible transmission paths

The tendon length is determined from its path through space.

This is fundamentally different from a fixed tendon, which is based on joint coordinates rather than geometric path length.

---

# 6. `range`

A tendon may define:

```xml
range="a b"
```

This defines an allowed tendon-length range.

Conceptually:

```text
joint range
→ allowed joint coordinate range

tendon range
→ allowed tendon length range
```

For example:

```xml
range="0.2 0.5"
```

can be interpreted as:

```text
allowed tendon length
→ 0.2 to 0.5
```

A limit setting is typically required for the range to act as an active constraint.

---

# 7. `frictionloss`

A tendon can define:

```xml
frictionloss="..."
```

This adds resistance to tendon motion.

Conceptually:

```text
tendon length tries to change
↓
frictionloss resists that motion
```

At the current stage, it is sufficient to understand it as tendon-level friction resistance.

---

# 8. `width`

For spatial tendons:

```xml
width="0.003"
```

mainly affects visualization.

Conceptually:

```text
larger width
→ tendon is drawn thicker

smaller width
→ tendon is drawn thinner
```

This should not be interpreted as the physical cross-sectional area of a real cable.

---

# 9. `rgba`

A tendon can also define:

```xml
rgba="1 0 0 1"
```

to control its displayed color.

For example:

```text
1 0 0 1
→ red tendon
```

This is mainly a visualization setting.

---

# 10. `stiffness`

A tendon can behave like a spring.

The parameter:

```xml
stiffness="..."
```

controls how strongly the tendon resists changes away from its spring reference length.

A simplified spring interpretation is:

```text
F ≈ k ΔL
```

where:

```text
k
→ stiffness

ΔL
→ tendon length deviation from reference length
```

Therefore:

```text
large stiffness
→ tendon behaves more rigidly

small stiffness
→ tendon behaves more softly
```

---

# 11. `springlength`

The parameter:

```xml
springlength="..."
```

defines the tendon spring reference length.

Conceptually:

```text
springlength
→ natural / reference tendon length
```

Together:

```text
springlength
→ where the spring is relaxed

stiffness
→ how strongly it resists length deviation
```

---

# 12. `damping`

The parameter:

```xml
damping="..."
```

adds resistance proportional to tendon length-change velocity.

A simplified interpretation is:

```text
damping force
≈
-c × tendon length velocity
```

Therefore:

```text
stiffness
→ resists length displacement

damping
→ resists how quickly the length changes
```

This is similar to a spring-damper system.

---

# 13. Passive Spatial Tendon Example

One studied example used:

```xml
<spatial
    name="M"
    springlength="0 0.5"
    stiffness="1000"
    damping="10"
    width="0.01"
    rgba="1 0 0 1">

    <site site="ceiling"/>
    <site site="hook1"/>
    <site site="hook2"/>
    <site site="hook3"/>

</spatial>
```

The tendon path is:

```text
ceiling
↓
hook1
↓
hook2
↓
hook3
```

This tendon has:

```text
high stiffness
+
damping
```

so it behaves like a passive elastic cable.

It does not require an actuator to produce spring and damping effects.

---

# 14. Active Spatial Tendon Example

A second tendon used:

```xml
<spatial
    name="A"
    springlength="0 0.5"
    stiffness="0"
    damping="10"
    width="0.01"
    rgba="1 0 0 1">

    <site site="hook4"/>
    <site site="hook5"/>

</spatial>
```

The path is:

```text
hook4
↓
hook5
```

This tendon has:

```text
stiffness = 0
```

so it does not act as a strong passive spring.

Instead, it is driven by a muscle actuator.

---

# 15. Muscle Driving a Tendon

The example used:

```xml
<actuator>
    <muscle
        name="A"
        tendon="A"
        ctrlrange="-15 15"/>
</actuator>
```

The important part is:

```xml
tendon="A"
```

The actuator does not directly control a joint.

Instead:

```text
muscle actuator
↓
tendon A
↓
sites
↓
bodies
↓
joint motion
```

This resembles biological actuation:

```text
muscle contraction
↓
tendon tension
↓
bone force
↓
joint rotation
```

---

# 16. Why Pulling a Spatial Tendon Moves Joints

Suppose:

```text
hook4
→ belongs to one body

hook5
→ belongs to another body
```

If tendon A applies tension:

```text
hook4 and hook5
→ are pulled toward each other
```

Because the sites are attached to different bodies:

```text
site force
↓
body force
↓
joint torque
↓
joint rotation
```

This is the basic idea behind tendon-driven robots.

---

# Part II - Fixed Tendon

## 17. Fixed Tendon

A `fixed` tendon is fundamentally different from a spatial tendon.

It does not define a geometric cable path.

Instead, it defines a mathematical combination of joint coordinates.

Example:

```xml
<tendon>
    <fixed name="T">
        <joint joint="joint1" coef="1"/>
        <joint joint="joint2" coef="2"/>
    </fixed>
</tendon>
```

This can be interpreted approximately as:

```text
T
=
1 × q1
+
2 × q2
```

where:

```text
q1
→ joint1 coordinate

q2
→ joint2 coordinate
```

So a fixed tendon behaves like a virtual combined coordinate.

---

# 18. `coef`

The parameter:

```xml
coef="..."
```

defines how strongly each joint contributes to the fixed tendon coordinate.

For example:

```text
coef = 1
→ normal contribution

coef = 2
→ double contribution

coef = -1
→ opposite-direction contribution
```

The sign is particularly important.

Positive and negative coefficients allow different joints to contribute in opposite directions.

---

# 19. Fixed Tendon as a Virtual Motion Axis

A useful mental model is:

> a fixed tendon combines several real joint coordinates into one virtual control coordinate.

For example:

```text
joint1
joint2
joint3
joint4
↓
fixed tendon
↓
virtual motion axis
```

An actuator can then control the tendon instead of controlling each joint independently.

---

# 20. Mecanum Wheel Example

The studied Mecanum example uses four main wheel joints:

```text
a1
b1
a2
b2
```

These are combined into three fixed tendons:

```text
forward
transverse
rotate
```

So:

```text
4 physical wheel joints
↓
3 fixed tendon coordinates
↓
3 intuitive motion commands
```

---

# 21. Forward Tendon

The forward tendon is:

```xml
<fixed name="forward">
    <joint joint="a1" coef="0.25"/>
    <joint joint="b1" coef="0.25"/>
    <joint joint="a2" coef="0.25"/>
    <joint joint="b2" coef="0.25"/>
</fixed>
```

This corresponds to:

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

All coefficients have the same sign.

Therefore the four wheel joints contribute in the same direction.

Conceptually:

```text
+  +
+  +
```

This produces the forward/backward motion combination.

---

# 22. Why `0.25`

There are four wheel joints.

Using:

```text
0.25 × 4 = 1
```

creates a normalized or average-like combination.

The exact value is less important than the relative coefficient pattern.

The most important feature is:

```text
same sign for all four wheels
```

---

# 23. Transverse Tendon

The transverse tendon uses:

```xml
<fixed name="transverse">
    <joint joint="a1" coef="0.25"/>
    <joint joint="b1" coef="-0.25"/>
    <joint joint="a2" coef="-0.25"/>
    <joint joint="b2" coef="0.25"/>
</fixed>
```

This corresponds to:

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
+   -
-   +
```

Because Mecanum rollers are mounted at opposite angles, this wheel-speed combination cancels much of the forward component while reinforcing lateral force.

Therefore:

```text
transverse
→ sideways motion
```

---

# 24. Rotate Tendon

The rotation tendon uses:

```xml
<fixed name="rotate">
    <joint joint="a1" coef="0.25"/>
    <joint joint="b1" coef="0.25"/>
    <joint joint="a2" coef="-0.25"/>
    <joint joint="b2" coef="-0.25"/>
</fixed>
```

This corresponds to:

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
+   +
-   -
```

One wheel group contributes in one direction while the other contributes in the opposite direction.

This generates yaw motion.

Therefore:

```text
rotate
→ vehicle rotation
```

---

# 25. Mecanum Tendon Summary

The three virtual control modes can be summarized as:

| Tendon | a1 | b1 | a2 | b2 | Main Effect |
|---|---:|---:|---:|---:|---|
| `forward` | + | + | + | + | Forward / backward |
| `transverse` | + | - | - | + | Sideways motion |
| `rotate` | + | + | - | - | Rotation |

The exact positive physical direction depends on wheel orientation and joint-axis conventions.

The important idea is the relative sign pattern.

---

# 26. Actuators Controlling Fixed Tendons

The example then uses:

```xml
<actuator>
    <velocity
        tendon="forward"
        name="forward"
        kv="30"
        ctrlrange="-15 15"/>

    <velocity
        tendon="transverse"
        name="transverse"
        kv="30"
        ctrlrange="-15 15"/>

    <velocity
        tendon="rotate"
        name="rotate"
        kv="30"
        ctrlrange="-15 15"/>
</actuator>
```

Notice:

```xml
tendon="..."
```

rather than:

```xml
joint="..."
```

So the control chain becomes:

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

---

# 27. Why This Is Useful

Without tendons, the controller might need to calculate and command all four wheel joints individually.

With fixed tendons:

```text
four wheel joints
↓
combined into
↓
forward / transverse / rotate
```

The control interface becomes much more intuitive.

Instead of thinking:

```text
a1 = ?
b1 = ?
a2 = ?
b2 = ?
```

the higher-level controller can think:

```text
forward
transverse
rotate
```

This is one of the most useful conceptual roles of fixed tendons.

---

# 28. Spatial vs Fixed Tendon

The two tendon types can be summarized as:

| Feature | Spatial Tendon | Fixed Tendon |
|---|---|---|
| Main idea | Geometric cable path | Joint-coordinate combination |
| Defined using | `site` | `joint` |
| Depends on geometry | Yes | Mainly no |
| Tendon length comes from | Spatial path | Joint coordinates and coefficients |
| Typical use | Cables, tendons, ropes | Joint coupling and transmissions |
| Important parameters | site, stiffness, damping | joint, coef |

A simple memory aid:

```text
spatial
→ real path

fixed
→ mathematical combination
```

---

# 29. Tendon vs Joint vs Actuator

These three should not be confused.

### Joint

```text
defines allowed relative motion
```

For example:

```text
hinge
→ one rotational DOF
```

### Tendon

```text
defines transmission or coupling
```

For example:

```text
spatial
→ cable path

fixed
→ combined joint coordinate
```

### Actuator

```text
provides active drive
```

Therefore:

```text
joint
→ how the mechanism can move

tendon
→ how motion / force is transmitted or coupled

actuator
→ what actively drives the mechanism
```

---

# 30. Core Understanding

The most important tendon relationships are:

```text
spatial tendon
→ site-based geometric path
→ tendon length changes with body geometry
```

```text
fixed tendon
→ weighted joint-coordinate combination
→ coef determines joint contribution
```

```text
actuator
→ can drive a tendon
→ tendon can then affect multiple joints or bodies
```

---

# 31. What to Remember

At the current stage, the most important concepts are:

```text
spatial
→ follows sites in space

fixed
→ combines joint coordinates

coef
→ joint contribution and direction

stiffness
→ spring strength

springlength
→ spring reference length

damping
→ resistance to tendon-length velocity

actuator tendon="..."
→ actuator drives tendon instead of directly driving a joint
```

The two example models reinforce:

```text
Mecanum wheels
→ fixed tendon
→ joint coupling

muscle-driven mechanism
→ spatial tendon
→ geometric cable force transmission
```

---

## Source

This note is based on the tendon section of:

```text
Albusgive/mujoco_learning
```

Source repository:

https://github.com/Albusgive/mujoco_learning

The original repository and teaching materials belong to the respective author(s).

This note records my own learning process, interpretation, example analysis, and understanding based on the source material.