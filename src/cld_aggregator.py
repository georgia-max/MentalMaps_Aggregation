import networkx as nx
import itertools as it
import matplotlib.pyplot as plt
# import parse_cld

class CLDGraph:
    
    def __init__(self, graph=None):
        self.graph = graph if graph is not None else nx.DiGraph()
    

    def set_node_attributes(self, cld_name, unique_theme_names=None):
        """
        Sets the node attributes in the graph. Assigns the 'cld' attribute to all nodes with the provided `cld_name`. If `unique_theme_names` is provided, it sets the 'level' attribute to 'theme' for those nodes, and 'org' for all other nodes. It also sets the 'degree' attribute for each node based on the node's degree in the graph.
        
        Args:
            cld_name (str): The name of the CLD to assign to all nodes.
            unique_theme_names (set, optional): A set of node names that should be marked as 'theme' level nodes.
        """

        nx.set_node_attributes(self.graph, name='cld', values=cld_name)
        if unique_theme_names is not None:
            attrs = {node: {'level': 'theme'} if node in unique_theme_names else {'level': 'org'} for node in self.graph.nodes()}
            nx.set_node_attributes(self.graph, attrs)
        node_degree_dict = {node: {'degree': int(degree)} for node, degree in self.graph.degree()}
        nx.set_node_attributes(self.graph, node_degree_dict)
    
    def set_edge_attributes(self, cld_name):
        """
        Sets the edge attributes of the graph, including the weight and the name of the CLD.
        
        Args:
            cld_name (str): The name of the CLD to set on the edges.
        
        Returns:
            None
        """

        attr = {edge: {'weight': int(weight)} for edge, weight in nx.get_edge_attributes(self.graph, 'weight').items()}
        nx.set_edge_attributes(self.graph, attr)
        nx.set_edge_attributes(self.graph, name='cld', values=cld_name)
    
    def graph_properties(self):
        """
        Prints various properties of the graph, including its type, whether it is directed, and the number of nodes and edges.
        """

        print("Graph data:")
        print("-------------")
        print('Type:', type(self.graph))
        print('Directed:', self.graph.is_directed())
        print('Number of nodes:', self.graph.number_of_nodes())
        print('Number of edges:', self.graph.number_of_edges())
    
    def node_properties(self):
        """
        Prints information about the first 20 nodes in the graph, including the node type, name, attributes, and degree.
        """

        print("Node data:")
        print("-------------")
        for node, attributes in list(self.graph.nodes.data())[:20]:
            print('Type:', type(node), type(attributes))
            print('Var Name:', node)
            print('Attributes:', attributes)
            print('Degree:', self.graph.degree(node))
    
    def edge_properties(self):
        """
        Prints information about the first 20 edges in the graph, including the type of the source and target nodes, and the edge attributes.
        """
        
        print("Edge data:")
        print("-------------")
        for source, target, attributes in list(self.graph.edges.data())[:20]:
            print('Type:', type(source), type(target), type(attributes))
            print('Source:', source)
            print('Target:', target)
            print('Attributes:', attributes)
    
    def combine_graphs_with_node_attributes(graphs):
        """
        Combines multiple graphs into a single graph, merging node attributes and edge attributes.
        
        Args:
            graphs (list): A list of NetworkX DiGraph objects to be combined.
        
        Returns:
            nx.DiGraph: A single combined graph with merged node and edge attributes.
        """

        combined_graph = nx.DiGraph()
        for g in graphs:
            for node, attrs in g.nodes(data=True):
                if node not in combined_graph:
                    combined_graph.add_node(node, **{k: [v] for k, v in attrs.items()})
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
                    combined_graph.add_edge(u, v, **{k: [v] for k, v in attrs.items()})
        for u, v, attrs in combined_graph.edges(data=True):
            if 'weight' in attrs:
                set_unique_weights = set(attrs['weight'])
                if 2 in set_unique_weights:
                    set_unique_weights.remove(2)
                if -2 in set_unique_weights:
                    set_unique_weights.remove(-2)
                if 0 in set_unique_weights:
                    combined_graph[u][v]['merge_weight'] = 0
                elif len(set_unique_weights) == 1:
                    combined_graph[u][v]['merge_weight'] = list(set_unique_weights)[0]
                elif 3 in set_unique_weights and len(set_unique_weights) == 2:
                    set_unique_weights.remove(3)
                    combined_graph[u][v]['merge_weight'] = list(set_unique_weights)[0]
                else:
                    combined_graph[u][v]['merge_weight'] = 0
        return combined_graph
    

    def draw_labeled_multigraph(self, attr_name, mapping, ax=None):
        """
        Draw a labeled networkx multigraph with the specified attributes.

        """

        plt.figure(figsize=(15, 10))
        connectionstyle = [f"arc3,rad={r}" for r in it.accumulate([0.15] * 4)]
        self.graph = nx.relabel_nodes(self.graph, mapping, copy=False)
        pos = nx.circular_layout(self.graph, scale=0.2)
        nx.draw_networkx_nodes(self.graph, pos, ax=ax, node_color="tab:blue", node_size=100)
        nx.draw_networkx_labels(self.graph, pos, font_size=20, ax=ax)
        nx.draw_networkx_edges(self.graph, pos, edge_color="red", connectionstyle=connectionstyle, ax=ax)
        labels = {tuple(edge): f"{attr_name}={attrs[attr_name]}" for *edge, attrs in self.graph.edges(keys=True, data=True)}
        nx.draw_networkx_edge_labels(self.graph, pos, labels, connectionstyle=connectionstyle, label_pos=0.3, font_color="red", font_size=20, bbox={"alpha": 0}, ax=ax)
        plt.tight_layout()
        

    def gravis_settings(self): 
        """
        Configures the visual settings for the nodes and edges in the graph.
        
        This method sets the color, click behavior, and title for each node in the graph based on the node's 'level' attribute. It also sets the color for each edge in the graph based on the edge's 'weight' attribute.
        
        The node colors are set as follows:
        - 'org' nodes are blue
        - 'theme' nodes are green
        
        The edge colors are set as follows:
        - Positive weights (1) are blue
        - Negative weights (-1) are green
        - Weights of 3 are black
        - Weights of 0 are red
        
        The click behavior and title for each node display the node's 'cld' and 'level' attributes.
        
        The click behavior for each edge displays the edge's 'cld' and 'weight' attributes.
        """
        

        # initialise colour helper 
        vals = nx.get_edge_attributes(self.graph, 'weight').values()

        # node feature
        node_color = {'org': 'blue', 'theme': 'green'}

        for node, data in self.graph.nodes(data=True):
            data['color'] = node_color[data['level']]
            data['click'] = (
                "\nNode Features:" +
                f"\nCLD: {data['cld']}" + 
                f"\nLevel: {data['level']}"
            )
            data['title'] = (
                "\nNode Features:" +
                f"\nCLD: {data['cld']}" + 
                f"\nLevel: {data['level']}" # + 
            ) 

        # edge features

        colors = {1: 'blue', -1: 'green', 3: 'black', 0: 'red'} 


        for u, v, data in self.graph.edges(data=True):
            if 'weight' in data:
                if data['weight'] in colors:
                    data['color'] = colors[data['weight']]
                else:
                    data['color'] = 'green'
            else:
                data['color'] = 'black'
            
            data['click'] = (
                    f"\nEdge Features:" + 
                    f"\nCLD: {data['cld']}" + 
                    f"\nPolarity Sign: {data['weight']}"
                )
    
    def clean_combined_graph(combined_graph, num_aggregate_nodes=1, num_aggregate_edges=1):
        """
        Cleans the combined graph by aggregating nodes and edges based on the provided thresholds.
        
        Args:
            combined_graph (nx.DiGraph): The combined graph to be cleaned.
            num_aggregate_nodes (int): The threshold of numbers of overlapping nodes to include in the graph.
            num_aggregate_edges (int): The minimum threshodld of number of aggregated edges to include in the graph.
        
        Returns:
            nx.DiGraph: The cleaned graph with aggregated nodes and edges.
        """

        new_graph = nx.DiGraph()
        for node, attrs in combined_graph.nodes(data=True):
            if len(attrs['cld']) > num_aggregate_nodes:
                attrs['single_level'] = attrs.pop('level')
                attrs['level'] = list(set(attrs['single_level']))[0]
                attrs['nums_cld'] = len(attrs['cld'])
                new_graph.add_node(node, **attrs)
        for u, v, attrs in combined_graph.edges(data=True):
            if u in new_graph and v in new_graph:
                edge_attrs = attrs.copy()
                edge_attrs['single_weight'] = edge_attrs.pop('weight')
                edge_attrs['weight'] = edge_attrs.pop('merge_weight')
                if edge_attrs['weight'] > num_aggregate_edges:
                    new_graph.add_edge(u, v, **edge_attrs)
        new_graph.remove_edges_from(nx.selfloop_edges(new_graph))
        return new_graph
    
    def multiply_weights(self):
        """
        Multiplies the weights (polarity sign) of all edges in the given graph `g`.
        
        If an edge has a weight of 1 or -1, it is included in the multiplication.
        Otherwise, the edge is skipped.

        This is used to determined if the cycle is a reinforcing or balancing loop. 
        
        Returns:
            The product of all included edge weights.
        """

        edge_weight = 1
        for u, v, attrs in self.graph.edges(data=True):
            if attrs['weight'] == 1 or attrs['weight'] == -1:
                edge_weight *= attrs['weight']
            else:
                pass
        return edge_weight
    
    def get_nx_graph(self, d, cld_name: str, theme_dict=None, unique_theme_names=None):
        g = nx.DiGraph(d)
        # relabel the nodes to string names
        if theme_dict is not None:
            g = nx.relabel_nodes(g, theme_dict)
        if unique_theme_names is not None:
            g = self.set_node_attributes(g, cld_name=cld_name, unique_theme_names=unique_theme_names)

        g = self.set_edge_attributes(g, cld_name=cld_name)
        
        return g



# # Example usage
# if __name__ == "__main__":""
#     # Initialize graph with data or add nodes/edges as needed
#     graph = nx.DiGraph()
#     cld_graph = CLDGraph(graph)
    
#     # Use the methods as needed
#     cld_graph.graph_properties()
#     cld_graph.node_properties()
#     cld_graph.edge_properties()
#     # Add more functionality as needed
