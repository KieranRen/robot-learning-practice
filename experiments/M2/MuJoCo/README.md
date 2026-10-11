# M2: MuJoCo Experiments

This directory contains the MuJoCo experiments completed during M2 of my Robot Learning roadmap.

The purpose of these experiments is to connect theoretical concepts with practical simulation work.

The experiments in this directory are based on concepts learned from the following upstream repository:

https://github.com/Albusgive/mujoco_learning.git

The original repository and teaching materials belong to their respective author(s).

The files in this directory record my own practice, experiments, example analysis, summaries, and understanding based on the learning process.

---

# Current Experiments

## 01. Review Model

The first MuJoCo experiment combines the basic concepts learned so far into one simulation scene.

### Files

```text
review_model.xml
review_model_report.md
review_model_report_zh.md
```

### Main concepts reviewed

```text
simulation configuration
visual settings
assets
texture
material
worldbody
body
geom
site
parent-child body hierarchy
relative coordinates
friction
mass
RGBA
```

The model contains:

```text
ground
support
motor
site
multiple geoms
```

This experiment mainly reinforced body hierarchy and relative coordinate relationships.

---

## 02. Pendulum

The second MuJoCo experiment focuses on joint behaviour using a simple pendulum.

### Files

```text
pendulum.xml
pendulum_report.md
pendulum_report_zh.md
```

### Main concepts reviewed

```text
body
joint
hinge
axis
range
joint position
joint axis
joint range
damping
initial orientation
center of mass
torque
gravitational rotational motion
```

The experiment demonstrates how a hinge joint constrains a body to one rotational degree of freedom.

It also reinforced the relationship:

```text
gravity
↓
center of mass offset
↓
torque
↓
rotational motion
```

---

## 03. Friction Comparison

The third MuJoCo experiment focuses on contact friction and the role of `condim`.

### Files

```text
friction_comparison.xml
friction_comparison_report.md
friction_comparison_report_zh.md
```

### Main model contains four main comparison groups

```text
box
condim 1 vs 3

sphere
condim 3 vs 6

cylinder on slope
condim 1 vs 3

sphere on slope
condim 4 vs 6
```

### Main concepts reviewed

```text
sliding friction
torsional friction
rolling friction
friction values
condim
contact dimensions
friction cone
priority
friction parameter structure
contact behaviour
```

### Main friction parameters

```text
friction="sliding torsional rolling"
```

Internally, the three friction values correspond conceptually to:

```text
sliding
sliding
torsional
rolling
rolling
```

### `condim`

The contact dimensionality determines which friction modes are active.

```text
condim = 1
→ normal force only

condim = 3
→ normal + two sliding directions

condim = 4
→ normal + sliding + torsional friction

condim = 6
→ normal + sliding + torsional + rolling friction
```

The experiment makes the effect of different contact models easier to compare visually.

---

## 04. Actuator Demo

The fourth MuJoCo experiment focuses on actuator behaviour using a simple two-joint mechanism.

### Files

```text
actuator_demo.xml
actuator_demo_report.md
actuator_demo_report_zh.md
```

### Main mechanism structure

```text
base
└── upper_arm
    ├── pivot
    │   └── position actuator
    │
    └── pendulum
        └── ph
            └── intvelocity actuator
```

The two joints use different actuator types:

```text
pivot
→ position actuator

ph
→ intvelocity actuator
```

### Main concepts reviewed

```text
actuator
general actuator structure
motor
position actuator
velocity actuator
intvelocity actuator
damper actuator
cylinder actuator
muscle actuator
joint-based actuation
tendon-based actuation
control input
ctrlrange
forcerange
gear
kp
kv
time constant
integrated velocity command
actuator force / torque limits
```

### Position actuator

Conceptually:

```text
target position
↓
position error
↓
actuator torque
↓
joint motion
```

A simplified interpretation is:

```text
torque ≈ kp × position_error - kv × velocity
```

### Intvelocity actuator

Conceptually:

```text
velocity-like control command
↓
internal integration
↓
internal target position
↓
position-like servo
↓
joint motion
```

This experiment reinforced that:

```text
data.ctrl
```

does not always represent the same physical quantity.

Its interpretation depends on the actuator type.

---

## 05. Tendon Example Analysis

The fifth experiment section records the analysis of two MuJoCo tendon examples.

### Files

```text
tendon_examples_report.md
tendon_examples_report_zh.md
```

These examples were analysed from the upstream learning material.

The complete original XML models were not independently reconstructed or claimed as original work in this repository.

### Example A: Mecanum Fixed Tendons

The first example uses four wheel joints:

```text
a1
b1
a2
b2
```

and combines them using three `fixed` tendons:

```text
forward
transverse
rotate
```

The coefficient patterns create three virtual motion coordinates:

```text
forward
→ + + + +

transverse
→ + - - +

rotate
→ + + - -
```

The key idea is:

```text
physical wheel joints
↓
fixed tendon
↓
virtual motion coordinate
```

Velocity actuators then act on the tendon coordinates rather than directly controlling each wheel joint.

Conceptually:

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

### Example B: Spatial Tendon and Muscle

The second example uses `spatial` tendons routed through sites.

The main paths include:

```text
M:
ceiling
↓
hook1
↓
hook2
↓
hook3
```

and:

```text
A:
hook4
↓
hook5
```

The `M` tendon demonstrates passive elastic and damping behaviour using:

```text
springlength
stiffness
damping
```

The `A` tendon is driven by a muscle actuator.

The transmission chain becomes:

```text
control input
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

### Main concepts reviewed

```text
tendon
spatial tendon
fixed tendon
site routing
joint coupling
coef
springlength
stiffness
damping
frictionloss
tendon visualization
muscle actuator
tendon-driven actuation
Mecanum wheel transmission
```

The most important distinction is:

```text
spatial tendon
→ geometric path through sites

fixed tendon
→ mathematical combination of joint coordinates
```

---

## 06. Sensor Example Analysis

The sixth experiment section records the analysis of a combined MuJoCo sensor example.

### Files

```text
sensor_example_report.md
sensor_example_report_zh.md
```

The model combines several independent sensor demonstrations into one XML scene.

### Main model structure

```text
world
├── free body B
│   ├── freejoint
│   ├── IMU site
│   └── body-mounted camera
│
├── force / torque structure
│   └── force_torque site
│
└── joint sensor structure
    └── support
        └── rotay_am
            ├── pivot hinge joint
            └── pendulum
                └── ph ball joint
```

### Main sensors studied

```text
framequat
accelerometer
gyro
subtreelinvel
framepos
force
torque
jointpos
jointvel
ballquat
ballangvel
```

### IMU-style sensing

A MuJoCo IMU can be constructed conceptually using:

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

### Joint sensing

For a hinge joint:

```text
jointpos
→ joint position

jointvel
→ joint velocity
```

For a ball joint:

```text
ballquat
→ orientation quaternion

ballangvel
→ 3D angular velocity
```

### Force / Torque sensing

Using:

```text
force
+
torque
```

provides:

```text
Fx Fy Fz
+
Tx Ty Tz
```

which is conceptually similar to a six-axis force/torque sensor.

### Sensor output

Sensor definitions in XML do not automatically print their values.

During simulation:

```text
simulation step
↓
sensor calculation
↓
data.sensordata
↓
Python
```

Python can then use the measurements for:

```text
terminal output
data logging
plotting
analysis
feedback control
```

### Main concepts reviewed

```text
sensor
site-based sensing
joint sensing
frame sensing
IMU
camera
rangefinder
force
torque
ball joint sensing
subtree sensing
data.sensordata
sensor output dimensions
Python sensor reading
feedback control
```

---

# Experiment Directory Structure

The current directory structure is:

```text
MuJoCo/
│
├── README.md
│
├── review_model.xml
├── review_model_report.md
├── review_model_report_zh.md
│
├── pendulum.xml
├── pendulum_report.md
├── pendulum_report_zh.md
│
├── friction_comparison.xml
├── friction_comparison_report.md
├── friction_comparison_report_zh.md
│
├── actuator_demo.xml
├── actuator_demo_report.md
├── actuator_demo_report_zh.md
│
├── tendon_examples_report.md
├── tendon_examples_report_zh.md
│
├── sensor_example_report.md
└── sensor_example_report_zh.md
```

---

# Current Experiment Progress

The current experiment sequence follows the development of the M2 learning process.

## 01. Review Model

Focus:

```text
MJCF structure
body
geom / site
assets and materials
basic rigid-body simulation
```

Status:

```text
Completed
```

---

## 02. Pendulum

Focus:

```text
joint
hinge
axis
range
gravity
torque
rotational motion
```

Status:

```text
Completed
```

---

## 03. Friction Comparison

Focus:

```text
contact
friction coefficients
condim
friction modes
priority
observed contact behaviour
```

Status:

```text
Completed
```

---

## 04. Actuator Demo

Focus:

```text
joint
actuator
data.ctrl
position control
intvelocity control
force / torque limits
physical joint motion
```

Status:

```text
Completed
```

---

## 05. Tendon Example Analysis

Focus:

```text
spatial tendon
fixed tendon
site routing
joint coupling
coef
muscle actuator
tendon transmission
```

Status:

```text
Example analysis completed
```

---

## 06. Sensor Example Analysis

Focus:

```text
IMU
joint sensors
frame sensors
force / torque sensors
ball joint sensors
subtree sensors
data.sensordata
sensor feedback
```

Status:

```text
Example analysis completed
```

---

# Skills Reinforced

These experiments and example analyses reinforce:

```text
MuJoCo XML structure
body hierarchy
relative coordinates
geom modelling
site usage
joint modelling
hinge and ball joints
contact and friction
actuator configuration
position and integrated-velocity control
tendon transmission
fixed joint coupling
spatial tendon routing
sensor configuration
sensor data interpretation
qpos / qvel
data.ctrl
data.sensordata
basic robot feedback architecture
```

The learning sequence is gradually moving from:

```text
geometry
↓
joint motion
↓
contact
↓
actuation
↓
transmission
↓
sensing
↓
feedback control
```

---

# Future Experiments

Future experiments may include topics such as:

```text
sensor-data logging with Python
named sensor access
closed-loop control
trajectory tracking
multi-joint control
camera rendering
rangefinder / LiDAR simulation
contact-force analysis
tendon-driven control
robot arm control
forward kinematics
inverse kinematics
trajectory generation
more complex robotic systems
```

`light` and `replicate` have also been studied mainly as MJCF modelling features rather than standalone experiments.

As more MuJoCo experiments are completed, they will be added to this directory and documented here.