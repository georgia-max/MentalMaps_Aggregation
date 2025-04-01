"""Test cases for the CLDGraph class."""

import pytest
import networkx as nx
from src.graph_processing.graph_properties import CLDGraph


@pytest.fixture
def sample_graph():
    """Create a sample directed graph for testing."""
    d = {
        'A': {'B': {'weight': 1}},
        'B': {'C': {'weight': -1}},
        'C': {'A': {'weight': 1}}
    }
    return nx.DiGraph(d)

@pytest.fixture
def sample_theme_dict():
    """Create a sample theme dictionary for testing."""
    return {'A': 'Alpha', 'B': 'Bravo', 'C': 'Charlie'}

def test_initialization(sample_graph):
    """Test graph initialization."""
    # Test initialization with no graph
    empty_graph = CLDGraph()
    assert isinstance(empty_graph, nx.DiGraph)
    assert empty_graph.number_of_nodes() == 0
    assert empty_graph.number_of_edges() == 0

    # Test initialization with existing graph
    cld_graph = CLDGraph(sample_graph)
    assert isinstance(cld_graph, nx.DiGraph)
    assert cld_graph.number_of_nodes() == 3
    assert cld_graph.number_of_edges() == 3


def test_set_node_attributes(sample_graph, sample_theme_dict):
    """Test setting node attributes."""
    cld_graph = CLDGraph(sample_graph)

    # Test without theme dictionary
    cld_graph.set_node_attributes()
    for node in cld_graph.nodes():
        assert 'level' not in cld_graph.nodes[node]

    # Test with theme dictionary
    cld_graph.set_node_attributes(sample_theme_dict)
    for node in cld_graph.nodes():
        assert 'level' in cld_graph.nodes[node]
        if node in sample_theme_dict:
            assert cld_graph.nodes[node]['level'] == 'theme'
        else:
            assert cld_graph.nodes[node]['level'] == 'org'


def test_set_edge_attributes(sample_graph):
    """Test setting edge attributes."""
    cld_graph = CLDGraph(sample_graph)
    cld_graph.set_edge_attributes()

    # Check that all edges have weight attributes
    for u, v, data in cld_graph.edges(data=True):
        assert 'weight' in data
        assert isinstance(data['weight'], int)


def test_graph_properties(sample_graph):
    """Test graph property methods."""
    cld_graph = CLDGraph(sample_graph)

    # Test graph_properties
    assert cld_graph.is_directed() is True
    assert cld_graph.number_of_nodes() == 3
    assert cld_graph.number_of_edges() == 3

    # Test node_properties
    nodes = list(cld_graph.nodes())
    assert len(nodes) == 3
    assert all(isinstance(node, str) for node in nodes)

    # Test edge_properties
    edges = list(cld_graph.edges())
    assert len(edges) == 3
    assert all(isinstance(edge[0], str) and isinstance(
        edge[1], str) for edge in edges)


def test_combine_graphs_with_node_attributes():
    """Test combining multiple graphs."""
    # Create two graphs to combine
    g1 = nx.DiGraph()
    g1.add_edge('A', 'B', weight=1)
    g1.add_node('A', level='theme')
    g1.add_node('B', level='org')

    g2 = nx.DiGraph()
    g2.add_edge('B', 'C', weight=-1)
    g2.add_node('B', level='org')
    g2.add_node('C', level='theme')

    # Create a list of graphs
    graphs = [g1, g2]

    # Create a CLDGraph and combine
    cld_graph = CLDGraph()
    combined = cld_graph.combine_graphs_with_node_attributes()

    # Check combined graph properties
    assert combined.number_of_nodes() == 3  # A, B, C
    assert combined.number_of_edges() == 2  # A->B, B->C

    # Check node attributes
    assert 'level' in combined.nodes['A']
    assert 'level' in combined.nodes['B']
    assert 'level' in combined.nodes['C']


def test_multiply_weights(sample_graph):
    """Test weight multiplication for cycle detection."""
    cld_graph = CLDGraph(sample_graph)

    # In this sample graph: 1 * -1 * 1 = -1 (balancing loop)
    result = cld_graph.multiply_weights()
    assert result == -1


def test_get_nx_graph():
    """Test creating a NetworkX graph from dictionary."""
    d = {
        'A': {'B': {'weight': 1}},
        'B': {'C': {'weight': -1}}
    }

    cld_graph = CLDGraph()
    g = cld_graph.get_nx_graph(d)

    assert isinstance(g, nx.DiGraph)
    assert g.number_of_nodes() == 3
    assert g.number_of_edges() == 2
    assert g.has_edge('A', 'B')
    assert g.has_edge('B', 'C')
    assert g['A']['B']['weight'] == 1
    assert g['B']['C']['weight'] == -1
