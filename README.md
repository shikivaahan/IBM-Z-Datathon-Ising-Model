# Susceptibility of Social Networks Using the Ising Model and Monte Carlo Simulations

## Overview

This repository contains code and documentation for modeling the susceptibility of social networks using the Ising model and Monte Carlo simulations. The Ising model is a mathematical model that describes interactions between particles, and it is particularly useful for understanding phase transitions in complex systems, such as social networks.

## Table of Contents

- [Background](#background)
- [Percolation Theory](#percolation-theory)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Background

In this project, we leverage the Ising model to simulate the interactions within social networks, focusing on how susceptibility to external influences can affect the dynamics of social behavior. Monte Carlo simulations are employed to explore various configurations and assess the stability of the network under different conditions.

## Percolation Theory

Percolation theory studies the behavior of connected clusters in a random graph. It is crucial for understanding how properties like connectivity and robustness emerge in complex networks.

### Key Concepts

- **Site Percolation:** Refers to the random occupation of nodes (sites) in a network. A cluster is formed if a set of occupied sites is connected.

- **Bond Percolation:** Involves the random occupation of edges (bonds) between nodes. A cluster is formed if there is a path of occupied edges connecting nodes.

### Percolation Threshold

The percolation threshold, \( p_c \), is the critical probability above which a giant connected component emerges in the network. It can be expressed as:

\[
p_c = \frac{1}{d}
\]

where \( d \) is the average degree of the network.

### Susceptibility

Susceptibility, \( \chi \), is a measure of how a system responds to external influences. It can be defined as:

\[
\chi = \left( \frac{\partial m}{\partial h} \right)_{h=0}
\]

where \( m \) is the magnetization of the system and \( h \) is the external field applied to the system.

### Order Parameter

The order parameter, \( m \), represents the extent of order in the system and can be defined as:

\[
m = \frac{1}{N} \sum_{i=1}^{N} \langle s_i \rangle
\]

where \( N \) is the total number of nodes, and \( s_i \) is the spin of node \( i \) (either +1 or -1).
