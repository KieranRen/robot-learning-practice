# SIM-T02 - Arm Joint Targets

[English](02_arm_joint_targets.md) | [中文](02_arm_joint_targets_zh.md)

---

## Overview

This scene extends the basic MuJoCo simulation workflow from SIM-T01 by introducing an articulated robot arm with actuators, sensors, target joint angles, and end-effector observation.

The main goals are to understand:

- hierarchical robot bodies in MJCF
- reusable defaults and mesh assets
- multiple geoms inside one body
- joint definitions and limits
- position actuators
- sensors for joint state and end-effector pose
- `data.ctrl` as the control target
- the difference between target joint angles and actual joint angles
- waypoint-based motion
- interpolation between joint targets
- how Python drives the robot and reads feedback
- how Viewer displays the controlled motion

This scene introduces the basic control loop:

```text
target joint angles
↓
data.ctrl
↓
position actuators
↓
joints move
↓
qpos / qvel change
↓
sensors read the resulting state
```

---

## 1. Scene Composition

The T02 scene is built by combining multiple XML files.

The main `scene.xml` includes:

```xml
<include file="../sim_t01_table_cube/scene.xml"/>
<include file="robot.xml"/>
```

This means the final scene combines:

```text
SIM-T01 scene
├── floor
├── table
├── cube
├── lights
└── cameras

+

robot.xml
├── robot body
├── left arm
├── right arm
├── actuators
├── sensors
└── contact settings
```

The T02 scene also changes:

```xml
<option timestep="0.001"/>
```

so the simulation timestep becomes:

```text
0.001 s
```

---

## 2. Robot XML Structure

The robot model contains:

```text
assets
defaults
worldbody
actuators
sensors
contact rules
```

A simplified hierarchy is:

```text
openarm_body
├── robot base / body
├── left arm
│   ├── left link 0
│   ├── left link 1
│   ├── ...
│   ├── left link 7
│   └── left gripper
└── right arm
    ├── right link 0
    ├── right link 1
    ├── ...
    ├── right link 7
    └── right gripper
```

Each robot link is represented using nested bodies.

---

## 3. Parent and Child Bodies

The robot arm uses nested MJCF bodies.

For example:

```text
parent body
└── child body
    └── grandchild body
        └── next body
```

This matches the physical structure of a serial robot arm:

```text
shoulder
↓
upper arm
↓
elbow
↓
forearm
↓
wrist
↓
gripper
```

A child body moves together with its parent body, while its own joint defines additional relative motion.

Therefore:

```text
child world motion
=
parent motion
+
child relative joint motion
```

---

## 4. Multiple Geoms in One Body

A body can contain multiple geoms.

For example:

```xml
<body name="link">
    <geom .../>
    <geom .../>
    <geom .../>
</body>
```

This does not mean there are multiple rigid bodies.

It means:

```text
one body
+
multiple geometric representations
```

Common purposes include:

```text
collision geom
→ used for physical collision calculations

visual geom
→ used for rendering

additional visual geoms
→ used to build a detailed appearance
```

All geoms inside one body move together as one rigid body.

---

## 5. Default Classes

The `<default>` section defines reusable parameter templates.

For example:

```xml
<default class="motor_DM8009">
    <joint .../>
</default>
```

Later, a joint can use:

```xml
<joint class="motor_DM8009" .../>
```

and automatically inherit those settings.

Typical default classes define:

- joint damping
- friction loss
- armature
- joint type
- collision parameters
- visual parameters
- actuator gains and limits

A useful interpretation is:

```text
default
→ parameter template

class
→ selects a template

joint / geom / actuator
→ actual object using the template
```

---

## 6. Mesh Assets

The `<asset>` section defines reusable 3D mesh resources.

For example:

```xml
<mesh name="body.obj"
      file="visual/body/openarm_body.obj"/>
```

This only registers the resource.

It does not yet create geometry in the robot.

A later geom uses it:

```xml
<geom type="mesh"
      mesh="body.obj"
      class="visual"/>
```

The relationship is:

```text
asset mesh
→ resource definition

geom type="mesh"
→ actual use of that resource
```

The model contains separate mesh groups such as:

```text
visual/body
visual/arm
visual/gripper

collision/arm
collision/gripper
```

This allows visual and collision geometry to be different.

---

## 7. Visual Mesh vs Collision Mesh

A robot link may contain both:

```text
visual mesh
→ detailed appearance

collision mesh
→ simplified physical collision geometry
```

This is useful because detailed visual meshes may be expensive or unsuitable for collision calculations.

The robot body may visually contain parts such as:

```text
base
housing
wheels
other structural details
```

even when those parts are not modeled as separate movable bodies.

A visible wheel therefore does not necessarily mean that the model contains an independent wheel joint or wheel body.

---

## 8. Left Arm Joints

The left arm contains seven rotational joints:

```text
openarm_left_joint1
openarm_left_joint2
...
openarm_left_joint7
```

Each joint defines parameters such as:

```text
axis
range
damping
frictionloss
armature
```

The XML compiler uses:

```xml
<compiler angle="radian" .../>
```

so joint ranges and target angles are expressed in radians.

The main concept is:

```text
joint
→ defines allowed relative motion between a body and its parent
```

---

## 9. Right Arm

The right arm uses the same general structure as the left arm:

```text
body
→ joint
→ geom
→ child body
```

The names and some mirrored transforms differ, but the modeling principle is the same.

In this scene, the main active control task focuses on the left arm.

---

## 10. Position Actuators

The model defines seven left-arm position actuators.

For example:

```xml
<position name="left_joint1_pos"
          joint="openarm_left_joint1"
          .../>
```

This actuator is attached to:

```text
openarm_left_joint1
```

The basic relationship is:

```text
Python target
↓
data.ctrl
↓
position actuator
↓
joint motion
```

A position actuator attempts to move the joint toward a target position.

It does not directly force the joint state to become equal to the target instantly.

---

## 11. `range`, `ctrlrange`, `ctrl`, and `qpos`

These four concepts must be distinguished.

### Joint Range

```text
range
```

defines where the physical joint is allowed to move.

### Control Range

```text
ctrlrange
```

defines which target values the actuator may accept.

### Control Input

```python
data.ctrl
```

contains the current actuator targets.

### Actual Joint Position

```python
qpos
```

contains the actual joint state.

Therefore:

```text
data.ctrl
= desired target

qpos
= actual position
```

They are not necessarily identical at every instant.

---

## 12. End-Effector Site

The model defines:

```xml
<site name="left_tool" .../>
```

This site is attached near the left gripper.

A site:

```text
does not create a new rigid body
does not add mass
does not directly create motion
```

Instead, it provides a useful reference frame.

Here it is used as the robot end-effector reference.

---

## 13. Sensors

The model defines several sensor types.

### Joint Position

```xml
<jointpos .../>
```

reads:

```text
current joint angle
```

### Joint Velocity

```xml
<jointvel .../>
```

reads:

```text
current joint angular velocity
```

### End-Effector Position

```xml
<framepos .../>
```

reads:

```text
left_tool position in world coordinates
```

The result is:

```text
(x, y, z)
```

### End-Effector Orientation

```xml
<framequat .../>
```

reads the orientation of `left_tool`.

The result is a quaternion:

```text
(w, x, y, z)
```

---

## 14. Contact Exclusion

The `<contact>` section contains rules such as:

```xml
<exclude body1="..." body2="..."/>
```

These rules tell MuJoCo to ignore collision checking between selected body pairs.

This is useful for adjacent robot links that are physically connected and may otherwise generate unnecessary collision calculations.

The purpose is:

```text
collision filtering
```

rather than creating new contacts.

---

## 15. Python Simulation Structure

The Python program adds active robot control.

The overall workflow is:

```text
load XML
↓
create model
↓
create data
↓
initialize robot
↓
define joint target waypoints
↓
write targets to data.ctrl
↓
advance with mj_step
↓
read joint and sensor states
↓
display or print results
```

---

## 16. Scene Path

The Python program first locates:

```text
simulation/mujoco/scenes/sim_t02_arm_joint_targets/scene.xml
```

This path is used by:

```python
mujoco.MjModel.from_xml_path(...)
```

to load the full scene.

---

## 17. Waypoints

The program defines several 7-joint target configurations:

```python
WAYPOINTS_RAD = (
    (...7 values...),
    (...7 values...),
    (...7 values...),
    (...7 values...),
)
```

Each waypoint represents:

```text
joint1 target
joint2 target
joint3 target
joint4 target
joint5 target
joint6 target
joint7 target
```

The sequence is approximately:

```text
pose A
↓
pose B
↓
pose C
↓
return to pose A
```

---

## 18. Timing

The motion uses:

```text
INITIAL_HOLD_SECONDS = 5.0
SECONDS_PER_SEGMENT = 4.0
FINAL_HOLD_SECONDS = 0.5
```

The motion timeline is:

```text
0–5 s
→ hold pose A

5–9 s
→ move A → B

9–13 s
→ move B → C

13–17 s
→ move C → A

17–17.5 s
→ final hold
```

Total simulated time:

```text
17.5 s
```

Since:

```text
timestep = 0.001 s
```

the simulation uses approximately:

```text
17.5 / 0.001
=
17500 physics steps
```

---

## 19. Joint, Actuator, and Sensor Names

The program automatically generates names such as:

```python
ARM_JOINTS
ARM_ACTUATORS
ANGLE_SENSORS
VELOCITY_SENSORS
```

For example:

```text
openarm_left_joint1
...
openarm_left_joint7
```

and:

```text
left_joint1_pos
...
left_joint7_pos
```

This avoids manually writing all seven names repeatedly.

---

## 20. SensorReading Structure

The program defines:

```python
class SensorReading(NamedTuple):
    ...
```

to package sensor data together.

Each reading contains:

```text
7 joint angles
7 joint velocities
tool position
tool orientation quaternion
```

This makes the sensor data easier to pass between functions.

---

## 21. Reading Sensors

The program reads sensor values using:

```python
data.sensor(name).data
```

It collects:

```text
joint angles
joint angular velocities
left_tool position
left_tool orientation
```

These values are then packaged into a `SensorReading`.

The conceptual relationship is:

```text
XML declares sensors
↓
MuJoCo computes sensor values
↓
Python reads sensor data
```

---

## 22. Initial Joint State

At the beginning of the simulation, the program directly initializes the left arm joint positions.

This is different from normal control.

Directly setting:

```text
qpos
```

is used only to place the robot in the initial configuration.

After initialization, the program controls motion using:

```python
data.ctrl
```

rather than repeatedly overwriting `qpos`.

This distinction is important:

```text
initialization
→ directly place the robot

control
→ command actuators and let physics produce motion
```

---

## 23. Writing Control Targets

The program writes joint targets into:

```python
data.ctrl
```

Each actuator receives one desired joint angle.

Conceptually:

```text
WAYPOINT target
↓
data.ctrl
↓
position actuator
↓
joint
```

The actuator then attempts to reduce the difference between:

```text
desired angle
and
actual angle
```

---

## 24. Target vs Actual Joint Angle

The target value does not instantly become the actual joint angle.

Instead:

```text
target angle
↓
actuator generates control action
↓
joint accelerates
↓
qpos changes over time
```

The actual motion depends on:

- inertia
- mass
- gravity
- damping
- actuator gain
- force limits
- timestep
- other physical interactions

Therefore:

```text
ctrl
≠
qpos at every instant
```

---

## 25. Linear Interpolation

The robot does not suddenly jump from one waypoint to another.

Instead, the program interpolates between them.

Conceptually:

```text
target =
start
+
alpha × (end - start)
```

where:

```text
alpha
```

gradually increases from:

```text
0 → 1
```

over one segment.

This creates smooth target transitions.

For example:

```text
1.30
→ 1.29
→ 1.28
→ ...
→ 1.05
```

rather than:

```text
1.30
→ immediately 1.05
```

---

## 26. Physics Stepping

After updating control targets, the simulation advances using:

```python
mujoco.mj_step(model, data)
```

Each step advances:

```text
0.001 s
```

During the step:

```text
actuators apply control
↓
joint accelerations are computed
↓
joint velocities change
↓
joint positions change
```

---

## 27. Sensor Refresh

Before selected sensor samples are read, the program uses:

```python
mujoco.mj_forward(model, data)
```

This refreshes calculations for the current state without advancing simulation time.

This helps keep sensor values aligned with the current:

```text
qpos
qvel
```

---

## 28. Sensor Sampling

Sensor data is sampled approximately every:

```text
1.0 s
```

This avoids printing values at every:

```text
0.001 s
```

physics step.

The printed output includes:

```text
q(rad)
→ actual joint angles

dq(rad/s)
→ actual joint velocities

tool_xyz(m)
→ end-effector position

tool_wxyz
→ end-effector orientation quaternion
```

---

## 29. Motion Verification

Several key times were checked.

At:

```text
5.000 s
```

the robot is still at the initial waypoint.

At:

```text
9.000 s
```

the first motion segment has finished and the robot has reached the second waypoint.

At:

```text
13.000 s
```

the second motion segment has finished and the robot has reached the third waypoint.

At approximately:

```text
17.000 s
```

the robot has returned to the final waypoint.

At:

```text
17.500 s
```

the final hold has completed and joint velocities are close to zero.

---

## 30. Why Joint Velocity Is Nonzero During Motion

For example, at:

```text
7 s
```

the robot is in the middle of:

```text
5–9 s
```

which is the first waypoint transition.

Therefore:

```text
dq ≠ 0
```

is expected.

A nonzero joint velocity means the joint is actively moving toward its target.

---

## 31. End-Effector Motion

As the seven joint angles change, the end-effector pose also changes.

The program observes:

```text
left_tool position
+
left_tool orientation
```

This demonstrates the relationship:

```text
joint configuration
↓
robot geometry
↓
end-effector pose
```

This scene does not compute inverse kinematics.

Instead, it observes the resulting end-effector pose after directly commanding joint targets.

---

## 32. Viewer

The simulation can be run with:

```bash
python -m examples.mujoco.sim_t02_arm_joint_targets --viewer
```

In this mode:

```text
Python controls the simulation
Viewer displays the current state
```

The program uses:

```python
viewer.sync()
```

to update the visual display.

---

## 33. Viewer Timing

The Python program contains additional timing logic to keep Viewer playback reasonably close to real time.

On Windows, it uses a high-resolution timer through system APIs.

This code is mainly an engineering helper for Viewer playback.

It is not part of the core MuJoCo robot-control logic.

The important conceptual role is simply:

```text
physics runs
↓
Viewer syncs
↓
program waits briefly
↓
visual playback remains understandable
```

---

## 34. Core Python Control Flow

The complete teaching script contains many additional features such as Viewer timing, command-line arguments, output formatting, and platform-specific helper functions.

However, the essential MuJoCo control logic can be reduced to a much smaller program:

```python
import mujoco

model = mujoco.MjModel.from_xml_path("scene.xml")
data = mujoco.MjData(model)

target = [1.0, 0.0, 0.0, 1.2, 0.0, 0.0, -1.0]

for i, value in enumerate(target):
    data.ctrl[i] = value

for _ in range(1000):
    mujoco.mj_step(model, data)

print(data.sensor("left_joint1_angle").data)
print(data.sensor("left_tool_position").data)
```

This simplified example contains the core ideas needed to understand how Python controls a MuJoCo robot.

### Step 1 - Import MuJoCo

```python
import mujoco
```

This imports the MuJoCo Python package so that the program can:

- load an MJCF/XML model
- create simulation state
- advance the simulation
- access joints, actuators, and sensors

---

### Step 2 - Load the XML Model

```python
model = mujoco.MjModel.from_xml_path("scene.xml")
```

This reads the MJCF/XML file and creates a MuJoCo model.

The `model` contains relatively fixed information such as:

```text
bodies
joints
geoms
actuators
sensors
mass
gravity
timestep
joint ranges
actuator settings
```

A useful interpretation is:

```text
model
=
the structure and rules of the simulation
```

---

### Step 3 - Create the Simulation State

```python
data = mujoco.MjData(model)
```

`MjData` stores the current state of this simulation instance.

It contains values that change while the simulation runs, such as:

```text
simulation time
joint positions
joint velocities
control inputs
contacts
sensor values
```

A useful distinction is:

```text
model
→ what the system is

data
→ what the system is doing right now
```

---

### Step 4 - Define a Target Joint Configuration

```python
target = [1.0, 0.0, 0.0, 1.2, 0.0, 0.0, -1.0]
```

The robot arm has seven controlled joints.

Therefore the seven values correspond to:

```text
joint1 → 1.0 rad
joint2 → 0.0 rad
joint3 → 0.0 rad
joint4 → 1.2 rad
joint5 → 0.0 rad
joint6 → 0.0 rad
joint7 → -1.0 rad
```

These values represent desired joint angles.

They are not the current actual joint angles.

---

### Step 5 - Write Targets to the Actuators

```python
for i, value in enumerate(target):
    data.ctrl[i] = value
```

`enumerate(target)` produces pairs such as:

```text
i = 0, value = 1.0
i = 1, value = 0.0
i = 2, value = 0.0
...
i = 6, value = -1.0
```

The program then writes each value into:

```python
data.ctrl[i]
```

Conceptually:

```text
data.ctrl[0]
→ target for actuator 1

data.ctrl[1]
→ target for actuator 2

...

data.ctrl[6]
→ target for actuator 7
```

Because the XML uses position actuators, each control value represents a desired joint position.

The control chain is:

```text
target value
↓
data.ctrl
↓
position actuator
↓
corresponding joint
```

At this point, the robot has received the desired targets, but the joints have not instantly moved to those angles.

---

### Step 6 - Advance the Physics Simulation

```python
for _ in range(1000):
    mujoco.mj_step(model, data)
```

This is the part that actually makes the robot move.

Each call to:

```python
mujoco.mj_step(model, data)
```

advances the simulation by one timestep.

For example, if:

```text
timestep = 0.001 s
```

then:

```text
1000 steps × 0.001 s
=
1.0 s simulated time
```

During each step, MuJoCo computes the physical response of the robot.

Conceptually:

```text
desired joint target
↓
position actuator detects position error
↓
actuator produces control effort
↓
joint accelerates
↓
joint velocity changes
↓
joint position changes
```

This process repeats every timestep.

Therefore the actual joint angle gradually approaches the desired target.

---

### Step 7 - Target and Actual State Are Different

A very important distinction is:

```text
data.ctrl
=
desired actuator target

qpos
=
actual joint position
```

The relationship is not:

```text
ctrl = 1.0
→ joint instantly becomes 1.0
```

Instead:

```text
ctrl = 1.0
↓
actuator drives the joint
↓
physics evolves over many mj_step calls
↓
qpos gradually approaches 1.0
```

The actual motion is affected by:

- robot mass
- inertia
- gravity
- damping
- friction
- actuator gains
- actuator force limits
- timestep

Therefore:

```text
target
and
actual state
```

may differ during motion.

---

### Step 8 - Read the Actual Joint State

```python
print(data.sensor("left_joint1_angle").data)
```

The XML defines a sensor similar to:

```xml
<jointpos
    name="left_joint1_angle"
    joint="openarm_left_joint1"/>
```

Python can access that sensor by name:

```python
data.sensor("left_joint1_angle").data
```

This returns the actual joint angle measured in the current simulation state.

Therefore:

```text
data.ctrl
→ what was requested

sensor joint angle
→ what actually happened
```

---

### Step 9 - Read the End-Effector Position

```python
print(data.sensor("left_tool_position").data)
```

The XML defines a `framepos` sensor attached to the `left_tool` site.

The returned value is approximately:

```text
[x, y, z]
```

representing the end-effector position in world coordinates.

This demonstrates an important robotics relationship:

```text
joint angles change
↓
robot link configuration changes
↓
end-effector position changes
```

---

### Simplified Control Loop

The essential Python-MuJoCo control process is therefore:

```text
load XML
↓
create model
↓
create data
↓
define target joint angles
↓
write targets to data.ctrl
↓
mj_step repeatedly advances physics
↓
actual qpos / qvel change
↓
sensors measure the resulting state
↓
Python reads the feedback
```

A shorter version is:

```text
target
↓
ctrl
↓
actuator
↓
joint
↓
mj_step
↓
actual state
↓
sensor
```

This is the most important Python control flow introduced in SIM-T02.

---

## 35. Main Control Relationship

The complete control and observation chain is:

```text
WAYPOINTS_RAD
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
sensor data
↓
end-effector pose
↓
terminal output / Viewer
```

This is the central concept of SIM-T02.

---

## 36. What Must Be Understood

The most important concepts from this scene are:

```text
joint
→ defines motion

actuator
→ drives the joint

ctrl
→ desired actuator input

qpos
→ actual joint position

qvel
→ actual joint velocity

sensor
→ reads simulation state

site
→ reference frame for end-effector observation

mj_step
→ advances physical simulation

mj_forward
→ refreshes current derived calculations
```

The large Python file also contains command-line handling, formatting, Viewer timing, and platform-specific helper code.

Those parts are useful engineering details but are less important than the core control loop.

---

## 37. Core Understanding

SIM-T02 extends the simulation workflow from passive observation to active control.

The main progression is:

```text
SIM-T01
XML
→ physics
→ observe natural motion

SIM-T02
XML
→ Python control target
→ actuator
→ joint motion
→ sensor feedback
```

The most important distinction is:

```text
target
≠
actual state
```

The control program gives the robot a desired target, while MuJoCo physics determines how the robot actually moves toward that target.

---

## Source

This note is based on the M2 `SIM-T02` material from:

```text
Robot_knowledge_study
v0.3.0
```

Source repository:

https://github.com/noBug01/Robot_knowledge_study

The original repository and teaching materials belong to their respective author(s).

This document records my own learning process, explanations, code interpretation, simulation verification, and understanding based on the source material.