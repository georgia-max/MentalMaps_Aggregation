"""Semantic matching module for the pipeline."""

from typing import Dict, List, Tuple, Union
from collections import OrderedDict
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
                    definition_dict: OrderedDict[Union[int, str], pd.DataFrame]) -> Tuple[Dict, Dict]:
        """
        Process a single CLD for semantic matching.

        Args:
            cld_id: name of the CLD being processed
            cld_data: Dictionary containing CLD data including the graph
            data_dictionary: Dictionary mapping CLD IDs to their variable definitions

        Returns:
            Tuple containing:
            - Updated CLD data with node-variable matches
            - Dictionary of variable definitions
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
        graph_dict["node_var_def_dict"] = node_var_def_dict

        return graph_dict

    def process_all_clds(self,
                         clds_dict: Dict,
                         data_dictionary: Dict[str, pd.DataFrame]) -> Tuple[Dict, Dict]:
        """
        Process all CLDs for semantic matching.

        Args:
            clds_dict: Dictionary containing all CLD data
            data_dictionary: Dictionary mapping CLD IDs to their variable definitions

        Returns:
            Tuple containing:
            - Updated CLDs dictionary with node-variable matches
            - Combined dictionary of all variable definitions
        """
        for cld_id, cld_data in clds_dict.items():
            cld_data = self.process_cld(cld_id, cld_data, data_dictionary)

        return cld_data
