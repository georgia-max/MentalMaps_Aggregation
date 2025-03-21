"""Semantic matching module for the pipeline."""

from typing import Dict, List, Tuple

import networkx as nx
import pandas as pd

from src.semantic_matching.matcher import SemanticMatcher


class SemanticMatchingProcessor:
    """Handles semantic matching between CLD nodes and variable definitions."""

    def __init__(self):
        self.matcher = SemanticMatcher()

    def process_cld(self,
                    cld_id: str,
                    cld_data: Dict,
                    data_dictionary: Dict[str, pd.DataFrame]) -> Tuple[Dict, Dict]:
        """
        Process a single CLD for semantic matching.

        Args:
            cld_id: ID of the CLD being processed
            cld_data: Dictionary containing CLD data including the graph
            data_dictionary: Dictionary mapping CLD IDs to their variable definitions

        Returns:
            Tuple containing:
            - Updated CLD data with node-variable matches
            - Dictionary of variable definitions
        """
        # Extract node names from the graph
        nx_graph = cld_data["cld_graph"]
        node_names = list(nx_graph.nodes)

        # Get definitions for this CLD
        df = data_dictionary[cld_id]
        vars_def_pair = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))

        # Find matches
        node_var_def_dict = self.matcher.find_matches(
            node_names, vars_def_pair)

        # Update CLD data with matches
        cld_data["node_var_def_dict"] = node_var_def_dict

        return cld_data, node_var_def_dict

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
        vars_def_dict = {}

        for cld_id, cld_data in clds_dict.items():
            cld_data, node_var_def_dict = self.process_cld(
                cld_id, cld_data, data_dictionary)
            clds_dict[cld_id] = cld_data
            vars_def_dict.update(node_var_def_dict)

        return clds_dict, vars_def_dict
