from __future__ import annotations
from algorithms.geometry import make_transform, rotation_z

import numpy as np
from numpy.typing import ArrayLike, NDArray


def millimeters_to_meters(values: ArrayLike) -> NDArray[np.float64]:
    """Convert finite real millimeter values to meters.

    The output keeps the same shape as the input, uses float64,
    and does not modify the caller's data.
    """

    array = np.asarray(values)

    if array.dtype.kind not in "iuf":
        raise ValueError("values must contain real integer or floating-point data")

    array = np.asarray(array, dtype=np.float64)

    if not np.isfinite(array).all():
        raise ValueError("values must contain finite float64 values")

    return array / 1000.0

def translate_points_example() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return points, offset, and correctly broadcast translated points."""

    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 2.0, 3.0],
        ]
    )

    offset = np.array([1.0, -1.0, 0.5])

    shifted = points + offset

    return points, offset, shifted


def matrix_vs_elementwise_example() -> tuple[np.ndarray, np.ndarray]:
    """Show the difference between matrix multiplication and elementwise multiplication."""

    R = np.array(
        [
            [1.0, 2.0],
            [3.0, 4.0],
        ]
    )

    p = np.array([5.0, 6.0])

    matrix_result = R @ p
    elementwise_result = R * p

    return matrix_result, elementwise_result

def _validate_rigid_transform(T: ArrayLike) -> NDArray[np.float64]:
    """Validate and return a 4x4 rigid transform as float64."""

    transform = np.asarray(T)

    if transform.dtype.kind not in "iuf":
        raise ValueError("T must contain real integer or floating-point data")

    transform = np.asarray(transform, dtype=np.float64)

    if transform.shape != (4, 4):
        raise ValueError("T must have shape (4, 4)")

    if not np.isfinite(transform).all():
        raise ValueError("T must contain finite float64 values")

    if not np.allclose(
        transform[3],
        [0.0, 0.0, 0.0, 1.0],
        rtol=0.0,
        atol=1e-9,
    ):
        raise ValueError("T must have homogeneous bottom row [0, 0, 0, 1]")

    R = transform[:3, :3]

    if not np.allclose(
        R.T @ R,
        np.eye(3),
        rtol=0.0,
        atol=1e-9,
    ):
        raise ValueError("T must contain an orthogonal rotation matrix")

    if not np.isclose(
        np.linalg.det(R),
        1.0,
        rtol=0.0,
        atol=1e-9,
    ):
        raise ValueError("T rotation must have determinant +1")

    return transform


def apply_transform(
    T: ArrayLike,
    points: ArrayLike,
) -> NDArray[np.float64]:
    """Apply a rigid transform to an (N, 3) batch of points."""

    transform = _validate_rigid_transform(T)

    point_array = np.asarray(points)

    if point_array.dtype.kind not in "iuf":
        raise ValueError("points must contain real integer or floating-point data")

    point_array = np.asarray(point_array, dtype=np.float64)

    if point_array.ndim != 2 or point_array.shape[1] != 3:
        raise ValueError("points must have shape (N, 3)")

    if not np.isfinite(point_array).all():
        raise ValueError("points must contain finite float64 values")

    R = transform[:3, :3]
    t = transform[:3, 3]

    try:
        with np.errstate(over="raise", invalid="raise"):
            result = point_array @ R.T + t
    except FloatingPointError as error:
        raise ValueError("transformed points exceed the finite float64 range") from error

    if not np.isfinite(result).all():
        raise ValueError("transformed points exceed the finite float64 range")

    return result


def invert_transform(T: ArrayLike) -> NDArray[np.float64]:
    """Return the inverse of a rigid 4x4 transform."""

    transform = _validate_rigid_transform(T)

    R = transform[:3, :3]
    t = transform[:3, 3]

    R_inv = R.T
    t_inv = -R_inv @ t

    inverse = np.eye(4, dtype=np.float64)
    inverse[:3, :3] = R_inv
    inverse[:3, 3] = t_inv

    return inverse

def transform_chain_example() -> dict[str, np.ndarray | float]:
    """Compare correct transform composition with a reversed-order failure case."""

    T_wa = make_transform(
        rotation_z(np.pi / 2),
        [1.0, 0.0, 0.0],
    )

    T_ab = make_transform(
        rotation_z(-np.pi / 2),
        [1.0, 0.0, 0.0],
    )

    p_b = np.array([[1.0, 0.0, 0.0]])

    # Path 1: B -> A -> W
    p_a = apply_transform(T_ab, p_b)
    p_w_stepwise = apply_transform(T_wa, p_a)

    # Path 2: compose first, then transform once
    T_wb = T_wa @ T_ab
    p_w_composed = apply_transform(T_wb, p_b)

    # Round trip: W -> B
    T_bw = invert_transform(T_wb)
    p_b_recovered = apply_transform(T_bw, p_w_composed)

    max_round_trip_error = float(
        np.max(np.abs(p_b_recovered - p_b))
    )

    # Controlled failure: wrong composition order
    T_wrong = T_ab @ T_wa
    p_wrong = apply_transform(T_wrong, p_b)

    return {
        "T_wa": T_wa,
        "T_ab": T_ab,
        "T_wb": T_wb,
        "p_b": p_b,
        "p_w_stepwise": p_w_stepwise,
        "p_w_composed": p_w_composed,
        "p_b_recovered": p_b_recovered,
        "max_round_trip_error": max_round_trip_error,
        "p_wrong": p_wrong,
    }