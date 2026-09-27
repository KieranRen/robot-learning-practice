# M2 MuJoCo Experiment - Review Model

[English](README.md) | [中文](README_zh.md)

---

## Overview

This experiment combines the MuJoCo concepts learned so far into one simple simulation scene.

The goal is to review and connect the following ideas:

- Simulation configuration
- Visual settings
- Assets
- Materials
- Worldbody
- Bodies
- Geometries
- Sites
- Relative coordinates
- Free joints
- Gravity
- Mass
- Friction
- Basic collision behavior

The experiment file is:

```text
review_model.xml
```

---

## Experiment Structure

The scene contains:

- A ground plane
- A custom checker texture
- A floor material
- A cylinder support body
- A nested motor body
- A site marker
- A freely falling sphere
- A fixed box
- A fixed capsule
- Gravity
- Friction
- Multiple geometry types

A simplified hierarchy is:

```text
worldbody
├── floor
├── support
│   └── motor
│       └── motor_top site
├── falling_ball
├── box
└── capsule
```

---

## 1. Simulation Configuration

The simulation uses:

```xml
<option timestep="0.002"
        gravity="0 0 -9.81"
        integrator="implicitfast"/>
```

This means:

```text
timestep = 0.002 s
gravity = (0, 0, -9.81)
integrator = implicitfast
```

The simulation therefore advances in small time steps while gravity acts in the negative z direction.

---

## 2. Visual Configuration

The scene also includes basic visual settings such as:

```xml
<visual>
    <global realtime="1"/>
    <quality shadowsize="4096"/>
    <headlight diffuse="1 1 1"
               specular="0.5 0.5 0.5"
               active="1"/>
</visual>
```

These settings control:

- Realtime playback
- Shadow quality
- Lighting
- Viewer appearance

---

## 3. Assets

The experiment defines reusable resources inside the `<asset>` section.

These include:

- A skybox
- A checker floor texture
- A floor material

Example:

```xml
<texture name="floor_tex"
         type="2d"
         builtin="checker"
         rgb1="0.2 0.2 0.2"
         rgb2="0.8 0.8 0.8"
         width="512"
         height="512"/>
```

The floor material then uses this texture:

```xml
<material name="floor_mat"
          texture="floor_tex"
          texrepeat="5 5"
          reflectance="0.2"/>
```

This reviews the relationship:

```text
texture
↓
material
↓
geom
```

---

## 4. Ground Plane

The scene contains a ground plane:

```xml
<geom name="floor"
      type="plane"
      size="5 5 0.1"
      material="floor_mat"
      friction="1 0.005 0.0001"/>
```

This geom:

- Uses a plane geometry
- Uses the custom floor material
- Has contact friction
- Acts as the ground for the simulation

---

## 5. Support Body

The main support body is defined as:

```xml
<body name="support"
      pos="0 0 1">
```

This means the support body has a local coordinate frame located at:

```text
(0, 0, 1)
```

relative to the world frame.

A cylinder geom is attached to this body.

Example:

```xml
<geom type="cylinder"
      size="0.15 0.5"
      mass="2"
      rgba="0.2 0.2 0.8 1"/>
```

This reviews the idea:

```text
body
→ rigid body + local coordinate frame

geom
→ physical geometry attached to the body
```

---

## 6. Nested Motor Body

A second body is nested inside the support body:

```xml
<body name="motor"
      pos="0 0 0.6">
```

Because `motor` is inside `support`, its position is relative to the support body's coordinate frame.

Therefore:

```text
support z = 1.0
motor relative z = 0.6
```

If there is no rotation:

```text
motor world z = 1.6
```

This is an example of parent-child body hierarchy.

---

## 7. Site Marker

A site is attached to the motor body:

```xml
<site name="motor_top"
      pos="0 0 0.25"
      size="0.05"
      rgba="0 1 0 1"/>
```

The site is not another rigid body.

It is a marker attached to the motor body.

It can later be useful for:

- End-effector locations
- Sensor locations
- Target points
- Reference positions

---

## 8. Falling Ball

The experiment includes a freely moving sphere:

```xml
<body name="falling_ball"
      pos="1 0 2">

    <freejoint/>

    <geom type="sphere"
          size="0.2"
          mass="1"
          friction="0.8 0.005 0.0001"
          rgba="1 0.5 0 1"/>

</body>
```

The important part is:

```xml
<freejoint/>
```

This allows the body to move freely in 3D.

The body can therefore respond to:

- Gravity
- Collision
- Contact
- Friction

Without a free joint or another joint, the body would remain fixed relative to its parent.

---

## 9. Box Geometry

The scene includes a box:

```xml
<geom name="box"
      type="box"
      pos="-1 0 0.25"
      size="0.3 0.3 0.25"
      rgba="0.2 0.8 0.2 1"
      mass="2"/>
```

For a box:

```text
size = half-dimensions
```

So:

```text
size = (0.3, 0.3, 0.25)
```

means full dimensions:

```text
0.6 × 0.6 × 0.5 m
```

Because the box height is `0.5 m`, placing its center at:

```text
z = 0.25
```

places its bottom surface approximately at:

```text
z = 0
```

---

## 10. Capsule Geometry

The scene also includes a capsule:

```xml
<geom name="capsule"
      type="capsule"
      pos="0 -1 0.6"
      size="0.15 0.4"
      rgba="0.7 0.3 0.9 1"
      mass="1"/>
```

For a capsule:

```text
first size value
→ radius

second size value
→ half-length of the cylindrical section
```

So:

```text
radius = 0.15 m
cylindrical half-length = 0.4 m
```

This reviews another common MuJoCo geometry type.

---

## 11. Concepts Reviewed

This experiment combines the main ideas learned so far:

```text
<mujoco>
<option>
<visual>
<asset>
<texture>
<material>
<worldbody>
<body>
<geom>
<site>
<freejoint>
```

It also reviews:

- `timestep`
- `gravity`
- `integrator`
- `pos`
- `size`
- `rgba`
- `mass`
- `friction`
- Geometry types
- Parent-child body hierarchy
- Relative coordinates

---

## 12. Running the Experiment

Activate the MuJoCo environment:

```bash
conda activate mujoco_env
```

Go to the folder containing the XML file:

```bash
cd /d "C:\Users\A\Desktop\Robot Learning\mujoco\model"
```

Then run:

```bash
python -m mujoco.viewer --mjcf review_model.xml
```

The MuJoCo Viewer should load the scene.

After starting the simulation, the free sphere should fall under gravity and interact with the ground.

---

## Key Understanding

This experiment connects the configuration side of MuJoCo with the model-building side.

A useful summary is:

```text
option
→ controls simulation physics

visual
→ controls appearance

asset
→ prepares reusable resources

worldbody
→ contains the physical scene

body
→ defines rigid-body frames

geom
→ defines physical geometry

site
→ defines reference markers

joint / freejoint
→ defines how bodies are allowed to move
```

---

## Source

This experiment is based on concepts learned from the following upstream repository:

https://github.com/Albusgive/mujoco_learning.git

The original repository and teaching materials belong to their respective author(s).

The experiment file and notes here are my own practice, organization, and understanding based on the learning process.