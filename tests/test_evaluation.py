import numpy as np
from traffic_quantile_study.evaluation import (
    empirical_quantile, interval_score, coverage_fraction,
    station_relative_change, holm_adjust, circular_block_indices,
)


def test_empirical_quantile_no_interpolation():
    assert empirical_quantile([1, 4, 9, 16], .25) == 1
    assert empirical_quantile([1, 4, 9, 16], .50) == 4
    assert empirical_quantile([1, 4, 9, 16], .95) == 16


def test_score_and_coverage():
    np.testing.assert_allclose(interval_score([2, 10], [1, 1], [3, 3], .9), [2, 142])
    assert coverage_fraction([1, 3], [1, 1], [3, 3]) == 1


def test_station_relative_not_pooled():
    mean, effects = station_relative_change([8, 16], [10, 20], [101, 102])
    assert np.isclose(mean, -20)
    assert len(effects) == 2


def test_holm():
    np.testing.assert_allclose(holm_adjust([.03, .01, .2]), [.06, .03, .2])


def test_block_indices():
    ix = circular_block_indices(23, 5, np.random.default_rng(123))
    assert len(ix) == 23
    assert (ix >= 0).all() and (ix < 23).all()
