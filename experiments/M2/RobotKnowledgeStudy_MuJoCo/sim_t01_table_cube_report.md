# SIM-T01 Experiment Report - Table and Falling Cube

[English](sim_t01_table_cube_report.md) | [中文](sim_t01_table_cube_report_zh.md)

---

## Experiment Goal

This experiment reproduces the first MuJoCo simulation scene from the `Robot_knowledge_study` M2 material.

The main purpose is to verify that I can:

- load an MJCF scene with Python
- advance the simulation using `mj_step`
- observe position and velocity
- detect contact
- compare simulation results with simple physical predictions
- inspect the scene using MuJoCo Viewer
- verify the implementation with automated tests

---

## Scene

The experiment uses:

```text
simulation/mujoco/scenes/sim_t01_table_cube/scene.xml
```

The scene contains:

- a ground plane
- a table
- a freely moving cube
- gravity
- two fixed cameras
- lighting

The cube starts above the table and falls under gravity.

---

## Initial Geometry Check

The tabletop center is:

```text
z = 0.725 m
```

Its half-thickness is:

```text
0.025 m
```

Therefore the top surface is:

```text
0.725 + 0.025
=
0.750 m
```

The cube center starts at:

```text
z = 1.05 m
```

The cube half-height is:

```text
0.05 m
```

Therefore the cube bottom initially lies at:

```text
1.05 - 0.05
=
1.00 m
```

The initial gap is:

```text
1.00 - 0.75
=
0.25 m
```

---

## Simulation Settings

The scene uses:

```xml
<option timestep="0.005" gravity="0 0 -9.81"/>
```

Therefore:

```text
physics timestep = 0.005 s
gravity = -9.81 m/s² along z
```

---

## Python Simulation Flow

The core Python flow is:

```text
load XML
↓
create MjModel
↓
create MjData
↓
compute initial state
↓
record initial observation
↓
repeat mj_step
↓
record updated state
```

The main objects are:

```text
MjModel
→ fixed model structure and simulation rules

MjData
→ current dynamic simulation state
```

---

## Observed Variables

The experiment records:

```text
simulation time
cube z position
cube z velocity
contact count
```

These are obtained from:

```python
data.time
```

```python
data.joint("cube_free").qpos[2]
```

```python
data.joint("cube_free").qvel[2]
```

```python
data.ncon
```

---

## Two-Step Verification

The first check used only two simulation steps.

The observed state was approximately:

```text
0.000 s
z = 1.0500 m
vz = 0.0000 m/s
contact = 0

0.005 s
z = 1.0498 m
vz = -0.0491 m/s
contact = 0

0.010 s
z = 1.0493 m
vz = -0.0981 m/s
contact = 0
```

This confirmed that:

```text
time increases continuously
cube position decreases
downward velocity increases in magnitude
no contact exists initially
```

The simulation is therefore evolving continuously from one state to the next.

---

## 200-Step Simulation

The full simulation used:

```text
200 steps
```

With:

```text
0.005 s per step
```

the total simulation time was:

```text
200 × 0.005
=
1.000 s
```

The cube first falls freely, then contacts the table, slightly rebounds, and finally settles.

---

## Contact Observation

Before impact:

```text
contact_count = 0
```

After the cube reaches the tabletop:

```text
contact_count > 0
```

The settled state produced:

```text
contact_count = 4
```

This represents the number of active contact points.

It does not directly represent the magnitude of the contact force.

---

## Final Height Prediction

The expected resting cube-center height is:

```text
table top
+
cube half-height
```

Therefore:

```text
0.750 + 0.050
=
0.800 m
```

The simulated final height was approximately:

```text
0.7999 m
```

This matches the geometric prediction very closely.

---

## 100-Step Personal Check

A separate 100-step simulation was used as an independent prediction exercise.

Predicted simulation time:

```text
100 × 0.005
=
0.500 s
```

Predicted final state:

```text
cube z ≈ 0.80 m
cube vz ≈ 0
```

Observed result:

```text
time = 0.500 s
cube_z ≈ 0.7999 m
cube_vz ≈ 0.0001 m/s
contact_count = 4
```

The prediction was confirmed.

---

## Interpretation of the Motion

The motion can be summarized as:

```text
cube starts above table
↓
gravity accelerates cube downward
↓
cube contacts tabletop
↓
contact response produces a small transient rebound
↓
velocity decreases toward zero
↓
cube settles near z = 0.80 m
```

This demonstrates the complete transition from free motion to contact-constrained motion.

---

## CSV Output

The simulation can save the full state history to CSV.

This provides numerical evidence of:

- falling motion
- increasing downward velocity
- first contact
- rebound
- settling
- final stable height

The CSV makes it possible to analyze the simulation without relying only on visual inspection.

---

## Automated Test

The provided automated test suite was run with `pytest`.

Result:

```text
3 passed
```

This confirmed that the scene and simulation behavior satisfied the expected checks.

---

## Viewer Check

The scene was also opened using MuJoCo Viewer.

The Viewer was used to:

- inspect the table and cube geometry
- observe the cube falling
- inspect contact behavior
- switch camera views
- understand the difference between direct XML viewing and Python-controlled simulation

Two useful execution modes are:

```bash
python -m mujoco.viewer --mjcf=simulation/mujoco/scenes/sim_t01_table_cube/scene.xml
```

and:

```bash
python -m examples.mujoco.sim_t01_table_cube --steps 400 --viewer
```

The first lets the Viewer directly load the XML.

The second lets Python control the physics while Viewer displays the current state.

---

## Main Learning Outcome

This experiment introduced the transition from static MJCF modeling to programmatic MuJoCo simulation.

The most important workflow is:

```text
XML scene
↓
MjModel
↓
MjData
↓
mj_step
↓
qpos / qvel / contact update
↓
observation
↓
numerical and visual verification
```

The most important distinction is:

```text
XML
→ defines the model and physics setup

Python
→ advances and observes the simulation
```

---

## Source

This experiment is based on:

```text
Robot_knowledge_study
M2
SIM-T01
v0.3.0
```

Source repository:

https://github.com/noBug01/Robot_knowledge_study

The original repository and teaching materials belong to their respective author(s).

This report records my own simulation process, calculations, observations, verification, and understanding based on the source material.