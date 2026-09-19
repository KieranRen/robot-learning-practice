"""Check numeric meaning, shape boundaries, and ownership of translated points."""

from __future__ import annotations

import numpy as np
import pytest
from numpy.typing import ArrayLike

from examples.numeric_basics import translate_points


def test_translation_matches_hand_computed_two_dimensional_points() -> None:
    """Each row receives the same coordinate offset, including fractional data."""

    result = translate_points([[0, 0], [1, 2], [-2, 3]], [0.5, -1.0])

    assert result.shape == (3, 2)
    assert result.dtype == np.dtype(np.float64)
    np.testing.assert_allclose(
        result, [[0.5, -1.0], [1.5, 1.0], [-1.5, 2.0]], rtol=0.0, atol=1e-12
    )


def test_translation_supports_one_three_dimensional_point() -> None:
    """One point still uses a batch axis and can contain three coordinates."""

    result = translate_points([[2.0, -3.0, 1.0]], [-1.0, 2.0, 0.5])

    np.testing.assert_allclose(result, [[1.0, -1.0, 1.5]], rtol=0.0, atol=1e-12)


def test_translation_does_not_change_inputs_or_share_output_storage() -> None:
    """A sliced input is safe, and changing the result cannot alter its source."""

    source = np.array([[0.0, 99.0, 2.0], [1.0, 99.0, 3.0]])
    original_source = source.copy()
    points = source[:, ::2]
    offset = np.array([0.5, -1.0])
    original_offset = offset.copy()

    result = translate_points(points, offset)
    result[0, 0] = -999.0

    np.testing.assert_array_equal(source, original_source)
    np.testing.assert_array_equal(offset, original_offset)
    assert not np.shares_memory(result, points)
    assert not np.shares_memory(result, offset)


def test_translation_preserves_an_empty_batch_with_known_dimension() -> None:
    """No points is valid when the coordinate dimension is still explicit."""

    result = translate_points(np.empty((0, 3)), [1.0, 2.0, 3.0])

    assert result.shape == (0, 3)
    assert result.dtype == np.dtype(np.float64)


@pytest.mark.parametrize("points", [[1.0, 2.0], 1.0, np.empty((2, 0))])
def test_translation_rejects_missing_batch_or_coordinate_axes(
    points: ArrayLike,
) -> None:
    """Shape mistakes fail at the interface rather than broadcasting silently."""

    with pytest.raises(ValueError, match="points must have shape"):
        translate_points(points, [0.0, 0.0])


@pytest.mark.parametrize(
    "offset", [1.0, [1.0], [[1.0, 2.0]], [[1.0], [2.0]], [1.0, 2.0, 3.0]]
)
def test_translation_rejects_offsets_that_do_not_describe_one_vector(
    offset: ArrayLike,
) -> None:
    """Even NumPy-broadcastable offsets must satisfy this function's contract."""

    with pytest.raises(ValueError, match="offset must have shape"):
        translate_points([[0.0, 0.0], [1.0, 2.0]], offset)


@pytest.mark.parametrize("bad_value", [np.nan, np.inf, -np.inf])
@pytest.mark.parametrize("bad_argument", ["points", "offset"])
def test_translation_rejects_nonfinite_coordinates(
    bad_value: float, bad_argument: str
) -> None:
    """Invalid sensor-like values cannot silently contaminate a whole batch."""

    points = [[bad_value, 0.0]] if bad_argument == "points" else [[0.0, 0.0]]
    offset = [bad_value, 0.0] if bad_argument == "offset" else [0.0, 0.0]

    with pytest.raises(ValueError, match="finite float64"):
        translate_points(points, offset)


@pytest.mark.parametrize(
    "points", [[[1.0 + 2.0j, 0.0]], [["1", "2"]], [[True, False]]]
)
def test_translation_rejects_data_that_is_not_real_numeric(points: ArrayLike) -> None:
    """Complex coordinates, text, and flags are not silently reinterpreted."""

    with pytest.raises(ValueError, match="real integer or floating-point"):
        translate_points(points, [0.0, 0.0])


def test_translation_reports_overflow_instead_of_returning_infinity() -> None:
    """Finite operands can still overflow during addition."""

    largest = np.finfo(np.float64).max

    with pytest.raises(ValueError, match="finite float64 range"):
        translate_points([[largest, 0.0]], [largest, 0.0])
