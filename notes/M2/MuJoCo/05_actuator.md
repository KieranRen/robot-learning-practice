# MuJoCo Actuator

[English](05_actuator.md) | [中文](05_actuator_zh.md)

---

## Overview

This note summarizes the actuator concepts covered in the Albusgive MuJoCo learning source.

The main topics are:

- actuator fundamentals
- relationship between actuator and joint
- `general`
- `motor`
- `position`
- `velocity`
- `intvelocity`
- `damper`
- `cylinder`
- `ctrlrange`
- `forcerange`
- `actrange`
- `gear`
- `kp`
- `kv`
- `timeconst`
- `inheritrange`
- simplified actuator control flow
- a two-joint actuator example

The most important relationship is:

```text
joint
→ defines how a body is allowed to move

actuator
→ defines how that joint is driven
```

From Python:

```text
data.ctrl
↓
actuator
↓
joint
↓
body motion
```

---

## 1. Actuator Container

MuJoCo actuators are defined inside:

```xml
<actuator>
    ...
</actuator>
```

Different actuator types can be placed inside the same actuator container.

Common types include:

```text
general
motor
position
velocity
intvelocity
damper
cylinder
muscle
adhesion
plugin
```

At the current learning stage, the most important ones are:

```text
motor
position
velocity
intvelocity
```

while:

```text
damper
cylinder
```

are useful physical actuator models.

---

## 2. `general` Actuator

`general` is the most flexible low-level actuator form.

Many other actuator types can be understood as convenient presets of `general`.

Important low-level parameters include:

```text
dyntype
→ internal actuator dynamics

gaintype
→ how the control input is amplified

biastype
→ how additional bias terms are generated

dynprm
→ dynamics parameters

gainprm
→ gain parameters

biasprm
→ bias parameters
```

At the current stage, it is not necessary to memorize the exact internal parameter arrays.

The important idea is:

```text
general
→ flexible low-level actuator

motor / position / velocity / ...
→ easier predefined actuator configurations
```

---

## 3. Actuator Target

An actuator must know what object it acts on.

Common targets include:

```text
joint
tendon
site
```

For example:

```xml
<position joint="joint1"/>
```

means:

```text
this actuator controls joint1
```

In most of the current examples, actuators are attached directly to joints.

---

## 4. `ctrlrange`

`ctrlrange` defines the allowed range of actuator control input.

Example:

```xml
<position
    joint="joint1"
    ctrllimited="true"
    ctrlrange="-1 1"/>
```

This means:

```text
data.ctrl
```

should remain within:

```text
[-1, 1]
```

The important distinction is:

```text
joint range
→ physical joint motion range

ctrlrange
→ allowed actuator input range
```

They are not the same parameter.

---

## 5. `forcerange`

`forcerange` limits the final force or torque that the actuator can apply.

Example:

```xml
<position
    joint="pivot"
    forcerange="-5 5"/>
```

For a hinge joint, this can be interpreted as limiting the actuator torque to approximately:

```text
[-5, 5] N·m
```

For example:

```text
calculated torque = +8
forcerange = [-5, 5]

actual actuator output
→ +5
```

Similarly:

```text
calculated torque = -7

actual actuator output
→ -5
```

Therefore:

```text
ctrlrange
→ limits actuator command

forcerange
→ limits final actuator force / torque
```

---

## 6. `actrange`

Some actuators contain an internal activation state.

`actrange` limits this internal state.

This is especially useful for actuator types that include:

```text
integration
filtering
activation dynamics
```

For example, `intvelocity` may integrate velocity commands into an internal target position.

Without an activation limit, the internal target could continue growing indefinitely.

---

## 7. `gear`

`gear` defines how actuator output is mapped to the target object.

For a simple joint actuator, it can be approximately understood as a scaling factor between actuator output and joint force or torque.

Conceptually:

```text
actuator output
× gear
↓
joint force / torque
```

A larger gear value can produce a stronger mechanical effect for the same actuator output.

However, `gear` can represent more general multi-dimensional transmission mappings, so its exact interpretation depends on the actuator configuration.

---

# Motor Actuator

## 8. `motor`

A motor actuator directly provides force or torque.

For a hinge joint:

```text
motor
→ torque control
```

For a translational joint:

```text
motor
→ force control
```

Example:

```xml
<motor
    name="Torque"
    joint="joint"/>
```

If Python writes:

```python
data.ctrl[0] = 0.5
```

this does not mean:

```text
target angle = 0.5 rad
```

Instead, the control input is mapped into actuator force or torque.

---

## 9. Motor vs Position

This distinction is fundamental.

### Motor

```text
control input
→ how strongly to push
```

### Position

```text
control input
→ where the joint should go
```

For example:

```text
motor ctrl = 1
→ apply positive driving effort

position ctrl = 1
→ try to move the joint toward 1 rad
```

With a motor actuator, the final joint position depends on:

- mass
- inertia
- gravity
- damping
- friction
- gear
- duration of the input

The motor itself does not automatically choose a target position.

---

## 10. Motor as a General Actuator Preset

A motor actuator can be understood as a simplified `general` actuator configuration.

Its behavior is approximately characterized by:

```text
dyntype = none
gaintype = fixed
biastype = none
```

This means:

```text
no additional activation dynamics
fixed input gain
no additional bias term
```

The control chain is approximately:

```text
data.ctrl
↓
fixed gain
↓
gear mapping
↓
joint force / torque
```

---

# Position Actuator

## 11. `position`

A position actuator controls a desired joint position.

Example:

```xml
<position
    joint="joint"
    name="pos"
    kp="2"
    kv="0.1"/>
```

If:

```python
data.ctrl[0] = 1.0
```

for a hinge joint, this means:

```text
desired joint angle
=
1.0 rad
```

The joint does not instantly become 1.0 rad.

Instead, the actuator generates force or torque to reduce the position error.

---

## 12. Position Error

The main position error is:

```text
target position
-
actual position
```

Approximately:

```text
error
=
ctrl - qpos
```

The position actuator uses this error to generate a control effort.

A simplified interpretation is:

```text
force / torque
≈
kp × (target - position)
-
kv × velocity
```

---

## 13. `kp`

`kp` is the position feedback gain.

Conceptually:

```text
larger position error
↓
larger control effort
```

A larger `kp` usually means:

```text
stronger correction
faster response
stiffer position control
```

A smaller `kp` usually means:

```text
softer response
slower convergence
```

If `kp` is too large, the system may exhibit:

```text
overshoot
oscillation
numerical instability
```

---

## 14. `kv` in Position Control

`kv` adds velocity-related damping.

It resists rapid motion and helps reduce oscillation.

Conceptually:

```text
kp
→ pulls the joint toward the target

kv
→ reduces excessive motion and oscillation
```

A useful physical analogy is:

```text
position actuator
≈
spring + damper
```

---

## 15. Why `ctrl` and `qpos` Are Different

For a position actuator:

```text
data.ctrl
→ desired position

qpos
→ actual position
```

The control process is:

```text
ctrl target
↓
position error
↓
actuator torque
↓
joint acceleration
↓
qvel changes
↓
qpos changes
```

Therefore:

```text
ctrl
≠
qpos at every instant
```

This explains the target-vs-actual behavior observed in previous robot-arm simulations.

---

## 16. `timeconst`

A position actuator may use a time constant to smooth actuator dynamics.

Conceptually:

```text
timeconst = 0
→ target changes immediately

timeconst > 0
→ actuator target changes more gradually
```

For example:

```text
control target:
0 → 1
```

may internally become:

```text
0
→ 0.2
→ 0.5
→ 0.75
→ 0.9
→ 1
```

instead of changing instantly.

This provides input smoothing.

---

## 17. `inheritrange`

`inheritrange` can automatically generate an actuator `ctrlrange` from the joint range.

Suppose:

```text
joint range = [-2, 2]
```

Then:

```text
inheritrange = 1
→ ctrlrange = [-2, 2]
```

If:

```text
inheritrange = 0.5
```

the control range becomes narrower:

```text
[-1, 1]
```

If:

```text
inheritrange = 1.5
```

the control range becomes wider:

```text
[-3, 3]
```

Conceptually:

```text
< 1
→ stricter / narrower control range

= 1
→ same as joint range

> 1
→ wider control range
```

The range remains centered around the midpoint of the joint range.

---

# Velocity Actuator

## 18. `velocity`

A velocity actuator controls a desired joint velocity.

Example:

```xml
<velocity
    joint="joint1"
    kv="5"/>
```

If Python writes:

```python
data.ctrl[0] = 1.0
```

for a hinge joint, this means approximately:

```text
target angular velocity
=
1 rad/s
```

It does not mean:

```text
target angle = 1 rad
```

---

## 19. Velocity Error

The actuator compares:

```text
target velocity
and
actual velocity
```

Approximately:

```text
velocity error
=
ctrl - qvel
```

A simplified control relation is:

```text
force / torque
≈
kv × (target velocity - actual velocity)
```

The actuator therefore accelerates or decelerates the joint so that its actual velocity approaches the requested velocity.

---

## 20. `kv` in Velocity Control

In a velocity actuator:

```text
kv
→ velocity feedback gain
```

A larger value means:

```text
stronger response to velocity error
```

A smaller value means:

```text
softer velocity tracking
```

This differs slightly from the role of `kv` in a position actuator, where it is mainly used as a damping term.

---

# Integrated Velocity Actuator

## 21. `intvelocity`

`intvelocity` accepts a velocity-like command but integrates it into an internal position target.

The main flow is:

```text
velocity command
↓
integration
↓
internal target position
↓
position-like servo
↓
joint motion
```

This is different from a normal velocity actuator.

---

## 22. Integrated Target Example

Suppose:

```text
ctrl = 0.5 rad/s
```

If maintained for:

```text
2 s
```

the internal target position changes by approximately:

```text
0.5 × 2
=
1.0 rad
```

Therefore the target evolves over time:

```text
0 s
→ 0 rad

1 s
→ 0.5 rad

2 s
→ 1.0 rad

3 s
→ 1.5 rad
```

The joint then follows this moving internal position target.

---

## 23. `dyntype="integrator"`

The key internal mechanism of `intvelocity` is integration.

Conceptually:

```text
internal target rate
=
ctrl
```

Therefore:

```text
ctrl > 0
→ internal target increases

ctrl = 0
→ internal target remains constant

ctrl < 0
→ internal target decreases
```

This explains why the actuator needs an activation state.

---

## 24. Why `actrange` Is Important for `intvelocity`

Because the internal target is integrated over time, it could grow indefinitely.

For example:

```text
ctrl = 1
```

for a long time would continuously increase the internal target.

Therefore:

```xml
actrange="-2 2"
```

can limit the internal activation / integrated target.

This prevents uncontrolled accumulation.

---

## 25. Velocity vs Intvelocity

The distinction is:

```text
velocity
→ directly tracks a target velocity

intvelocity
→ integrates the velocity command into an internal position target
→ then tracks that position target
```

A useful summary is:

```text
velocity
→ “move at this speed”

intvelocity
→ “move the internal target at this speed”
```

---

# Damper Actuator

## 26. `damper`

A damper actuator produces a force opposite to motion.

A simplified relation is:

```text
F
=
-kv × velocity × control
```

Therefore:

```text
higher velocity
→ larger opposing force
```

The negative sign means that the actuator resists the direction of motion.

---

## 27. Damper Example

Suppose:

```text
velocity = +2
kv = 3
ctrl = 0.5
```

Then approximately:

```text
F
=
-3 × 2 × 0.5
=
-3
```

The force opposes the positive motion.

If:

```text
velocity = -2
```

then:

```text
F
=
-3 × (-2) × 0.5
=
+3
```

Again, the force opposes the motion.

---

## 28. Damper vs Joint Damping

A joint can already contain:

```xml
damping="..."
```

However:

```text
joint damping
→ fixed property of the joint

damper actuator
→ damping strength can be controlled through ctrl
```

Therefore a damper actuator behaves like a controllable damping device.

---

## 29. Integrator Choice for Strong Damping

Strong velocity-dependent damping can make simulation numerically difficult.

For this reason, actuator examples may use:

```text
implicit
implicitfast
```

integrators.

At the current stage, the main idea is:

```text
strong damping
→ implicit integration is often more stable
```

---

# Cylinder Actuator

## 30. `cylinder`

A cylinder actuator is designed to model a pneumatic or hydraulic cylinder.

The physical idea is:

```text
pressure
×
piston area
↓
linear force
```

Therefore important parameters include:

```text
area
diameter
timeconst
bias
```

---

## 31. `area`

`area` represents effective piston area.

A larger area means:

```text
same input
→ larger generated force
```

Conceptually:

```text
Force
≈
Pressure × Area
```

---

## 32. `diameter`

Instead of specifying area directly, the piston diameter can be given.

The area can then be obtained approximately from:

```text
A = πd² / 4
```

Therefore:

```text
area
→ specify piston area directly

diameter
→ specify piston diameter and derive area
```

---

## 33. `timeconst` in Cylinder Dynamics

Real pneumatic or hydraulic systems do not respond instantly.

`timeconst` introduces a response delay or filtering effect.

Conceptually:

```text
small timeconst
→ faster response

large timeconst
→ slower response
```

A sudden input may therefore result in a gradual actuator response.

---

## 34. Mixed Actuator Types

Different actuator types can coexist inside the same `<actuator>` block.

For example:

```xml
<actuator>
    <position
        joint="rfd"
        name="rfdp"
        kp="2"
        kv="0.1"/>

    <motor
        joint="rfa"
        name="rfav"/>
</actuator>
```

This means:

```text
joint rfd
→ controlled by a position actuator

joint rfa
→ controlled by a motor actuator
```

The actuator container can therefore mix different control strategies for different joints.

---

# Example - Two-Joint Mechanism

## 35. Mechanism Structure

The actuator example uses a simple mechanism:

```text
world
└── support
    └── rotay_am
        ├── pivot joint
        ├── horizontal arm
        └── pendulum
            ├── ph joint
            ├── pendulum rod
            └── end mass
```

The two movable joints are:

```text
pivot
→ hinge around the z axis

ph
→ hinge around the x axis
```

---

## 36. Pivot Position Actuator

The first actuator is:

```xml
<position
    kp="2"
    kv="0.1"
    name="pivot"
    joint="pivot"
    ctrlrange="-3.14 3.14"
    forcerange="-5 5"/>
```

This controls:

```text
joint="pivot"
```

Therefore:

```text
data.ctrl
→ desired pivot angle
```

The actuator uses:

```text
kp
→ position feedback

kv
→ velocity damping
```

The command is limited to:

```text
[-3.14, 3.14] rad
```

and actuator torque is limited to:

```text
[-5, 5]
```

---

## 37. Pivot Control Chain

The control process is:

```text
desired pivot angle
↓
data.ctrl
↓
position actuator
↓
position error
↓
control torque
↓
pivot hinge
↓
horizontal arm rotates
```

---

## 38. Pendulum Intvelocity Actuator

The second actuator is:

```xml
<intvelocity
    name="ph"
    joint="ph"
    kp="100"
    kv="2"
    actrange="-2 2"/>
```

It controls:

```text
joint="ph"
```

The command is interpreted as a velocity-like input.

The main process is:

```text
ctrl velocity command
↓
integrator
↓
internal target position
↓
position-like control
↓
ph joint
↓
pendulum moves
```

The activation state is limited by:

```text
actrange="-2 2"
```

to prevent unlimited integration.

---

## 39. Two Different Control Strategies in One Model

This example demonstrates two actuator types at the same time:

```text
pivot
→ position actuator
→ directly commands desired angle

ph
→ intvelocity actuator
→ velocity command is integrated into an internal position target
```

This clearly shows that:

```text
same mechanical model
can use different actuator strategies
for different joints
```

---

## 40. Core Comparison

The main actuator types studied can be summarized as:

```text
motor
→ “push with this force / torque”

position
→ “move to this position”

velocity
→ “move at this velocity”

intvelocity
→ “move the internal position target at this velocity”

damper
→ “resist motion with controllable damping”

cylinder
→ “simulate pneumatic / hydraulic linear actuation”
```

---

## 41. Core Understanding

The most important relationship is:

```text
Python
↓
data.ctrl
↓
actuator
↓
joint / tendon / site
↓
physical motion
```

The meaning of `data.ctrl` depends on actuator type.

For example:

```text
motor
→ force / torque command

position
→ position target

velocity
→ velocity target

intvelocity
→ integrated velocity command
```

Therefore `data.ctrl` does not always represent the same physical quantity.

---

## 42. What to Remember

At the current stage, the most important actuator concepts are:

```text
motor
→ direct force / torque control

position
→ target position control

velocity
→ target velocity control

intvelocity
→ integrated velocity command

damper
→ controllable damping

cylinder
→ pneumatic / hydraulic actuator model
```

Important actuator limits:

```text
ctrlrange
→ control input limit

forcerange
→ actuator output force / torque limit

actrange
→ internal activation-state limit
```

Important position-servo parameters:

```text
kp
→ position feedback strength

kv
→ velocity damping
```

---

## Source

This note is based on the actuator section of:

```text
Albusgive/mujoco_learning
```

Source repository:

https://github.com/Albusgive/mujoco_learning

The original repository and teaching materials belong to the respective author(s).

This note records my own learning process, interpretation, example analysis, and understanding based on the source material.