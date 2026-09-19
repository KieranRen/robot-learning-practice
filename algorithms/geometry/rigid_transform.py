"""Rigid transforms with the column-vector convention p_a = R_ab @ p_b + t_ab.

Distances use metres and angles use radians. Points are stored as N rows of
three coordinates, including a single point with shape (1, 3).
"""

from __future__ import annotations

import math

import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatArray = NDArray[np.float64]
_ATOL = 1e-9


def _real_array(value: ArrayLike, name: str) -> FloatArray:
    """Reject non-real or non-finite values before any geometric operation."""

    array = np.asarray(value)
    if array.dtype.kind not in "iuf":
        raise ValueError(f"{name} must contain real numbers")
    array = np.asarray(array, dtype=np.float64)
    if not np.isfinite(array).all():
        raise ValueError(f"{name} must contain only finite numbers")
    return array


def _rotation_matrix(rotation: ArrayLike) -> FloatArray:
    matrix = _real_array(rotation, "rotation")
    if matrix.shape != (3, 3):
        raise ValueError("rotation must have shape (3, 3)")
    # R's columns must be an orthonormal, right-handed basis: R.T R = I, det R = 1.
    with np.errstate(over="ignore", invalid="ignore"):
        orthogonal = np.allclose(matrix.T @ matrix, np.eye(3), atol=_ATOL, rtol=0)
    if not orthogonal:
        raise ValueError("rotation must be orthogonal: rotation.T @ rotation = I")
    if not np.isclose(np.linalg.det(matrix), 1.0, atol=_ATOL, rtol=0):
        raise ValueError("rotation must have determinant +1")
    return matrix


def _transform_matrix(transform: ArrayLike) -> FloatArray:
    matrix = _real_array(transform, "transform")
    if matrix.shape != (4, 4):
        raise ValueError("transform must have shape (4, 4)")
    if not np.allclose(matrix[3], [0.0, 0.0, 0.0, 1.0], atol=_ATOL, rtol=0):
        raise ValueError("transform bottom row must be [0, 0, 0, 1]")
    _rotation_matrix(matrix[:3, :3])
    return matrix


def rotation_z(angle_rad: float) -> FloatArray:
    """Return the right-handed 3x3 rotation about +z for a finite scalar angle."""

    angle = _real_array(angle_rad, "angle_rad")
    if angle.shape != ():
        raise ValueError("angle_rad must be a scalar in radians")
    cosine, sine = math.cos(float(angle)), math.sin(float(angle))
    return np.array(
        [[cosine, -sine, 0.0], [sine, cosine, 0.0], [0.0, 0.0, 1.0]]
    )


def make_transform(rotation: ArrayLike, translation: ArrayLike) -> FloatArray:
    """Build T_ab = [[R_ab, t_ab], [0, 1]] from shapes (3, 3) and (3,)."""

    matrix = _rotation_matrix(rotation)
    vector = _real_array(translation, "translation")
    if vector.shape != (3,):
        raise ValueError("translation must have shape (3,)")
    transform = np.eye(4)
    transform[:3, :3] = matrix
    transform[:3, 3] = vector
    return transform


def inverse_transform(transform: ArrayLike) -> FloatArray:
    """Return T_ba using R_ab.T and -R_ab.T @ t_ab, without a general inverse."""

    matrix = _transform_matrix(transform)
    rotation, translation = matrix[:3, :3], matrix[:3, 3]
    inverse = np.eye(4)
    inverse[:3, :3] = rotation.T
    with np.errstate(over="ignore", invalid="ignore"):
        inverse[:3, 3] = -rotation.T @ translation
    if not np.isfinite(inverse).all():
        raise ValueError("inverse translation exceeds the finite float64 range")
    return inverse


def transform_points(transform: ArrayLike, points: ArrayLike) -> FloatArray:
    """Map finite points of shape (N, 3) to the target frame; N may be zero."""

    matrix = _transform_matrix(transform)
    point_array = _real_array(points, "points")
    if point_array.ndim != 2 or point_array.shape[1] != 3:
        raise ValueError("points must have shape (N, 3); use (1, 3) for one point")
    rotation, translation = matrix[:3, :3], matrix[:3, 3]
    # Transpose the storage, apply the column-vector equation, then restore rows.
    with np.errstate(over="ignore", invalid="ignore"):
        transformed = (rotation @ point_array.T).T + translation
    if not np.isfinite(transformed).all():
        raise ValueError("transformed points exceed the finite float64 range")
    return transformed
