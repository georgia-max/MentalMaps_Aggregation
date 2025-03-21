import itertools as it

# import parse_cld
from functools import reduce

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def draw_labeled_multigraph(G, attr_name, mapping, ax=None):
    """
    Draws a labeled multigraph using NetworkX and Matplotlib.
    https://networkx.org/documentation/stable/auto_examples/drawing/plot_multigraphs.html
    """
    plt.figure(figsize=(15, 10))

    # Works with arc3 and angle3 connectionstyles
    connectionstyle = [f"arc3,rad={r}" for r in it.accumulate([0.15] * 4)]
    # connectionstyle = [f"angle3,angleA={r}" for r in it.accumulate([30] * 4)]
    G = nx.relabel_nodes(G, mapping, copy=False)

    pos = nx.circular_layout(G, scale=0.2)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color="tab:blue", node_size=100)
    nx.draw_networkx_labels(G, pos, font_size=20, ax=ax)
    nx.draw_networkx_edges(
        G, pos, edge_color="red",
        connectionstyle=connectionstyle,
        ax=ax
    )

    labels = {
        tuple(edge): f"{attr_name}={attrs[attr_name]}"
        for *edge, attrs in G.edges(keys=True, data=True)
    }
    nx.draw_networkx_edge_labels(
        G,
        pos,
        labels,
        connectionstyle=connectionstyle,
        label_pos=0.3,
        font_color="red",
        font_size=20,
        bbox={"alpha": 0},
        ax=ax,
    )
    plt.tight_layout()
    # plt.show()


def gravis_settings(g):

    # initialise colour helper
    vals = nx.get_edge_attributes(g, 'weight').values()

    # node feature
    node_color = {'org': 'blue', 'theme': 'green'}

    for node, data in g.nodes(data=True):
        if 'level' in data:

            if isinstance(data['level'], list):
                data['color'] = node_color[data['level'][0]]
            else:

                data['color'] = node_color[data['level']]

        # data['click'] = (
        #     "\nNode Features:" +
        #     f"\nCLD: {data['cld']}" +
        #     f"\nLevel: {data['level']}"
        # )
        # data['title'] = (
        #     "\nNode Features:" +
        #     f"\nCLD: {data['cld']}" +
        #     f"\nLevel: {data['level']}" # +
        # )

    # edge features
    # blue is positive, green is negative, black is no sign

    colors = {1: 'blue', -1: 'green', 3: 'black', 0: 'red'}

    for u, v, data in g.edges(data=True):
        if 'weight' in data:

            if data['weight'] in colors:
                data['color'] = colors[data['weight']]
            else:
                data['color'] = 'green'
        else:
            data['color'] = 'black'

        # data['click'] = (
        #         f"\nEdge Features:" +
        #         f"\nCLD: {data['cld']}" +
        #         f"\nPolarity Sign: {data['weight']}"
        #     )


def clean_graph_for_gravis(graph):
    # Convert all node and edge attributes to JSON serializable types
    for node, attrs in graph.nodes(data=True):
        for key, value in attrs.items():

            if isinstance(value, np.int64):
                attrs[key] = int(value)
            elif isinstance(value,  np.floating):
                attrs[key] = float(value)

    for u, v, attrs in graph.edges(data=True):
        for key, value in attrs.items():
            if isinstance(value, np.integer):
                attrs[key] = int(value)
            elif isinstance(value,  np.floating):
                attrs[key] = float(value)
    return graph


def cld_nx_properties(G):

    print("Graph data:")
    print("-------------")
    print('Type:', type(G))
    print('Directed:', G.is_directed())
    print('Number of nodes:', G.number_of_nodes())
    print('Number of edges:', G.number_of_edges())


def cld_nx_node_properties(G):
    """
    Prints the node properties of a NetworkX graph `G`.

    This function iterates through the nodes in the graph and prints the node type, ID, attributes, and degree for each node. It only prints the first node's information and then the first node-attribute pair.

    Args:
        G (networkx.Graph): The NetworkX graph to print the node properties for.

    Returns:
        None
    """

    print("Node data:")
    print("-------------")
    print()
    for node, attributes in list(G.nodes.data())[:5]:
        print('Type:', type(node), type(attributes))
        print('Var Name:', node)
        print('Attributes:', attributes)
        print('Degree:', G.degree(node))


def cld_nx_edge_properties(G):

    print("Edge data:")
    print("-------------")

    for source, target, attributes in list(G.edges.data()):
        print('Type:', type(source), type(target), type(attributes))
        print('Source:', source)
        print('Target:', target)
        print('Attributes:', attributes)
        for k, v in attributes.items():
            print(f'\t{k}: {v}')
            print('Type', type(v))
        for k, v in attributes.items():
            print(f'\t{k}: {v}')
            print('Type', type(v))


def set_node_theme_attributes(g, unique_theme_names=None):
    """
    Sets the node attributes of a NetworkX graph `G`.

    This function iterates through the nodes in the graph and sets the node attributes for each node.
    Includes two categories of node attributes:
        - Node attributes from the origial CLD 
        - Node attributes of the level of the node in the graph (theme v.s. origiinal )

    Args:
        G (networkx.Graph): The NetworkX graph to set the node attributes for.
        unique_theme_names (list): A list of theme names.


    """
    if unique_theme_names is not None:
        attrs = {node: {'level': 'theme'} if node in unique_theme_names else {
            'level': 'org'} for node in g.nodes()}
        nx.set_node_attributes(g, attrs)

    node_degree_dict = {node: {'degree': int(
        degree)} for node, degree in g.degree()}
    nx.set_node_attributes(g, node_degree_dict)

    return g


def set_edge_attributes(g, cld_name: str):
    # TODO: fix this
    # TODO: fix this
    """
    Sets the edge attributes of a NetworkX graph `G`.

    This function iterates through the edges in the graph and sets the edge attributes for each edge.

    Args:
        G (networkx.Graph): The NetworkX graph to set the edge attributes for.
        cld_name (str): The name of the CLD.

    """
    attr = {edge: {'weight': int(weight)} for edge, weight in nx.get_edge_attributes(
        g, 'weight').items()}
    nx.set_edge_attributes(g, attr)

    return g


def combine_graphs_with_node_attributes(graphs):
    combined_graph = nx.DiGraph()

    for g in graphs:
        for node, attrs in g.nodes(data=True):
            if node not in combined_graph:
                combined_graph.add_node(
                    node, **{k: [v] for k, v in attrs.items()})
            else:
                for attr, value in attrs.items():
                    if attr in combined_graph.nodes[node]:
                        combined_graph.nodes[node][attr].append(value)
                    else:
                        combined_graph.nodes[node][attr] = [value]

        for u, v, attrs in g.edges(data=True):
            if combined_graph.has_edge(u, v):
                for attr, value in attrs.items():
                    if attr in combined_graph[u][v]:
                        combined_graph[u][v][attr].append(value)
                    else:
                        combined_graph[u][v][attr] = [value]
            else:
                combined_graph.add_edge(
                    u, v, **{k: [v] for k, v in attrs.items()})

    # Calculate merged_weight for each edge
    for u, v, attrs in combined_graph.edges(data=True):
        if 'weight' in attrs:
            set_unique_weights = set(attrs['weight'])
            if 2 in set_unique_weights:

                set_unique_weights.remove(2)

            if -2 in set_unique_weights:

                set_unique_weights.remove(-2)

            # 0 means that there is a merge in the single CLD of -1 and 1

            if 0 in set_unique_weights:
                combined_graph[u][v]['merge_weight'] = 0
                # meaning the there is both -1 and 1 in shown in the link

            elif len(set_unique_weights) == 1:
                # if all graphs have the same polarity sign, use it.
                combined_graph[u][v]['merge_weight'] = list(
                    set_unique_weights)[0]
            elif 3 in set_unique_weights and len(set_unique_weights) == 2:
                # 3 means that there is no defined sign in the org cld. Therefore
                # we use the ones that have a sign
                set_unique_weights.remove(3)

                combined_graph[u][v]['merge_weight'] = list(
                    set_unique_weights)[0]
            else:
                combined_graph[u][v]['merge_weight'] = 0

    return combined_graph


def clean_combined_graph(combined_graph, num_aggregate_nodes=0, num_aggregate_edges=0):

    new_graph = nx.DiGraph()

    # Add nodes to the new graph
    for node, attrs in combined_graph.nodes(data=True):

        if len(attrs['cld']) > num_aggregate_nodes:
            attrs['single_level'] = attrs.pop('level')
            attrs['level'] = list(set(attrs['single_level']))[0]
            attrs['nums_cld'] = len(attrs['cld'])
            new_graph.add_node(node, **attrs)

    # Add edges to the new graph with sum_weighted as the weight
    for u, v, attrs in combined_graph.edges(data=True):
        if u in new_graph and v in new_graph:
            edge_attrs = attrs.copy()
            edge_attrs['single_weight'] = edge_attrs.pop('weight')

            edge_attrs['weight'] = int(edge_attrs.pop('merge_weight'))
            edge_attrs.pop('single_weight')

            if edge_attrs['weight'] > num_aggregate_edges:
                new_graph.add_edge(u, v, **edge_attrs)

    # new_graph.remove_edges_from(nx.selfloop_edges(new_graph))

    return new_graph


def clean_up_combined_graph(combined_graph):

    new_graph = nx.DiGraph()

    # # Add nodes to the new graph
    # for node, attrs in combined_graph.nodes(data=True):

    #     if len(attrs['cld']) > num_aggregate_nodes:
    #         attrs['single_level'] = attrs.pop('level')
    #         attrs['level'] = list(set(attrs['single_level']))[0]
    #         attrs['nums_cld'] = len(attrs['cld'])
    #         new_graph.add_node(node, **attrs)

    # Add edges to the new graph with sum_weighted as the weight
    for u, v, attrs in combined_graph.edges(data=True):
        if u in new_graph and v in new_graph:
            edge_attrs = attrs.copy()
            edge_attrs['single_weight'] = edge_attrs.pop('weight')

            edge_attrs['weight'] = int(edge_attrs.pop('merge_weight'))
            edge_attrs.pop('single_weight')

            # if edge_attrs['weight'] > num_aggregate_edges:
            #     new_graph.add_edge(u, v, **edge_attrs)

    # new_graph.remove_edges_from(nx.selfloop_edges(new_graph))

    return new_graph


def mulitiple_weights(g):
    """
    This function multiple the weights of a cycle of a graph. The weights in the graph 
    represents the polarity signe between variables. +1 postive, -1 negative, 3 neutral. 
    In this function, I ignored all the neutral weights, and assume they are postive. 

    # TODO: find a way to address the neutral weights later on. 

    params: 
    g: a subgraph of a graph that contains a cycle
    """
    edge_weight = 1

    # get reinforcing or balancing loop

    for u, v, attrs in g.edges(data=True):
        # multiple all weights together
        if attrs['weight'] == 1 or attrs['weight'] == -1:
            edge_weight *= attrs['weight']
        else:
            pass

    return edge_weight


def get_nx_graph(g, cld_name: str, theme_dict=None, unique_theme_names=None):

    # g = nx.DiGraph(d)
    # relabel the nodes to string names
    if theme_dict is not None:
        g = nx.relabel_nodes(g, theme_dict)
    # if unique_theme_names is not None:
    #     g = set_node_attributes(g, cld_name =cld_name, unique_theme_names = unique_theme_names)
    # g = set_edge_attributes(g, cld_name =cld_name)
    # g = nx.DiGraph(d)
    # relabel the nodes to string names
    if theme_dict is not None:
        g = nx.relabel_nodes(g, theme_dict)
    # if unique_theme_names is not None:
    #     g = set_node_attributes(g, cld_name =cld_name, unique_theme_names = unique_theme_names)
    # g = set_edge_attributes(g, cld_name =cld_name)

    return g


def clean_variable_name(variable_name):
    """
    Cleans a variable name by performing the following transformations:
    - Replaces '&' with 'and'
    - Replaces '/' with ' and '
    - Replaces '_' with ' '
    - Replaces common abbreviations and acronyms with their full forms
    - Removes leading/trailing whitespace
    - Removes extra whitespace between words
    - Converts the name to lowercase

    Args:
        variable_name (str): The variable name to be cleaned.

    Returns:
        str: The cleaned variable name.
    """

    replacements = {
        # TODO: Q: Need to refine these.
        '&': 'and',  # remove '&'
        '/': ' and ',  # replace '/' with ' or '
        # '-': ' ',  # replace '-' with ' '
        '_': ' ',  # replace '_' with ' '
        'ipv': 'intimate partner violence',
        'dss': ' department of social service',
        'aian': 'american indian and alaska native',
        'u.s.': 'U.S.',
        'passages': 'reentry facility',
        'fasd': 'Fetal alcohol spectrum disorder',
        'alc m': 'alcohol mortality',
        'mh': 'mental health',
        'tx': 'tax',
        'ihs': 'indian health service',
        'med': 'medication',
        'sub': 'substance',
        'ptsd': 'Post-traumatic stress disorder',
        'aep': 'anti-establishment parties',
        'skillset': 'skill set',
        'rez': 'restorative',
        'aces': 'adverse childhood experience',
        'ai': 'american indian',
        'mh': 'mental health'

    }

    for old, new in replacements.items():
        variable_name = variable_name.replace(old, new)

    variable_name = variable_name.strip()  # remove leading/trailing whitespace
    # remove extra whitespace between words
    variable_name = " ".join(variable_name.split())
    variable_name = variable_name.lower()  # convert to lowercase

    return variable_name


def get_cld_graph(dict_cld, cld_name=str):
    cld_list = dict_cld[cld_name]
    G = nx.from_dict_of_dicts(cld_list[1], create_using=nx.DiGraph)

    G = nx.relabel_nodes(G, cld_list[0])

    return cld_list, G


# def get_dict_of_cld(data_dict, df_aggregate_names, dict_file_rename):

#     dict_cld = {}

#     for k, v in data_dict.items():
#         merge_df,  theme_dict = parse_cld.get_theme_cld(v, df_aggregate_names)

#         unique_theme_names = set(df_aggregate_names['theme'])


#         df_subset = merge_df[['from', 'to', 'polarity_type']]
#         df_subset = df_subset.rename(columns={'polarity_type': 'weight'})

#         d = parse_cld.get_dict_of_dicts(df_subset)
#         # cld_name = k
#         cld_name = dict_file_rename.get(k)

#         g = get_nx_graph(d, theme_dict, cld_name, unique_theme_names)
#         dict_cld[cld_name] = g

#         return dict_cld
