"""Semantic matching module for the pipeline."""

from collections import OrderedDict
from typing import Dict, List, Tuple, Union

import networkx as nx
import pandas as pd

from src.semantic_matching.matcher import SemanticMatcher


class SemanticMatchingProcessor:
    """Handles semantic matching between CLD nodes and variable definitions."""

    def __init__(self):
        self.matcher = SemanticMatcher()

    def process_single_cld(self,
                           cld_name: Union[int, str],
                           graph_dict: OrderedDict,
                           definition_dict: OrderedDict[Union[int, str], pd.DataFrame]) -> Dict:
        """
        Process a single CLD for semantic matching.

        Args:
            cld_name: name of the CLD being processed
            graph_dict: OrderedDict containing CLD data including the graph
            definition_dict: OrderedDict mapping CLD names to their variable definitions

        Returns:
            Dictionary containing the processed CLD data with node-variable matches
        """
        # Extract node names from the graph
        nx_graph = graph_dict[cld_name]['nx_graph']
        node_names = list(nx_graph.nodes)

        # Get definitions for this CLD
        vars_def_pair = definition_dict[cld_name]['definition']

        # Find matches
        node_var_def_dict = self.matcher.find_matches(
            node_names, vars_def_pair)

        # Update CLD data with matches
        graph_dict[cld_name]["node_var_def_dict"] = node_var_def_dict

        return graph_dict[cld_name]

    def process_all_clds(self,
                         graph_dict: OrderedDict,
                         definition_dict: OrderedDict[Union[int, str], pd.DataFrame]) -> Tuple[OrderedDict, Dict]:
        """
        Process all CLDs for semantic matching.

        Args:
            graph_dict: OrderedDict containing all CLD data
            definition_dict: OrderedDict mapping CLD names to their variable definitions

        Returns:
            Tuple containing:
            - Updated OrderedDict with node-variable matches
            - Combined dictionary of all variable definitions
        """
        processed_clds = OrderedDict()
        vars_def_dict = {}

        for cld_name in graph_dict.keys():
            processed_cld = self.process_single_cld(
                cld_name, graph_dict, definition_dict)
            processed_clds[cld_name] = processed_cld
            vars_def_dict.update(processed_cld.get("node_var_def_dict", {}))

        return processed_clds, vars_def_dict
