"""Evaluation utilities consistent with the manuscript's published definitions.

These utilities are not the original model-training scripts. They do not
reproduce published numeric results without the original predictions.
"""
from __future__ import annotations

import numpy as np


def empirical_quantile(samples, q: float) -> float:
    """Left-continuous empirical inverse CDF: inf{z: F_n(z) >= q}."""
    x = np.sort(np.asarray(samples, dtype=float))
    if not len(x) or not 0 < q < 1 or not np.all(np.isfinite(x)):
        raise ValueError("Need finite, nonempty samples and 0 < q < 1")
    return float(x[int(np.ceil(q * len(x))) - 1])


def interval_score(y, lower, upper, coverage: float):
    """Winkler interval score with alpha = 1 - nominal coverage."""
    if not 0 < coverage < 1:
        raise ValueError("coverage must lie strictly between 0 and 1")
    y, lower, upper = np.broadcast_arrays(np.asarray(y), np.asarray(lower), np.asarray(upper))
    if np.any(lower > upper):
        raise ValueError("lower must not exceed upper")
    alpha = 1.0 - coverage
    return (upper - lower) + (2 / alpha) * np.maximum(lower - y, 0) + (2 / alpha) * np.maximum(y - upper, 0)


def coverage_fraction(y, lower, upper):
    """Inclusive-endpoint empirical coverage."""
    return float(np.mean((np.asarray(y) >= np.asarray(lower)) & (np.asarray(y) <= np.asarray(upper))))


def mean_width(lower, upper):
    return float(np.mean(np.asarray(upper) - np.asarray(lower)))


def station_relative_change(scores_a, scores_b, station_ids):
    """Equal-station mean of 100*(mean_score_a_j/mean_score_b_j - 1).

    Observations must be aligned and contain no missing values. For repeated
    random systems, average pointwise scores *before* calling this routine.
    """
    a, b, s = map(np.asarray, (scores_a, scores_b, station_ids))
    if not (len(a) == len(b) == len(s)) or not len(a):
        raise ValueError("aligned nonempty arrays required")
    if not (np.all(np.isfinite(a)) and np.all(np.isfinite(b))):
        raise ValueError("scores must be finite")
    effects = {}
    for station in np.unique(s):
        mask = s == station
        denom = float(np.mean(b[mask]))
        if denom <= 0:
            raise ValueError("comparator mean score must be positive")
        effects[str(station)] = 100 * (float(np.mean(a[mask])) / denom - 1)
    return float(np.mean(list(effects.values()))), effects


def holm_adjust(pvalues):
    """Holm familywise step-down adjusted p-values, preserving original order."""
    p = np.asarray(pvalues, dtype=float)
    if p.ndim != 1 or np.any(~np.isfinite(p)) or np.any((p < 0) | (p > 1)):
        raise ValueError("p-values must be a vector in [0,1]")
    order = np.argsort(p)
    adjusted = np.empty(len(p))
    adjusted[order] = np.minimum(1., np.maximum.accumulate((len(p) - np.arange(len(p))) * p[order]))
    return adjusted


def circular_block_indices(n: int, block_length: int, rng: np.random.Generator):
    """Return n circular moving-block resample indices for *one shared timeline*.

    Use the SAME indices at all stations in a bootstrap replicate.
    """
    if n <= 0 or block_length <= 0:
        raise ValueError("n and block_length must be positive")
    starts = rng.integers(0, n, size=int(np.ceil(n / block_length)))
    return ((starts[:, None] + np.arange(block_length)) % n).ravel()[:n]
