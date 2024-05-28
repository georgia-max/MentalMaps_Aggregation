from tqdm import tqdm
import matplotlib.pyplot as plt
import networkx as nx
import pickle
import sys
import time
import os

import gravis
import pandas as pd

from src.vensim_parser import CLDParser
# from src import parse_cld, cld_nx

# sys.path.append(os.path.abspath(os.path.join('..', 'src')))
# from src import parse_cld, cld_nx
# from src.parse_cld import read_cld_file, get_cld_df, get_dict_to_vars, get_adjacency_matrix, get_polarity_matrix, get_cld
# from src.cld_nx import draw_labeled_multigraph
import traceback

def main():


    try:
        # Check if the file exists
        if not os.path.isfile(sys.argv[1]):
            print(sys.argv[1], "does not exist or is not a file.")

            raise FileNotFoundError(f"File not found: {sys.argv[1]}")


         # Open the file and read its contents
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        
        parser = CLDParser(input_file)
        df = parser.read_cld_file()

        dict_vars_final, dict_var_org = parser.get_dict_to_vars(df)

        cld_dict = parser.get_cld_dict(df)

        # Combine the variable names dict and CLD data
        cld_data = [dict_vars_final, cld_dict]


        with open(output_file, 'wb') as f:
            pickle.dump(cld_data, f)

        # G = nx.MultiDiGraph(d)

        # cld_nx.draw_labeled_multigraph(G, "weight", dict_vars_name)
        # # plt.show()
        # plt.savefig(file_name + ".png")

    except Exception as e:

        traceback.print_exc()  # This will print the error traceback

        if len(sys.argv) != 3:
            print("Type in the .mdl file and the output file name. Example: python3 main.py input.mdl output.json")

        sys.exit(1)
if __name__ == "__main__":

    for i in tqdm(range(100), desc=f"Loading..."):
        pass
    main()
