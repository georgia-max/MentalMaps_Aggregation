import itertools as it
import matplotlib.pyplot as plt
import networkx as nx
from typing import Union


class CLDGraph(nx.DiGraph):

    def __init__(self, graph=None):
        """
        Initialize a CLDGraph instance.

        Args:
            graph (nx.DiGraph, optional): Input graph must be a directed graph

        Raises:
            TypeError: If input graph is not None and not a directed graph
        """
        super().__init__()

        if graph is not None:
            # Check if input is a directed graph
            if not isinstance(graph, (nx.DiGraph, CLDGraph)):
                raise TypeError(
                    "Input graph must be a directed graph (nx.DiGraph)")

            # Check if the graph actually has directed edges
            if not graph.is_directed():
                raise ValueError(
                    "Input graph must be directed (have directed edges)")

            self.add_edges_from(graph.edges(data=True))
            self.add_nodes_from(graph.nodes(data=True))

    def set_node_attributes(self, theme_dict=None, cld_name=None):
        """
        Sets the node attributes in the graph.

        Args:
            theme_dict (dict, optional): Dictionary mapping node names to themes.
                If provided, sets the 'level' attribute to 'theme' for nodes in the dictionary,
                and 'org' for all other nodes.

        Returns:
            CLDGraph: self for method chaining
        """
        # Set node levels if theme_dict is provided
        if theme_dict is not None:
            attrs = {node: {'level': 'theme'} if node in theme_dict else {
                'level': 'org'} for node in self.nodes()}
            nx.set_node_attributes(self, attrs)

        if cld_name is not None:
            nx.set_node_attributes(
                self, {node: {'cld_name': cld_name} for node in self.nodes()})

        return self

    def set_edge_attributes(self, name_of_attr_to_set=None, dict_of_weights=None):
        """
        Sets the edge attributes of the graph, including the weight.

        Returns:
            CLDGraph: self for method chaining
        """
        edge_attrs = {
            edge: {'weight': int(weight)}
            for edge, weight in nx.get_edge_attributes(self, 'weight').items()
        }
        # TODO: this is not working
        if name_of_attr_to_set is not None:
            for edge in edge_attrs:
                if edge in dict_of_weights:
                    edge_attrs[edge][name_of_attr_to_set] = dict_of_weights[edge]

        nx.set_edge_attributes(self, edge_attrs)
        return self

    def graph_properties(self):
        """
        Prints various properties of the graph, including its type, whether it is directed, and the number of nodes and edges.
        """
        return {
            "type": type(self),
            "directed": self.is_directed(),
            "num_nodes": int(self.number_of_nodes()),
            "num_edges": int(self.number_of_edges())
        }

    def node_properties(self):
        """
        return the node properties for all nodes in the graph

        Returns:
            dict: A dictionary containing the node properties for all nodes in the graph
        """

        node_info = {}
        for node, attributes in list(self.nodes.data()):
            node_info[node] = {
                'type': str(type(node)),
                'attributes': attributes,
                'degree': self.degree(node)
            }
        return node_info

    def edge_properties(self):
        """
        return the edge properties for all edges in the graph


        Returns:
            dict: A dictionary containing the edge properties for all edges in the graph
        """
        edge_properties = {}
        for source, target, attributes in self.edges.data():
            edge_properties[source, target] = attributes

        return edge_properties
    
    def to_gravis(self) -> nx.DiGraph:
        """Convert CLDGraph to nx.DiGraph format suitable for gravis"""
        digraph = nx.DiGraph(self)
        digraph.graph = self.graph.copy()
        return digraph


    def gravis_settings(self):

        new_graph = nx.convert_node_labels_to_integers(self, label_attribute='label')

        # set node size
        new_graph.graph['node_size'] = 10
        # new_graph.graph['edge_size'] = 2  
        new_graph.graph['node_color'] = 'green'
        new_graph.graph['edge_color'] = 'black'

        # new_graph.graph['node_label'] = str

        # edge properties based on weight 
        if any('weight' in data for _, _, data in new_graph.edges.data()):
            for edge in new_graph.edges:
                edge = new_graph.edges[edge]
                edge['edge_size'] = edge['weight'] *0.7

        else:
            new_graph.graph['edge_size'] = 1

        





        # # set edge size based on weight or count
        # if 'weight' in self.edges.data():
        #     wieght_dict = {edge: self.edges[edge]['weight'] for edge in self.edges}
            

        #     nx.set_edge_attributes(new_graph, wieght_dict, 'edge_size')
        # else:
        #     nx.set_edge_attributes(new_graph, 2, 'edge_size')



        # # nx.set_node_attributes(new_graph, 10, 'size')
        # nx.set_node_attributes(new_graph, 'green', 'color')

        # # set edge size
        # nx.set_edge_attributes(new_graph, 2, 'size')
        # nx.set_edge_attributes(new_graph, 'black', 'color')

        # # set node label
        # nx.set_node_attributes(new_graph, str, 'label')

        # # Initialize graph metadata if not present
        # if not hasattr(self, 'graph'):
        #     self.graph = {}
        
        # # Set basic graph attributes
        # self.graph['directed'] = True
        # self.graph['name'] = 'CLD Graph'
        
        # # Set node attributes
        # for node in self.nodes():
        #     self.nodes[node].update({
        #         'size': 10,
        #         'color': node_color if isinstance(node_color, str) else node_color.get(node, 'lightblue'),
        #         'label': str(node)
        #     })
        
        # # Set edge attributes
        # for edge in self.edges():
        #     self.edges[edge].update({
        #         'size': 2,
        #         'color': edge_color if isinstance(edge_color, str) else edge_color.get(edge, 'black'),
        #         'label': str(self.edges[edge].get('weight', ''))
        #     })

        return new_graph
    

    def build_CLD_graph(self, cld_name=None,  theme_dict=None) -> 'CLDGraph':
        """
        Build a CLD graph with the specified theme dictionary.

        Args:
            theme_dict (dict, optional): Dictionary mapping node names to themes

        Returns:
            CLDGraph: The processed CLD graph with all attributes set
        """
        # Instead of creating a new instance, modify self
        self.set_node_attributes(theme_dict, cld_name)
        self.set_edge_attributes()
        return self


def sample_graph():
    """Create a sample directed graph for testing."""
    d = {
        'A': {'B': {'weight': 1}},
        'B': {'C': {'weight': -1}},
        'C': {'A': {'weight': 1}}
    }
    return nx.DiGraph(d)


# Example usage
if __name__ == "__main__":
    # Create a sample graph
    source_graph = sample_graph()
    theme_dict = {'A': 'Alpha', 'B': 'Bravo', 'C': 'Charlie'}

    # Create and build CLD graph
    cld_graph = CLDGraph(source_graph)
    cld_graph = cld_graph.build_CLD_graph(theme_dict)

    # Print graph properties
    print("Graph Properties:", cld_graph.graph_properties())
    print("\nNode Properties:", cld_graph.node_properties())
    print("\nEdge Properties:", cld_graph.edge_properties())
