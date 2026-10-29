# Ising Model on Reddit Reply Networks

**An IBM Z Datathon exploration of collective alignment on social-network graphs.**

Can a simple binary-state model help explore how local interactions produce
collective alignment on a discussion network? This Python project builds graphs
from Reddit replies, annotates users with comment sentiment and Louvain communities,
and runs an Ising model on the reply topology using Metropolis Monte Carlo.

The Ising model supplies a deliberately simple mechanism: neighbouring nodes
favour matching states, while temperature controls acceptance of energy-increasing
changes. Here temperature is a model parameter, not a measured social quantity.
The project studies simulated alignment—not a predictive model of real opinions.

## What was implemented

- **Data preparation:** Reddit comment-tree extraction with `praw`, retaining
  authors, reply targets, text and thread timestamps.
- **Network analysis:** undirected NetworkX reply graphs, per-user sentiment-label
  lists and Louvain community detection.
- **Sentiment annotation:** a pretrained DistilBERT SST-2 classifier maps comments
  to positive (`+1`) or negative (`−1`) labels.
- **Simulation:** single-spin-flip Metropolis updates with unit ferromagnetic
  coupling; energy, absolute magnetisation and signed mean spin versus temperature.
- **Visualisation:** saved reply-graph drawings, sentiment/community colourings
  and temperature-response plots in the notebooks.

**Important distinction:** sentiment is stored as graph metadata, but the Ising
implementation initialises random spins and does not read those labels. Its saved
sweep concerns alignment on a reply topology, not the evolution of observed sentiment.

## Data and graph representation

The saved raw data contains 62 comments from a One Direction megathread and
222 comments from World News discussions in October 2024. Files ending in
`_soccer` contain World News data in this snapshot; the suffix is historical.
The labelled World News artifacts cover an earlier, smaller scrape.

Each username becomes a node and each reply adds an undirected edge. Repeated
replies collapse to one edge; reply direction and frequency are not modelled.
Self-replies remain as self-loops. Top-level comments connect to the post author,
which can make moderator/post-author accounts prominent hubs.

The labelled graphs contain 52 nodes/57 edges for One Direction and 57 nodes/62
edges for World News, each with eight recorded Louvain communities. The current
raw World News graph is larger (133 nodes/178 edges); these are different snapshots,
not interchangeable versions of one experimental input.

## Computational workflow

| Stage | Main entry point | Output |
| --- | --- | --- |
| Scrape and construct graph | [01_scraping.ipynb](Notebooks/01_scraping.ipynb) | Comment tables, raw edge lists and reply-graph drawing |
| Annotate and inspect | [02_feature_engineering.ipynb](Notebooks/02_feature_engineering.ipynb) | Sentiment labels, Louvain partitions and coloured network plots |
| Simulate and plot | [03_ising_model.ipynb](Notebooks/03_ising_model.ipynb) | Temperature sweep, three plots and result CSV |

Reusable helpers live in [`src/data_processing/`](src/data_processing/),
[`src/network_graph/`](src/network_graph/), [`src/Sentiment/`](src/Sentiment/)
and [`src/Ising_Model/`](src/Ising_Model/). The stack uses pandas, NumPy, NetworkX,
`praw`, Transformers/PyTorch, `python-louvain`, Matplotlib and `tqdm`.

## Interaction model

For spins $s_i\in\{-1,+1\}$ on reply edges $\mathcal E$, the implementation uses

$$E=-\sum_{(i,j)\in\mathcal E}s_i s_j.$$

There is no external field. Each sweep visits every node in index order, proposes
a spin flip and recomputes total energy before/after. For positive temperature,
energy-increasing moves are accepted with probability $\exp(-\Delta E/T)$;
other moves are accepted. Full-energy recomputation favours a transparent
implementation over an efficient neighbour-local update.

The stored run uses 50 sweeps per temperature and resets spins randomly at each
temperature: it is not annealing. Only the final configuration is recorded at each
point, not an equilibrium average over a sampled trajectory.

## Recorded results

[`soccer_ising.csv`](Dataset/ising_data/soccer_ising.csv) stores 100 temperature
points from −100 to +100. `od_ising.csv` is byte-identical: there is one stored
sweep, not an independent comparison of the two discussion networks.
The saved values are consistent with the older 57-node World News graph.

| Selected stored temperature | Energy per node | Absolute magnetisation |
| ---: | ---: | ---: |
| 1.01 | −0.982 | 0.895 |
| 3.03 | −0.456 | 0.193 |
| 5.05 | 0.000 | 0.053 |

These configurations illustrate stronger alignment at the lowest sampled positive
temperature than at the next two points. A single terminal state per temperature,
with spacing about 2.02, does not locate a critical temperature or establish
an equilibrium phase transition.

The existing **energy, magnetisation and “correlation” figures** are stored in
[notebook 03](Notebooks/03_ising_model.ipynb). Network drawings are stored in
[notebooks 01](Notebooks/01_scraping.ipynb) and [02](Notebooks/02_feature_engineering.ipynb).
[Results and figure interpretation →](docs/results.md)

## Interpretation boundaries

- **“Correlation” is signed mean spin**, not a two-point correlation function.
- **Susceptibility and percolation thresholds are not calculated.** Mean degree
  alone does not determine a general network's percolation threshold.
- **Negative-temperature outputs are not equilibrium evidence:** the implemented
  acceptance condition accepts every flip there. Fifty full sweeps return the
  initial random state at each negative temperature.
- **Classifier polarity is not agreement:** positive/negative text labels do not
  establish support/opposition to a topic or a community's dominant opinion.
- Network communities are detected and visualised, but no quantitative test links
  them to the Monte Carlo dynamics.

[Methodology, computed quantities and mathematical assumptions →](docs/methodology.md)
