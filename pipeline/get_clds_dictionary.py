# -*- coding: utf-8 -*-
"""
This script processes Causal Loop Diagrams (CLDs) and their associated data dictionaries to create a mapping
between CLD nodes and their definitions.

Key functionality:
- Loads CLD graphs from JSON files and data dictionary definitions from Excel
- Uses semantic similarity matching to find corresponding definitions for CLD nodes
- Creates a dictionary mapping CLD nodes to their matching definitions
- Saves results to pickle files for later use

Input files:
- JSON files containing CLD graphs in /data/jsonfiles/
- Excel file 'RC_models_data dictionary.xlsx' containing node definitions

Output files:
- all_vars_def_dictionary.pkl: Dictionary mapping all nodes to their definitions
- clds_dictionary.pkl: Dictionary containing CLD graphs with node-definition mappings

Dependencies:
- networkx: For graph processing
- sentence_transformers: For semantic similarity matching
- pandas: For data manipulation
- pickle: For saving/loading data
"""

import os
import pickle
from collections import OrderedDict

import networkx as nx
import pandas as pd
from sentence_transformers import SentenceTransformer

# Constants for file paths and model parameters
FOLDER_PATH = '/Users/gl665/Documents/Phrame-MentalMaps-1/data/jsonfiles'
INPUT_FILE = 'data/data_dictionary/RC_models_data dictionary.xlsx'
SIMILARITY_THRESHOLD = 0.7  # Minimum similarity score to consider a match
# Sentence transformer model for semantic matching
MODEL_NAME = "all-mpnet-base-v2"
OUTPUT_FILE = 'data/data_dictionary/all_vars_def_dictionary.pkl'
CLD_DICT_OUTPUT_FILE = 'data/data_dictionary/clds_dictionary.pkl'


def load_clds_from_json():
    """
    Load CLD graphs from JSON files in the specified folder.

    Returns:
        OrderedDict: Dictionary mapping IDs to CLD graphs and their metadata
            {
                id: {
                    'name': filename,
                    'cld_graph': networkx.DiGraph
                }
            }
    """
    clds_dict = OrderedDict()
    count = 1
    for filename in os.listdir(FOLDER_PATH):
        if filename.endswith('.json'):
            file_path = os.path.join(FOLDER_PATH, filename)
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
                G = nx.from_dict_of_dicts(data[1], create_using=nx.DiGraph)
                G = nx.relabel_nodes(G, data[0])
                clds_dict[count] = {
                    'name': filename,
                    'cld_graph': G
                }
                count += 1
    return clds_dict


def load_data_dictionary():
    """
    Load data dictionary from Excel file containing node definitions.

    Returns:
        dict: Dictionary mapping sheet numbers to pandas DataFrames containing variables and definitions
            {
                sheet_number: DataFrame(columns=['variable', 'definition'])
            }
    """
    file_path = os.path.join(os.getcwd(), INPUT_FILE)
    excel_data = pd.read_excel(file_path, sheet_name=None)

    data_dictionary = {}
    for k, v in excel_data.items():
        v.columns.values[0] = "variable"
        v.columns.values[1] = "definition"
        k = int(k)
        data_dictionary[k] = v
    return data_dictionary


def find_node_name_matches(vensim_nodes, vars_def_pair):
    """
    Find matching nodes between CLD nodes and data dictionary entries using semantic similarity.

    Args:
        vensim_nodes (list): List of node names from the CLD
        vars_def_pair (dict): Dictionary mapping variable names to their definitions

    Returns:
        dict: Dictionary mapping CLD nodes to their matching variables and definitions
            {
                node_name: [[matching_var, definition], ...]
            }
    """
    model = SentenceTransformer(MODEL_NAME)
    embeddings_cld = model.encode(vensim_nodes)
    excel_nodes = list(vars_def_pair.keys())
    embeddings_excel = model.encode(excel_nodes)

    node_var_def_dict = {}
    similarities = model.similarity(embeddings_cld, embeddings_excel)

    for idx_i, vensim_node in enumerate(vensim_nodes):
        matches = []
        for idx_j, excel_node in enumerate(excel_nodes):
            if similarities[idx_i][idx_j] > SIMILARITY_THRESHOLD:
                matches.append([excel_node, vars_def_pair[excel_node]])
        if matches:
            node_var_def_dict[vensim_node] = matches

    return node_var_def_dict


def main():
    """
    Main execution function that:
    1. Loads CLD graphs and data dictionary
    2. Finds matching definitions for nodes in each CLD
    3. Saves results to pickle files
    """
    # Load CLDs and data dictionary
    clds_dict = load_clds_from_json()
    data_dictionary = load_data_dictionary()
    vars_def_dict = {}

    # Process each CLD
    for v, k in clds_dict.items():
        nx_graph = clds_dict[v]["cld_graph"]
        node_names = list(nx_graph.nodes)

        df = data_dictionary[v]
        vars_def_pair = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))

        node_var_def_dict = find_node_name_matches(node_names, vars_def_pair)
        clds_dict[v]["node_var_def_dict"] = node_var_def_dict

        vars_def_dict.update(node_var_def_dict)

        # Save results to pickle files
        with open(OUTPUT_FILE, 'wb') as f:
            pickle.dump(vars_def_dict, f)

        with open(CLD_DICT_OUTPUT_FILE, 'wb') as f:
            pickle.dump(clds_dict, f)


if __name__ == "__main__":
    main()
