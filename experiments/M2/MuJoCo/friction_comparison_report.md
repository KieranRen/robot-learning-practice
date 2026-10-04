# Friction Comparison Experiment

[English](friction_comparison_report.md) | [中文](friction_comparison_report_zh.md)

---

## 1. Purpose

This experiment was created to verify and reinforce the MuJoCo friction concepts studied in the Albusgive MuJoCo learning source.

The main goals are to compare:

- `condim=1` vs `condim=3`
- `condim=3` vs `condim=6`
- `condim=4` vs `condim=6`
- the effect of different friction modes
- the role of `priority`
- the relationship between `friction` and `condim`

The core question is:

> How does changing the contact dimension affect the types of friction that are actually active?

---

## 2. Model File

The experiment model is stored in:

```text
experiments/M2/MuJoCo/friction_comparison.xml
```

The model contains four comparison groups:

```text
Group 1
Box: condim 1 vs 3

Group 2
Sphere: condim 3 vs 6

Group 3
Cylinder on slope: condim 1 vs 3

Group 4
Sphere on slope: condim 4 vs 6
```

---

## 3. Global Simulation Settings

The model uses:

```xml
<option
    timestep="0.002"
    gravity="0 0 -9.81"
    integrator="implicitfast"
    cone="elliptic"
    impratio="1"/>
```

Important settings:

```text
timestep = 0.002 s
→ simulation advances by 2 ms per physics step

gravity = 0 0 -9.81
→ normal Earth-like gravity

integrator = implicitfast
→ implicit integrator used for stable simulation

cone = elliptic
→ elliptic friction-cone representation

impratio = 1
→ default relative friction-constraint impedance setting for this experiment
```

---

## 4. Friction Parameters

MuJoCo uses:

```xml
friction="a b c"
```

where:

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
friction="1 0.005 0.0001"
```

means:

```text
sliding friction = 1
torsional friction = 0.005
rolling friction = 0.0001
```

However, defining all three values does not mean that all three friction modes are automatically active.

That depends on:

```text
condim
```

---

## 5. Role of `condim`

The main values used in this experiment are:

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

This means:

```text
friction
→ defines friction strength

condim
→ determines which friction modes are included in the contact model
```

This experiment was designed to make that difference visible.

---

# Experiment Group 1 - Box Comparison

## 6. Box with `condim=1`

The first box uses:

```xml
friction="1 0.005 0.0001"
condim="1"
```

Although the friction coefficients are defined, the contact model only includes:

```text
normal contact
```

Sliding friction is not active in the contact constraint.

Therefore the box can move much more freely along the floor.

---

## 7. Box with `condim=3`

The second box uses:

```xml
friction="1 0.005 0.0001"
condim="3"
```

Now the contact includes:

```text
normal contact
+
two sliding friction directions
```

Therefore the first friction coefficient becomes physically relevant.

The box should resist tangential motion more strongly than the `condim=1` box.

---

## 8. Expected Comparison

The key comparison is:

```text
Box A
condim = 1
→ no sliding friction mode

Box B
condim = 3
→ sliding friction enabled
```

Therefore:

```text
Box A
→ easier to slide

Box B
→ stronger resistance to sliding
```

The main variable is `condim`.

---

# Experiment Group 2 - Sphere Comparison

## 9. Sphere with `condim=3`

The first sphere uses:

```xml
friction="1 0.01 0.01"
condim="3"
```

This enables:

```text
normal contact
+
sliding friction
```

but does not include:

```text
torsional friction
rolling friction
```

as full contact dimensions.

---

## 10. Sphere with `condim=6`

The second sphere uses:

```xml
friction="1 0.01 0.05"
condim="6"
```

This enables:

```text
normal
+
sliding
+
torsional
+
rolling
```

The rolling-friction coefficient is intentionally more noticeable:

```text
rolling friction = 0.05
```

so the effect can be observed more clearly.

---

## 11. Expected Comparison

The comparison is:

```text
Sphere A
condim = 3

Sphere B
condim = 6
```

The second sphere contains additional resistance modes, especially rolling resistance.

Therefore the `condim=6` sphere should lose rolling motion more strongly than the `condim=3` sphere.

---

# Experiment Group 3 - Cylinders on a Slope

## 12. Purpose of the Slope

A slope makes the effect of gravity easier to observe.

The gravitational component along the slope tends to move the cylinder downward.

This provides a natural driving force without requiring an actuator.

---

## 13. Cylinder with `condim=1`

The first cylinder uses:

```xml
condim="1"
```

This means:

```text
normal contact only
```

The cylinder therefore receives little or no sliding-friction resistance from the contact model.

It should move down the slope relatively easily.

---

## 14. Cylinder with `condim=3`

The second cylinder uses:

```xml
condim="3"
```

This enables sliding friction.

Therefore the motion down the slope should be more strongly resisted.

---

## 15. Expected Comparison

```text
Cylinder A
condim = 1
→ mainly normal support

Cylinder B
condim = 3
→ normal + sliding friction
```

Expected behavior:

```text
condim=1
→ moves down the slope more freely

condim=3
→ stronger resistance to motion
```

---

# Experiment Group 4 - Spheres on a Slope

## 16. Sphere with `condim=4`

The first slope sphere uses:

```xml
friction="1 0.01 0.05"
condim="4"
```

This enables:

```text
normal
+
sliding
+
torsional
```

but not full rolling-friction dimensions.

---

## 17. Sphere with `condim=6`

The second sphere uses:

```xml
friction="1 0.01 0.05"
condim="6"
```

This includes:

```text
normal
+
sliding
+
torsional
+
rolling
```

Therefore rolling resistance becomes part of the contact model.

---

## 18. Expected Comparison

The key comparison is:

```text
condim = 4
→ no rolling-friction dimensions

condim = 6
→ rolling-friction dimensions enabled
```

Since both spheres use the same rolling-friction coefficient:

```text
0.05
```

the main difference comes from whether rolling friction is actually enabled by `condim`.

This makes the comparison more meaningful.

---

# Contact Priority

## 19. Floor and Slope Priority

The floor and slopes use:

```xml
priority="-1"
```

The moving objects use:

```xml
priority="0"
```

Therefore:

```text
moving-object priority
>
surface priority
```

This was intentional.

---

## 20. Why Priority Matters

When two geoms have different priority values, the higher-priority geom determines important contact settings.

This can include:

```text
friction
condim
solref
solimp
```

Therefore using:

```text
surface priority = -1
moving object priority = 0
```

allows each moving object to define the contact behavior used in the comparison.

This avoids the floor or slope overriding the intended `condim` setting.

---

## 21. Control-Variable Design

The experiment follows a control-variable approach.

For each pair, the model tries to keep most properties similar while changing one important contact setting.

Examples:

```text
box
→ same general geometry and friction
→ change condim 1 to 3
```

```text
sphere
→ similar geometry
→ change condim 3 to 6
```

```text
slope sphere
→ same friction values
→ change condim 4 to 6
```

This makes it easier to connect observed motion to a specific contact-model change.

---

# Friction Cone

## 22. Elliptic Friction Cone

The model uses:

```xml
cone="elliptic"
```

For the elliptic friction-cone representation:

```text
constraint dimension
=
condim
```

Therefore:

```text
condim = 1
→ 1 contact dimension

condim = 3
→ 3 contact dimensions

condim = 4
→ 4 contact dimensions

condim = 6
→ 6 contact dimensions
```

This experiment therefore uses a direct correspondence between:

```text
condim
and
contact constraint dimension
```

---

## 23. Physical Interpretation

For `condim=6`, the contact includes:

```text
1 normal direction
2 sliding directions
1 torsional direction
2 rolling directions
```

Total:

```text
6 dimensions
```

This is why the values progress as:

```text
1 → 3 → 4 → 6
```

rather than:

```text
1 → 2 → 3 → 4
```

---

# Model Independence

## 24. No External Asset Dependency

An earlier learning example used an external skybox file such as:

```text
../asset/desert.png
```

When that asset was not present locally, MuJoCo Viewer could not load the model.

For this experiment, the external dependency was removed.

Instead, the floor uses a built-in checker texture:

```xml
builtin="checker"
```

This makes the experiment more portable and easier to reproduce.

---

## 25. Why This Matters

A learning experiment should ideally be:

```text
easy to copy
easy to run
easy to inspect
easy to reproduce
```

Removing unnecessary external dependencies helps achieve this.

---

# Results and Interpretation

## 26. Main Learning Result

The most important conclusion from the experiment is:

```text
friction coefficients alone are not enough
```

The actual contact behavior depends strongly on:

```text
condim
```

because `condim` determines which friction directions exist in the contact model.

---

## 27. Core Relationship

The experiment reinforces:

```text
friction
→ how strong a friction mode is

condim
→ whether that friction mode exists

priority
→ which geom's contact settings dominate

cone
→ how the friction constraints are represented mathematically
```

These parameters work together.

---

## 28. Main Comparison Summary

```text
Box
condim 1 vs 3
→ sliding friction

Sphere
condim 3 vs 6
→ additional torsional and rolling friction

Cylinder on slope
condim 1 vs 3
→ sliding resistance under gravity

Sphere on slope
condim 4 vs 6
→ rolling-friction effect
```

---

## 29. What I Learned

Before this experiment, it was easy to think that:

```text
friction="1 0.01 0.05"
```

automatically meant that all three friction types were active.

The experiment clarifies that this is not correct.

Instead:

```text
friction values
+
condim
```

must be interpreted together.

For example:

```text
rolling friction coefficient exists
but condim = 4
→ rolling-friction dimensions are not enabled
```

while:

```text
rolling friction coefficient exists
and condim = 6
→ rolling friction can affect the contact
```

This distinction is one of the most important results of this learning section.

---

## 30. Current Understanding

At the current stage, the most useful mental model is:

```text
friction
→ strength

condim
→ enabled friction modes

priority
→ whose contact settings are used

cone
→ mathematical representation
```

The detailed solver implementation is not yet necessary for practical model construction.

---

## Source

This experiment is based on concepts studied from:

```text
Albusgive/mujoco_learning
```

Source repository:

https://github.com/Albusgive/mujoco_learning

The XML model and this report were reorganized as part of my own learning and verification process.

The purpose of this experiment is to record my understanding of MuJoCo contact and friction behavior rather than reproduce the original source material.