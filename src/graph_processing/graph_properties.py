import itertools as it
import matplotlib.pyplot as plt
import networkx as nx


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
            nx.set_node_attributes(self, {node: {'cld_name': cld_name} for node in self.nodes()})

        return self

    def set_edge_attributes(self, name_of_attr_to_set = None, dict_of_weights=None):
        """
        Sets the edge attributes of the graph, including the weight.

        Returns:
            CLDGraph: self for method chaining
        """
        edge_attrs = {
            edge: {'weight': int(weight)}
            for edge, weight in nx.get_edge_attributes(self, 'weight').items()
        }
        #TODO: this is not working
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

    def build_CLD_graph(self, cld_name=None,  theme_dict=None ) -> 'CLDGraph':
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
