"""Module for trimming and processing graph links."""

from collections import defaultdict
from typing import Dict, List, Set, Tuple

import networkx as nx
import gravis as gv
from src.data_management.data_loader import DataLoader
from src.data_management.data_saver import DataSaver
from src.graph_processing.graph_properties import CLDGraph
from src.graph_processing.link_trimmer import LinkTrimmer
from src.graph_processing.graph_visual import GraphVisualizer


def main():
    # Example usage

    save_data = DataLoader()

    data = save_data.load_file(
        file_path="/Users/gl665/Documents/Phrame-MentalMaps-1/notebook/data/processed/list_of_org_graphs.pkl")

    # print(data)
    print(type(data))
    data = data[0:3]

    # Create a dictionary to store CLDGraph instances
    list_of_cld_graphs = []
    i = 0
    for graph in data:
        cld_graph = CLDGraph(graph)
        cld_graph.build_CLD_graph(cld_name=i)
        # print(cld_graph.graph_properties())
        # print(cld_graph.node_properties())
        # print(cld_graph.edge_properties())
        list_of_cld_graphs.append(cld_graph)
        i += 1

    trimmer = LinkTrimmer(list_of_cld_graphs)

    # Set thresholds
    edge_threshold = 1
    node_threshold = 1

    # Get trimmed graph
    trimmed_graph = trimmer.get_trimmed_graph(
        trimmed_edges_threshold=edge_threshold,
        trimmed_nodes_threshold=node_threshold
    )

    final_graph = CLDGraph(trimmed_graph)
    final_graph = final_graph.build_CLD_graph()

    print(final_graph.graph_properties())

    print(final_graph.node_properties())
    print(final_graph.edge_properties())

    # graph_print = GraphVisualizer(
    #     final_graph, edge_colors='blue', node_colors='lightblue')

    # # Convert to gravis format and visualize
    # gravis_data = graph_print.to_gravis_format()
    # gv.d3(gravis_data,
    #       graph_height=600,
    #       edge_curvature=-0.5,
    #       node_drag_fix=False,
    #       node_size_data_source="degree",
    #       use_node_size_normalization=True,
    #       node_size_normalization_min=15,
    #       node_size_normalization_max=35,
    #       show_node_label=True,
    #       many_body_force_strength=-500
    #       )

    # print(graph_print.node_colors)

    # graph_print.visualize_networkx()

    # data_saver = DataSaver()

    # # save trimmed graph
    # data_saver.save_data(
    #     file_path="/Users/gl665/Documents/Phrame-MentalMaps-1/notebook/data/processed/trimmed_graph.pkl",
    #     data=trimmed_graph
    # )


if __name__ == "__main__":
    main()
