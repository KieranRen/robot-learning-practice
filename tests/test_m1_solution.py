from __future__ import annotations

import numpy as np
import pytest
from numpy.testing import assert_allclose

from algorithms.geometry import make_transform, rotation_z

from examples.m1_solution import (
    apply_transform,
    invert_transform,
    matrix_vs_elementwise_example,
    millimeters_to_meters,
    transform_chain_example,
    translate_points_example,
)


def test_millimeters_to_meters_converts_known_values() -> None:
    result = millimeters_to_meters([0, 250, -1000])

    assert result.shape == (3,)
    assert result.dtype == np.dtype(np.float64)
    assert_allclose(result, [0.0, 0.25, -1.0], rtol=0.0, atol=1e-12)


def test_millimeters_to_meters_preserves_two_dimensional_shape() -> None:
    result = millimeters_to_meters(
        [
            [1000, 2000],
            [3000, 4000],
        ]
    )

    assert result.shape == (2, 2)
    assert_allclose(
        result,
        [
            [1.0, 2.0],
            [3.0, 4.0],
        ],
        rtol=0.0,
        atol=1e-12,
    )


def test_millimeters_to_meters_does_not_modify_input() -> None:
    values = np.array([0.0, 250.0, -1000.0])
    original = values.copy()

    result = millimeters_to_meters(values)

    assert_allclose(values, original, rtol=0.0, atol=0.0)
    assert not np.shares_memory(result, values)


@pytest.mark.parametrize("bad_value", [np.nan, np.inf, -np.inf])
def test_millimeters_to_meters_rejects_nonfinite_values(bad_value: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        millimeters_to_meters([0.0, bad_value, 1000.0])

def test_pynum_t02_correct_broadcasting_example() -> None:
    points, offset, shifted = translate_points_example()

    assert points.shape == (2, 3)
    assert offset.shape == (3,)
    assert shifted.shape == (2, 3)

    assert_allclose(
        shifted,
        [
            [1.0, -1.0, 0.5],
            [2.0, 1.0, 3.5],
        ],
        rtol=0.0,
        atol=1e-12,
    )


def test_pynum_t02_wrong_column_offset_fails_broadcasting() -> None:
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 2.0, 3.0],
        ]
    )

    wrong_offset = np.array(
        [
            [1.0],
            [-1.0],
            [0.5],
        ]
    )

    with pytest.raises(ValueError):
        np.add(points, wrong_offset)


def test_pynum_t02_broadcastable_but_semantically_wrong_example() -> None:
    column_vector = np.array([[1.0], [2.0], [3.0]])
    row_vector = np.array([10.0, 20.0, 30.0])

    result = column_vector + row_vector

    assert result.shape == (3, 3)

    assert_allclose(
        result,
        [
            [11.0, 21.0, 31.0],
            [12.0, 22.0, 32.0],
            [13.0, 23.0, 33.0],
        ],
        rtol=0.0,
        atol=1e-12,
    )


def test_pynum_t02_matrix_and_elementwise_multiplication_differ() -> None:
    matrix_result, elementwise_result = matrix_vs_elementwise_example()

    assert_allclose(matrix_result, [17.0, 39.0], rtol=0.0, atol=1e-12)

    assert_allclose(
        elementwise_result,
        [
            [5.0, 12.0],
            [15.0, 24.0],
        ],
        rtol=0.0,
        atol=1e-12,
    )


def test_pynum_t02_floating_point_residual_is_small_but_nonzero() -> None:
    residual = 0.1 + 0.2 - 0.3

    assert residual != 0.0
    assert abs(residual) < 1e-15

def test_geom_t02_identity_transform_keeps_points() -> None:
    T = np.eye(4)

    points = np.array(
        [
            [1.0, 2.0, 3.0],
            [-1.0, 0.5, 4.0],
        ]
    )

    result = apply_transform(T, points)

    assert_allclose(result, points, rtol=0.0, atol=1e-12)


def test_geom_t02_known_rotation_and_translation() -> None:
    T = make_transform(
        rotation_z(np.pi / 2),
        [1.0, 0.0, 0.0],
    )

    points = np.array([[2.0, 1.0, 0.0]])

    result = apply_transform(T, points)

    assert_allclose(
        result,
        [[0.0, 2.0, 0.0]],
        rtol=0.0,
        atol=1e-12,
    )


def test_geom_t02_inverse_round_trip() -> None:
    T = make_transform(
        rotation_z(0.37),
        [2.0, -3.0, 5.0],
    )

    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 2.0, 3.0],
            [-2.0, 4.0, 0.5],
        ]
    )

    transformed = apply_transform(T, points)
    recovered = apply_transform(invert_transform(T), transformed)

    assert_allclose(
        recovered,
        points,
        rtol=0.0,
        atol=1e-12,
    )


@pytest.mark.parametrize(
    "bad_points",
    [
        [1.0, 2.0, 3.0],
        [[1.0, 2.0]],
        [[1.0], [2.0], [3.0]],
        [[[1.0, 2.0, 3.0]]],
    ],
)
def test_geom_t02_rejects_invalid_point_shapes(bad_points) -> None:
    with pytest.raises(ValueError, match="shape"):
        apply_transform(np.eye(4), bad_points)


@pytest.mark.parametrize(
    "bad_points",
    [
        [[np.nan, 0.0, 0.0]],
        [[np.inf, 0.0, 0.0]],
        [[-np.inf, 0.0, 0.0]],
    ],
)
def test_geom_t02_rejects_nonfinite_points(bad_points) -> None:
    with pytest.raises(ValueError, match="finite"):
        apply_transform(np.eye(4), bad_points)


@pytest.mark.parametrize(
    "bad_transform",
    [
        np.eye(3),
        np.zeros((4, 4)),
        np.diag([1.0, 1.0, -1.0, 1.0]),
        np.diag([1.0, 1.0, 1.0, 2.0]),
    ],
)
def test_geom_t02_rejects_invalid_rigid_transforms(bad_transform) -> None:
    with pytest.raises(ValueError):
        apply_transform(bad_transform, [[0.0, 0.0, 0.0]])

    with pytest.raises(ValueError):
        invert_transform(bad_transform)

def test_geom_t03_stepwise_and_composed_paths_agree() -> None:
    result = transform_chain_example()

    assert_allclose(
        result["p_w_stepwise"],
        [[2.0, 1.0, 0.0]],
        rtol=0.0,
        atol=1e-12,
    )

    assert_allclose(
        result["p_w_composed"],
        [[2.0, 1.0, 0.0]],
        rtol=0.0,
        atol=1e-12,
    )

    assert_allclose(
        result["p_w_stepwise"],
        result["p_w_composed"],
        rtol=0.0,
        atol=1e-12,
    )


def test_geom_t03_round_trip_returns_original_point() -> None:
    result = transform_chain_example()

    assert_allclose(
        result["p_b_recovered"],
        result["p_b"],
        rtol=0.0,
        atol=1e-12,
    )

    assert result["max_round_trip_error"] <= 1e-12


def test_geom_t03_reversed_composition_exposes_frame_chain_error() -> None:
    result = transform_chain_example()

    assert_allclose(
        result["p_wrong"],
        [[2.0, -1.0, 0.0]],
        rtol=0.0,
        atol=1e-12,
    )

    assert not np.allclose(
        result["p_wrong"],
        result["p_w_composed"],
        rtol=0.0,
        atol=1e-12,
    )

def test_geom_t04_modified_scene_matches_prediction() -> None:
    T_wa = make_transform(
        rotation_z(np.pi / 2),
        [1.0, 0.0, 0.0],
    )

    T_ab = make_transform(
        rotation_z(-np.pi / 2),
        [2.0, 0.0, 0.0],
    )

    T_wb = T_wa @ T_ab

    p_b = np.array([[1.0, 0.0, 0.0]])

    p_w = apply_transform(T_wb, p_b)

    assert_allclose(
        T_wb[:3, 3],
        [1.0, 2.0, 0.0],
        rtol=0.0,
        atol=1e-12,
    )

    assert_allclose(
        p_w,
        [[2.0, 2.0, 0.0]],
        rtol=0.0,
        atol=1e-12,
    )