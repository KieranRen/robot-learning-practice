# Actuator Demo Experiment

[English](actuator_demo_report.md) | [中文](actuator_demo_report_zh.md)

---

## 1. Purpose

This experiment was created to reinforce the actuator concepts studied in the Albusgive MuJoCo learning source.

The main goals are to understand:

- how actuators are attached to joints
- how different actuator types interpret `data.ctrl`
- the difference between `position` and `intvelocity`
- the role of `ctrlrange`
- the role of `forcerange`
- the role of `actrange`
- the relationship between actuator control and joint motion

The most important question is:

> How does the meaning of `data.ctrl` change depending on the actuator type?

---

## 2. Model File

The experiment model is stored in:

```text
experiments/M2/MuJoCo/actuator_demo.xml
```

The model contains two movable joints:

```text
pivot
ph
```

and two different actuator types:

```text
pivot
→ position actuator

ph
→ intvelocity actuator
```

---

# Mechanical Structure

## 3. Body Hierarchy

The model structure is:

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

This hierarchy is important because:

```text
support
→ fixed base

rotary_arm
→ child of support

pendulum
→ child of rotary_arm
```

Therefore motion of the parent body affects the child body as well.

---

## 4. Fixed Support

The support body is:

```xml
<body name="support" pos="0 0 0.1">
```

It contains a cylindrical geom.

The support itself has no joint.

Therefore:

```text
support
→ fixed relative to world
```

It acts as the base of the mechanism.

---

## 5. Rotary Arm

Inside `support` is:

```xml
<body name="rotary_arm" pos="0 0 0.51">
```

This body contains the joint:

```xml
<joint
    name="pivot"
    type="hinge"
    axis="0 0 1"/>
```

Therefore:

```text
pivot
→ hinge joint
→ rotates around z axis
```

The horizontal arm is attached to this body.

So when `pivot` rotates:

```text
horizontal arm rotates around z
```

---

## 6. Pendulum

At the end of the horizontal arm is:

```xml
<body name="pendulum" pos="0.2 0 0">
```

This body contains:

```xml
<joint
    name="ph"
    type="hinge"
    axis="1 0 0"/>
```

Therefore:

```text
ph
→ hinge joint
→ rotates around x axis
```

The pendulum rod and end mass belong to this body.

So:

```text
ph motion
→ pendulum swings around x axis
```

---

# Actuator Structure

## 7. Actuator Container

The model uses:

```xml
<actuator>
    ...
</actuator>
```

Inside this block, two actuators are defined.

The important relationship is:

```text
actuator
→ references a joint
→ drives that joint
```

---

# Position Actuator

## 8. Pivot Position Actuator

The first actuator is:

```xml
<position
    name="pivot_position"
    joint="pivot"
    kp="2"
    kv="0.1"
    ctrllimited="true"
    ctrlrange="-3.14 3.14"
    forcelimited="true"
    forcerange="-5 5"/>
```

This actuator controls:

```text
joint="pivot"
```

Therefore its job is to control the horizontal arm rotation.

---

## 9. Meaning of `data.ctrl`

For a position actuator:

```text
data.ctrl
→ target position
```

For this hinge joint:

```text
data.ctrl
→ target angle
```

For example:

```python
data.ctrl[0] = 1.0
```

means approximately:

```text
target pivot angle
=
1.0 rad
```

It does not mean that the joint instantly becomes 1 rad.

---

## 10. Position Control Process

The actuator compares:

```text
target position
and
actual position
```

Approximately:

```text
position error
=
ctrl - qpos
```

The actuator then generates torque to reduce this error.

A simplified interpretation is:

```text
torque
≈
kp × (target - position)
-
kv × velocity
```

The process is:

```text
data.ctrl
↓
target angle
↓
position error
↓
actuator torque
↓
pivot joint accelerates
↓
qvel changes
↓
qpos changes
```

---

## 11. `kp`

The parameter:

```xml
kp="2"
```

controls position feedback strength.

Conceptually:

```text
larger position error
→ larger corrective torque
```

A larger `kp` generally creates:

```text
stronger response
faster position correction
stiffer control
```

---

## 12. `kv`

The parameter:

```xml
kv="0.1"
```

adds velocity-related damping.

It helps reduce:

```text
overshoot
oscillation
excessive motion
```

A useful interpretation is:

```text
kp
→ pulls toward the target

kv
→ reduces excessive movement
```

---

# Control Input Limit

## 13. `ctrlrange`

The actuator uses:

```xml
ctrllimited="true"
ctrlrange="-3.14 3.14"
```

This means the allowed control input is limited to:

```text
[-3.14, 3.14]
```

For this position-controlled hinge:

```text
ctrlrange
→ allowed target-angle range
```

approximately corresponding to:

```text
-π to +π rad
```

---

## 14. `ctrlrange` vs Joint Range

`ctrlrange` does not directly mean:

```text
physical joint motion limit
```

It means:

```text
actuator input limit
```

The distinction is:

```text
joint range
→ how far the joint is physically allowed to move

ctrlrange
→ what target values the actuator is allowed to receive
```

These can be related, but they are conceptually different.

---

# Output Force Limit

## 15. `forcerange`

The actuator also uses:

```xml
forcelimited="true"
forcerange="-5 5"
```

This limits the actuator output.

For a hinge joint, the output is interpreted mainly as torque.

Therefore:

```text
forcerange = [-5, 5]
```

means the actuator cannot output more than approximately:

```text
+5 N·m
```

or less than:

```text
-5 N·m
```

---

## 16. Force-Limiting Example

Suppose the position controller calculates:

```text
required torque = +8
```

but:

```text
forcerange = [-5, 5]
```

Then the actual actuator output is limited to:

```text
+5
```

Similarly:

```text
calculated torque = -7
```

becomes:

```text
-5
```

Therefore:

```text
forcerange
→ actuator output saturation
```

---

## 17. Why `forcerange` Matters

Without an output limit, a strong position error combined with a large gain could create a very large actuator torque.

Using `forcerange` makes the actuator more realistic and prevents unlimited control effort.

This is especially useful when simulating:

```text
real motors
limited actuators
robot joints with torque limits
```

---

# Intvelocity Actuator

## 18. Pendulum Intvelocity Actuator

The second actuator is:

```xml
<intvelocity
    name="ph_intvelocity"
    joint="ph"
    kp="100"
    kv="2"
    actlimited="true"
    actrange="-2 2"/>
```

This controls:

```text
joint="ph"
```

which is the pendulum hinge.

---

## 19. Meaning of `data.ctrl` for Intvelocity

For `intvelocity`:

```text
data.ctrl
```

does not directly represent a target position.

It also does not behave exactly like a normal velocity actuator.

Instead:

```text
ctrl
→ velocity-like command
↓
integration
↓
internal target position
↓
position-like control
```

---

## 20. Integrated Target

Suppose:

```text
ctrl = 0.5 rad/s
```

and this command remains active for:

```text
2 s
```

Then the internal target position changes by approximately:

```text
0.5 × 2
=
1.0 rad
```

The internal target develops approximately as:

```text
0 s
→ 0 rad

1 s
→ 0.5 rad

2 s
→ 1.0 rad
```

So the actuator is effectively moving an internal position target.

---

## 21. Why It Is Called `intvelocity`

The name can be understood as:

```text
integrated velocity
```

because the velocity command is integrated over time.

The conceptual relationship is:

```text
position change
=
velocity × time
```

Therefore:

```text
velocity-like input
↓
integration
↓
position target
```

---

# Activation Limit

## 22. `actrange`

The intvelocity actuator uses:

```xml
actlimited="true"
actrange="-2 2"
```

This limits its internal activation state.

For this actuator, that internal state is closely related to the integrated position target.

---

## 23. Why `actrange` Is Needed

If:

```text
ctrl = 1
```

continues for a long time, the internal target would keep increasing:

```text
1 s
→ +1

2 s
→ +2

3 s
→ +3

4 s
→ +4
```

and so on.

That is usually undesirable.

Therefore:

```text
actrange="-2 2"
```

prevents the internal target from growing indefinitely.

The internal state is limited to approximately:

```text
[-2, 2]
```

---

## 24. `ctrlrange`, `forcerange`, and `actrange`

These three parameters limit different things.

```text
ctrlrange
→ input command

forcerange
→ final actuator output force / torque

actrange
→ internal actuator activation state
```

This distinction is very important.

They operate at different stages of the actuator.

---

# Position vs Intvelocity

## 25. Position Actuator

The position actuator receives:

```text
desired position
```

For example:

```text
ctrl = 1.0
```

means:

```text
go to 1.0 rad
```

---

## 26. Intvelocity Actuator

The intvelocity actuator receives:

```text
velocity-like command
```

For example:

```text
ctrl = 0.5
```

means approximately:

```text
move the internal target at 0.5 rad/s
```

The actuator then tracks the integrated target position.

---

## 27. Core Difference

The simplest comparison is:

```text
position
→ “go to this position”

intvelocity
→ “move the internal position target at this speed”
```

This is the main conceptual purpose of the experiment.

---

# Relation to Normal Velocity Actuator

## 28. Velocity Actuator

A normal velocity actuator behaves approximately as:

```text
ctrl
→ target velocity

qvel
→ actual velocity
```

The controller tries to reduce:

```text
ctrl - qvel
```

---

## 29. Velocity vs Intvelocity

The difference is:

```text
velocity
→ directly tracks velocity

intvelocity
→ integrates velocity command first
→ then tracks an internal position target
```

Therefore:

```text
velocity
→ speed control

intvelocity
→ moving-position-target control
```

---

# Relationship with Python Control

## 30. Control Array

In Python, MuJoCo actuator commands are usually written through:

```python
data.ctrl
```

Since this model has two actuators:

```text
data.ctrl[0]
→ pivot_position

data.ctrl[1]
→ ph_intvelocity
```

The exact ordering depends on actuator declaration order.

---

## 31. Example Interpretation

For example:

```python
data.ctrl[0] = 1.0
data.ctrl[1] = 0.5
```

can be interpreted as:

```text
pivot_position
→ move pivot toward 1.0 rad

ph_intvelocity
→ move the internal ph target at approximately 0.5 rad/s
```

The same `data.ctrl` array therefore contains commands with different physical meanings.

---

## 32. Important Lesson About `data.ctrl`

This experiment reinforces an important point:

> `data.ctrl` does not have one universal physical meaning.

Its meaning depends on the actuator type.

For example:

```text
motor
→ force / torque-like command

position
→ position target

velocity
→ velocity target

intvelocity
→ integrated velocity command
```

This is essential when reading or writing MuJoCo control code.

---

# Mechanical Response

## 33. Why `ctrl` and Motion Are Not Identical

Even with a position actuator:

```text
ctrl = 1 rad
```

does not mean:

```text
qpos instantly becomes 1 rad
```

The actuator must generate torque, and the joint must physically move.

The result depends on:

- inertia
- gravity
- damping
- friction
- actuator gain
- force limits
- simulation timestep

So MuJoCo remains a physics simulation rather than directly assigning joint positions.

---

## 34. Target vs Actual State

The general relationship is:

```text
target
↓
controller
↓
force / torque
↓
physics
↓
actual state
```

Therefore:

```text
target state
≠
actual state at every instant
```

This is the same idea previously observed in the Robot Knowledge Study arm-control example.

---

# Model Independence

## 35. Removed External Dependencies

The original learning example contained external or unused asset-related elements that could prevent the model from loading when files were missing.

For this experiment:

```text
external skybox dependency
→ removed

unused mesh-related default
→ removed
```

The model instead uses:

```xml
builtin="checker"
```

for the floor texture.

This makes the model easier to reproduce.

---

## 36. Why the Simplified Model Is Useful

The experiment focuses only on the parts needed for actuator learning:

```text
body hierarchy
joint
geom
position actuator
intvelocity actuator
actuator limits
```

Removing unrelated model components makes the control structure easier to inspect.

---

# Main Results

## 37. Main Learning Result

The most important result is that actuator type determines how control input is interpreted.

For the two joints:

```text
pivot
→ position actuator
→ ctrl = target angle

ph
→ intvelocity actuator
→ ctrl = velocity-like input
→ integrated into target position
```

Therefore two actuator commands in the same `data.ctrl` array can represent different physical quantities.

---

## 38. Limit Parameters

The experiment also reinforces:

```text
ctrlrange
→ limits command input

forcerange
→ limits actuator output

actrange
→ limits internal actuator state
```

These should not be confused with each other.

---

## 39. Actuator-Control Chain

The general control chain is:

```text
Python
↓
data.ctrl
↓
actuator
↓
joint
↓
force / torque
↓
body motion
↓
qpos / qvel
```

The exact internal actuator step depends on actuator type.

---

## 40. What I Learned

The key mental model from this experiment is:

```text
joint
→ defines how movement is allowed

actuator
→ defines how that movement is driven
```

For actuator types:

```text
motor
→ push with this effort

position
→ go to this position

velocity
→ move at this velocity

intvelocity
→ move the internal target at this velocity
```

For limits:

```text
ctrlrange
→ input limit

forcerange
→ output limit

actrange
→ internal-state limit
```

This provides a clearer foundation for later robot control experiments.

---

## Source

This experiment is based on actuator concepts studied from:

```text
Albusgive/mujoco_learning
```

Source repository:

https://github.com/Albusgive/mujoco_learning

The model was simplified and reorganized as part of my own learning process to focus specifically on actuator behavior and actuator limits.

This report records my own interpretation and understanding of the example rather than reproducing the original source material.