# Rigid Transforms

本目录提供 M1 坐标变换练习使用的最小实现。只依赖已有 NumPy，支持 Python 3.10 及以上版本。项目步骤与数学说明从 [M1 入口](../../projects/M1_robot_math/README.md) 查阅。

## 约定与公式

采用右手坐标系，位置单位为米，角度单位为弧度。`T_ab` 将 B 系坐标转换为 A 系坐标，旋转列向量表示 B 系各轴在 A 系中的方向，平移表示 B 系原点在 A 系的位置。

```text
p_a = R_ab @ p_b + t_ab
T_ab = [[R_ab, t_ab], [0, 0, 0, 1]]
T_ac = T_ab @ T_bc
T_ba = [[R_ab.T, -R_ab.T @ t_ab], [0, 0, 0, 1]]
```

这些规则对应 Kevin M. Lynch 与 Frank C. Park 的 [Modern Robotics 第 3.3.1 节](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-1-homogeneous-transformation-matrices/)。本目录为按公式编写的教学实现，没有引入教材软件包。

数学中的点使用列向量。API 为便于批量处理，将每个点存成数组的一行；因此 `points` 必须是 `(N, 3)`，单点也写成 `[[x, y, z]]`。实现中的 `(R @ points.T).T + t` 保留了列向量公式，结果仍为 `(N, 3)`。

## 接口与输入检查

从 `algorithms.geometry` 导入以下函数。

| 函数 | 输入与返回 |
| --- | --- |
| `rotation_z(angle_rad)` | 有限实数标量，返回绕正 z 轴旋转的 `(3, 3)` 矩阵 |
| `make_transform(rotation, translation)` | 输入 `(3, 3)` 旋转与 `(3,)` 平移，返回 `(4, 4)` 齐次变换 |
| `inverse_transform(transform)` | 输入 `(4, 4)` 齐次变换，直接按转置与平移公式返回逆变换 |
| `transform_points(transform, points)` | 输入变换和 `(N, 3)` 点，返回目标坐标；允许 `(0, 3)` 空点集 |

支持由整数或浮点数组成的列表与 NumPy 数组，结果为 `float64`。形状、实数与有限性不满足时抛出 `ValueError`。旋转要求 `R.T @ R = I` 且 `det(R) = +1`，齐次变换底行为 `[0, 0, 0, 1]`；这些数值检查使用绝对容差 `1e-9`、相对容差 `0`。输入错误不会被自动投影为旋转矩阵。极端数值使点或逆平移溢出时也会报错。

组合直接使用 `@`，先检查相邻坐标下标能否连接。[NumPy 的 `matmul` 文档](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html) 说明 `@` 的矩阵乘法语义；它不同于逐元素相乘的 `*`。[`allclose` 文档](https://numpy.org/doc/stable/reference/generated/numpy.allclose.html) 说明容差比较和广播，因此本实现先检查形状，再检查数值条件。

## 可观察示例

在仓库根目录运行，使用当前任务对应的环境。

```bash
python -m examples.coordinate_frames --output outputs/m1/frames.svg
```

固定场景为 `T_wa = Rz(pi/2), t=[1,0,0]`，`T_ab = Rz(-pi/2), t=[1,0,0]`，`p_b=[[1,0,0]]`。应观察到 A 系原点位于 W 系 `(1,0,0)`，B 系原点位于 `(1,1,0)`，点的 W 系坐标为 `[[2,1,0]]`。逆变换将点送回 B 系，最大坐标误差应接近浮点舍入误差。

交换相乘顺序会得到数值结果 `[[2,-1,0]]`。逆序矩阵的坐标下标不构成 B 到 W 的变换链，示例将其明确标为错误顺序的数值反例。

终端日志显示各矩阵、点和往返误差。指定 `--output` 时用标准库生成 SVG，并自动创建父目录；同一路径再次运行会覆盖该示例图。不指定时只输出日志。图展示固定场景的 XY 切片、W/A/B 坐标箭头及两个计算结果，正 z 轴朝向纸外，不能据此检验任意三维场景。

## 验证范围

```bash
python -m pytest tests/test_rigid_transform.py tests/test_coordinate_frames.py
```

测试检查手算变换、非交换性、非平面旋转、点集往返与距离不变性，拒绝错误形状、反射、非正交旋转和非有限值；另检查 SVG 的 XML、标签、点位与网格数值，以及命令行输出路径。实际运行环境与结果随本次任务记录。本实现不包含旋转估计、四元数、机器人运动学或仿真接口。
