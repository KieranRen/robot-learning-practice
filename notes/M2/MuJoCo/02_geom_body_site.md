# 02 - Geom, Body and Site

[English](02_geom_body_site.md) | [中文](02_geom_body_site_zh.md)

---

## Overview

This note records the MuJoCo concepts related to geometry, rigid bodies, body hierarchy, contact properties, and site markers.

Topics covered:

- `geom`
- Geometry types
- `size`
- `pos`
- `rgba`
- `material`
- `mass`
- `density`
- `friction`
- `condim`
- `contype`
- `conaffinity`
- `fromto`
- `body`
- Parent-child body hierarchy
- Relative coordinates
- `site`

---

## 1. Geom

The `<geom>` element defines a geometric object in MuJoCo.

A geom can describe:

- Shape
- Size
- Position
- Orientation
- Color
- Material
- Mass-related properties
- Collision properties
- Friction properties

A simple example:

```xml
<geom type="sphere"
      size="0.2"
      rgba="1 0 0 1"/>
```

This defines a red sphere with a radius of 0.2 m.

A useful way to understand `geom` is:

```text
geom
→ the physical geometric shape of an object
```

---

## 2. Common Geometry Types

Common MuJoCo geometry types include:

- `plane`
- `sphere`
- `box`
- `cylinder`
- `capsule`
- `mesh`

Example:

```xml
<geom type="box"
      size="0.3 0.2 0.1"/>
```

---

## 3. Size

The meaning of `size` depends on the geometry type.

### Sphere

```xml
<geom type="sphere"
      size="0.2"/>
```

For a sphere:

```text
size = radius
```

So:

```text
radius = 0.2 m
diameter = 0.4 m
```

---

### Box

```xml
<geom type="box"
      size="0.3 0.2 0.1"/>
```

For a box, the three values are half-sizes.

Therefore the full dimensions are:

```text
x = 0.6 m
y = 0.4 m
z = 0.2 m
```

So:

```text
box size
→ half-length in x
→ half-length in y
→ half-length in z
```

---

### Cylinder

```xml
<geom type="cylinder"
      size="0.1 0.5"/>
```

For a cylinder:

```text
first value
→ radius

second value
→ half-length
```

Therefore:

```text
radius = 0.1 m
full cylinder length = 1.0 m
```

---

### Capsule

```xml
<geom type="capsule"
      size="0.15 0.4"/>
```

For a capsule:

```text
first value
→ radius

second value
→ half-length of the cylindrical section
```

The cylindrical section has a full length of:

```text
0.8 m
```

The rounded ends add additional length.

---

## 4. Position

The `pos` attribute defines the position of an element.

Example:

```xml
<geom type="sphere"
      pos="1 0 2"
      size="0.2"/>
```

This means:

```text
x = 1
y = 0
z = 2
```

If a geom is directly inside `worldbody`, its position is relative to the world frame.

If a geom is inside a `body`, its position is relative to that body's local coordinate frame.

---

## 5. RGBA

The `rgba` attribute controls color and transparency.

Example:

```xml
rgba="1 0 0 1"
```

means:

```text
R = 1
G = 0
B = 0
A = 1
```

This represents opaque red.

Another example:

```xml
rgba="0 1 0 0.5"
```

represents semi-transparent green.

---

## 6. Material

A geom can use a material defined in the `<asset>` section.

Example:

```xml
<geom type="plane"
      material="floor_mat"/>
```

The material may have been defined earlier:

```xml
<material name="floor_mat"
          texture="floor_tex"/>
```

The relationship is:

```text
texture
↓
material
↓
geom
```

---

## 7. Mass and Density

MuJoCo can define the physical mass of a geom using either `mass` or `density`.

### Mass

Example:

```xml
<geom type="sphere"
      size="0.2"
      mass="1"/>
```

This directly sets:

```text
mass = 1 kg
```

---

### Density

Example:

```xml
<geom type="sphere"
      size="0.2"
      density="1000"/>
```

Here MuJoCo uses the geometry volume and density to calculate the mass.

So:

```text
mass
→ directly define the total mass

density
→ MuJoCo calculates mass from volume
```

In most cases, it is better to choose one approach instead of specifying both.

---

## 8. Friction

The `friction` attribute controls contact friction.

Example:

```xml
friction="0.8 0.005 0.0001"
```

The three values correspond to:

```text
1st value
→ sliding friction

2nd value
→ torsional friction

3rd value
→ rolling friction
```

At this stage, the most important value is the first one.

Larger sliding friction usually means:

```text
more grip
→ less sliding
```

Smaller sliding friction usually means:

```text
less grip
→ easier sliding
```

---

## 9. Contact Dimension

The `condim` attribute controls the dimensionality of contact constraints.

A useful simplified understanding is:

```text
condim = 1
→ normal contact only
→ no friction

condim = 3
→ normal contact + sliding friction

condim = 4
→ adds torsional friction

condim = 6
→ adds rolling friction
```

This affects what types of contact forces MuJoCo considers during contact.

---

## 10. Collision Filtering

MuJoCo uses:

```text
contype
conaffinity
```

to control which geoms are allowed to collide.

These parameters work as collision filters.

A useful way to understand them is:

```text
condim
→ what happens after contact occurs

contype / conaffinity
→ whether two geoms are allowed to contact each other
```

This becomes useful in robot models where some robot links should collide with the environment but not with certain nearby links.

---

## 11. From-To Definition

The `fromto` attribute is useful for defining long shapes between two points.

Example:

```xml
<geom type="capsule"
      fromto="0 0 0  0 0 1"
      size="0.1"/>
```

This creates a capsule extending between:

```text
Point A = (0, 0, 0)
Point B = (0, 0, 1)
```

with radius:

```text
0.1 m
```

This is useful for objects such as:

- Robot links
- Arms
- Legs
- Rods
- Structural members

Using `fromto` can avoid manually calculating:

- Center position
- Length
- Orientation

---

## 12. Body

The `<body>` element represents a rigid body and defines a local coordinate frame.

Example:

```xml
<body name="support"
      pos="0 0 1">

    <geom type="cylinder"
          size="0.15 0.5"/>

</body>
```

The body defines the rigid object frame, while the geom defines its physical geometric shape.

A useful mental model is:

```text
body
→ rigid body + local coordinate frame

geom
→ physical shape attached to the body
```

---

## 13. Worldbody

Bodies are usually created inside:

```xml
<worldbody>
```

Example:

```xml
<worldbody>

    <body name="support"
          pos="0 0 1">

        <geom type="cylinder"
              size="0.15 0.5"/>

    </body>

</worldbody>
```

The `worldbody` represents the root of the physical scene.

So:

```text
worldbody
→ simulation world

body
→ rigid body inside the world

geom
→ physical geometry attached to a body
```

---

## 14. Body Hierarchy

Bodies can be nested inside other bodies.

Example:

```xml
<body name="support"
      pos="0 0 1">

    <body name="motor"
          pos="0 0 0.6">

    </body>

</body>
```

The structure is:

```text
world
└── support
    └── motor
```

The child body position is defined relative to its parent body.

In this example:

```text
support world z = 1.0
motor relative z = 0.6
```

If there is no rotation:

```text
motor world z = 1.0 + 0.6
              = 1.6
```

This is one of the most important ideas in MuJoCo robot modeling.

---

## 15. Relative Coordinates

A body hierarchy forms a tree of coordinate frames.

For example:

```text
world
└── support
    └── motor
        └── camera
```

Each child body has its own local coordinate frame.

Its position and orientation are defined relative to its parent.

Therefore:

```text
parent transformation
↓
child transformation
↓
next child transformation
↓
...
```

This idea is closely related to robot forward kinematics.

---

## 16. Geom Inside a Body

A body can contain one or more geoms.

Example:

```xml
<body name="robot_part">

    <geom type="box"
          size="0.2 0.1 0.1"/>

    <geom type="cylinder"
          pos="0 0 0.3"
          size="0.05 0.2"/>

</body>
```

Both geoms belong to the same rigid body.

Therefore:

```text
one body
→ can contain multiple geoms
```

This is useful for building more complex rigid-body shapes.

---

## 17. Site

A `<site>` is an auxiliary marker attached to a body.

Example:

```xml
<site name="motor_top"
      pos="0 0 0.25"
      size="0.05"
      rgba="0 1 0 1"/>
```

A site can be used for:

- End-effector markers
- Sensor locations
- Target points
- Reference points
- Force application points

A useful way to understand it is:

```text
site
→ a marker attached to a body
```

It is not another rigid body.

---

## 18. Site as a Child Element

Consider:

```xml
<body name="motor">

    <geom type="sphere"
          size="0.18"/>

    <site name="motor_top"
          pos="0 0 0.25"
          size="0.05"/>

</body>
```

The structure is:

```text
motor
├── geom
└── site
```

The site is a child element of the body.

However:

```text
site ≠ child rigid body
```

It does not create a new rigid-body hierarchy level.

If the motor moves or rotates:

```text
geom moves with motor
site moves with motor
```

because both are attached to the same body.

---

## 19. Practical Structure

A simple MuJoCo model may look like:

```xml
<worldbody>

    <geom name="floor"
          type="plane"/>

    <body name="support"
          pos="0 0 1">

        <geom type="cylinder"
              size="0.15 0.5"/>

        <body name="motor"
              pos="0 0 0.6">

            <geom type="sphere"
                  size="0.18"/>

            <site name="motor_top"
                  pos="0 0 0.25"
                  size="0.05"/>

        </body>

    </body>

</worldbody>
```

The hierarchy is:

```text
worldbody
├── floor
└── support
    ├── support geom
    └── motor
        ├── motor geom
        └── motor_top site
```

---

## Key Understanding

The most important relationships from this section are:

```text
worldbody
→ the simulation world

body
→ rigid body + local coordinate frame

geom
→ physical geometry

site
→ reference marker
```

The hierarchy can be understood as:

```text
world
↓
parent body
↓
child body
↓
child body
```

while elements such as:

```text
geom
site
```

are attached to a body.

Another important distinction is:

```text
body
→ defines a rigid-body hierarchy

geom
→ defines shape and physical contact geometry

site
→ defines a reference or marker
```

---

## Source

This learning section is based on the following upstream repository:

https://github.com/Albusgive/mujoco_learning.git

The original repository and teaching materials belong to their respective author(s).

The notes above are my own summaries and understanding based on the learning process.