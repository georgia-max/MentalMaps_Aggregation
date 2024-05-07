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
    df_cld = parse_cld.get_cld_df(df)

    my_dict = parse_cld.get_dict_to_vars(df)

    df_subset = df_cld[['from', 'to', 'polarity_type']]

    # Change the column name polarity type of weight
    df_subset = df_subset.rename(columns={'polarity_type': 'weight'})
    d = parse_cld.get_dict_of_dicts(df_subset)

    with open(output_file, 'wb') as f:
        pickle.dump(d, f)

    G = nx.MultiDiGraph(d)
    cld_nx.draw_labeled_multigraph(G, "weight", my_dict)
    plt.savefig(file_name + ".png")


if __name__ == "__main__":
    for i in tqdm(range(40), desc="Loading..."):
        pass

    main()
