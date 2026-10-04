# MuJoCo Friction

[English](04_friction.md) | [中文](04_friction_zh.md)

---

## Overview

This note summarizes the MuJoCo friction concepts covered in the Albusgive MuJoCo learning source.

The main topics are:

- `friction="a b c"`
- sliding friction
- torsional friction
- rolling friction
- `condim`
- friction cone models
- `cone="elliptic"`
- `cone="pyramidal"`
- `priority`
- friction parameter selection between two geoms
- constraint dimensions
- internal friction expansion
- practical comparison examples

The most important idea is:

```text
friction
→ controls how strong each friction type is

condim
→ controls which friction modes are included

cone
→ controls how the friction constraints are represented mathematically
```

---

## 1. Friction Parameters

A MuJoCo geom can define:

```xml
<geom friction="a b c"/>
```

The three values represent:

```text
a
→ sliding friction

b
→ torsional friction

c
→ rolling friction
```

For example:

```xml
<geom friction="1 0.005 0.0001"/>
```

means:

```text
sliding friction = 1
torsional friction = 0.005
rolling friction = 0.0001
```

---

## 2. Sliding Friction

Sliding friction resists motion parallel to the contact surface.

Example:

```text
[ box ] →→→
────────────
```

The first friction parameter controls this effect:

```text
friction[0]
→ sliding friction
```

This is usually the largest of the three friction coefficients.

---

## 3. Torsional Friction

Torsional friction resists rotation around the normal direction of the contact.

Conceptually:

```text
     ↻
 [ object ]
────────────
```

The second friction parameter controls this:

```text
friction[1]
→ torsional friction
```

This becomes active when the contact model includes torsional friction.

---

## 4. Rolling Friction

Rolling friction resists rolling motion.

Example:

```text
O →→→
────────────
```

The third friction parameter controls rolling resistance:

```text
friction[2]
→ rolling friction
```

This is especially relevant for:

- spheres
- wheels
- rollers

---

## 5. `condim`

`condim` determines how many contact directions are included in the contact model.

Common values are:

```text
condim = 1
→ normal contact only

condim = 3
→ normal + sliding friction

condim = 4
→ normal + sliding + torsional friction

condim = 6
→ normal + sliding + torsional + rolling friction
```

This can be remembered as:

```text
1
→ do not penetrate

3
→ do not slide easily

4
→ do not twist easily

6
→ do not roll easily
```

---

## 6. Why `condim` Uses 1, 3, 4, and 6

The contact directions are grouped physically.

Sliding friction has two tangent directions:

```text
tangent direction 1
tangent direction 2
```

Rolling friction also has two rotational directions.

Therefore the dimensional progression becomes:

```text
1
→ normal only

3
→ +2 sliding directions

4
→ +1 torsional direction

6
→ +2 rolling directions
```

---

## 7. Friction Requires the Corresponding `condim`

Even if all three friction coefficients are defined:

```xml
<geom friction="1 0.01 0.001"
      condim="3"/>
```

`condim="3"` only enables:

```text
normal contact
+
sliding friction
```

Therefore the torsional and rolling friction parameters are not fully used by that contact model.

To enable torsional friction:

```text
condim = 4
```

To enable rolling friction:

```text
condim = 6
```

So:

```text
friction
→ defines strength

condim
→ defines which friction types are active
```

---

## 8. Friction Cone Models

MuJoCo supports two main friction-cone representations:

```xml
<option cone="elliptic"/>
```

and:

```xml
<option cone="pyramidal"/>
```

These do not directly change the friction coefficients.

Instead, they change how friction constraints are represented mathematically.

---

## 9. Elliptic Friction Cone

The elliptic model represents the friction cone more directly.

Its constraint dimension is:

```text
constraint dimension = condim
```

Therefore:

```text
condim = 1
→ 1 dimension

condim = 3
→ 3 dimensions

condim = 4
→ 4 dimensions

condim = 6
→ 6 dimensions
```

For `condim=6`, the physical contact directions are:

```text
1 normal
2 sliding
1 torsional
2 rolling
```

Total:

```text
6 dimensions
```

---

## 10. Pyramidal Friction Cone

The pyramidal model approximates the friction cone using polyhedral edge directions.

For most frictional contacts:

```text
constraint dimension
=
2 × (condim - 1)
```

Therefore:

```text
condim = 3
→ 4 constraint directions

condim = 4
→ 6 constraint directions

condim = 6
→ 10 constraint directions
```

`condim=1` remains a one-dimensional normal contact.

---

## 11. Why Pyramidal Uses More Constraint Directions

The pyramidal representation splits friction directions into positive and negative edge directions.

For example:

```text
sliding direction 1
→ +m1
→ -m1

sliding direction 2
→ +m2
→ -m2
```

Therefore two sliding directions become four pyramidal constraint directions.

Similarly:

```text
torsional
→ +m3
→ -m3
```

and the two rolling directions become:

```text
+m4
-m4

+m5
-m5
```

Thus for `condim=6`:

```text
2 sliding directions
→ 4 constraints

1 torsional direction
→ 2 constraints

2 rolling directions
→ 4 constraints

total
→ 10 constraints
```

These are mathematical constraint directions, not ten different physical friction effects.

---

## 12. Elliptic vs Pyramidal Summary

```text
elliptic
→ smoother/direct friction-cone representation
→ constraint dimension = condim

pyramidal
→ polyhedral approximation
→ friction directions split into positive and negative edges
→ usually more constraint directions
```

A useful summary is:

| condim | elliptic | pyramidal |
|---|---:|---:|
| 1 | 1 | 1 |
| 3 | 3 | 4 |
| 4 | 4 | 6 |
| 6 | 6 | 10 |

---

## 13. Internal Friction Expansion

In MJCF, a geom uses three friction coefficients:

```text
[a, b, c]
```

where:

```text
a = sliding
b = torsional
c = rolling
```

Internally, MuJoCo expands these into five directional values:

```text
[a, a, b, c, c]
```

This corresponds to:

```text
2 sliding directions
1 torsional direction
2 rolling directions
```

So internally:

```text
friction[0]
→ sliding direction 1

friction[1]
→ sliding direction 2

friction[2]
→ torsional

friction[3]
→ rolling direction 1

friction[4]
→ rolling direction 2
```

The XML still only requires three friction values.

---

## 14. `priority`

When two geoms make contact, MuJoCo must decide which contact parameters to use.

One important parameter is:

```xml
priority="..."
```

If the two geoms have different priority values:

```text
higher priority
→ its contact parameters are selected
```

This can affect:

- friction
- `condim`
- `solref`
- `solimp`

---

## 15. Equal Priority

If the two geoms have equal priority, MuJoCo combines friction using the maximum of each component.

For example:

```text
geom A:
friction = 1.0 0.01 0.001

geom B:
friction = 0.6 0.02 0.0005
```

With equal priority, the resulting friction is:

```text
1.0 0.02 0.001
```

because each component is selected independently:

```text
sliding
→ max(1.0, 0.6)

torsional
→ max(0.01, 0.02)

rolling
→ max(0.001, 0.0005)
```

---

## 16. Why Negative Priority Is Useful in Experiments

In the friction comparison scene, the floor and slopes use:

```xml
priority="-1"
```

while moving objects use the default higher priority.

This means:

```text
moving object contact parameters
→ take priority over the floor or slope
```

This makes it possible to compare different:

```text
condim
friction
```

settings on otherwise similar surfaces.

---

## 17. `impratio`

`impratio` changes the relative impedance of frictional constraints.

A larger value can make friction constraints behave more strongly relative to normal constraints.

Conceptually:

```text
larger impratio
→ friction constraints act more strongly
→ sliding may become harder
```

However:

```text
impratio
```

should not be treated as a replacement for properly setting:

```text
friction
condim
contact parameters
solver settings
```

At the current learning stage, only the high-level meaning is necessary.

---

## 18. Practical Example - Boxes

Consider two boxes with identical friction coefficients:

```text
Box A
condim = 1

Box B
condim = 3
```

Both may define:

```xml
friction="1 0.005 0.0001"
```

However:

```text
Box A
→ only normal contact
→ sliding friction is not active

Box B
→ normal + sliding friction
→ friction[0] becomes active
```

Therefore Box A can slide much more easily under horizontal force.

---

## 19. Practical Example - Spheres

Consider two spheres:

```text
Sphere A
condim = 3

Sphere B
condim = 6
```

Both may use:

```xml
friction="1 0.01 0.01"
```

For Sphere A:

```text
normal
+
sliding friction
```

are active.

For Sphere B:

```text
normal
+
sliding
+
torsional
+
rolling
```

are active.

Therefore the second sphere can experience rolling resistance while the first does not use the full rolling-friction model.

---

## 20. Practical Example - Objects on Slopes

A slope experiment can compare:

```text
cylinder with condim=1
vs
cylinder with condim=3
```

The `condim=1` cylinder mainly experiences normal contact and can move down the slope more freely.

The `condim=3` cylinder also experiences sliding friction.

Similarly:

```text
sphere with condim=4
vs
sphere with condim=6
```

can demonstrate the additional effect of rolling friction.

---

## 21. Control-Variable Experiment Design

The friction example is essentially a control-variable experiment.

The scene keeps many properties similar while changing:

```text
condim
friction
priority
```

This makes it easier to observe how each contact setting affects motion.

The comparison structure is:

```text
Box
1 vs 3
→ sliding friction

Sphere
3 vs 6
→ rolling/torsional friction

Cylinder on slope
1 vs 3
→ sliding friction on slope

Sphere on slope
4 vs 6
→ rolling friction
```

---

## 22. Core Understanding

The most important relationships are:

```text
friction="a b c"

a
→ sliding friction

b
→ torsional friction

c
→ rolling friction
```

and:

```text
condim = 1
→ normal only

condim = 3
→ + sliding

condim = 4
→ + torsional

condim = 6
→ + rolling
```

Also:

```text
elliptic
→ constraint dimension = condim

pyramidal
→ approximately 2 × (condim - 1)
```

and:

```text
priority different
→ higher-priority geom wins

priority equal
→ friction components use the larger value
```

---

## 23. What to Remember

At the current stage, the most important points are:

```text
friction
→ strength of friction

condim
→ which friction modes exist

cone
→ mathematical representation of friction

priority
→ which geom's contact settings are used
```

The detailed solver equations and internal impedance calculations do not need to be memorized yet.

---

## Source

This note is based on the friction section of:

```text
Albusgive/mujoco_learning
```

Source repository:

https://github.com/Albusgive/mujoco_learning

The original repository and teaching material belong to the respective author(s).

This note records my own learning process, interpretation, example analysis, and understanding based on the source material.