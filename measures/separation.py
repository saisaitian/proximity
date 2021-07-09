"""Proximity functions"""
from collections import defaultdict

import numpy as np

try:
    import graph_tool.all as gt
except ModuleNotFoundError:
    pass
try:
    import networkx as nx
except ModuleNotFoundError:
    pass


def get_avg_shortest_paths(net, A, B):
    """Get average shortest paths between two sets of nodes.
    
    Parameters
    ----------
    net: proximity.Network
    A, B: Container
        Each contains nodes from net.Graph

    Returns
    -------
    S_AB: float
    """
    A = set(A)
    B = set(B)
    # Are sets not identical?
    different_sets = (A != B)
    graph = net.Graph
    # Set the function to calculate shortest paths
    if net.module == 'gt':
        # A property map will define the value for paths that
        # does not exist. A 32-bit int has a max value of 2147483647.
        pm = graph.new_vp('int32_t')
        distance = lambda x, y, z: gt.shortest_distance(x, y, z, dist_map=pm)
    elif net.module == 'nx':
        distance = nx.shortest_path_length
    # For each node, get its min distance with nodes from the other group
    min_distance = defaultdict(lambda: float('inf'))
    for a in A:
        for b in B:
            # zeros in same-group nodes are ignored
            if different_sets or a != b:
                # Sometimes there is no path between `a` and `b`
                try:
                    spl = distance(graph, a, b)  # gt will return `inf`
                except nx.NetworkXNoPath:
                    continue
                # Update min distance
                min_distance[a] = min(spl, min_distance[a])
                min_distance[b] = min(spl, min_distance[b])
    
    # Get average of all min distances
    bad_values = (float('inf'), np.nan, 2147483647)
    min_lengths = [x for x in min_distance.values() if x not in bad_values]
    S_AB = np.mean(min_lengths)
    
    return S_AB


def separation(net, A, B):
    """Calculate the separation [1]_ between node sets A and B.

    Parameters
    ----------
    net: prximity.Network
    A: container
        A subset of nodes in net.Graph
    B: container
        A subset of nodes in net.Graph

    Returns
    -------
    sep: the separation of nodes A and B in net.Graph

    References
    ----
    .. [1] Menche, Jörg, et al.
        Uncovering disease-disease relationships through the
        incomplete interactome.
        Science 347.6224 (2015).
    """
    s_aa = get_avg_shortest_paths(net, A, A)
    s_bb = get_avg_shortest_paths(net, B, B)
    s_ab = get_avg_shortest_paths(net, A, B)

    sep = s_ab - (s_aa + s_bb) / 2

    return sep