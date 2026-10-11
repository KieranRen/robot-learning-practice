# MuJoCo Sensor Example Analysis

[English](sensor_example_report.md) | [中文](sensor_example_report_zh.md)

## Overview

This report records the analysis of a combined MuJoCo sensor example studied from the Albusgive MuJoCo learning source.

The example demonstrates several sensor types in one model, including:

- camera observation
- IMU-style sensing
- `subtreelinvel`
- `framepos`
- `force`
- `torque`
- `jointpos`
- `jointvel`
- `ballquat`
- `ballangvel`

It also includes:

- a free body
- a fixed support
- a hinge joint
- a ball joint
- a position actuator
- several sensor mounting sites

The purpose of the example is not to represent one complete robot.

Instead, it acts as a compact demonstration of how different MuJoCo sensors can be attached to different model elements.

---

# 1. Overall Model Structure

The example contains several independent demonstration sections.

Conceptually:

```text
world
├── floor
├── external camera
├── free body B
│   ├── freejoint
│   ├── IMU site
│   └── body-mounted camera
│
├── force / torque demo
│   └── up_box
│       └── force_torque site
│
└── joint sensor demo
    └── support
        └── rotay_am
            ├── pivot hinge joint
            ├── horizontal link
            └── pendulum
                ├── ph ball joint
                ├── vertical link
                └── sphere mass
```

The model therefore combines several different sensing situations into one XML file.

---

# 2. Basic Simulation Settings

The example uses standard simulation configuration such as:

```xml
<compiler
    angle="radian"
    meshdir="meshes"
    autolimits="true"/>
```

This means:

```text
angle
→ radians

meshdir
→ default mesh directory

autolimits
→ automatically enables relevant limits when ranges are defined
```

The simulation options include values such as:

```text
timestep = 0.002
gravity = 0 0 -9.81
integrator = implicitfast
```

So:

```text
one simulation step
→ 0.002 s
```

which corresponds to a nominal simulation-step rate of:

```text
500 steps per second
```

---

# 3. Asset Section

The example defines visual assets including:

```text
texture
material
mesh
```

A checker-style texture/material is used for the floor.

A tetrahedron mesh is also defined in the asset section.

In the analysed portion of the example, the important sensor logic does not depend on this mesh.

So its presence is mainly part of the model resource setup rather than the central sensor demonstration.

---

# 4. Floor and Light

The `worldbody` contains a floor geom and a directional light.

Conceptually:

```text
floor
→ physical / visual ground plane

light
→ scene rendering
```

These are not sensors.

They provide the environment in which the sensor examples are displayed.

---

# 5. External Camera `c2`

One camera is defined outside body `B`.

Conceptually equivalent to:

```xml
<camera
    name="c2"
    pos="1 0 1"
    mode="targetbody"
    target="B"
    fovy="54.225"/>
```

Important parameters:

```text
name="c2"
→ camera name

pos
→ camera position

mode="targetbody"
→ camera points toward a target body

target="B"
→ target body is B

fovy
→ vertical field of view
```

So this camera behaves like:

```text
external observer
↓
keeps looking toward body B
```

---

# 6. Free Body `B`

The example contains:

```xml
<body name="B" pos="0 0 0">
    <freejoint/>
    <site name="imu"/>
    ...
</body>
```

The most important element is:

```xml
<freejoint/>
```

This gives body `B` full spatial freedom.

Conceptually:

```text
3 translational DOF
+
3 rotational DOF
=
6 DOF
```

Therefore body `B` can:

```text
move in x / y / z
+
rotate in three dimensions
```

---

# 7. IMU Site

Inside body `B`:

```xml
<site name="imu"/>
```

defines a site used as a sensor reference location.

The site can be understood as:

```text
sensor mounting point
+
sensor coordinate frame
```

This is useful for sensors such as:

```text
framequat
accelerometer
gyro
```

---

# 8. Body-Mounted Camera `c1`

Body `B` also contains a camera.

Conceptually:

```xml
<camera
    name="c1"
    mode="fixed"
    fovy="54.225"
    euler="1.57 0 0"/>
```

Because this camera belongs to body `B` and uses:

```text
mode="fixed"
```

it moves together with body `B`.

So the two cameras demonstrate different observation styles:

```text
c2
→ external camera watching B

c1
→ camera mounted on B
```

---

# 9. IMU-Style Sensors

The example contains IMU-related sensors that may be enabled or disabled using XML comments.

These include:

```xml
<framequat
    name="orientation"
    objtype="site"
    objname="imu"/>

<gyro
    name="base_ang_vel"
    site="imu"/>

<accelerometer
    name="accel"
    site="imu"/>
```

Together they provide:

```text
framequat
→ orientation

gyro
→ angular velocity

accelerometer
→ acceleration
```

So:

```text
IMU-style sensing
≈
orientation
+
angular velocity
+
acceleration
```

---

# 10. `subtreelinvel`

One active sensor in the example is:

```xml
<subtreelinvel
    name="base_lin_vel"
    body="B"/>
```

This measures the linear velocity of the center of mass of the subtree rooted at body `B`.

Conceptually:

```text
body B
+
all descendants of B
↓
combined subtree COM
↓
linear velocity
```

Since body `B` is relatively simple in this demonstration, it can be interpreted approximately as the overall linear velocity of the free body system.

---

# 11. `framepos`

The example also includes a `framepos` sensor that may be commented out:

```xml
<framepos
    name="base_pos"
    objtype="body"
    objname="B"/>
```

This measures the position of body `B`.

Because no reference frame is explicitly specified:

```text
base_pos
→ position of B relative to the world frame
```

Output conceptually contains:

```text
x
y
z
```

---

# 12. Force/Torque Demo Structure

Another part of the model contains a parent body and a child body:

```text
parent body
└── up_box
    ├── force_torque site
    └── box geom
```

Conceptually:

```xml
<body pos="0 0 1">
    <geom type="box" .../>

    <body name="up_box" pos="0 0 .02">
        <site name="force_torque"/>
        <geom type="box" .../>
    </body>
</body>
```

The site:

```text
force_torque
```

is used as the measurement frame for force and torque sensors.

---

# 13. Force Sensor

The example defines:

```xml
<force
    name="force"
    site="force_torque"/>
```

This sensor measures a 3D force vector:

```text
Fx
Fy
Fz
```

Conceptually:

```text
force
→ interaction force measured at the sensor site
```

---

# 14. Torque Sensor

The example also defines:

```xml
<torque
    name="torque"
    site="force_torque"/>
```

This measures:

```text
Tx
Ty
Tz
```

So:

```text
force
+
torque
```

provides:

```text
3 force components
+
3 torque components
=
6-dimensional force/torque information
```

This is conceptually similar to a 6-axis force/torque sensor used in robotics.

---

# 15. Joint Sensor Demonstration Structure

The joint-sensor section has a nested body hierarchy:

```text
world
└── support
    └── rotay_am
        └── pendulum
```

The important point is that each child body position is defined relative to its parent body.

---

# 16. `support` Body

The support body is approximately:

```xml
<body name="support" pos="1 0 0.1">
```

It contains a cylindrical geom.

Because `support` has no joint connecting it to the world:

```text
support
→ fixed to world
```

The cylinder acts as a rigid support structure.

---

# 17. Support Geometry

The support geom uses:

```text
type="cylinder"
```

with approximately:

```text
radius = 0.05
half-length = 0.5
```

Therefore the total cylinder height is approximately:

```text
1.0
```

The geom has a relatively large mass value in the example.

However, because the support body is fixed to the world, the central conceptual point is simply that it provides a stable base.

---

# 18. `rotay_am` Body

Inside `support` is:

```xml
<body name="rotay_am" pos="0 0 0.51">
```

The position:

```text
0 0 0.51
```

is relative to `support`.

This places the rotating arm near the top of the support.

---

# 19. `pivot` Hinge Joint

Inside `rotay_am`:

```xml
<joint
    type="hinge"
    name="pivot"
    pos="0 0 0"
    axis="0 0 1"
    damping="0.001"
    frictionloss="0.0"
    stiffness="0.5"/>
```

Important parameters:

```text
type="hinge"
→ 1 rotational DOF

name="pivot"
→ joint identifier

axis="0 0 1"
→ rotation around z-axis

damping
→ velocity-dependent resistance

frictionloss
→ additional joint friction loss

stiffness
→ elastic restoring behaviour
```

So:

```text
pivot
→ rotates the arm in the xy plane
```

---

# 20. Horizontal Link

The rotating arm contains a capsule geom:

```xml
<geom
    type="capsule"
    fromto="0 0 0 0.2 0 0"
    size="0.01"
    .../>
```

This creates a link extending approximately:

```text
0.2 along +x
```

The `pendulum` body is located at:

```xml
pos="0.2 0 0"
```

which places it at the end of this horizontal link.

---

# 21. `pendulum` Body

The child body:

```xml
<body name="pendulum" pos="0.2 0 0">
```

is attached to `rotay_am`.

Because it is a child body:

```text
rotay_am motion
↓
changes the parent frame of pendulum
```

Then the pendulum can also move relative to its parent through its own joint.

---

# 22. `ph` Ball Joint

Inside the pendulum:

```xml
<joint
    type="ball"
    name="ph"
    pos="0 0 0"
    damping="0.001"
    frictionloss="0.0"/>
```

A ball joint has:

```text
3 rotational DOF
```

Unlike a hinge joint, it does not need a single `axis` parameter.

Conceptually:

```text
hinge
→ rotation around one axis

ball
→ general 3D rotation
```

---

# 23. Ball Joint State

For a ball joint:

```text
position state
→ quaternion
→ 4 values

velocity state
→ angular velocity
→ 3 values
```

Therefore MuJoCo provides dedicated sensors:

```text
ballquat
ballangvel
```

---

# 24. Pendulum Link

The pendulum contains a vertical capsule:

```xml
<geom
    type="capsule"
    fromto="0 0 0 0 0 -0.3"
    size="0.01"
    .../>
```

This means the link extends:

```text
0.3 along -z
```

from the ball-joint location.

---

# 25. Pendulum End Mass

The same body also contains a sphere:

```xml
<geom
    type="sphere"
    pos="0 0 -0.3"
    size="0.03"
    .../>
```

The sphere is located at the lower end of the pendulum link.

Conceptually:

```text
ball joint
↓
vertical link
↓
sphere end mass
```

---

# 26. Multiple Geoms in One Body

The pendulum body contains:

```text
capsule
+
sphere
```

These are not two independent bodies.

They are two geoms attached to the same body.

Therefore:

```text
capsule
+
sphere
↓
move as one rigid body
```

This reinforces an important MuJoCo concept:

```text
body
→ rigid-body object

geom
→ shape attached to the body
```

---

# 27. Parent-Child Motion

The hierarchy is:

```text
support
↓
rotay_am
↓
pendulum
```

If `pivot` rotates:

```text
rotay_am rotates
↓
pendulum parent frame moves with it
```

Then the ball joint `ph` can create additional relative rotation.

Therefore:

```text
child motion
=
parent motion
+
joint-relative motion
```

This is the basic behaviour of a serial kinematic chain.

---

# 28. Joint Position Sensor

The example defines:

```xml
<jointpos
    name="pivot_p"
    joint="pivot"/>
```

Since `pivot` is a hinge joint:

```text
pivot_p
→ one joint-angle value
```

This corresponds to the relevant joint coordinate in:

```python
data.qpos
```

---

# 29. Joint Velocity Sensor

The example defines:

```xml
<jointvel
    name="pivot_v"
    joint="pivot"/>
```

Since `pivot` is a hinge joint:

```text
pivot_v
→ one angular-velocity value
```

This corresponds to the relevant state in:

```python
data.qvel
```

---

# 30. Ball Quaternion Sensor

The example may enable:

```xml
<ballquat
    name="ballquat"
    joint="ph"/>
```

This measures the orientation of the ball joint.

Output:

```text
quaternion
→ 4 values
```

---

# 31. Ball Angular Velocity Sensor

The example may also enable:

```xml
<ballangvel
    name="ballangvel"
    joint="ph"/>
```

This measures the ball joint angular velocity.

Output:

```text
ωx
ωy
ωz
```

---

# 32. Position Actuator

The example includes a position actuator for the `pivot` hinge joint:

```xml
<position
    kp="2"
    kv="0.1"
    name="pivot"
    joint="pivot"
    ctrlrange="-3.14 3.14"
    forcerange="-5 5"/>
```

This means:

```text
actuator type
→ position servo

controlled joint
→ pivot

ctrl
→ desired joint position

forcerange
→ limits final actuator output force/torque
```

The simplified control idea is:

```text
target position
↓
position error
↓
actuator torque
↓
pivot motion
```

---

# 33. Actuator and Sensor Together

This example demonstrates both sides of a robot control system.

Actuator side:

```text
data.ctrl
↓
actuator
↓
joint motion
```

Sensor side:

```text
joint/body state
↓
sensor
↓
measurement
```

Together:

```text
controller
↓
actuator
↓
robot motion
↓
sensor
↓
controller
```

This is the basic structure of feedback control.

---

# 34. Sensor Output Storage

Defining the sensors in XML does not automatically display their values.

MuJoCo stores enabled sensor outputs in:

```python
data.sensordata
```

Conceptually:

```text
simulation step
↓
state changes
↓
sensor values updated
↓
data.sensordata
```

---

# 35. Reading Sensor Data with Python

A minimal example is:

```python
import mujoco

model = mujoco.MjModel.from_xml_path("model.xml")
data = mujoco.MjData(model)

for _ in range(1000):
    mujoco.mj_step(model, data)
    print(data.sensordata)
```

The important sequence is:

```text
mj_step
↓
simulation state updates
↓
sensor output updates
↓
Python reads sensordata
```

---

# 36. Why `data.sensordata` Can Contain Many Values

Different sensor types produce different output dimensions.

For example:

```text
jointpos
→ 1

jointvel
→ 1

force
→ 3

torque
→ 3

framepos
→ 3

framequat
→ 4

ballquat
→ 4

ballangvel
→ 3
```

Therefore:

```python
data.sensordata
```

contains the outputs of all active sensors in one combined array.

---

# 37. Sensor Names and Larger Models

For very small models, it may be possible to inspect:

```python
data.sensordata
```

directly.

However, in larger models it is better to work by sensor name.

Conceptually:

```text
sensor name
↓
sensor ID
↓
sensor data address
↓
correct part of data.sensordata
```

This avoids manually remembering numeric array indices.

---

# 38. Main Sensor Groups Demonstrated

The example combines several sensor categories.

## Body / Frame Observation

```text
framepos
framequat
subtreelinvel
```

## IMU-Style Observation

```text
framequat
gyro
accelerometer
```

## Joint State

```text
jointpos
jointvel
ballquat
ballangvel
```

## Mechanical Interaction

```text
force
torque
```

## Visual Observation

```text
camera
```

---

# 39. Main Learning Outcome

The most important lesson from this example is that different parts of a MuJoCo model require different sensing methods.

For example:

```text
hinge joint
→ jointpos / jointvel

ball joint
→ ballquat / ballangvel

body or site frame
→ frame sensors

IMU location
→ framequat + accelerometer + gyro

mechanical connection
→ force + torque
```

So sensor choice depends on:

```text
what object is being observed
+
what physical quantity is needed
```

---

# 40. Final Understanding

The complete conceptual flow is:

```text
XML
↓
define bodies, joints, sites, cameras, actuators and sensors
↓
MjModel
↓
MjData
↓
mj_step
↓
physical state changes
↓
sensor outputs update
↓
data.sensordata
↓
Python
↓
display / save / analyse / control
```

This example therefore connects several previously learned MuJoCo concepts:

```text
body hierarchy
joint
site
camera
actuator
sensor
qpos
qvel
sensordata
Python control
```

into one combined model.

---

## Source

This analysis is based on a sensor example from:

```text
Albusgive/mujoco_learning
```

Source repository:

https://github.com/Albusgive/mujoco_learning

The original model and teaching materials belong to the respective author(s).

This report records my own learning process, structural analysis, and interpretation of the example model.