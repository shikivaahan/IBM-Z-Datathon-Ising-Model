# Methodology

[Project overview](../README.md) · [Stored results](results.md)

## Data preparation and graph construction

[`scrape.py`](../src/data_processing/scrape.py), used by
[notebook 01](../Notebooks/01_scraping.ipynb), reads hot posts through `praw`,
expands comment trees and records `user`, `replying_to`, `comment`, `timestamp`.
Deleted comments/authors and replies whose parent author is deleted are skipped.
Top-level comments use the post author as reply target. The timestamp is the
**post's creation time**, not the time of each reply.

[`graph_handling.py`](../src/network_graph/graph_handling.py) constructs an
undirected `networkx.Graph` from `user` and `replying_to`. Multiple interactions
between a pair collapse to one edge; self-loops remain. Thus the model represents
binary connectivity, not direction, interaction intensity or temporal dynamics.
Node/edge tables are exported under `Dataset/`.

## Sentiment and community annotation

[Notebook 02](../Notebooks/02_feature_engineering.ipynb) calls a Transformers
text-classification pipeline using
`distilbert/distilbert-base-uncased-finetuned-sst-2-english`. It truncates comment
text to 512 characters and maps `POSITIVE` to `+1`, `NEGATIVE` to `−1`.
Each user's node receives a **list** of their comment labels; this is not a single
user-level opinion. The sentiment visualisation uses the first list entry rather
than an aggregate. Text polarity should not be interpreted as agreement with a
thread's topic.

[`community_detection.py`](../src/network_graph/community_detection.py) applies
`python-louvain`'s `best_partition` and stores the result in a `community` attribute.
Both saved labelled graphs have eight communities. This is a structural
partition; the project does not test its relationship to simulated spin dynamics.

The [`process_nodes.py`](../src/network_graph/process_nodes.py) helper can attach
`spin` attributes, but the notebooks do not call it. The simulation constructor
and each temperature run instead draw random spins; sentiment attributes do not
initialise or constrain the Monte Carlo state.

## Interaction model and measured quantities

[`IsingModel.py`](../src/Ising_Model/IsingModel.py) maps graph nodes to array indices
and evaluates

$$E=-\sum_{(i,j)\in\mathcal E}s_i s_j,\qquad s_i\in\{-1,+1\}.$$

Each undirected edge is counted once. Coupling is uniformly $J=1$ and the external
field is zero; temperature is in units with $k_B=1$. A self-loop contributes
$-s_i^2=-1$ regardless of spin and therefore cannot affect flip acceptance.

| Stored column | Implemented definition | Interpretation |
| --- | --- | --- |
| `Energy` | $E/N$ | Interaction energy per node |
| `Magnetization` | $\lvert\sum_i s_i\rvert/N$ | Absolute alignment |
| `Correlation` | $\sum_i s_i/N$ | Signed mean spin, **not** pair correlation |

Despite internal names such as `avg_energy`, these quantities are taken from one
terminal configuration per temperature. They are not averages over configurations.

### Metropolis updates

One `monte_carlo_step` visits all nodes in fixed index order. For each spin it
calculates full energy, flips the spin and calculates full energy again. At
positive $T$, it accepts an energy-lowering/neutral move and accepts an
energy-increasing move with probability $e^{-\Delta E/T}$, otherwise undoing it.
The straightforward full-energy implementation costs $O(N|\mathcal E|)$ per sweep.

[Notebook 03](../Notebooks/03_ising_model.ipynb) specifies
`np.linspace(-100, 100, 100)` and 50 sweeps per temperature, despite a stale comment
suggesting a different range. Every temperature starts with newly randomised
spins, rather than continuing the preceding configuration. No burn-in assessment,
trajectory averaging or repeated-run uncertainty estimate is implemented.

For $T<0$, the rejection condition never fires: uphill moves have
$e^{-\Delta E/T}>1$, and downhill/neutral moves are accepted unconditionally.
All spins flip once per sweep, so fifty sweeps return the initial random state.
This code path is not a valid negative-temperature equilibrium sampler. The
stored grid excludes zero; it does not establish zero-temperature behaviour.

## Quantities discussed previously but not computed

### Susceptibility

The project neither varies an external field nor estimates equilibrium spin
fluctuations. Susceptibility is therefore not a result of this implementation.
A zero-field Hamiltonian does **not** make susceptibility impossible to estimate:
for equilibrium samples at positive $T$, with signed $m=\sum_i s_i/N$, the
per-spin fluctuation relation is

$$\chi=\frac{N}{T}\left(\langle m^2\rangle-\langle m\rangle^2\right).$$

One final configuration at each different temperature does not supply those
fixed-temperature ensemble moments.

### Percolation

No site/bond removal experiment or percolation threshold is computed. The earlier
unqualified $p_c=1/d$ expression is not a general rule for mean degree $d$.
For an asymptotically large, uncorrelated, locally tree-like configuration-model
network, the bond threshold is

$$p_c=\frac{\langle k\rangle}{\langle k^2\rangle-\langle k\rangle}.$$

For a $d$-regular tree-like network this reduces to $1/(d-1)$; for a Poisson degree
distribution of mean $d$ it reduces to $1/d$. Degree correlations, clustering,
finite size and degree-distribution shape matter. None of these idealised
expressions is a measured threshold for the project's reply graphs.
