from classes.network import Network
import unittest
from measures.separation import get_avg_shortest_paths, separation


import networkx as nx


class TestProximity(unittest.TestCase):
    G = nx.karate_club_graph()
    net = Network(G)
    A = [21, 7, 29, 30, 4]
    B = [1, 3, 30, 15, 23, 10, 31, 14]
    def test_intra_avg_shp(self):
        ground_truth = 2
        S_AA = get_avg_shortest_paths(self.net, self.A, self.A)
        self.assertEqual(S_AA, ground_truth)
    def test_intra_avg_shp_ap(self):
        ground_truth = 1.625
        S_BB = get_avg_shortest_paths(self.net, self.B, self.B)
        self.assertAlmostEqual(S_BB, ground_truth)
    def test_separation(self):
        ground_truth = -0.6458333333333333
        S_AB = separation(self.net, self.A, self.B)
        self.assertAlmostEqual(S_AB, ground_truth)