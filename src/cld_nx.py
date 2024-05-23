import networkx as nx
import itertools as it
import matplotlib.pyplot as plt

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

    pos = nx.circular_layout(G, scale = 0.2)
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
        font_size= 20,
        bbox={"alpha": 0},
        ax=ax,
    )
    plt.tight_layout()
    # plt.show()

def get_nx_graph(d, theme_dict, unique_theme_names, cld_name: str):

    g = nx.DiGraph(d)
    # relabel the nodes to string names 
    g = nx.relabel_nodes(g, theme_dict)
    g = set_node_attributes(g, unique_theme_names, cld_name =cld_name)
    g = set_edge_attributes(g, cld_name =cld_name)

    return g

def gravis_settings(g): 

    # initialise colour helper 
    vals = nx.get_edge_attributes(g, 'weight').values()

    # if vals  = 1 color is red, -1 color is blue, 3 is black 
    colors = {1: 'red', -1: 'blue', 3: 'black', 2: 'green'} #TODO: check what does 2 means 


    # get rgb string for each node
    for u, v, data in g.edges(data=True):

        if 'weight' in data:
            if data['weight'] in colors:

                data['color'] = colors[data['weight']]
            else:
                data['color'] = 'green'
        else:
            data['color'] = 'black'

    # node feature
    for node, data in g.nodes(data=True):
        data['click'] = (
            "\nNode Features:" +
            f"\nCLD: {data['cld']}" + 
            f"\nLevel: {data['level']}" #+ 
        )

    # edge features
    for u, v, data in g.edges(data=True):
        data['click'] = (
                f"\nEdge Features:" + 
                f"\nCLD: {data['cld']}" + 
                f"\nPolarity Sign: {data['weight']}"
            )

    for node, data in g.nodes(data=True):
        data['title'] = (
            "\nNode Features:" +
            f"\nCLD: {data['cld']}" + 
            f"\nLevel: {data['level']}" # + 
        ) 
    


def cld_nx_properties(G): 

    
    print("Graph data:")
    print("-------------")
    print('Type:', type(G))
    print('Directed:', G.is_directed())
    print('Number of nodes:', G.number_of_nodes())
    print('Number of edges:', G.number_of_edges())
    print('Attributes:', G.graph)

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
    for node, attributes in list(G.nodes.data())[:3]: 
        print('Type:', type(node), type(attributes))
        print('Var Name:', node)
        print('Attributes:', attributes)
        print('Degree:', G.degree(node))
        
def cld_nx_edge_properties(G):
    
    print("Edge data:")
    print("-------------")

    for source, target, attributes in list(G.edges.data())[:3]:
        print('Type:', type(source), type(target), type(attributes))
        print('Source:', source)
        print('Target:', target)
        print('Attributes:', attributes)

def set_node_attributes(g, unique_theme_names, cld_name: str):
    """
    Sets the node attributes of a NetworkX graph `G`.

    This function iterates through the nodes in the graph and sets the node attributes for each node.
    Includes two categories of node attributes:
        - Node attributes from the origial CLD 
        - Node attributes of the level of the node in the graph (theme v.s. origiinal )

    Args:
        G (networkx.Graph): The NetworkX graph to set the node attributes for.
        unique_theme_names (list): A list of theme names.
        cld_name (str): The name of the CLD.

    """
    nx.set_node_attributes(g, name='cld', values=  cld_name)

    attrs = {node: {'level': 'theme'} if node in unique_theme_names else {'level': 'org'} for node in g.nodes()}
    nx.set_node_attributes(g, attrs)

    return g 

def set_edge_attributes(g, cld_name: str):
    """
    Sets the edge attributes of a NetworkX graph `G`.

    This function iterates through the edges in the graph and sets the edge attributes for each edge.

    Args:
        G (networkx.Graph): The NetworkX graph to set the edge attributes for.
        cld_name (str): The name of the CLD.
    
    """
    attr = {edge: {'weight': int(weight)} for edge, weight in nx.get_edge_attributes(g, 'weight').items()}
    nx.set_edge_attributes(g,attr)

    nx.set_edge_attributes(g, name='cld', values= cld_name)
    return g


