# Similar-Trajectory Quantiles in Forecast Ensembles

Companion repository scaffold for the conference-paper draft
**Augmenting Quantile Forecast Ensembles with Similar-Trajectory Quantiles: A Controlled Traffic Study**
(İlker Arslan and Ümit Işlak).

## Important reproducibility status

**This archive is a PARTIAL scaffold. It does not include the original experiment
training code or original prediction files and cannot yet reproduce the paper's
reported results.** Evaluation functions here were reconstructed from the supplied
manuscript and tested; they are **not** represented as the original scripts.

The original previously generated packages were named
`pems03_20station_experiment.zip` and `long_validation_experiment.zip`.
Import the original experiment scripts, configurations, selected station list,
random seeds, model outputs, and data provenance from those packages before
claiming computational reproduction of the study.

## Experiments reported in the manuscript

- 2018 PeMS03: 20 newly sampled stations, 5-minute forecasting horizon,
  5,242 test targets per station.
- 2019 LargeST: 14 retained matching IDs from the 2018 selection,
  73 days / 21,024 test timestamps per station.
- Quantiles: 0.025, 0.05, 0.95, 0.975.
- QRF and quantile gradient boosting base predictions; CQRA combination.
- Candidates: similar trajectories (ST), random, calendar-only (Seasonal),
  and secondary local error corrections SC / Global.
- Relative score effect is an **equal-station mean of station-level ratios**, not
  the ratio of pooled mean scores.
- Original manuscript uses 3,000 joint one-day circular-block bootstrap
  replicates (block length 288), joint HAC inference with Bartlett lag 288,
  and Holm corrections for six primary comparisons per panel.

## Setup

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
pytest -q
```

## Repository layout

- `paper/manuscript_snapshot.tex`: verbatim supplied working draft, for reference.
- `src/traffic_quantile_study/evaluation.py`: score, empirical quantile,
  station aggregation, Holm, and shared circular-block index utilities.
- `tests/`: simple unit tests for the reconstructed utilities.
- `results/`: reserved for **actual** outputs, not populated with fabricated numbers.

## Missing for a complete release

1. Original model-fitting and candidate-construction `.py` scripts.
2. Exact original 2018 and 2019 preprocessing and saved split identifiers.
3. Sensor-ID selection file and random seed list for repeated random controls.
4. Frozen prediction arrays and per-station results / joint resampling scripts.
5. Dataset acquisition and license/redistribution statements.
6. Environment freeze with actual versions used to run experiments.

The data and output folders should remain out of version control when they
contain large or redistribution-restricted files. Instead supply dataset URLs,
checksums and scripts to recreate outputs once original artifacts are available.
