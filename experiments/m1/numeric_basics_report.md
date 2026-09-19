# M1 Experiment Report — Python and NumPy Foundations

## Overview

This report records the execution and verification of the M1 Python and NumPy numerical examples.

The purpose of this experiment is to verify that the numerical examples run correctly in the configured development environment and that the corresponding automated tests pass.

## Environment

The experiment was executed using the project Conda environment:

```text
robot_manipulation_learning
```

Relevant software versions:

```text
Python 3.11.16
NumPy 2.4.6
pytest 8.4.2
```

Reference learning material:

```text
knowledge tag: v0.2.0
```

## Files

The main implementation and test files used in this experiment are:

```text
examples/numeric_basics.py
tests/test_numeric_basics.py
```

## Commands

The numerical example was executed with:

```bash
python -m examples.numeric_basics
```

The automated tests were executed with:

```bash
python -m pytest tests/test_numeric_basics.py -q
```

## Observed Output

The example produced four main categories of output:

### 1. Array Operations

```text
ARRAY | points shape=(2, 2) dtype=float64
ARRAY | offset shape=(2,); translated (m)=[[0.5, -1.0], [1.5, 1.0]]
ARRAY | after view edit: source=[9.0, 2.0, 3.0] copy=[1.0, 2.0]
```

This verifies several NumPy concepts:

- the point set has shape `(2, 2)`
- the offset has shape `(2,)`
- broadcasting applies the same offset to every point
- a slice may share data with the original array
- `.copy()` creates independent data

The translated points are:

```text
[0.0, 0.0] + [0.5, -1.0] = [0.5, -1.0]

[1.0, 2.0] + [0.5, -1.0] = [1.5, 1.0]
```

## 2. Vector Length

Observed output:

```text
VECTOR | components (m)=[3.0, 4.0] squares (m^2)=[9.0, 16.0]
VECTOR | squared length=25.0 m^2; length=5.0 m
```

The mathematical calculation is:

```math
3^2+4^2=25
```

and therefore:

```math
\sqrt{25}=5
```

This verifies that the Euclidean length of the vector `[3, 4]` is 5.

## 3. Matrix Operations

Observed output:

```text
MATRIX | A @ v=[11.0, 4.0]
MATRIX | A * v=[[3.0, 8.0], [0.0, 4.0]]
```

This demonstrates the difference between:

```python
A @ v
```

and:

```python
A * v
```

`@` performs matrix multiplication, while `*` performs elementwise multiplication with NumPy broadcasting.

The matrix-vector multiplication produces:

```math
\begin{bmatrix}
1 & 2\\
0 & 1
\end{bmatrix}
\begin{bmatrix}
3\\
4
\end{bmatrix}
=
\begin{bmatrix}
11\\
4
\end{bmatrix}
```

## 4. Floating-Point and Error Checks

Observed output:

```text
ERROR | equal elementwise=[False, True]
ERROR | max absolute residual=5.551e-17
ERROR | allclose(rtol=0, atol=1e-12)=True
ERROR | accidental (2, 1) - (2,) shape=(2, 2)
ERROR | expected rejection: offset must have shape (2,)
```

The first comparison shows that direct floating-point equality can fail:

```python
0.1 + 0.2 == 0.3
```

is not necessarily `True` internally.

The observed residual was approximately:

```text
5.551e-17
```

which is extremely small.

Using:

```python
np.allclose(...)
```

with an appropriate tolerance therefore gives:

```text
True
```

The shape example also demonstrates an important risk:

```text
(2, 1) - (2,)
```

broadcasts to:

```text
(2, 2)
```

Although NumPy allows the operation, the result may not represent the intended mathematical meaning.

The implementation therefore explicitly rejects invalid offset shapes.

## Automated Test Result

The test command produced:

```text
22 passed
```

This indicates that all 22 automated checks in `tests/test_numeric_basics.py` passed in the current environment.

A passing test suite confirms that the tested conditions behave as expected, but it does not prove that every possible bug or modelling error has been eliminated.

## What This Experiment Demonstrates

This experiment provides executable evidence of understanding and verification of:

- NumPy array shape and dtype
- indexing, slicing, views, and copies
- broadcasting
- vector length
- matrix multiplication
- elementwise multiplication
- floating-point comparison
- input shape validation
- automated testing with `pytest`

## Key Reflection

The main lesson from this experiment is that numerical code can execute successfully while still containing semantic mistakes.

In robotics code, correctness depends not only on whether NumPy accepts an operation, but also on:

- array shape
- coordinate meaning
- physical units
- mathematical operation
- numerical tolerance
- interface assumptions

For this reason, numerical examples should be checked using both mathematical reasoning and automated tests.