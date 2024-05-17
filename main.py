from tqdm import tqdm
import matplotlib.pyplot as plt
import networkx as nx
import pickle
import sys
import time
import os
import py_scripts.parse_cld as parse_cld
import cld_nx
import traceback

def main():

    # for i in tqdm(range(100), desc=f"Loading..."):
    #     pass
    try:
        # Check if the file exists
        if not os.path.isfile(sys.argv[1]):
            print(sys.argv[1], "does not exist or is not a file.")

            raise FileNotFoundError(f"File not found: {sys.argv[1]}")

        # Open the file and read its contents
        input_file = sys.argv[1]
        print(input_file)
        output_file = sys.argv[2]
        file_name = output_file.split(".")[0]

        df = parse_cld.read_cld_file(input_file)
        d = parse_cld.get_cld(df)
        dict_vars_name = parse_cld.get_dict_to_vars(df)

        # combine the variable names dict and cld data
        cld_data = [dict_vars_name, d]

        with open(output_file, 'wb') as f:
            pickle.dump(cld_data, f)

        G = nx.MultiDiGraph(d)
        cld_nx.draw_labeled_multigraph(G, "weight", dict_vars_name)
        # plt.show()
        plt.savefig(file_name + ".png")

    except Exception as e:

        traceback.print_exc()  # This will print the error traceback

        if len(sys.argv) != 3:
            print("Type in the .mdl file and the output file name. Example: python3 main.py input.mdl output.json")

        sys.exit(1)
if __name__ == "__main__":

    for i in tqdm(range(100), desc=f"Loading..."):
        pass
    main()
