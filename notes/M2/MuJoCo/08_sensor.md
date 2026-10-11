# MuJoCo Sensors

[English](08_sensor.md) | [中文](08_sensor_zh.md)

## Overview

This note summarizes the MuJoCo sensor concepts studied from the Albusgive MuJoCo learning source.

The main topics include:

- camera-related observation
- IMU-style sensing
- `framequat`
- `accelerometer`
- `gyro`
- `jointpos`
- `jointvel`
- `rangefinder`
- `force`
- `torque`
- `ballquat`
- `ballangvel`
- `framepos`
- `framequat`
- `framelinvel`
- `frameangvel`
- `framelinacc`
- `frameangacc`
- subtree-related sensors
- a combined sensor example

The main idea is:

```text
MuJoCo simulation
↓
body / joint / site states
↓
sensor definitions
↓
sensor measurements
↓
Python reads data.sensordata
```

Sensors define what should be measured.

Python usually decides what to do with the measurements:

```text
print
save
plot
control
verify
```

---

# 1. Sensor Data in MuJoCo

Defining a sensor in XML does not automatically print its value.

For example:

```xml
<sensor>
    <jointpos name="pivot_p" joint="pivot"/>
    <jointvel name="pivot_v" joint="pivot"/>
</sensor>
```

The XML defines the sensors.

During simulation, MuJoCo calculates their outputs and stores them in:

```python
data.sensordata
```

So the complete flow is:

```text
XML defines sensor
↓
simulation runs
↓
MuJoCo calculates sensor output
↓
data.sensordata
↓
Python reads the data
```

Python can then:

```text
print to terminal
save to CSV
plot data
use it for feedback control
```

---

# 2. Camera

A camera is not itself a `<sensor>` element, but it is an important observation component in robot simulation.

A camera can define:

- position
- orientation
- tracking mode
- target body
- field of view
- camera intrinsics

Example:

```xml
<camera
    name="c2"
    pos="1 0 1"
    mode="targetbody"
    target="B"
    fovy="54.225"/>
```

This camera:

```text
is positioned at a specified location
↓
tracks body B
↓
keeps looking toward B
```

---

# 3. Camera Modes

Important camera modes include:

```text
fixed
track
trackcom
targetbody
targetbodycom
```

A simple interpretation is:

```text
fixed
→ camera is fixed relative to its parent body

targetbody
→ camera points toward a specified body

track
→ camera follows an object

trackcom
→ tracks center-of-mass motion

targetbodycom
→ targets the center of mass of a body
```

---

# 4. Camera Field of View

The most direct camera projection parameter is:

```xml
fovy="..."
```

This defines the vertical field of view in degrees.

Conceptually:

```text
smaller fovy
→ narrower view
→ more zoomed-in

larger fovy
→ wider view
```

---

# 5. Camera Intrinsics

MuJoCo can also define more camera-like intrinsic parameters.

These include:

```text
focal
focalpixel
sensorsize
resolution
principal
principalpixel
```

Conceptually:

```text
focal
→ focal length in physical units

focalpixel
→ focal length in pixels

sensorsize
→ physical sensor size

resolution
→ image resolution

principal
→ principal point in physical units

principalpixel
→ principal point in pixels
```

For basic simulation, `fovy` is often the simpler method.

---

# 6. IMU in MuJoCo

MuJoCo does not require one single sensor called:

```text
IMU
```

Instead, IMU-like measurements are built by combining multiple sensor types.

A typical combination is:

```text
framequat
+
accelerometer
+
gyro
```

So:

```text
IMU
≈
orientation
+
linear acceleration
+
angular velocity
```

---

# 7. IMU Site

A site is commonly used to define where the IMU is mounted.

Example:

```xml
<site
    name="imu"
    type="box"
    size="0.02 0.02 0.02"/>
```

The site defines:

```text
sensor position
+
sensor coordinate frame
```

Then sensors can refer to the site.

Example:

```xml
<accelerometer
    name="accel"
    site="imu"/>

<gyro
    name="base_ang_vel"
    site="imu"/>
```

---

# 8. `framequat`

Example:

```xml
<framequat
    name="orientation"
    objtype="site"
    objname="imu"/>
```

This measures the orientation of the specified frame.

Output:

```text
quaternion
```

which contains four values.

Conceptually:

```text
framequat
→ which direction is this frame facing?
```

---

# 9. `accelerometer`

Example:

```xml
<accelerometer
    name="accel"
    site="imu"/>
```

This measures acceleration at the IMU site.

Conceptually:

```text
accelerometer
→ linear acceleration measured at this sensor location
```

The result is a 3D vector.

---

# 10. `gyro`

Example:

```xml
<gyro
    name="base_ang_vel"
    site="imu"/>
```

This measures angular velocity at the site.

Output:

```text
ωx
ωy
ωz
```

Conceptually:

```text
gyro
→ how quickly the sensor frame is rotating
```

---

# 11. IMU Summary

A typical IMU-style setup is:

```text
site "imu"
↓
framequat
→ orientation

accelerometer
→ acceleration

gyro
→ angular velocity
```

This is conceptually similar to a real robot IMU.

---

# 12. `jointpos`

Example:

```xml
<jointpos
    name="pivot_p"
    joint="pivot"/>
```

This reads the position coordinate of a joint.

For a hinge joint:

```text
jointpos
→ joint angle
```

For a slide joint:

```text
jointpos
→ translational position
```

The value corresponds to the relevant joint state in:

```python
data.qpos
```

So conceptually:

```text
jointpos
≈
structured sensor access to a joint coordinate
```

---

# 13. `jointvel`

Example:

```xml
<jointvel
    name="pivot_v"
    joint="pivot"/>
```

This reads joint velocity.

For a hinge joint:

```text
jointvel
→ angular velocity
```

For a slide joint:

```text
jointvel
→ linear velocity
```

The value corresponds to the relevant state in:

```python
data.qvel
```

---

# 14. `jointpos` vs `jointvel`

The distinction is simple:

```text
jointpos
→ where the joint is

jointvel
→ how fast the joint is moving
```

For a hinge joint:

```text
jointpos
→ rad

jointvel
→ rad/s
```

---

# 15. Direct State vs Sensor Interface

It is possible to read:

```python
data.qpos
data.qvel
```

directly.

But sensors provide a more structured interface.

Conceptually:

```text
data.qpos / data.qvel
→ low-level system state arrays
```

while:

```text
jointpos / jointvel
→ named sensor measurements
```

This can make model organization clearer.

---

# 16. `rangefinder`

A rangefinder measures distance along a ray.

Example:

```xml
<rangefinder site="rf"/>
```

The site defines:

```text
ray origin
+
ray direction
```

So the basic idea is:

```text
site
↓
ray is emitted
↓
ray intersects geometry
↓
distance is returned
```

This is essentially ray casting.

---

# 17. Why Rangefinder Uses a Site

A distance sensor needs:

```text
where the ray starts
+
which direction it points
```

A site already defines:

```text
position
orientation
```

Therefore:

```xml
<rangefinder site="rf"/>
```

means:

```text
start from site rf
↓
cast a ray along the site's sensing direction
↓
measure distance to the first detected object
```

---

# 18. Single-Beam Rangefinder

One rangefinder corresponds to one measurement ray.

Conceptually:

```text
one site
↓
one ray
↓
one distance value
```

This behaves like a simple single-beam lidar or laser distance sensor.

---

# 19. Building a LiDAR-Like Sensor

A larger lidar can be approximated using many sites and many rangefinders.

For example:

```text
many sites
↓
different orientations
↓
one rangefinder per site
↓
many distance samples
```

With enough rays:

```text
rangefinder array
→ point-cloud-like observation
```

The previously learned `replicate` feature can help create repeated sensor layouts.

---

# 20. Rangefinder Performance

If many rangefinders are used:

```text
more rays
↓
more ray-intersection calculations
↓
higher computational cost
```

The learning material points out that sensor calculation can become expensive when a large number of lidar-like rays are updated at simulation frequency.

In practical simulation:

```text
physics simulation
→ may run at high frequency

lidar feedback
→ may be updated less frequently
```

This is an important engineering consideration.

---

# 21. `force`

Example:

```xml
<force
    name="force"
    site="force_torque"/>
```

This measures force at the specified site.

Output:

```text
Fx
Fy
Fz
```

So the result is a 3D force vector.

---

# 22. `torque`

Example:

```xml
<torque
    name="torque"
    site="force_torque"/>
```

This measures torque at the same site.

Output:

```text
Tx
Ty
Tz
```

So the result is a 3D torque vector.

---

# 23. Force/Torque Sensor

Combining:

```text
force
+
torque
```

gives:

```text
3 force components
+
3 torque components
=
6-dimensional force/torque information
```

This is similar to a 6-axis force/torque sensor used in robotics.

Typical applications include:

```text
robot wrist sensing
gripper force measurement
foot-ground interaction
contact measurement
```

---

# 24. Why Force/Torque Uses a Site

The site defines:

```text
measurement location
+
measurement coordinate frame
```

Therefore:

```text
force
torque
```

can be interpreted relative to the sensor frame defined by the site.

---

# 25. Ball Joint Sensors

A ball joint has:

```text
3 rotational DOF
```

Unlike a hinge joint, its orientation cannot be represented by only one angle.

MuJoCo therefore provides dedicated sensors:

```text
ballquat
ballangvel
```

---

# 26. `ballquat`

Example:

```xml
<ballquat
    name="ballquat"
    joint="ph"/>
```

This measures the orientation of the ball joint.

Output:

```text
quaternion
```

which contains four values.

Conceptually:

```text
ballquat
→ current orientation of the ball joint
```

---

# 27. `ballangvel`

Example:

```xml
<ballangvel
    name="ballangvel"
    joint="ph"/>
```

This measures angular velocity of the ball joint.

Output:

```text
ωx
ωy
ωz
```

So:

```text
ballquat
→ orientation

ballangvel
→ angular velocity
```

---

# 28. Why Ball Joint Position Uses 4 Values

A ball joint has:

```text
3 rotational DOF
```

but its orientation is stored using a unit quaternion:

```text
w
x
y
z
```

The quaternion has four values but one normalization constraint:

```text
||q|| = 1
```

so it still represents three independent rotational degrees of freedom.

---

# 29. Hinge vs Ball Joint Sensors

| Joint Type | Position Sensor | Velocity Sensor |
|---|---|---|
| Hinge | `jointpos` | `jointvel` |
| Slide | `jointpos` | `jointvel` |
| Ball | `ballquat` | `ballangvel` |

---

# 30. Frame Sensors

MuJoCo provides a family of sensors whose names begin with:

```text
frame...
```

These sensors measure the state of an object frame rather than only one joint coordinate.

Examples include:

```text
framepos
framequat
framelinvel
frameangvel
framelinacc
frameangacc
```

---

# 31. `framepos`

Example:

```xml
<framepos
    name="base_pos"
    objtype="body"
    objname="B"/>
```

This measures the position of object `B`.

Output:

```text
x
y
z
```

If no reference object is specified, it can be interpreted as the object's position relative to the global/world frame.

---

# 32. `framequat`

Example:

```xml
<framequat
    name="base_quat"
    objtype="body"
    objname="B"/>
```

This measures orientation.

Output:

```text
quaternion
```

So:

```text
framepos
+
framequat
```

together describe object pose:

```text
position
+
orientation
```

---

# 33. `framelinvel`

This measures the linear velocity of an object frame.

Output:

```text
vx
vy
vz
```

Conceptually:

```text
framelinvel
→ how fast this frame is translating
```

---

# 34. `frameangvel`

This measures angular velocity.

Output:

```text
ωx
ωy
ωz
```

Conceptually:

```text
frameangvel
→ how fast this frame is rotating
```

---

# 35. `framelinacc`

This measures linear acceleration.

Output:

```text
ax
ay
az
```

Conceptually:

```text
framelinacc
→ how quickly the frame's linear velocity changes
```

---

# 36. `frameangacc`

This measures angular acceleration.

Output:

```text
αx
αy
αz
```

Conceptually:

```text
frameangacc
→ how quickly angular velocity changes
```

---

# 37. Relative Frame Sensors

Frame sensors can also use:

```text
reftype
refname
```

These define a reference frame.

For example:

```xml
<framepos
    objtype="site"
    objname="end_effector"
    reftype="body"
    refname="base"/>
```

This means:

```text
measure end_effector position
relative to base
```

rather than relative to the world.

---

# 38. Object and Reference

A useful way to remember the parameters is:

```text
objtype + objname
→ what am I observing?

reftype + refname
→ relative to which frame?
```

This is directly related to coordinate-frame concepts from robotics.

For example:

```text
end-effector relative to base
```

is different from:

```text
end-effector relative to world
```

---

# 39. Frame Sensors and Robot Kinematics

Suppose a robot has:

```text
world
└── base
    └── arm
        └── end_effector
```

Then:

```text
framepos of end_effector relative to world
```

gives global position.

But:

```text
framepos of end_effector relative to base
```

gives the end-effector coordinate in the robot base frame.

This connects directly to robotics concepts such as:

```text
world frame
base frame
tool frame
relative transform
```

---

# 40. Subtree Sensors

The learning material also introduced subtree-related sensors.

These include:

```text
subtreecom
subtreelinvel
subtreeangmom
```

A subtree means:

```text
a selected body
+
all of its descendant bodies
```

---

# 41. `subtreecom`

This measures the center of mass of an entire body subtree.

Example structure:

```text
upper_arm
└── forearm
    └── hand
```

If `upper_arm` is selected as the subtree root:

```text
subtreecom
```

describes the combined center of mass of:

```text
upper_arm
+
forearm
+
hand
```

rather than only the `upper_arm` body.

---

# 42. `subtreelinvel`

This measures the linear velocity of the subtree center of mass.

Conceptually:

```text
subtree
↓
combined center of mass
↓
linear velocity
```

---

# 43. `subtreeangmom`

This measures the angular momentum of a body subtree.

Conceptually:

```text
subtreeangmom
→ overall rotational momentum of the selected body subtree
```

---

# 44. Combined Sensor Example

The studied example combines several independent sensor demonstrations into one XML model.

It includes:

```text
free body B
force/torque structure
hinge joint
ball joint
camera
actuator
multiple sensors
```

The purpose is not to create one realistic robot.

Instead, it acts as:

```text
a sensor demonstration model
```

---

# 45. Free Body `B`

The example contains:

```xml
<body name="B" pos="0 0 0">
    <freejoint/>
    <site name="imu"/>
    ...
</body>
```

The `freejoint` gives body B full spatial freedom:

```text
3 translational DOF
+
3 rotational DOF
```

The `imu` site is used as an observation location.

Possible sensors include:

```text
framequat
accelerometer
gyro
framepos
subtreelinvel
```

---

# 46. External and Body-Mounted Cameras

The example includes two cameras.

One camera uses:

```text
mode="targetbody"
target="B"
```

This acts like an external camera watching body B.

Another camera is placed inside body B using:

```text
mode="fixed"
```

This camera moves with body B.

So:

```text
external target camera
→ observes B from outside

body-mounted fixed camera
→ moves together with B
```

---

# 47. Force/Torque Demo Body

The example includes a parent body and a child body:

```text
parent body
└── up_box
    ├── force_torque site
    └── geom
```

The site is used by:

```xml
<force name="force" site="force_torque"/>
<torque name="torque" site="force_torque"/>
```

This demonstrates 6-axis force/torque measurement.

---

# 48. Hinge Joint Demo

The example includes:

```xml
<joint
    type="hinge"
    name="pivot"
    axis="0 0 1"
    .../>
```

This is a 1-DOF rotational joint.

The sensors:

```xml
<jointpos name="pivot_p" joint="pivot"/>
<jointvel name="pivot_v" joint="pivot"/>
```

measure:

```text
pivot_p
→ pivot joint angle

pivot_v
→ pivot angular velocity
```

---

# 49. Ball Joint Demo

The example also contains:

```xml
<joint
    type="ball"
    name="ph"
    .../>
```

This gives the pendulum body three rotational degrees of freedom.

The related sensors are:

```xml
<ballquat
    name="ballquat"
    joint="ph"/>

<ballangvel
    name="ballangvel"
    joint="ph"/>
```

These measure:

```text
ballquat
→ ball joint orientation

ballangvel
→ ball joint angular velocity
```

---

# 50. Body Hierarchy in the Sensor Example

The studied structure is approximately:

```text
world
└── support
    └── rotay_am
        ├── pivot hinge joint
        ├── horizontal capsule
        └── pendulum
            ├── ph ball joint
            ├── vertical capsule
            └── sphere mass
```

---

# 51. `support`

The outer body:

```xml
<body name="support" pos="1 0 0.1">
```

has no joint connecting it to the world.

Therefore it is fixed.

It contains a cylindrical support geometry.

---

# 52. `rotay_am`

The child body:

```xml
<body name="rotay_am" pos="0 0 0.51">
```

is positioned relative to `support`.

It contains:

```xml
<joint
    type="hinge"
    name="pivot"
    axis="0 0 1"
    .../>
```

Therefore `rotay_am` can rotate around the z-axis.

---

# 53. Horizontal Capsule

The geometry:

```xml
<geom
    type="capsule"
    fromto="0 0 0 0.2 0 0"
    size="0.01"
    .../>
```

defines a horizontal link extending approximately:

```text
0.2 m along +x
```

The pendulum body is then placed at:

```xml
pos="0.2 0 0"
```

which is at the end of this horizontal link.

---

# 54. `pendulum`

The pendulum body contains:

```xml
<joint
    type="ball"
    name="ph"
    .../>
```

So the pendulum can rotate freely in three rotational dimensions relative to its parent.

The pendulum geometry extends downward:

```xml
fromto="0 0 0 0 0 -0.3"
```

and a sphere mass is placed at:

```xml
pos="0 0 -0.3"
```

---

# 55. Multiple Geoms in One Body

The pendulum body contains:

```text
capsule
+
sphere
```

These are not separate rigid bodies.

They are two geoms belonging to the same rigid body.

Therefore:

```text
capsule
+
sphere
↓
move together as one rigid body
```

This is an important MuJoCo modeling concept:

```text
body
→ rigid body

geom
→ shape belonging to that body
```

---

# 56. Parent-Child Motion

If the parent hinge joint `pivot` rotates:

```text
rotay_am rotates
↓
pendulum parent frame moves with it
```

Then the ball joint `ph` can additionally rotate relative to `rotay_am`.

So:

```text
final child motion
=
parent motion
+
child joint relative motion
```

This is the basic principle of a serial kinematic chain.

---

# 57. Actuator in the Combined Example

The example also includes:

```xml
<position
    kp="2"
    kv="0.1"
    name="pivot"
    joint="pivot"
    ctrlrange="-3.14 3.14"
    forcerange="-5 5"/>
```

This actuator controls the hinge joint `pivot`.

The control chain is:

```text
data.ctrl
↓
position actuator
↓
pivot joint
↓
rotary arm motion
```

---

# 58. Sensor and Actuator Together

The actuator changes the system state:

```text
control input
↓
actuator
↓
joint/body motion
```

Sensors observe the state:

```text
joint/body motion
↓
sensor
↓
measurement
```

This forms the foundation of feedback control:

```text
control
↓
robot motion
↓
sensor feedback
↓
controller
↓
new control
```

---

# 59. Sensor Output Dimensions

Different sensor types produce different numbers of values.

Examples:

| Sensor | Typical Output Size |
|---|---:|
| `jointpos` | 1 |
| `jointvel` | 1 |
| `force` | 3 |
| `torque` | 3 |
| `gyro` | 3 |
| `accelerometer` | 3 |
| `framepos` | 3 |
| `framequat` | 4 |
| `ballquat` | 4 |
| `ballangvel` | 3 |

Therefore:

```python
data.sensordata
```

is effectively a combined array containing outputs from all enabled sensors.

---

# 60. Reading Sensor Data in Python

A minimal example is:

```python
import mujoco

model = mujoco.MjModel.from_xml_path("model.xml")
data = mujoco.MjData(model)

for _ in range(1000):
    mujoco.mj_step(model, data)
    print(data.sensordata)
```

The simulation step:

```python
mujoco.mj_step(model, data)
```

updates the physical state and sensor measurements.

Then:

```python
data.sensordata
```

contains the current sensor outputs.

---

# 61. Why Sensor Names Matter

When many sensors exist, it is not ideal to manually remember:

```text
index 0 means ...
index 1 means ...
index 2 means ...
```

A better workflow is:

```text
sensor name
↓
find sensor ID
↓
find sensor address
↓
read the correct section of data.sensordata
```

This becomes more important in larger robot models.

---

# 62. Sensor Categories

The sensors studied can be organized into several groups.

### Joint State Sensors

```text
jointpos
jointvel
ballquat
ballangvel
```

These describe joint state.

### Frame State Sensors

```text
framepos
framequat
framelinvel
frameangvel
framelinacc
frameangacc
```

These describe the state of a body/site/geom/camera frame.

### IMU-Style Sensors

```text
framequat
accelerometer
gyro
```

These can be combined to approximate IMU measurements.

### Interaction Sensors

```text
force
torque
```

These measure mechanical interaction.

### Distance Sensors

```text
rangefinder
```

This measures ray-based distance.

### Subtree Sensors

```text
subtreecom
subtreelinvel
subtreeangmom
```

These describe aggregate body-subtree properties.

---

# 63. Core Understanding

The most important sensor workflow is:

```text
simulation state
↓
sensor definition
↓
measurement
↓
data.sensordata
↓
Python
```

The role of XML is mainly:

```text
what should be measured?
where should it be measured?
relative to which frame?
```

The role of Python is mainly:

```text
what should be done with the measurement?
```

For example:

```text
display
save
analyse
control
verify
```

---

# 64. What to Remember

At the current stage, the most important concepts are:

```text
site
→ often defines sensor location and coordinate frame

jointpos
→ joint position

jointvel
→ joint velocity

ballquat
→ ball joint orientation

ballangvel
→ ball joint angular velocity

accelerometer
→ acceleration

gyro
→ angular velocity

force
→ 3D force

torque
→ 3D torque

rangefinder
→ ray-based distance

framepos
→ frame position

framequat
→ frame orientation

framelinvel
→ frame linear velocity

frameangvel
→ frame angular velocity

framelinacc
→ frame linear acceleration

frameangacc
→ frame angular acceleration

subtreecom
→ subtree center of mass
```

The larger idea is:

```text
actuator
→ changes robot state

sensor
→ observes robot state

Python
→ connects sensing and control
```

This is the foundation of robot feedback control.

---

## Source

This note is based on the sensor section of:

```text
Albusgive/mujoco_learning
```

Source repository:

https://github.com/Albusgive/mujoco_learning

The original repository and teaching materials belong to the respective author(s).

This note records my own learning process, interpretation, example analysis, and understanding based on the source material.