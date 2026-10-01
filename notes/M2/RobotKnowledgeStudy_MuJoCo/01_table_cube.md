# SIM-T01 - Table and Falling Cube

[English](01_table_cube.md) | [中文](01_table_cube_zh.md)

---

## Overview

This scene introduces the basic MuJoCo simulation workflow using a simple table-and-cube setup.

The main goals are to understand:

- how an MJCF XML scene defines geometry and physical properties
- how Python loads the XML model
- how `MjModel` and `MjData` are used
- how simulation time advances with `mj_step`
- how position, velocity, and contact information can be observed
- how simulation results can be checked numerically and visually

The scene contains:

- a floor
- a table
- a freely falling cube
- two fixed cameras
- lighting

The cube falls under gravity, contacts the table, and eventually settles.

---

## 1. Scene Structure

The main XML structure is:

```text
mujoco
├── option
└── worldbody
    ├── light
    ├── camera: front_view
    ├── camera: top_view
    ├── floor geom
    ├── table top geom
    ├── four table-leg geoms
    └── cube body
        ├── freejoint
        └── cube geom
```

This structure illustrates an important MuJoCo rule:

```text
geom directly inside worldbody
→ fixed in the world

body + joint
→ movable rigid body
```

---

## 2. Simulation Settings

The scene uses:

```xml
<option timestep="0.005" gravity="0 0 -9.81"/>
```

This means:

```text
timestep = 0.005 s
gravity = (0, 0, -9.81) m/s²
```

Each call to:

```python
mujoco.mj_step(model, data)
```

advances simulation time by:

```text
0.005 s
```

---

## 3. Table Geometry

The tabletop is defined using a box geom:

```xml
<geom name="table_top"
      type="box"
      pos="0 0 0.725"
      size="0.5 0.35 0.025"/>
```

For a box, MuJoCo `size` values are half-extents.

Therefore the full tabletop dimensions are:

```text
length = 1.00 m
width  = 0.70 m
height = 0.05 m
```

The tabletop center is at:

```text
z = 0.725 m
```

so the top surface is:

```text
0.725 + 0.025 = 0.750 m
```

---

## 4. Cube Definition

The cube is defined as:

```xml
<body name="cube" pos="0 0 1.05">
    <freejoint name="cube_free"/>
    <geom name="cube_geom"
          type="box"
          size="0.05 0.05 0.05"
          mass="0.1"/>
</body>
```

The body center initially starts at:

```text
z = 1.05 m
```

The cube half-height is:

```text
0.05 m
```

so its bottom surface initially lies at:

```text
1.05 - 0.05 = 1.00 m
```

The initial gap above the table is therefore:

```text
1.00 - 0.75 = 0.25 m
```

---

## 5. Role of the Free Joint

The cube contains:

```xml
<freejoint name="cube_free"/>
```

A free joint gives the cube:

```text
3 translational degrees of freedom
+
3 rotational degrees of freedom
```

Therefore the cube is not fixed and can fall under gravity.

The main relationship is:

```text
body
→ rigid body

freejoint
→ allows free motion

geom
→ defines physical shape, mass, appearance, and contact geometry
```

---

## 6. Model and Simulation State

The Python program loads the XML using:

```python
model = mujoco.MjModel.from_xml_path(...)
data = mujoco.MjData(model)
```

These two objects have different roles:

```text
model
→ model structure and fixed simulation rules

data
→ current simulation state
```

The model includes information such as:

```text
geometry
mass
gravity
joints
timestep
```

The data object contains values such as:

```text
current time
positions
velocities
contacts
control inputs
sensor data
```

---

## 7. Initial State

Before advancing simulation time, the program uses:

```python
mujoco.mj_forward(model, data)
```

This computes the current derived state without advancing time.

Then the initial state is recorded:

```python
samples = [observe(data)]
```

This produces the step-0 record at:

```text
time = 0.000 s
```

Because this record is created before the loop:

```text
200 simulation steps
+
1 initial record
=
201 total records
```

---

## 8. Advancing the Simulation

Each simulation iteration follows this pattern:

```python
mujoco.mj_step(model, data)
mujoco.mj_forward(model, data)
samples.append(observe(data))
```

The roles are:

```text
mj_step
→ advances physics by one timestep

mj_forward
→ refreshes derived calculations for the current state
→ does not advance simulation time

observe
→ records the current state
```

The same `data` object is reused continuously.

The simulation does not restart from the initial state after every step.

---

## 9. Observed State

The program records four values:

```text
time_s
cube_z_m
cube_vz_m_s
contact_count
```

These correspond to:

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

For the free joint:

```text
qpos[0] = x
qpos[1] = y
qpos[2] = z
```

The remaining four `qpos` values represent orientation using a quaternion.

The free-joint velocity vector contains:

```text
3 translational velocities
+
3 angular velocities
```

so:

```text
qvel[2]
```

is the cube's vertical velocity.

---

## 10. First Two Steps

The first two steps verify that the state evolves continuously.

Typical output is:

```text
time_s cube_z_m cube_vz_m_s contact_count

0.000  1.0500   0.0000    0
0.005  1.0498  -0.0491    0
0.010  1.0493  -0.0981    0
```

This shows:

```text
time increases
cube height decreases
vertical velocity becomes more negative
contact count remains zero
```

The cube is accelerating downward under gravity.

---

## 11. Full 200-Step Simulation

With:

```text
200 steps
```

and:

```text
timestep = 0.005 s
```

the total simulated time is:

```text
200 × 0.005 = 1.000 s
```

The cube initially falls freely.

Around the contact time:

```text
contact_count changes from 0 to a positive value
```

After contacting the table, the cube undergoes a small transient response and eventually settles.

---

## 12. Predicted Final Height

The table top surface is:

```text
0.75 m
```

The cube half-height is:

```text
0.05 m
```

Therefore the expected settled cube-center height is approximately:

```text
0.75 + 0.05 = 0.80 m
```

The simulation produced approximately:

```text
0.7999 m
```

which closely matches the geometric prediction.

---

## 13. Contact Count

The simulation uses:

```python
data.ncon
```

to inspect the number of active contact points.

Typical behavior is:

```text
cube in air
→ contact_count = 0

cube resting on table
→ contact_count > 0
```

In this scene, the resting cube produced:

```text
contact_count = 4
```

This value represents the number of detected contact points.

It does not directly represent contact force.

---

## 14. 100-Step Prediction Check

A separate 100-step run was used as a prediction exercise.

Since:

```text
100 × 0.005 = 0.500 s
```

the expected final simulation time was:

```text
0.500 s
```

The predicted settled state was approximately:

```text
cube_z ≈ 0.80 m
cube_vz ≈ 0
```

The actual result was approximately:

```text
time = 0.500 s
cube_z = 0.7999 m
cube_vz = 0.0001 m/s
contact_count = 4
```

This confirmed the prediction.

---

## 15. CSV Output

The simulation can save every recorded step to CSV.

This makes it possible to inspect:

- when the cube begins falling
- when the first contact occurs
- how vertical velocity changes
- when the cube approaches rest
- how the final height compares with prediction

The CSV provides a numerical history of the simulation rather than only a visual animation.

---

## 16. Automated Testing

The scene includes automated tests using `pytest`.

The tests verify important properties of the scene and simulation behavior.

The completed run passed all tests:

```text
3 passed
```

This provides an additional reproducibility check.

---

## 17. Viewer

The scene can also be explored using the MuJoCo Viewer.

Two main approaches are available.

### Independent Viewer

The XML can be opened directly:

```bash
python -m mujoco.viewer --mjcf=simulation/mujoco/scenes/sim_t01_table_cube/scene.xml
```

This is useful for:

- pausing and resuming
- resetting
- switching cameras
- inspecting geometry
- viewing contact points and forces
- exploring the scene manually

### Python-Controlled Viewer

The simulation script can also launch a passive Viewer:

```bash
python -m examples.mujoco.sim_t01_table_cube --steps 400 --viewer
```

In this mode:

```text
Python controls mj_step
Viewer displays the current simulation state
```

---

## 18. Viewer as a Debugging Tool

Useful Viewer features include:

```text
F2
→ simulation information

C
→ contact points

F
→ contact forces

W
→ wireframe

T
→ transparent mode

[ / ]
→ switch between fixed cameras

Esc
→ return to free camera
```

The Viewer is therefore not only for animation.

It can also be used to inspect and verify simulation behavior.

---

## 19. Core Understanding

The full simulation workflow can be summarized as:

```text
XML defines the physical scene
↓
MjModel loads the model
↓
MjData stores the current state
↓
mj_step advances physics
↓
qpos / qvel / contacts change
↓
observe records the state
↓
CSV and Viewer provide numerical and visual verification
```

The most important conceptual distinction is:

```text
XML
→ what exists and what the physical rules are

Python
→ how the simulation is advanced and observed
```

This scene marks the transition from static MJCF modeling to programmatic MuJoCo simulation.

---

## Source

This note is based on the M2 `SIM-T01` material from:

```text
Robot_knowledge_study
v0.3.0
```

Source repository:

https://github.com/noBug01/Robot_knowledge_study

The original repository and teaching materials belong to their respective author(s).

This document records my own learning process, explanations, calculations, simulation checks, and understanding based on the source material.