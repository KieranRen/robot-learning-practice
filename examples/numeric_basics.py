"""Show the array operations used before learning robot geometry."""

from __future__ import annotations

import logging

import numpy as np
from numpy.typing import ArrayLike, NDArray

LOGGER = logging.getLogger(__name__)


def _as_finite_float_array(value: ArrayLike, name: str) -> NDArray[np.float64]:
    """Convert real numeric data without silently discarding imaginary parts."""

    array = np.asarray(value)
    if array.dtype.kind not in "iuf":
        raise ValueError(f"{name} must contain real integer or floating-point data")
    with np.errstate(over="ignore", invalid="ignore"):
        array = np.asarray(array, dtype=np.float64)
    if not np.isfinite(array).all():
        raise ValueError(f"{name} must contain finite float64 values")
    return array


def translate_points(points: ArrayLike, offset: ArrayLike) -> NDArray[np.float64]:
    """Return new (N, D) points plus one (D,) offset in the same frame and unit.

    D must be positive; an empty batch (0, D) is allowed. Inputs must contain
    finite real numbers. Invalid shapes, data, or overflow raise ValueError.
    No input array is modified, and the result has dtype float64.
    """

    points_array = _as_finite_float_array(points, "points")
    offset_array = _as_finite_float_array(offset, "offset")
    if points_array.ndim != 2 or points_array.shape[1] == 0:
        raise ValueError("points must have shape (N, D) with D >= 1")
    dimension = points_array.shape[1]
    if offset_array.shape != (dimension,):
        raise ValueError(f"offset must have shape ({dimension},)")
    try:
        with np.errstate(over="raise", invalid="raise"):
            return points_array + offset_array
    except FloatingPointError as error:
        raise ValueError("translation exceeds the finite float64 range") from error


def main() -> None:
    """Display hand-checkable arrays, vectors, matrices, and residuals."""

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    points_m = np.array([[0.0, 0.0], [1.0, 2.0]], dtype=np.float64)
    offset_m = np.array([0.5, -1.0], dtype=np.float64)
    moved_m = translate_points(points_m, offset_m)
    LOGGER.info("ARRAY | points shape=%s dtype=%s", points_m.shape, points_m.dtype)
    LOGGER.info(
        "ARRAY | offset shape=%s; translated (m)=%s", offset_m.shape, moved_m.tolist()
    )

    source = np.array([1.0, 2.0, 3.0])
    view = source[:2]
    independent = source[:2].copy()
    view[0] = 9.0
    LOGGER.info(
        "ARRAY | after view edit: source=%s copy=%s",
        source.tolist(),
        independent.tolist(),
    )

    vector_m = np.array([3.0, 4.0])
    squares_m2 = vector_m * vector_m
    squared_length_m2 = float(np.sum(squares_m2))
    length_m = float(np.sqrt(squared_length_m2))
    LOGGER.info(
        "VECTOR | components (m)=%s squares (m^2)=%s",
        vector_m.tolist(),
        squares_m2.tolist(),
    )
    LOGGER.info(
        "VECTOR | squared length=%.1f m^2; length=%.1f m", squared_length_m2, length_m
    )

    matrix = np.array([[1.0, 2.0], [0.0, 1.0]])
    LOGGER.info("MATRIX | A @ v=%s", (matrix @ vector_m).tolist())
    LOGGER.info("MATRIX | A * v=%s", (matrix * vector_m).tolist())

    actual = np.array([0.1 + 0.2, 0.5])
    expected = np.array([0.3, 0.5])
    residual = actual - expected
    LOGGER.info("ERROR | equal elementwise=%s", (actual == expected).tolist())
    LOGGER.info("ERROR | max absolute residual=%.3e", float(np.max(np.abs(residual))))
    LOGGER.info(
        "ERROR | allclose(rtol=0, atol=1e-12)=%s",
        np.allclose(actual, expected, rtol=0.0, atol=1e-12),
    )
    LOGGER.info(
        "ERROR | accidental (2, 1) - (2,) shape=%s", (actual[:, None] - expected).shape
    )

    try:
        translate_points(points_m, [[0.5, -1.0]])
    except ValueError as error:
        LOGGER.info("ERROR | expected rejection: %s", error)


if __name__ == "__main__":
    main()
