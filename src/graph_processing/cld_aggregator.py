

#TODO:old redundant code

class CLD_aggregator:
    def __init__(self, graph):
        self.graph = graph

    def combine_graphs_with_node_attributes(self):
        """
        Combines multiple graphs into a single graph, merging node attributes and edge attributes.

        Args:
            graphs (list): A list of NetworkX DiGraph objects to be combined.

        Returns:
            nx.DiGraph: A single combined graph with merged node and edge attributes.
        """

        combined_graph = nx.DiGraph()
        for g in self:
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
                    combined_graph[u][v]['merge_weight'] = list(
                        set_unique_weights)[0]
                elif 3 in set_unique_weights and len(set_unique_weights) == 2:
                    set_unique_weights.remove(3)
                    combined_graph[u][v]['merge_weight'] = list(
                        set_unique_weights)[0]
                else:
                    combined_graph[u][v]['merge_weight'] = 0
        return combined_graph

    def clean_combined_graph(self, combined_graph, num_aggregate_nodes=1, num_aggregate_edges=1):
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
