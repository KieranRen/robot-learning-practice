# Notes

This directory contains structured learning notes produced throughout my Robot Learning roadmap.

The notes are organized by learning module and source so that concepts from different upstream repositories remain clearly separated.

The purpose of these notes is not only to record what was learned, but also to document the reasoning, interpretation, implementation ideas, and technical understanding developed during the learning process.

---

# M1 - Robotics Foundations

M1 focuses on the mathematical and programming foundations required for later robotics learning.

The main topics include:

- Python fundamentals
- NumPy
- vectors
- coordinate systems
- rigid transformations
- homogeneous transformation matrices
- point transformation
- robot geometry
- basic implementation and testing

M1 notes are stored in the corresponding M1 directory.

M1 also introduced the basic workflow used throughout this repository:

```text
learn
↓
understand
↓
implement
↓
test
↓
document
```

---

# M2 - MuJoCo and Robot Simulation

M2 focuses on robot simulation and MuJoCo.

Unlike M1, M2 currently uses two different upstream learning sources.

These two sources are intentionally kept separate.

```text
M2
├── MuJoCo
│   └── Albusgive/mujoco_learning
│
└── RobotKnowledgeStudy_MuJoCo
    └── noBug01/Robot_knowledge_study
```

This separation is important because the two sources have different structures, learning objectives, examples, and development workflows.

---

# Source A - Albusgive MuJoCo Learning

Directory:

```text
notes/M2/MuJoCo/
```

Upstream source:

```text
https://github.com/Albusgive/mujoco_learning
```

This source focuses on learning MuJoCo concepts progressively through MJCF structure, model elements, contact, actuation, transmission, sensing, and simulation examples.

Current status:

```text
In Progress
```

---

## 01. Environment and Assets

Files:

```text
M2/MuJoCo/01_environment_and_assets.md
M2/MuJoCo/01_environment_and_assets_zh.md
```

Main topics:

```text
MuJoCo environment
MJCF structure
compiler
option
visual
asset
mesh
texture
material
hfield
skybox
simulation configuration
rendering configuration
```

Important concepts include:

```text
timestep
gravity
integrator
solver
iterations
tolerance
density
viscosity
wind
```

and visual parameters such as:

```text
realtime
shadowsize
headlight
lighting
RGBA
fog
```

---

## 02. Geom, Body and Site

Files:

```text
M2/MuJoCo/02_geom_body_site.md
M2/MuJoCo/02_geom_body_site_zh.md
```

Main topics:

```text
geom
body
site
body hierarchy
relative coordinates
multiple geoms in one body
mass
density
friction
fromto
material
RGBA
```

Important understanding:

```text
body
→ rigid body

geom
→ shape belonging to a body

site
→ reference / marker / attachment location
```

Nested body coordinates are relative to their parent body.

---

## 03. Joint

Files:

```text
M2/MuJoCo/03_joint.md
M2/MuJoCo/03_joint_zh.md
```

Main topics:

```text
free joint
ball joint
slide joint
hinge joint
joint axis
joint range
damping
stiffness
frictionloss
armature
ref
```

Core relationship:

```text
body
→ rigid body

joint
→ defines allowed relative motion

geom
→ defines shape
```

A simple pendulum example was also analysed to connect:

```text
gravity
↓
center-of-mass offset
↓
torque
↓
rotational motion
```

---

## 04. Friction

Files:

```text
M2/MuJoCo/04_friction.md
M2/MuJoCo/04_friction_zh.md
```

Main topics:

```text
sliding friction
torsional friction
rolling friction
friction parameter structure
condim
contact dimensions
friction cones
priority
impratio
```

MuJoCo friction uses three main values:

```text
friction="sliding torsional rolling"
```

Conceptually expanded internally as:

```text
sliding
sliding
torsional
rolling
rolling
```

Important `condim` values:

```text
condim = 1
→ normal force only

condim = 3
→ normal + sliding friction

condim = 4
→ normal + sliding + torsional friction

condim = 6
→ normal + sliding + torsional + rolling friction
```

Both elliptic and pyramidal friction cones were studied.

---

## 05. Actuator

Files:

```text
M2/MuJoCo/05_actuator.md
M2/MuJoCo/05_actuator_zh.md
```

Main topics:

```text
general actuator
motor actuator
position actuator
velocity actuator
intvelocity actuator
damper actuator
cylinder actuator
muscle actuator
```

Important parameters include:

```text
ctrlrange
forcerange
actrange
gear
kp
kv
timeconst
gainprm
biasprm
```

Core control chain:

```text
Python data.ctrl
↓
actuator
↓
joint / tendon / site
↓
robot motion
```

Important distinctions:

```text
motor
→ how much force / torque to apply

position
→ where the joint should go

velocity
→ how fast the joint should move

intvelocity
→ velocity-like command integrated into an internal position target
```

---

## 06. Light and Replicate

Files:

```text
M2/MuJoCo/06_light_and_replicate.md
M2/MuJoCo/06_light_and_replicate_zh.md
```

### Light

Main topics:

```text
pos
dir
directional
castshadow
active
ambient
diffuse
specular
attenuation
cutoff
exponent
mode
target
```

Conceptually:

```text
light
→ controls scene illumination
```

### Replicate

Main topics:

```text
count
offset
euler
sep
nested replicate
linear repetition
circular repetition
```

Conceptually:

```text
replicate
→ repeatedly creates model structures
```

It can be used for structures such as:

```text
roller arrays
sensor arrays
repeated geometry
multidimensional patterns
```

---

## 07. Tendon

Files:

```text
M2/MuJoCo/07_tendon.md
M2/MuJoCo/07_tendon_zh.md
```

Main topics:

```text
tendon fundamentals
spatial tendon
fixed tendon
site routing
joint coupling
coef
range
frictionloss
width
springlength
stiffness
damping
muscle actuator
```

The two main tendon types are:

```text
spatial
→ geometric path through sites

fixed
→ mathematical combination of joint coordinates
```

### Spatial Tendon

A spatial tendon follows a path through sites:

```text
site
↓
site
↓
site
```

Body motion changes site positions, which changes tendon geometry and tendon length.

Important parameters include:

```text
springlength
stiffness
damping
width
```

A muscle actuator can drive a spatial tendon:

```text
control
↓
muscle actuator
↓
spatial tendon
↓
sites
↓
bodies
↓
joint motion
```

### Fixed Tendon

A fixed tendon combines joint coordinates using coefficients:

```text
T
=
coef1 × q1
+
coef2 × q2
+
...
```

The studied Mecanum example combines four wheel joints into:

```text
forward
transverse
rotate
```

virtual control coordinates.

Core relationship:

```text
physical joints
↓
fixed tendon
↓
virtual motion coordinate
```

---

## 08. Sensor

Files:

```text
M2/MuJoCo/08_sensor.md
M2/MuJoCo/08_sensor_zh.md
```

Main topics:

```text
camera
IMU
framequat
accelerometer
gyro
jointpos
jointvel
rangefinder
force
torque
ballquat
ballangvel
framepos
framelinvel
frameangvel
framelinacc
frameangacc
subtree sensors
data.sensordata
```

### IMU-Style Sensing

MuJoCo can construct IMU-like measurements using:

```text
framequat
+
accelerometer
+
gyro
```

which provides:

```text
orientation
+
acceleration
+
angular velocity
```

A `site` is commonly used as the sensor mounting location and coordinate frame.

### Joint Sensors

For hinge or slide joints:

```text
jointpos
→ joint position

jointvel
→ joint velocity
```

For ball joints:

```text
ballquat
→ orientation quaternion

ballangvel
→ angular velocity
```

### Rangefinder

A rangefinder uses a site to define:

```text
ray origin
+
ray direction
```

Conceptually:

```text
site
↓
ray casting
↓
geom intersection
↓
distance
```

Multiple rangefinders can be arranged into a LiDAR-like sensor array.

### Force and Torque

```text
force
→ Fx Fy Fz

torque
→ Tx Ty Tz
```

Together they provide six-axis force/torque information.

### Frame Sensors

Frame sensors include:

```text
framepos
framequat
framelinvel
frameangvel
framelinacc
frameangacc
```

They can measure either global or relative frame state.

Important logic:

```text
objtype + objname
→ what is being observed

reftype + refname
→ relative to which frame
```

### Sensor Data

Sensor values are stored in:

```python
data.sensordata
```

The basic workflow is:

```text
XML defines sensors
↓
simulation runs
↓
sensor values update
↓
data.sensordata
↓
Python
↓
display / save / analyse / control
```

---

# Albusgive MuJoCo Learning Progress

Completed topics so far include:

- environment and assets
- geom, body, and site
- joint modeling
- pendulum simulation
- friction
- `condim`
- elliptic and pyramidal friction cones
- contact priority
- actuator fundamentals
- motor actuator
- position actuator
- velocity actuator
- integrated velocity actuator
- damper actuator
- cylinder actuator
- actuator limits and control parameters
- light
- replicate
- linear and circular replication
- nested replication
- tendon fundamentals
- spatial tendon
- fixed tendon
- tendon routing with sites
- joint coupling with `coef`
- muscle-driven tendon actuation
- Mecanum fixed-tendon transmission
- camera fundamentals
- IMU-style sensing
- joint position and velocity sensors
- rangefinder
- force and torque sensors
- ball-joint sensing
- frame sensors
- relative frame sensing
- subtree sensing
- `data.sensordata`

More topics from this source will continue to be added as the learning progresses.

---

# Source B - Robot Knowledge Study MuJoCo

Directory:

```text
notes/M2/RobotKnowledgeStudy_MuJoCo/
```

Upstream source:

```text
https://github.com/noBug01/Robot_knowledge_study
```

Version studied:

```text
v0.3.0
```

Current M2 material from this source has been completed.

---

## 01. Table and Falling Cube

Files:

```text
M2/RobotKnowledgeStudy_MuJoCo/01_table_cube.md
M2/RobotKnowledgeStudy_MuJoCo/01_table_cube_zh.md
```

Main topics:

```text
MJCF model loading
MjModel
MjData
mj_forward
mj_step
qpos
qvel
contact detection
data.ncon
CSV output
numerical prediction
simulation verification
Viewer
camera operation
automated testing
```

Core workflow:

```text
XML
↓
MjModel
↓
MjData
↓
mj_step
↓
state changes
↓
observation
↓
verification
```

The falling-cube example connected physical prediction with numerical simulation.

---

## 02. Arm Joint Targets

Files:

```text
M2/RobotKnowledgeStudy_MuJoCo/02_arm_joint_targets.md
M2/RobotKnowledgeStudy_MuJoCo/02_arm_joint_targets_zh.md
```

Main topics:

```text
robot XML structure
default blocks
assets
mesh
body hierarchy
joint definitions
actuator
sensor
contact
joint targets
waypoints
interpolation
data.ctrl
qpos
qvel
sensor feedback
tool-frame state
```

The model includes two robot arms, with the left arm actively controlled.

The main control idea is:

```text
target waypoint
↓
interpolation
↓
data.ctrl
↓
position actuators
↓
joint motion
↓
sensor / qpos feedback
```

This source also introduced practical Python-based simulation control in addition to MJCF model reading.

---

# M2 Source Status

The two M2 sources currently have different progress states:

```text
Robot Knowledge Study
→ Completed

Albusgive MuJoCo Learning
→ In Progress

Overall M2
→ In Progress
```

This distinction is intentionally preserved because completing one source does not mean the entire M2 module is complete.

---

# Purpose

These notes serve three goals:

1. Support long-term review and revision.
2. Document the reasoning behind the implementations in this repository.
3. Provide evidence of continuous and structured technical learning.

The notes are designed to record not only:

```text
what was learned
```

but also:

```text
why it works
how different concepts connect
how the ideas are implemented
how they relate to robot simulation and control
```

As the Robot Learning roadmap progresses, new notes and learning sources will continue to be added while keeping each source clearly separated.