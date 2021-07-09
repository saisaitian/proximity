# Proximity Measures

This module will contain a compilation of proximity measures between two sets of nodes of a given network.

## Usage

In order to use the code you can just clone the repository

```bash
git clone https://github.com/Barabasi-Lab/proximity
```

A class called `Network` serves as a wrapper to the libraries [graph-tool](https://graph-tool.skewed.de/) and [networkx](https://networkx.org/), so in practice you can use either.

Examples of how to use the code can be found in the `jupyter` directory.

## $S_{A,B}$ Separation

Given two sets of nodes $A$ and $B$ from the same network, the $S_{A,B}$ separation between $A$ and $B$ is defined as

$$S_{A,B} = \langle d_{A,B}\rangle - \frac{\langle d_{A,A} \rangle + \langle d_{B,B} \rangle}{2} $$

Where $d_{A,B}$ is the mean minimal distance between nodes in $A$ and $B$. If a node belongs to both sets then its minimal distance is 0.