import networkx as nx
import matplotlib.pyplot as plt
from typing import Optional, Dict, Any, Union   
from src.graph_processing.graph_properties import CLDGraph


class GraphVisualizer:
    """A class to visualize CLDGraph using different visualization libraries."""

    def __init__(self, cld_graph: Union[CLDGraph],
                 edge_colors: Optional[Dict[int, str]] = None,
                 node_colors: Optional[Dict[str, str]] = None):
        """
        Initialize the visualizer with a CLDGraph instance.

        Args:
            cld_graph (CLDGraph): Instance of CLDGraph to visualize
            edge_colors (dict, optional): Custom edge color mapping
            node_colors (dict, optional): Custom node color mapping

        Raises:
            TypeError: If input graph is not a CLDGraph instance
        """
        # Type checking for CLDGraph
        if not isinstance(cld_graph, CLDGraph):
            raise TypeError("Input graph must be an instance of CLDGraph")

        self.graph = cld_graph
        self.node_colors = node_colors # or {'org': 'blue', 'theme': 'green'}
        self.edge_colors = edge_colors or {1: 'blue', -1: 'green',
                                           3: 'black', 0: 'red'}

    def visualize_networkx(self, figsize: tuple = (12, 8)) -> None:
        """
        Create a NetworkX visualization of the graph using matplotlib.

        Args:
            figsize: Tuple specifying the figure size (width, height)
        """
        # set font size
        # Increased font size for better readability
        plt.rcParams.update({'font.size': 8})
        plt.figure(figsize=figsize)
        pos = nx.circular_layout(self.graph)

        # Draw nodes
        # node colors can be one color or a list of colors
        if isinstance(self.node_colors, str):
            node_colors = self.node_colors
        else:
            node_colors = [self.node_colors.get(data.get('level', 'org'), 'gray')
                           for _, data in self.graph.nodes(data=True)]
        nx.draw_networkx_nodes(self.graph, pos,
                               node_color=node_colors,
                               node_size=1000)
        # Draw edges with different colors based on weight
        if isinstance(self.edge_colors, str):
            edge_colors = self.edge_colors
        else:
            edge_colors = [self.edge_colors.get(data.get('weight', 0), 'gray')
                           for _, _, data in self.graph.edges(data=True)]

        edges = list(self.graph.edges)

        # Add labels with font size parameter
        nx.draw_networkx_labels(self.graph, pos, font_size=8)

        # Add edge labels (weights) with font size parameter
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels, font_size=8)
        nx.draw_networkx_edges(self.graph, pos, edgelist=edges,
                               edge_color=edge_colors,
                               arrows=True,  # Add arrows to show direction
                               arrowstyle='-|>',  # Set arrow style
                               arrowsize=25,  # Set arrow size
                               connectionstyle='arc3,rad=0.1',  # Set connection style
                               width=2)

        plt.title("CLD Graph Visualization")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    def get_node_info(self, node: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific node.

        Args:
            node: The node identifier

        Returns:
            Dictionary containing node information
        """
        if node in self.graph.nodes:
            return dict(self.graph.nodes[node])
        return {}

    def get_edge_info(self, source: str, target: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific edge.

        Args:
            source: Source node identifier
            target: Target node identifier

        Returns:
            Dictionary containing edge information
        """
        if self.graph.has_edge(source, target):
            return dict(self.graph.edges[source, target])
        return {}



    def get_graph(self) -> CLDGraph:
        """
        Get the graph with visual settings applied.

        Returns:
            CLDGraph: The graph with visual settings applied
        """
        return self.gravis_settings()


# Example usage
def example_visualization():
    # Create a sample CLDGraph
    from src.graph_processing.graph_properties import CLDGraph

    # Create a sample graph
    G = CLDGraph()

    # Add some nodes with attributes
    G.add_node('A', level='theme', cld='CLD1')
    G.add_node('B', level='org', cld='CLD1')
    G.add_node('C', level='theme', cld='CLD1')

    # Add edges with weights
    G.add_edge('A', 'B', weight=1, cld='CLD1')
    G.add_edge('B', 'C', weight=-1, cld='CLD1')
    G.add_edge('C', 'A', weight=3, cld='CLD1')

    # Create visualizer
    visualizer = GraphVisualizer(G)

    # Create Graphviz visualization
    visualizer.visualize_networkx(figsize=(12, 8))

    # Get node and edge information
    print("Node A info:", visualizer.get_node_info('A'))
    print("Edge A->B info:", visualizer.get_edge_info('A', 'B'))


if __name__ == "__main__":
    example_visualization()
