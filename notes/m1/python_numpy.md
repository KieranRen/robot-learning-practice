# M1 — Python and NumPy Foundations

[English](python_numpy.md) | [中文](python_numpy_zh.md)

This note records my understanding of the Python and NumPy concepts used in M1. It focuses on the ideas that are most relevant to robotics and numerical computing rather than attempting to reproduce the source material.

## 1. Functions and Modules

A Python function packages a calculation so it can be reused.

```python
def millimeters_to_meters(value_mm: float) -> float:
    return value_mm / 1000.0
```

Key ideas:

- `def` defines a function.
- Function parameters are the inputs.
- `return` sends a result back to the caller.
- `print()` only displays information and does not replace `return`.
- Type hints such as `value_mm: float` and `-> float` document the intended interface but are not enforced in the same way as C types.

A `.py` file can also be used as a module.

```python
from examples.numeric_basics import translate_points
```

This imports `translate_points` from `examples/numeric_basics.py`.

The common pattern

```python
if __name__ == "__main__":
```

allows demonstration code to run when the module is executed directly without automatically running it when the module is imported elsewhere.

---

## 2. NumPy Arrays: `shape`, `ndim`, and `dtype`

For numerical robotics code, understanding array structure is essential.

Example:

```python
points = np.array([
    [0.0, 0.0],
    [1.0, 2.0]
], dtype=np.float64)
```

The array has:

```text
shape = (2, 2)
ndim  = 2
dtype = float64
```

Interpretation:

- `shape` describes the length of each axis.
- `ndim` is the number of axes.
- `dtype` describes how the elements are stored.

Examples:

```text
(3,)      -> one-dimensional array, ndim = 1
(3, 2)    -> two-dimensional array, ndim = 2
(2, 3, 4) -> three-dimensional array, ndim = 3
```

A one-dimensional array such as

```python
np.array([1.0, 2.0])
```

has shape `(2,)`.

It is not the same as:

```text
[[1.0, 2.0]]   -> shape (1, 2)

[[1.0],
 [2.0]]        -> shape (2, 1)
```

---

## 3. Indexing and Slicing

For a point array

```python
points = np.array([
    [0.0, 0.0],
    [1.0, 2.0],
    [3.0, 4.0]
])
```

common indexing operations include:

```python
points[1, 0]   # one scalar
points[1]      # one row
points[1:3]    # a slice of rows
points[:, 0]   # all rows, first column
```

Python slicing follows:

```text
[start : stop]
```

where `start` is included and `stop` is excluded.

For example:

```python
points[:2]
```

returns rows 0 and 1.

A particularly important distinction is:

```python
points[0]
```

which returns shape `(2,)`, while

```python
points[:1]
```

returns shape `(1, 2)`.

This distinction matters because later matrix and broadcasting operations depend on shape.

A new axis can be inserted using `None`:

```python
a = np.array([1.0, 2.0])

a[None, :].shape   # (1, 2)
a[:, None].shape   # (2, 1)
```

---

## 4. Views and Copies

NumPy slicing often returns a view that shares the original array's data.

```python
source = np.array([1.0, 2.0, 3.0])
view = source[:2]

view[0] = 9.0
```

Now:

```text
source = [9.0, 2.0, 3.0]
view   = [9.0, 2.0]
```

The original data changed because `view` shares memory with `source`.

To create an independent copy:

```python
independent = source[:2].copy()
```

A normal assignment such as

```python
other = source
```

does not copy the array. It only creates another reference to the same object.

This is important in experiments because temporary modifications can unintentionally change the original data.

---

## 5. Broadcasting

Broadcasting allows NumPy to perform elementwise operations on arrays with different shapes.

The basic rule is:

> Compare shapes from right to left. Each pair of dimensions is compatible if they are equal, one of them is `1`, or one side does not contain that dimension.

Examples:

```text
(3, 2) and (2,)   -> compatible
(3, 2) and (3,)   -> not compatible
(3, 2) and (3, 1) -> compatible
(3, 2) and (1, 2) -> compatible
```

Example:

```python
points = np.array([
    [0.0, 0.0],
    [1.0, 2.0]
])

offset = np.array([0.5, -1.0])

translated = points + offset
```

The `(2,)` offset is applied to every row.

Result:

```text
[[0.5, -1.0],
 [1.5,  1.0]]
```

An important lesson is:

> A broadcastable operation is not automatically a semantically correct operation.

For example, if each point should have a separate scale factor:

```python
scales = np.array([10.0, 100.0])
```

then

```python
points * scales
```

scales columns.

To scale rows independently:

```python
points * scales[:, None]
```

changes `scales` from shape `(2,)` to `(2, 1)`.

---

## 6. Vector Length

For a vector

```python
v = np.array([3.0, 4.0])
```

the Euclidean length is

\[
\|v\| = \sqrt{3^2 + 4^2} = 5.
\]

The expanded calculation is:

```python
squares = v * v
squared_length = np.sum(squares)
length = np.sqrt(squared_length)
```

This helps show the mathematical process.

In practical NumPy code, the simpler form is:

```python
np.linalg.norm(v)
```

Also,

```python
v @ v
```

computes the dot product of the vector with itself:

\[
v \cdot v = \|v\|^2.
\]

---

## 7. `*` Versus `@`

This distinction is essential.

```python
A * v
```

means elementwise multiplication, with broadcasting if required.

```python
A @ v
```

means matrix multiplication.

Example:

```python
A = np.array([
    [1.0, 2.0],
    [0.0, 1.0]
])

v = np.array([3.0, 4.0])
```

Matrix multiplication:

```python
A @ v
```

gives:

```text
[11.0, 4.0]
```

because:

\[
1(3) + 2(4) = 11
\]

and

\[
0(3) + 1(4) = 4.
\]

Elementwise multiplication:

```python
A * v
```

gives:

```text
[[3.0, 8.0],
 [0.0, 4.0]]
```

For two-dimensional matrices:

```text
(m, n) @ (n, k) -> (m, k)
```

The inner dimensions must match.

---

## 8. Physical Units

NumPy does not know the physical meaning of a number.

For example:

```python
np.array([500.0, -1000.0])
```

does not indicate whether the values are in metres, millimetres, or another unit.

Therefore units must be managed explicitly through:

- variable names
- documentation
- function interfaces
- conversions

Example:

```python
v_mm = np.array([3000.0, 4000.0])
v_m = v_mm / 1000.0
```

If metre and millimetre values are mixed, the array shape and numerical type can still look correct while the physical result is wrong by a factor of 1000.

---

## 9. Floating-Point Error

Floating-point values do not exactly represent every decimal number.

For example:

```python
0.1 + 0.2
```

is not necessarily stored exactly as `0.3`.

Therefore:

```python
actual == expected
```

may produce `False` even when the mathematical values should be considered equal.

For numerical calculations, it is better to use:

```python
np.allclose(actual, expected)
```

or in tests:

```python
np.testing.assert_allclose(actual, expected)
```

The approximate comparison follows:

\[
|actual - expected|
\le
atol + rtol \cdot |expected|.
\]

`atol` is the absolute tolerance.

`rtol` is the relative tolerance.

Near zero, absolute tolerance is especially important because the relative reference value is also close to zero.

Tolerance should come from the numerical or physical requirements of the problem, not simply be increased until a test passes.

---

## 10. Automated Testing with `pytest`

Three common forms of checks are:

### Shape or logical checks

```python
assert result.shape == (2, 2)
```

### Numerical checks

```python
np.testing.assert_allclose(
    result,
    expected,
    rtol=0.0,
    atol=1e-12
)
```

### Expected errors

```python
with pytest.raises(ValueError):
    function_with_invalid_input(...)
```

A useful test suite should verify:

- valid inputs produce correct results
- output shapes are correct
- numerical values are correct within tolerance
- invalid inputs are rejected

A passing test suite only proves that the tested conditions passed. It does not prove that every possible bug or physical modelling error has been eliminated.

---

## 11. `translate_points`

`translate_points` is a project-defined function rather than a NumPy function.

Its conceptual interface is:

```text
points: (N, D)
offset: (D,)
```

where:

- `N` is the number of points
- `D` is the coordinate dimension

The core calculation is:

```python
points_array + offset_array
```

which uses broadcasting to apply the same translation to every point.

Example:

```python
translate_points(
    [[0.0, 0.0], [1.0, 2.0]],
    [0.5, -1.0]
)
```

produces:

```text
[[0.5, -1.0],
 [1.5,  1.0]]
```

The function also checks its input contract so that shapes such as `(1, D)` are not silently accepted where `(D,)` is required.

---

## 12. Main Lessons

The most important ideas I want to retain from this section are:

1. Always inspect array `shape` before assuming what an array represents.
2. `(N,)`, `(1, N)`, and `(N, 1)` are different structures.
3. Slices can share data with the original array; use `.copy()` when independent data is required.
4. Broadcasting follows shape rules, but valid broadcasting does not guarantee correct physical meaning.
5. Use `@` for matrix multiplication and `*` for elementwise multiplication.
6. NumPy does not track physical units.
7. Floating-point results should usually be compared with tolerances.
8. Tests should check shape, values, and expected failures separately.
9. Numerical code should be both mathematically correct and explicit about its interface assumptions.