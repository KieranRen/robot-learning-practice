# MuJoCo Light and Replicate

[English](06_light_and_replicate.md) | [中文](06_light_and_replicate_zh.md)

---

## Overview

This note summarizes two MJCF topics from the Albusgive MuJoCo learning source:

- `light`
- `replicate`

These two features serve very different purposes.

```text
light
→ controls scene illumination and rendering

replicate
→ automatically creates repeated MJCF structures
```

`light` mainly affects visualization.

`replicate` mainly improves model construction efficiency when many similar objects need to be created.

---

# Part I - Light

## 1. What `light` Does

A MuJoCo light controls how objects are illuminated in the Viewer.

A light can define:

- position
- direction
- ambient lighting
- diffuse lighting
- specular highlights
- shadows
- attenuation
- spotlight angle
- tracking behavior

A light mainly affects rendering.

It does not directly change:

```text
mass
gravity
joint motion
actuator control
collision behavior
```

---

## 2. Basic Light Example

A simple light may look like:

```xml
<light
    directional="true"
    pos="0 0 5"
    dir="0 0 -1"
    ambient="1 1 1"
    diffuse="1 1 1"
    specular="1 1 1"/>
```

This can be interpreted as:

```text
light position
→ above the scene

light direction
→ downward

ambient / diffuse / specular
→ define different lighting components
```

---

## 3. `pos`

The parameter:

```xml
pos="x y z"
```

defines the light position.

For example:

```xml
pos="0 0 5"
```

places the light five units above the world origin.

This is especially important for non-directional lights.

---

## 4. `dir`

The parameter:

```xml
dir="x y z"
```

defines the direction the light points.

For example:

```xml
dir="0 0 -1"
```

means:

```text
point downward along the negative z direction
```

---

## 5. `directional`

The parameter:

```xml
directional="true"
```

creates a directional light.

A directional light behaves approximately like sunlight:

```text
light rays are nearly parallel
```

Its effect is mainly determined by direction rather than distance from the source.

If:

```xml
directional="false"
```

the light behaves more like a local source whose position matters.

---

## 6. `ambient`

`ambient` provides basic background illumination.

For example:

```xml
ambient="0.2 0.2 0.2"
```

means surfaces receive some light even if they are not directly facing the light source.

A useful interpretation is:

```text
ambient
→ base brightness of the scene
```

---

## 7. `diffuse`

`diffuse` controls normal surface illumination.

This is usually the main component that makes surfaces visibly brighter when they face the light.

Conceptually:

```text
surface faces light
↓
stronger diffuse illumination
```

A useful interpretation is:

```text
diffuse
→ ordinary visible illumination
```

---

## 8. `specular`

`specular` controls shiny highlights.

This creates bright reflections on surfaces depending on:

- surface orientation
- light direction
- camera direction
- material properties

A useful interpretation is:

```text
specular
→ highlight / shine
```

---

## 9. Ambient, Diffuse, and Specular

These three can be remembered as:

```text
ambient
→ basic background brightness

diffuse
→ ordinary surface illumination

specular
→ shiny highlight
```

They mainly affect appearance rather than physical simulation.

---

## 10. `castshadow`

The parameter:

```xml
castshadow="true"
```

allows the light to produce shadows.

If disabled:

```text
objects can still be illuminated
but the light will not cast shadows
```

This can affect rendering performance.

---

## 11. `active`

The parameter:

```xml
active="true"
```

enables the light.

If:

```xml
active="false"
```

the light is defined but inactive.

---

## 12. Spotlight Parameters

A local light can behave like a spotlight.

Useful parameters include:

```text
cutoff
exponent
```

### `cutoff`

`cutoff` controls the light-cone angle.

Conceptually:

```text
smaller cutoff
→ narrower spotlight

larger cutoff
→ wider spotlight
```

### `exponent`

`exponent` controls how concentrated the light is near the center of the beam.

Conceptually:

```text
larger exponent
→ brighter center
→ stronger falloff near the edge
```

---

## 13. `attenuation`

Local light intensity can decrease with distance.

MuJoCo provides:

```xml
attenuation="a b c"
```

A simplified interpretation is:

```text
light intensity
≈
1 / (a + b·d + c·d²)
```

where:

```text
d
→ distance from the light
```

Therefore larger distance-dependent terms produce faster brightness reduction.

At the current stage, it is sufficient to remember:

```text
attenuation
→ controls how quickly light becomes weaker with distance
```

---

## 14. Light Modes

A light can use different modes such as:

```text
fixed
track
trackcom
targetbody
targetbodycom
```

These determine how the light position or direction relates to bodies in the model.

---

## 15. `fixed`

With:

```text
mode="fixed"
```

the light remains fixed relative to its parent frame.

It does not actively track another body.

---

## 16. `track`

A tracking light can move with a body.

Conceptually:

```text
body moves
↓
light follows
```

This is useful when a light should remain attached to a moving robot or object.

---

## 17. `trackcom`

`trackcom` follows the center of mass of a body.

This is useful when the light should follow the overall motion of an object.

---

## 18. `targetbody`

A light can point toward a specific body.

Example:

```xml
<light
    mode="targetbody"
    target="arm0"
    .../>
```

This means:

```text
light
→ continuously points toward arm0
```

This can be useful for robot visualization.

---

## 19. `targetbodycom`

This mode targets the center of mass of a body.

Conceptually:

```text
targetbody
→ target body reference

targetbodycom
→ target body center of mass
```

---

## 20. Light Summary

The most important parameters are:

```text
pos
→ light position

dir
→ light direction

directional
→ directional or local light

ambient
→ background illumination

diffuse
→ normal surface illumination

specular
→ highlights

castshadow
→ shadow generation

mode / target
→ tracking or targeting behavior

cutoff / exponent
→ spotlight shape

attenuation
→ distance falloff
```

The main principle is:

```text
light
→ rendering / visualization
→ not robot dynamics
```

---

# Part II - Replicate

## 21. What `replicate` Does

`replicate` automatically creates multiple copies of an MJCF structure.

It is similar to pattern tools in CAD software:

```text
linear pattern
circular pattern
array
```

Instead of manually writing the same XML many times, one structure can be copied using:

```xml
<replicate>
```

---

## 22. Basic Replicate Example

For example:

```xml
<replicate count="4" offset="0 0.5 0">
    <geom type="box" size="0.1 0.1 0.1"/>
</replicate>
```

This creates four box geoms.

Each copy is translated relative to the previous copy.

The approximate positions are:

```text
copy 0
→ y = 0

copy 1
→ y = 0.5

copy 2
→ y = 1.0

copy 3
→ y = 1.5
```

---

## 23. `count`

The parameter:

```xml
count="4"
```

defines the total number of replicated instances.

It means:

```text
final number of copies
=
4
```

not:

```text
1 original + 4 additional copies
```

---

## 24. `offset`

The parameter:

```xml
offset="x y z"
```

defines the translation increment between copies.

For example:

```xml
offset="0 0.5 0"
```

means:

```text
x
→ unchanged

y
→ +0.5 for each copy

z
→ unchanged
```

This creates a linear array.

---

## 25. Vertical Replication

For example:

```xml
<replicate count="5" offset="0 0 0.1">
```

creates copies stacked along the z axis:

```text
z = 0
z = 0.1
z = 0.2
z = 0.3
z = 0.4
```

This demonstrates that `offset` can be used along any axis.

---

## 26. `euler`

`euler` defines an incremental rotation between copies.

Example:

```xml
<replicate
    count="50"
    euler="0 0 0.1254">
```

means:

```text
each new copy
→ rotates an additional 0.1254 rad around z
```

if the model uses radians.

---

## 27. Circular Replication

If an object is first placed away from the rotation center:

```xml
<site
    pos="0.1 0 0"
    .../>
```

and then replicated with:

```xml
<replicate
    count="50"
    euler="0 0 0.1254">
```

the copies can form a circle.

The reason is:

```text
site is placed at radius 0.1
↓
each copy is rotated around the center
↓
positions move around the circle
```

Since:

```text
2π / 50
≈ 0.12566 rad
```

an increment near:

```text
0.1254 rad
```

creates approximately one full revolution after 50 copies.

---

## 28. Why the Original Position Matters

If the replicated site were located at:

```text
pos="0 0 0"
```

then rotation would not move its position.

All copies would remain at the center.

Therefore circular replication requires:

```text
nonzero radius from rotation center
+
incremental rotation
```

---

## 29. `offset` and `euler` Together

Both translation and rotation can be applied at the same time.

For example:

```xml
<replicate
    count="4"
    offset="0 0.5 0"
    euler="0 0 0.2">
```

produces approximately:

```text
copy 0
→ original position
→ original orientation

copy 1
→ +0.5 y
→ +0.2 rad

copy 2
→ +1.0 y
→ +0.4 rad

copy 3
→ +1.5 y
→ +0.6 rad
```

The transforms accumulate between copies.

---

## 30. `sep`

`sep` controls the separator used when MuJoCo automatically generates names for replicated objects.

For example:

```xml
<replicate
    count="4"
    sep="-">
```

If the original object is:

```xml
<site name="rf"/>
```

the replicated names can become similar to:

```text
rf-0
rf-1
rf-2
rf-3
```

Therefore:

```text
sep
→ affects generated names
```

It does not change physics or geometry.

---

## 31. Why Unique Names Are Needed

MJCF elements such as:

```text
body
joint
geom
site
```

often use names for later references.

If many identical objects are replicated, each generated element must still have a unique identifier.

`replicate` automatically handles these suffixes.

---

## 32. Nested Replicate

A `replicate` block can contain another `replicate`.

Example:

```xml
<replicate
    count="2"
    offset="0 1 0"
    euler="90 0 0">

    <replicate
        count="2"
        sep="-"
        offset="1 0 0"
        euler="0 90 0">

        <geom name="Alice" size=".1"/>

    </replicate>
</replicate>
```

The inner replicate creates:

```text
2 copies
```

and the outer replicate duplicates that entire structure:

```text
2 × 2
=
4 final objects
```

---

## 33. Nested Replicate as Multi-Dimensional Arrays

Nested replication can be understood similarly to nested loops.

For example:

```text
one replicate
→ one-dimensional pattern

two nested replicates
→ two-dimensional pattern

three nested replicates
→ three-dimensional pattern
```

This is useful for:

- grids
- repeated obstacles
- sensor arrays
- repeated geometric structures

---

## 34. Replicating Bodies

`replicate` does not only work with simple geoms.

A complete body can be replicated.

For example:

```xml
<replicate count="5" offset="1 0 0">
    <body>
        <joint .../>
        <geom .../>
        <site .../>
    </body>
</replicate>
```

This can create five copies of an entire articulated structure.

Therefore `replicate` can duplicate much more than visual geometry.

---

## 35. Replicating Sites

Sites are especially useful with `replicate`.

For example, repeated sites can create:

```text
sensor positions
measurement points
visual markers
ray directions
```

The circular site example demonstrates this use.

---

## 36. Replicated Names and References

When named objects are replicated, MuJoCo automatically modifies the names.

Related references can also be expanded consistently.

For example, if a replicated structure contains:

```text
site
sensor referencing that site
```

the replicated names and references can remain correctly associated.

This makes `replicate` much more useful than manually copying only geometry.

---

## 37. Replicate vs Manual XML Copying

Without `replicate`, creating 50 similar objects might require writing the same XML structure 50 times.

With `replicate`:

```text
define structure once
+
define transform increment
+
define copy count
```

This improves:

- readability
- maintainability
- consistency
- modeling speed

---

## 38. Common Replication Patterns

### Linear Pattern

```text
count
+
offset
```

Example:

```xml
<replicate count="10" offset="0.2 0 0">
```

---

### Circular Pattern

```text
count
+
euler
+
object positioned away from center
```

---

### Grid Pattern

```text
nested replicate
+
different offsets
```

---

### Repeated Mechanism

```text
replicate
+
complete body hierarchy
```

---

## 39. Core Replicate Parameters

The most important parameters are:

```text
count
→ number of generated instances

offset
→ translation increment

euler
→ rotation increment

sep
→ separator used in generated names
```

These four are sufficient for understanding most beginner `replicate` examples.

---

## 40. Core Understanding

The main concept of `replicate` is:

```text
define one structure
↓
repeat it automatically
↓
apply incremental transform
↓
generate unique names
```

A useful summary is:

```text
offset only
→ linear pattern

euler + radius
→ circular pattern

nested replicate
→ grid / multidimensional pattern
```

---

# Light vs Replicate

## 41. Different Roles

Although they are taught in the same chapter, `light` and `replicate` solve completely different problems.

```text
light
→ controls how the scene looks

replicate
→ controls how repeated model structures are generated
```

More specifically:

```text
light
→ rendering

replicate
→ model construction
```

Neither directly replaces:

```text
body
joint
geom
actuator
```

They support the scene around those core elements.

---

## 42. What to Remember

For `light`, remember:

```text
pos
→ where the light is

dir
→ where it points

directional
→ parallel or local lighting

ambient
→ base illumination

diffuse
→ normal illumination

specular
→ highlights

castshadow
→ shadows

mode / target
→ tracking behavior
```

For `replicate`, remember:

```text
count
→ how many

offset
→ translation increment

euler
→ rotation increment

sep
→ generated-name separator
```

The simplest memory aid is:

```text
light
→ illuminate

replicate
→ copy
```

---

## Source

This note is based on the Light and Replicate section of:

```text
Albusgive/mujoco_learning
```

Source repository:

https://github.com/Albusgive/mujoco_learning

The original repository and teaching materials belong to the respective author(s).

This note records my own learning process, interpretation, example analysis, and understanding based on the source material.