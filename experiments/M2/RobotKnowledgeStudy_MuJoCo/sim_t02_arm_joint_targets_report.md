# SIM-T02 Experiment Report - Arm Joint Targets

[English](sim_t02_arm_joint_targets_report.md) | [中文](sim_t02_arm_joint_targets_report_zh.md)

---

## Experiment Goal

This experiment reproduces the second MuJoCo simulation scene from the `Robot_knowledge_study` M2 material.

The main purpose is to verify that I can:

- load a multi-body robot model
- understand parent-child body hierarchy
- understand robot joint definitions
- use position actuators
- write target joint angles from Python
- advance the simulation with `mj_step`
- observe actual joint position and velocity
- read end-effector position and orientation
- compare target joint angles with actual joint states
- visualize the controlled motion in MuJoCo Viewer

---

## Scene Composition

The T02 scene combines:

```text
SIM-T01 table-and-cube scene
+
robot.xml
```

The T02 `scene.xml` includes:

```xml
<include file="../sim_t01_table_cube/scene.xml"/>
<include file="robot.xml"/>
```

Therefore the full scene contains:

- floor
- table
- cube
- lighting
- cameras
- robot body
- left arm
- right arm
- actuators
- sensors
- collision settings

The timestep is:

```text
0.001 s
```

---

## Robot Structure

The robot uses a hierarchical body structure.

A simplified representation is:

```text
openarm_body
├── robot body / base
├── left arm
│   ├── link0
│   ├── link1
│   ├── link2
│   ├── ...
│   ├── link7
│   └── gripper
└── right arm
    ├── link0
    ├── link1
    ├── ...
    ├── link7
    └── gripper
```

The body hierarchy follows the physical structure of a serial robot arm.

A child body moves with its parent body while also having its own relative motion if a joint is defined.

---

## Default Classes

The model uses `<default>` blocks to define reusable settings.

These templates are used for:

- joint damping
- friction loss
- armature
- collision settings
- visual settings
- actuator gains
- actuator limits

This reduces repeated XML code.

The basic relationship is:

```text
default
→ reusable parameter template

class
→ selects a template

joint / geom / actuator
→ actual object using the template
```

---

## Mesh Assets

The `<asset>` section defines reusable mesh resources.

For example:

```xml
<mesh name="body.obj"
      file="visual/body/openarm_body.obj"/>
```

The mesh becomes visible only when a geom uses it.

For example:

```xml
<geom type="mesh"
      mesh="body.obj"
      class="visual"/>
```

The robot uses separate mesh resources for:

```text
visual geometry
collision geometry
```

This allows the displayed model and the physical collision model to be different.

---

## Multiple Geoms Inside One Body

A single robot body can contain multiple geoms.

This does not create multiple rigid bodies.

Instead:

```text
one body
+
multiple geoms
```

can represent:

- collision geometry
- visual geometry
- several visual mesh parts

All geoms belonging to one body move together as one rigid body.

---

## Left Arm Joints

The active arm contains seven joints:

```text
openarm_left_joint1
openarm_left_joint2
openarm_left_joint3
openarm_left_joint4
openarm_left_joint5
openarm_left_joint6
openarm_left_joint7
```

The joint definitions include properties such as:

- rotation axis
- allowed range
- damping
- friction loss
- armature

The model uses radians for joint angles.

---

## Position Actuators

The left arm also contains seven position actuators.

For example:

```xml
<position name="left_joint1_pos"
          joint="openarm_left_joint1"
          .../>
```

The control relationship is:

```text
Python target
↓
data.ctrl
↓
position actuator
↓
corresponding joint
```

The actuator attempts to move the joint toward the requested target angle.

---

## Target and Actual State

One of the most important concepts in this experiment is the difference between:

```text
target
and
actual state
```

The Python control input:

```python
data.ctrl
```

represents the desired actuator target.

The actual joint position is stored in:

```text
qpos
```

Therefore:

```text
ctrl
= where I want the joint to go

qpos
= where the joint actually is
```

They may differ while the robot is moving.

---

## Sensors

The model defines several sensors.

### Joint Position

```text
jointpos
```

measures the current joint angle.

### Joint Velocity

```text
jointvel
```

measures the current joint angular velocity.

### End-Effector Position

```text
framepos
```

measures the world position of:

```text
left_tool
```

and returns:

```text
(x, y, z)
```

### End-Effector Orientation

```text
framequat
```

measures the orientation of `left_tool`.

The orientation is represented as:

```text
(w, x, y, z)
```

---

## End-Effector Site

The robot contains a site named:

```text
left_tool
```

This site is used as a reference frame near the end of the left gripper.

It does not create a new rigid body.

Instead, it provides a convenient location for measuring:

- end-effector position
- end-effector orientation

---

## Contact Exclusion

The model uses:

```xml
<exclude body1="..." body2="..."/>
```

to disable collision checking between selected body pairs.

This is useful for adjacent links that are physically connected and may otherwise produce unnecessary self-collision calculations.

---

## Python Control Program

The Python program controls the left arm using predefined joint-space waypoints.

The overall control flow is:

```text
load scene
↓
create model
↓
create data
↓
initialize robot
↓
define joint targets
↓
interpolate between targets
↓
write values to data.ctrl
↓
advance simulation
↓
read actual joint state
↓
read end-effector pose
```

---

## Waypoints

The program defines four 7-joint target configurations.

Conceptually:

```text
pose A
↓
pose B
↓
pose C
↓
return to pose A
```

Each waypoint contains one target value for each of the seven left-arm joints.

---

## Timing

The experiment uses:

```text
initial hold = 5.0 s
segment duration = 4.0 s
final hold = 0.5 s
```

The full motion timeline is:

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

Total simulation time:

```text
17.5 s
```

With:

```text
timestep = 0.001 s
```

this corresponds to approximately:

```text
17500 physics steps
```

---

## Initial Joint State

At the start of the experiment, the program directly initializes the joint positions to the first waypoint.

This is an initialization step.

After initialization, the robot is controlled through:

```python
data.ctrl
```

rather than directly overwriting `qpos`.

This preserves physical simulation during motion.

---

## Writing Control Targets

Each target joint angle is written into the corresponding actuator control slot.

Conceptually:

```text
joint target
↓
data.ctrl
↓
position actuator
↓
joint
```

The actuator then drives the joint toward that target.

---

## Linear Interpolation

The target does not jump instantly from one waypoint to another.

The program interpolates smoothly between them.

A simplified expression is:

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

changes gradually from:

```text
0
```

to:

```text
1
```

during each segment.

This produces smooth target motion.

---

## Physics Simulation

The simulation advances using:

```python
mujoco.mj_step(model, data)
```

Each step represents:

```text
0.001 s
```

of simulated time.

During each step:

```text
actuator receives target
↓
control effort is generated
↓
joint velocity changes
↓
joint position changes
```

---

## Sensor Reading

The program periodically reads:

```text
joint angles
joint velocities
left_tool position
left_tool orientation
```

The terminal output includes:

```text
q(rad)
dq(rad/s)
tool_xyz(m)
tool_wxyz
```

This provides both joint-space and end-effector information.

---

## Sensor Refresh

Before selected sensor samples are recorded, the program uses:

```python
mujoco.mj_forward(model, data)
```

This refreshes current derived quantities without advancing simulation time.

It helps ensure that the sensor readings correspond to the current state.

---

## Key Time Checks

Several important times were checked.

### 5.000 s

The robot is still at the initial waypoint.

### 9.000 s

The first transition has completed.

The actual joint configuration is very close to the second target waypoint.

### 13.000 s

The second transition has completed.

The actual joint configuration is very close to the third waypoint.

### 17.000 s

The arm has returned to the final waypoint, which matches the initial pose.

### 17.500 s

The final hold has completed.

Joint velocities are approximately zero.

---

## Joint Velocity During Motion

At intermediate times such as:

```text
7 s
```

the robot is still moving between waypoints.

Therefore:

```text
dq ≠ 0
```

is expected.

This confirms that the robot is actively transitioning between target poses.

---

## Target vs Actual Comparison

The experiment printed both:

```text
target joint configuration
```

and:

```text
actual joint configuration
```

at key times.

The results showed that the position actuators successfully drove the arm very close to the target waypoints.

This verifies the control chain:

```text
target
↓
ctrl
↓
actuator
↓
joint
↓
actual qpos
```

---

## End-Effector Observation

As the joint configuration changes:

```text
joint angles change
↓
robot links move
↓
left_tool position changes
↓
left_tool orientation changes
```

This demonstrates the connection between:

```text
joint-space motion
and
end-effector pose
```

No inverse kinematics is used in this experiment.

The experiment directly commands joint targets and observes the resulting end-effector pose.

---

## Simplified Core Python Control

The essential control logic can be reduced to:

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

This simplified version contains the essential control loop.

---

## Simplified Control Interpretation

The code can be understood as:

```text
load XML
↓
create model
↓
create data
↓
define desired joint angles
↓
write targets to ctrl
↓
position actuators receive targets
↓
mj_step advances the physical system
↓
actual joint positions change
↓
sensors measure the resulting state
```

The key distinction is:

```text
target
≠
instantaneous actual state
```

The target tells the robot where to go.

The physics simulation determines how the robot moves there.

---

## Viewer Check

The controlled motion was also observed in MuJoCo Viewer using:

```bash
python -m examples.mujoco.sim_t02_arm_joint_targets --viewer
```

In this mode:

```text
Python
→ controls the simulation

Viewer
→ displays the current simulation state
```

This made it possible to visually confirm the waypoint transitions.

---

## Viewer Timing

The full Python program also contains additional timing code.

On Windows, a high-resolution timer is used to keep Viewer playback reasonably close to real time.

This timing system is useful for visualization but is not part of the core robot-control logic.

The essential idea is:

```text
physics step
↓
viewer sync
↓
short real-time wait
↓
next physics step
```

---

## Main Learning Outcome

This experiment introduced active robot control in MuJoCo.

The complete control and observation chain is:

```text
WAYPOINTS
↓
interpolation
↓
data.ctrl
↓
position actuators
↓
joint motion
↓
qpos / qvel
↓
sensors
↓
end-effector pose
↓
terminal / Viewer
```

The most important concepts are:

```text
joint
→ defines allowed motion

actuator
→ drives the joint

ctrl
→ desired target

qpos
→ actual position

qvel
→ actual velocity

sensor
→ measures simulation state

site
→ end-effector reference frame

mj_step
→ advances physics
```

---

## Progression from SIM-T01

SIM-T01 focused on passive physical behavior:

```text
gravity
↓
free motion
↓
contact
↓
observation
```

SIM-T02 adds active control:

```text
target
↓
actuator
↓
joint motion
↓
sensor feedback
```

This marks the transition from observing a simulation to actively controlling a robot inside the simulation.

---

## Source

This experiment is based on:

```text
Robot_knowledge_study
M2
SIM-T02
v0.3.0
```

Source repository:

https://github.com/noBug01/Robot_knowledge_study

The original repository and teaching materials belong to their respective author(s).

This report records my own simulation process, code interpretation, observations, verification, and understanding based on the source material.