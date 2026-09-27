# 01 - Environment and Assets

[English](01_environment_and_assets.md) | [中文](01_environment_and_assets_zh.md)

---

## Overview

This note records the basic MuJoCo environment configuration and asset-related concepts learned in M2.

Topics covered:

- MuJoCo root structure
- Compiler settings
- Simulation options
- Visual settings
- Assets
- Textures
- Materials
- Meshes
- Height fields
- Skyboxes

---

## 1. MuJoCo Root Structure

A MuJoCo XML / MJCF model is usually wrapped inside:

```xml
<mujoco model="model_name">

    ...

</mujoco>
```

The `<mujoco>` element is the root element of the whole model.

Example:

```xml
<mujoco model="My Model">

</mujoco>
```

The `model` attribute gives the model a readable name.

---

## 2. Compiler

The `<compiler>` element controls how MuJoCo interprets parts of the model.

Example:

```xml
<compiler angle="degree" autolimits="true"/>
```

Important settings learned so far:

- `angle="degree"`  
  Angle values are interpreted in degrees.

- `angle="radian"`  
  Angle values are interpreted in radians.

- `autolimits="true"`  
  MuJoCo can automatically infer certain joint limit settings from defined ranges.

---

## 3. Simulation Options

The `<option>` element controls important global physical simulation settings.

Example:

```xml
<option timestep="0.002"
        gravity="0 0 -9.81"
        integrator="implicitfast"/>
```

### `timestep`

```xml
timestep="0.002"
```

This means each simulation step advances time by:

```text
0.002 s
```

Therefore:

```text
500 steps = 1 second
```

Smaller timesteps generally give finer simulation resolution, but require more computation.

### `gravity`

```xml
gravity="0 0 -9.81"
```

This represents the gravity vector:

```text
x = 0
y = 0
z = -9.81
```

So gravity acts in the negative z direction.

Example of zero gravity:

```xml
gravity="0 0 0"
```

### `integrator`

The integrator determines how MuJoCo numerically updates motion from one simulation step to the next.

Common options include:

- `Euler`
- `RK4`
- `implicit`
- `implicitfast`

Example:

```xml
integrator="implicitfast"
```

At this stage, the important idea is:

> The integrator controls how motion is numerically advanced through time.

### `solver`

The solver handles constraints such as:

- Contact
- Friction
- Joint constraints
- Collision response

Common solver types include:

- `PGS`
- `CG`
- `Newton`

The main distinction is:

```text
integrator
→ how motion is advanced

solver
→ how physical constraints are solved
```

### `iterations`

Example:

```xml
iterations="100"
```

This sets the maximum number of solver iterations.

More iterations may improve convergence, but also require more computation.

### `tolerance`

Example:

```xml
tolerance="1e-8"
```

This defines a stopping tolerance for the solver.

The solver may stop before reaching the maximum iteration count if the solution is already accurate enough.

---

## 4. Visual Settings

The `<visual>` section controls how the simulation looks in the MuJoCo Viewer.

Example:

```xml
<visual>

    <global realtime="1"/>

    <quality shadowsize="4096"/>

    <headlight diffuse="1 1 1"
               specular="0.5 0.5 0.5"
               active="1"/>

</visual>
```

### `global`

Example:

```xml
<global realtime="1"/>
```

This controls global viewer-related settings.

`realtime="1"` means the viewer tries to run simulation time close to real time.

### `quality`

Example:

```xml
<quality shadowsize="4096"/>
```

This controls visual rendering quality.

Examples include:

- Shadow quality
- Rendering detail
- Anti-aliasing related settings

Higher quality generally requires more computation.

### `headlight`

Example:

```xml
<headlight diffuse="1 1 1"
           specular="0.5 0.5 0.5"
           active="1"/>
```

The headlight is a light source associated with the viewer camera.

Important concepts:

- `diffuse` - diffuse light color
- `specular` - reflected highlight intensity
- `active` - whether the headlight is enabled

### RGBA

MuJoCo commonly uses RGBA color values:

```text
R = Red
G = Green
B = Blue
A = Alpha
```

Example:

```xml
rgba="1 0 0 1"
```

represents opaque red.

---

## 5. Assets

The `<asset>` section defines reusable resources for the model.

A useful way to understand it is:

> `asset` prepares resources, while other parts of the model use those resources.

Assets are not necessarily external files.

They can either:

- Be generated directly by MuJoCo
- Be loaded from external files

---

## 6. Texture

A texture defines an image or surface pattern.

### Built-in Texture

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

This creates a checker texture directly inside MuJoCo.

No external image file is needed.

### External Texture

Example:

```xml
<texture name="card_texture"
         type="2d"
         file="card.png"/>
```

This loads the texture from an external image file.

---

## 7. Material

A material controls how a surface appears.

Example:

```xml
<material name="floor_mat"
          texture="floor_tex"
          texrepeat="5 5"
          reflectance="0.2"/>
```

This material uses the previously defined texture:

```text
floor_tex
```

The relationship is:

```text
texture
↓
material
↓
geom
```

Example:

```xml
<geom type="plane"
      material="floor_mat"/>
```

---

## 8. Mesh

A mesh is a 3D geometry resource.

It can be loaded from an external model file.

Example:

```xml
<mesh name="forearm"
      file="forearm.stl"/>
```

The mesh can later be used by a geometry:

```xml
<geom type="mesh"
      mesh="forearm"/>
```

This is useful when importing CAD-generated robot parts.

---

## 9. Height Field

A height field can represent uneven terrain.

Example:

```xml
<hfield name="terrain"
        file="terrain.png"
        size="10 10 1 1"/>
```

Height fields can be useful for:

- Rough terrain
- Slopes
- Outdoor robot simulation
- Legged robot testing

---

## 10. Skybox

A skybox creates the background environment around the scene.

Example using an external image:

```xml
<texture type="skybox"
         file="desert.png"/>
```

Example using a MuJoCo built-in gradient:

```xml
<texture name="sky"
         type="skybox"
         builtin="gradient"
         rgb1="0.4 0.6 0.9"
         rgb2="0.9 0.9 0.9"
         width="512"
         height="512"/>
```

This allows a background to be generated without an external image.

---

## Key Understanding

The main structure learned in this section is:

```text
<mujoco>
    <compiler/>
    <option/>
    <visual/>
    <asset/>
</mujoco>
```

A useful mental model is:

```text
compiler
→ how MuJoCo interprets the model

option
→ how the physics simulation runs

visual
→ how the simulation looks

asset
→ reusable resources prepared for later use
```

---

## Source

This learning section is based on the following upstream repository:

https://github.com/Albusgive/mujoco_learning.git

The notes above are my own summaries and understanding based on the learning process.