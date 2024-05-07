from tqdm import tqdm

import matplotlib.pyplot as plt
import parse_cld, cld_nx
import networkx as nx
import pickle
import sys
import time


def main():

    if len(sys.argv) != 3:
        print("Usage: python3 main.py input.mdl")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    file_name = output_file.split(".")[0]

    df = parse_cld.read_cld_file(input_file)
    d = parse_cld.get_cld(df)
    dict_vars_name = parse_cld.get_dict_to_vars(df)

    with open(output_file, 'wb') as f:
        pickle.dump(d, f)

    G = nx.MultiDiGraph(d)
    cld_nx.draw_labeled_multigraph(G, "weight", dict_vars_name)
    # plt.show()
    plt.savefig(file_name + ".png")


if __name__ == "__main__":
    for i in tqdm(range(100), desc="Loading..."):
        pass

    main()
