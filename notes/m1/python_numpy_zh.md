# M1 — Python 与 NumPy 基础

[English](python_numpy.md) | [中文](python_numpy_zh.md)

这份笔记记录我在 M1 中对 Python 和 NumPy 基础内容的理解。重点放在机器人与数值计算中真正会反复用到的概念，而不是简单复述教材内容。

## 1. 函数与模块

Python 函数可以把一段计算封装起来，方便重复使用。

```python
def millimeters_to_meters(value_mm: float) -> float:
    return value_mm / 1000.0
```

关键点：

- `def` 用来定义函数。
- 参数是函数的输入。
- `return` 把结果返回给调用者。
- `print()` 只是把内容显示出来，不能代替 `return`。
- `value_mm: float` 和 `-> float` 属于类型提示，用来说明预期接口，但不像 C 语言那样强制限制运行时类型。

一个 `.py` 文件也可以作为模块被其他代码导入。

```python
from examples.numeric_basics import translate_points
```

这表示从 `examples/numeric_basics.py` 中导入 `translate_points` 函数。

常见写法：

```python
if __name__ == "__main__":
```

表示只有当这个模块被直接运行时，下面的演示代码才执行；如果这个模块只是被其他文件导入，则不会自动运行这些演示代码。

---

## 2. NumPy 数组：`shape`、`ndim` 与 `dtype`

在机器人数值代码中，理解数组结构非常重要。

例如：

```python
points = np.array([
    [0.0, 0.0],
    [1.0, 2.0]
], dtype=np.float64)
```

这个数组具有：

```text
shape = (2, 2)
ndim  = 2
dtype = float64
```

含义分别是：

- `shape`：每条轴的长度。
- `ndim`：数组一共有多少条轴。
- `dtype`：数组中的元素按什么数据类型存储。

例如：

```text
(3,)      -> 一维数组，ndim = 1
(3, 2)    -> 二维数组，ndim = 2
(2, 3, 4) -> 三维数组，ndim = 3
```

例如：

```python
np.array([1.0, 2.0])
```

shape 是：

```text
(2,)
```

它只是一个长度为 2 的一维数组。

它和下面两种结构不同：

```text
[[1.0, 2.0]]   -> shape (1, 2)

[[1.0],
 [2.0]]        -> shape (2, 1)
```

因此：

```text
(2,)
(1, 2)
(2, 1)
```

虽然都包含两个数，但它们在 NumPy 中是不同的结构。

---

## 3. 索引与切片

假设有一个点集：

```python
points = np.array([
    [0.0, 0.0],
    [1.0, 2.0],
    [3.0, 4.0]
])
```

常见索引方式包括：

```python
points[1, 0]   # 取一个具体元素
points[1]      # 取一整行
points[1:3]    # 取一段行
points[:, 0]   # 所有行的第 0 列
```

Python 切片使用：

```text
[start : stop]
```

规则是：

> 包含 `start`，不包含 `stop`。

例如：

```python
points[:2]
```

得到第 0 行和第 1 行。

一个非常重要的区别是：

```python
points[0]
```

结果 shape 是：

```text
(2,)
```

而：

```python
points[:1]
```

结果 shape 是：

```text
(1, 2)
```

前者表示“取一个点”，后者表示“取一个包含 1 个点的批次”。

这个区别很重要，因为后面的矩阵运算和 broadcasting 都会受到 shape 影响。

可以使用 `None` 插入新的轴：

```python
a = np.array([1.0, 2.0])

a[None, :].shape   # (1, 2)
a[:, None].shape   # (2, 1)
```

---

## 4. View 与 Copy

NumPy 的普通切片通常返回一个 view，也就是和原数组共享底层数据。

例如：

```python
source = np.array([1.0, 2.0, 3.0])
view = source[:2]

view[0] = 9.0
```

此时：

```text
source = [9.0, 2.0, 3.0]
view   = [9.0, 2.0]
```

原因是 `view` 并没有真正复制数据，而是共享 `source` 的前两个元素。

如果希望得到独立副本，可以使用：

```python
independent = source[:2].copy()
```

这样后续修改其中一个数组，不会影响另一个。

另外：

```python
other = source
```

也不会创建副本，只是给同一个数组对象增加了另一个变量名。

---

## 5. Broadcasting

Broadcasting 允许 NumPy 对 shape 不完全相同的数组进行逐元素运算。

核心规则是：

> 从 shape 的最右边开始比较。每一维只要满足以下任意条件，就可以兼容：
>
> - 两个维度相等
> - 其中一个维度是 `1`
> - 某一边不存在这一维

例如：

```text
(3, 2) 和 (2,)   -> 可以广播
(3, 2) 和 (3,)   -> 不可以广播
(3, 2) 和 (3, 1) -> 可以广播
(3, 2) 和 (1, 2) -> 可以广播
```

例如：

```python
points = np.array([
    [0.0, 0.0],
    [1.0, 2.0]
])

offset = np.array([0.5, -1.0])

translated = points + offset
```

结果：

```text
[[0.5, -1.0],
 [1.5,  1.0]]
```

一个非常重要的经验是：

> 可以广播，并不代表这个运算在物理或数学意义上一定正确。

如果想让每一行分别使用一个缩放系数：

```python
scales = np.array([10.0, 100.0])
```

需要写：

```python
points * scales[:, None]
```

而不是直接：

```python
points * scales
```

---

## 6. 向量长度

对于：

```python
v = np.array([3.0, 4.0])
```

欧几里得长度为：

$$
\|v\| = \sqrt{3^2 + 4^2} = 5
$$

展开计算：

```python
squares = v * v
squared_length = np.sum(squares)
length = np.sqrt(squared_length)
```

实际 NumPy 中更方便：

```python
np.linalg.norm(v)
```

另外：

```python
v @ v
```

计算：

$$
v \cdot v = \|v\|^2
$$

---

## 7. `*` 与 `@`

```python
A * v
```

表示逐元素乘法。

```python
A @ v
```

表示矩阵乘法。

例如：

```python
A = np.array([
    [1.0, 2.0],
    [0.0, 1.0]
])

v = np.array([3.0, 4.0])
```

则：

```python
A @ v
```

得到：

```text
[11.0, 4.0]
```

因为：

$$
1(3)+2(4)=11
$$

以及：

$$
0(3)+1(4)=4
$$

而：

```python
A * v
```

得到：

```text
[[3.0, 8.0],
 [0.0, 4.0]]
```

---

## 8. 物理单位

NumPy 不知道一个数字表示米、毫米还是其他单位。

例如：

```python
np.array([500.0, -1000.0])
```

本身没有物理单位信息。

因此单位必须通过变量命名、接口和显式转换管理。

例如：

```python
v_mm = np.array([3000.0, 4000.0])
v_m = v_mm / 1000.0
```

毫米和米混用时，程序可能完全不报错，但结果会差 1000 倍。

---

## 9. 浮点误差

计算机无法精确表示所有十进制小数。

例如：

```python
0.1 + 0.2
```

通常不会和 `0.3` 完全相同。

所以：

```python
actual == expected
```

可能得到 `False`。

更合适的是：

```python
np.allclose(actual, expected)
```

或者测试中：

```python
np.testing.assert_allclose(actual, expected)
```

近似比较满足：

$$
|actual - expected|
\le
atol + rtol \cdot |expected|
$$

其中：

- `atol`：绝对容差
- `rtol`：相对容差

接近 0 时尤其需要关注 `atol`。

---

## 10. 使用 `pytest` 做自动测试

Shape 检查：

```python
assert result.shape == (2, 2)
```

数值检查：

```python
np.testing.assert_allclose(
    result,
    expected,
    rtol=0.0,
    atol=1e-12
)
```

预期异常：

```python
with pytest.raises(ValueError):
    function_with_invalid_input(...)
```

测试应该同时覆盖：

- 正常输入
- shape
- 数值
- 错误输入

测试通过并不代表所有 bug 或物理建模问题都不存在。

---

## 11. `translate_points`

`translate_points` 是项目自己定义的函数，不是 NumPy 自带函数。

接口：

```text
points: (N, D)
offset: (D,)
```

核心计算：

```python
points_array + offset_array
```

例如：

```python
translate_points(
    [[0.0, 0.0], [1.0, 2.0]],
    [0.5, -1.0]
)
```

结果：

```text
[[0.5, -1.0],
 [1.5,  1.0]]
```

---

## 12. 这一部分最需要长期记住的内容

1. 看到 NumPy 数组时，先看 `shape`。
2. `(N,)`、`(1,N)` 和 `(N,1)` 不相同。
3. 普通切片可能共享原数据。
4. Broadcasting 能运行不代表数学意义正确。
5. `@` 是矩阵乘法，`*` 是逐元素乘法。
6. NumPy 不会管理物理单位。
7. 浮点数通常需要容差比较。
8. 测试应分别检查 shape、数值和错误输入。
9. 数值代码必须明确接口、单位和数学含义。