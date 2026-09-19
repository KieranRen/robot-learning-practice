"""Check rigid-transform conventions against hand calculations and invariants."""

from __future__ import annotations

import numpy as np
from numpy.testing import assert_allclose
import pytest

from algorithms.geometry import (
    inverse_transform,
    make_transform,
    rotation_z,
    transform_points,
)


@pytest.mark.parametrize(
    ("angle", "expected"),
    [
        (0.0, [[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
        (np.pi / 2, [[0, -1, 0], [1, 0, 0], [0, 0, 1]]),
        (-np.pi / 2, [[0, 1, 0], [-1, 0, 0], [0, 0, 1]]),
        (np.pi, [[-1, 0, 0], [0, -1, 0], [0, 0, 1]]),
    ],
)
def test_rotation_z_matches_right_handed_quarter_turns(angle, expected) -> None:
    assert_allclose(rotation_z(angle), expected, atol=1e-12, rtol=0)


def test_make_transform_places_translation_in_last_column() -> None:
    transform = make_transform([[0, -1, 0], [1, 0, 0], [0, 0, 1]], [2, 3, 4])
    assert_allclose(
        transform, [[0, -1, 0, 2], [1, 0, 0, 3], [0, 0, 1, 4], [0, 0, 0, 1]],
        atol=1e-12, rtol=0,
    )


def test_inverse_matches_hand_computed_nonplanar_transform() -> None:
    transform = make_transform([[0, 0, 1], [1, 0, 0], [0, 1, 0]], [2, -3, 5])
    expected = [[0, 1, 0, 3], [0, 0, 1, -5], [1, 0, 0, -2], [0, 0, 0, 1]]
    assert_allclose(inverse_transform(transform), expected, atol=1e-12, rtol=0)


def test_nonplanar_transform_maps_a_batch_without_changing_point_storage() -> None:
    transform = make_transform([[0, 0, 1], [1, 0, 0], [0, 1, 0]], [2, -3, 5])
    points = np.array([[0, 0, 0], [1, 2, 3], [-2, 4, 0.5]])
    result = transform_points(transform, points)
    assert result.shape == (3, 3)
    assert_allclose(result, [[2, -3, 5], [5, -2, 7], [2.5, -5, 9]], atol=1e-12, rtol=0)
    np.testing.assert_array_equal(points, [[0, 0, 0], [1, 2, 3], [-2, 4, 0.5]])


def test_transform_composition_is_not_commutative() -> None:
    t_wa = make_transform(rotation_z(np.pi / 2), [1, 0, 0])
    t_ab = make_transform(rotation_z(-np.pi / 2), [1, 0, 0])
    assert_allclose(transform_points(t_wa @ t_ab, [[1, 0, 0]]), [[2, 1, 0]], atol=1e-12, rtol=0)
    assert_allclose(transform_points(t_ab @ t_wa, [[1, 0, 0]]), [[2, -1, 0]], atol=1e-12, rtol=0)


def test_inverse_round_trip_and_pairwise_distances_are_preserved() -> None:
    transform = make_transform(rotation_z(0.37), [2, -3, 5])
    points = np.array([[0, 0, 0], [1, 2, 3], [-2, 4, 0.5]])
    result = transform_points(transform, points)
    assert_allclose(
        transform_points(inverse_transform(transform), result), points, atol=1e-12, rtol=0
    )
    distances_before = np.linalg.norm(points[:, None, :] - points[None, :, :], axis=-1)
    distances_after = np.linalg.norm(result[:, None, :] - result[None, :, :], axis=-1)
    assert_allclose(distances_after, distances_before, atol=1e-12, rtol=0)


def test_empty_point_batch_keeps_shape() -> None:
    result = transform_points(np.eye(4), np.empty((0, 3)))
    assert result.shape == (0, 3)
    assert result.dtype == np.float64


@pytest.mark.parametrize("angle", [np.nan, np.inf, -np.inf, [0.0], 1j, "90"])
def test_rotation_z_rejects_nonfinite_or_nonscalar_angles(angle) -> None:
    with pytest.raises(ValueError):
        rotation_z(angle)


@pytest.mark.parametrize(
    "rotation",
    [np.eye(2), np.ones(3), np.zeros((3, 3)), np.diag([1, 1, -1]),
     np.diag([1, 1, 1.01]), np.full((3, 3), np.nan), np.eye(3, dtype=complex)],
)
def test_make_transform_rejects_invalid_rotation(rotation) -> None:
    with pytest.raises(ValueError):
        make_transform(rotation, [0, 0, 0])


@pytest.mark.parametrize("translation", [[1, 2], [[1, 2, 3]], [1, 2, np.inf], [0, 0, 1j]])
def test_make_transform_rejects_invalid_translation(translation) -> None:
    with pytest.raises(ValueError):
        make_transform(np.eye(3), translation)


@pytest.mark.parametrize(
    "points", [[1, 2, 3], [[1], [2], [3]], [[1, 2]], [[[1, 2, 3]]],
               [[np.nan, 0, 0]], [[0, np.inf, 0]], [[0, 0, 1j]]],
)
def test_transform_points_rejects_invalid_batches(points) -> None:
    with pytest.raises(ValueError):
        transform_points(np.eye(4), points)


@pytest.mark.parametrize("operation", ["inverse", "points"])
@pytest.mark.parametrize(
    "transform",
    [np.eye(3), np.zeros((4, 4)), np.diag([1, 1, -1, 1]),
     np.diag([1, 1, 1, 2]), np.full((4, 4), np.nan),
     [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0.1, 0, 0, 1]]],
)
def test_transform_operations_reject_invalid_homogeneous_matrices(operation, transform) -> None:
    with pytest.raises(ValueError):
        if operation == "inverse":
            inverse_transform(transform)
        else:
            transform_points(transform, [[0, 0, 0]])


def test_transform_points_rejects_nonfinite_arithmetic_result() -> None:
    transform = make_transform(np.eye(3), [1e308, 0, 0])
    with pytest.raises(ValueError, match="finite float64 range"):
        transform_points(transform, [[1e308, 0, 0]])
