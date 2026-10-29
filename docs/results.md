# Stored results and figures

[Project overview](../README.md) · [Methodology](methodology.md)

## Monte Carlo artifact

[`soccer_ising.csv`](../Dataset/ising_data/soccer_ising.csv) contains 100 terminal
configurations' measurements at temperatures from −100 to +100, spaced by about
2.02. [`od_ising.csv`](../Dataset/ising_data/od_ising.csv) is byte-identical, so these
files do not establish a comparison between One Direction and World News networks.

The saved values are consistent with 57 spins and the older 62-edge World News
graph, rather than the current 133-node/178-edge raw graph. The labelled World News
edge list retains the smaller topology. Raw and annotated artifacts come from
different snapshots; the result file should not be attributed to the larger graph.

For selected positive-temperature rows, see the [overview table](../README.md#recorded-results).
The large absolute magnetisation at $T\approx1.01$ and much smaller values at the
next two sampled temperatures are consistent with stronger low-temperature
alignment under ferromagnetic coupling. They do not establish a critical point,
equilibration or the persistence/loss of one configuration as temperature changes:
each point starts from a new random state.

The negative half of the sweep must not be interpreted as equilibrium behaviour.
As detailed in the [methodology](methodology.md#metropolis-updates), every proposed
flip is accepted there and the even number of sweeps restores the initial state.
Overall averages mixing positive and negative temperatures therefore do not
characterise a physical temperature response.

## Network artifacts

| Saved edge list | Nodes | Edges | Recorded Louvain communities |
| --- | ---: | ---: | ---: |
| [One Direction, labelled](../Dataset/labelled_graph/edges_list_labelled.csv) | 52 | 57 | 8 |
| [World News, labelled](../Dataset/labelled_graph/edges_list_labelled_soccer.csv) | 57 | 62 | 8 |
| [World News, current raw](../Dataset/raw_graph/edges_list_soccer.csv) | 133 | 178 | Not annotated in this artifact |

The One Direction graph is strongly hub-dominated: its post-author account
`1DMod` has degree 40. The smaller World News graph has maximum degree 11, at
`AutoModerator`. These describe reply structure under the top-level-comment
mapping, not influence or social importance. The raw World News graph includes
two self-loops; the smaller labelled graph includes one.

The labelled comment tables contain 34 positive/28 negative labels for One
Direction and 12 positive/60 negative labels for World News. These are classifier
outputs for those saved comments, not independently validated sentiment or
population-level opinion estimates. The labelled World News table has 72 comments,
whereas its current raw counterpart has 222; they are not a matched before/after pair.

## Existing visualisations

All figures are stored inline in notebooks; no standalone image files are needed.

| Notebook | Existing figure | What it supports |
| --- | --- | --- |
| [01_scraping.ipynb](../Notebooks/01_scraping.ipynb) | Reply graph, output of `visualise_graph(G)` | Inspecting connectivity and hubs in that saved run |
| [02_feature_engineering.ipynb](../Notebooks/02_feature_engineering.ipynb) | Graph coloured by `label` | Viewing first-comment classifier polarity per user, not aggregated opinion |
| [02_feature_engineering.ipynb](../Notebooks/02_feature_engineering.ipynb) | Graph coloured by `community` | Viewing the Louvain partition |
| [03_ising_model.ipynb](../Notebooks/03_ising_model.ipynb) | Energy, magnetisation and “correlation” against temperature | Inspecting saved terminal-state measurements, subject to the temperature/sampling limitations above |

The third simulation plot is signed mean spin; its absolute value duplicates the
magnetisation magnitude rather than adding an independent correlation statistic.
The network pictures show annotations, but the simulation does not use those
sentiment labels or analyse community-resolved spin outcomes.

## What was learned

The project connects a concrete reply network to a transparent graph-based Ising
implementation and records contrasting alignment at selected positive temperatures.
It also exposes an important modelling distinction: topology, text sentiment and
simulated binary states are separate representations. The available artifacts do
not demonstrate real social dynamics, susceptibility, percolation, or a measured
relationship between Louvain communities and collective alignment.
