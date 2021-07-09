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

