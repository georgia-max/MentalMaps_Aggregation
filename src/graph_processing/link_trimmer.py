"""Module for trimming and processing graph links."""

from collections import defaultdict
from typing import Dict, List, Set, Tuple, Union

import networkx as nx

from src.data_management.data_loader import DataLoader
from src.data_management.data_saver import DataSaver
from src.graph_processing.graph_properties import CLDGraph


def get_all_possible_links(graph: Union[nx.DiGraph, CLDGraph]) -> List[Tuple[str, str]]:
    """
    Get all possible links from a directed graph.

    Args:
        graph: NetworkX directed graph

    Returns:
        List of tuples representing possible links
    """
    return list(graph.edges())


class LinkTrimmer:
    """Class for trimming and processing graph links based on appearance counts."""

    def __init__(self, list_of_graphs: List[Union[nx.DiGraph, CLDGraph]]):
        """
        Initialize the LinkTrimmer.

        Args:
            list_of_graphs: List of NetworkX directed graphs
        """
        self.list_of_graphs = list_of_graphs

    def count_node_appearances(self) -> Dict[str, int]:
        """
        Count the number of times each node appears in the list of graphs.

        Returns:
            Dictionary mapping node names to their appearance counts
        """
        all_nodes: Set[str] = set()
        for graph in self.list_of_graphs:
            all_nodes.update(graph.nodes())

        # Count appearances of each node
        node_counts = {
            node: sum(node in graph.nodes() for graph in self.list_of_graphs)
            for node in all_nodes
        }

        return node_counts

    def count_edge_appearances(self) -> Dict[Tuple[str, str], int]:
        """
        Count the number of times each edge appears in the list of graphs.

        Returns:
            Dictionary mapping edges to their appearance counts
        """
        edge_counts = defaultdict(int)

        for graph in self.list_of_graphs:
            for link in get_all_possible_links(graph):
                edge_counts[link] += 1

        return dict(edge_counts)

    def trim_nodes(self, trim_node_threshold: int = 0) -> Dict[str, int]:
        """
        Trim nodes based on appearance count threshold.

        Args:
            trim_node_threshold: Minimum number of appearances for a node to be kept

        Returns:
            Dictionary of kept nodes and their counts
        """
        node_counts = self.count_node_appearances()
        return {
            node: count
            for node, count in node_counts.items()
            if count > trim_node_threshold
        }

    def trim_edges(self,
                   trim_edge_threshold: int = 0,
                   trim_nodes_threshold: int = 0) -> Dict[Tuple[str, str], int]:
        """
        Trim edges based on appearance count and node thresholds.

        Args:
            trim_edge_threshold: Minimum number of appearances for an edge to be kept
            trim_nodes_threshold: Minimum number of appearances for nodes to be kept

        Returns:
            Dictionary of kept edges and their counts
        """
        edge_counts = self.count_edge_appearances()
        trimmed_nodes = self.trim_nodes(trim_nodes_threshold)

        return {
            edge: count
            for edge, count in edge_counts.items()
            if (edge[0] in trimmed_nodes or edge[1] in trimmed_nodes)
            and count > trim_edge_threshold
        }

    def get_link_weights(self) -> Dict[Tuple[str, str], List[int]]:
        """
        Get the weights of the links in the graph.
        """
        dict_of_weights = defaultdict()

        for graph in self.list_of_graphs:
            for link in get_all_possible_links(graph):
                if link not in dict_of_weights:
                    dict_of_weights[link] = [graph.get_edge_data(link[0], link[1])[
                        'weight']]
                else:
                    link_weight = graph.get_edge_data(
                        link[0], link[1])['weight']
                    dict_of_weights[link].append(link_weight)

        return dict_of_weights

    def get_trimmed_graph(self,
                          trimmed_edges_threshold: int = 0,
                          trimmed_nodes_threshold: int = 0) -> nx.DiGraph:
        """
        Create a new graph with trimmed edges and nodes.

        Args:
            trimmed_edges_threshold: Minimum number of appearances for edges
            trimmed_nodes_threshold: Minimum number of appearances for nodes

        Returns:
            New NetworkX directed graph with trimmed edges
        """
        trimmed_edges = self.trim_edges(
            trimmed_edges_threshold,
            trimmed_nodes_threshold
        )

        # Create edges with weights
        weighted_edges = [
            (edge[0], edge[1], count)
            for edge, count in trimmed_edges.items()
        ]

        # Create and return the trimmed graph
        trimmed_graph = nx.Digraph()

        trimmed_graph.add_weighted_edges_from(weighted_edges, weight="count")
        print(trimmed_graph.edges(data=True))

        # trimmed_graph = trimmed_graph.build_CLD_graph()

        # linked_weights = self.get_link_weights()
        # for link, weights in linked_weights.items():
        #     print(link, weights)

        # trimmed_graph.add_weighted_edges_from(self.get_link_weights(), weight="weights")

        # trimmed_graph.add_edges_from(original_graph.edges())

        return trimmed_graph
