# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 14:00:32 2023
@author: gl665

This script is used to find the matching nodes in the CLDs in the vensim file and the data dictionary in the excel file.
The final output is a dictionary of CLD graphs with the matching nodes and their definitions.

"""


import os
import pickle
from collections import OrderedDict

import networkx as nx
import pandas as pd
from sentence_transformers import SentenceTransformer

# Constants
FOLDER_PATH = '/Users/gl665/Documents/Phrame-MentalMaps-1/data/jsonfiles'
INPUT_FILE = 'data/data_dictionary/RC_models_data dictionary.xlsx'
SIMILARITY_THRESHOLD = 0.7
MODEL_NAME = "all-mpnet-base-v2"
OUTPUT_FILE = 'data/data_dictionary/all_vars_def_dictionary.pkl'
CLD_DICT_OUTPUT_FILE = 'data/data_dictionary/clds_dictionary.pkl'


def load_clds_from_json():
    """Load CLD graphs from JSON files"""
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
    """Load data dictionary from Excel file"""
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
    """Find matching nodes based on semantic similarity"""
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

        with open(OUTPUT_FILE, 'wb') as f:
            pickle.dump(vars_def_dict, f)
        
        
        with open(CLD_DICT_OUTPUT_FILE, 'wb') as f:
            pickle.dump(clds_dict, f)


if __name__ == "__main__":
    main()
