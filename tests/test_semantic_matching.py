"""Tests for the semantic matching component."""

import pytest
import pandas as pd
import networkx as nx
from collections import OrderedDict
from src.semantic_matching.semantic_matching import SemanticMatchingProcessor


@pytest.fixture
def sample_graph_data():
    """Create sample CLD data for testing."""
    # Create graphs for both CLDs
    graph1 = nx.DiGraph()
    graph1.add_nodes_from(
        ["climate change", "economic growth", "population size"])
    graph1.add_edges_from(
        [("climate change", "economic growth"), ("economic growth", "population size")])

    graph2 = nx.DiGraph()
    graph2.add_nodes_from(
        ["sea level rise", "economic growth", "number of people"])
    graph2.add_edges_from(
        [("sea level rise", "economic growth"), ("economic growth", "number of people")])

    # Combine into ordered dictionary
    graph_dict = OrderedDict()
    graph_dict["cld1"] = {
        "name": "cld1",
        "nx_graph": graph1,
        "node_var_def_dict": {}  # Will be populated by semantic matching
    }
    
    graph_dict["cld2"] = {
        "name": "cld2",
        "nx_graph": graph2,
        "node_var_def_dict": {}  # Will be populated by semantic matching
    }

    return graph_dict

    
@pytest.fixture
def sample_data_dictionary():
    """Create sample data dictionary for testing."""
    # Create a DataFrame with variable definitions
    
    data1 = {
        "variable": ["climate change", "economic growth", "population size"],
        "definition": ["Rise in Earth's temperature", "Increase in economic output", "Study of population characteristics"]
    }
    
    data2 = {
        "variable": ["sea level rise", "economic growth", "number of people"], 
        "definition": ["Increase in sea level", "Increase in economic output", "Study of population characteristics"]
    }
    
    outer_dict = OrderedDict()
    outer_dict['cld1'] = {'name': 'cld1', 'definition': dict(zip(data1['variable'], data1['definition']))}
    outer_dict['cld2'] = {'name': 'cld2', 'definition': dict(zip(data2['variable'], data2['definition']))}
    
    return outer_dict




@pytest.fixture
def semantic_processor():
    """Create a SemanticMatchingProcessor instance."""
    return SemanticMatchingProcessor()

#TODO: not yet totally fixed. 
def test_process_single_cld(semantic_processor, sample_graph_data, sample_data_dictionary):
    """Test processing a single CLD."""
    cld_name = 'cld1'
    updated_cld_data = semantic_processor.process_single_cld(
        cld_name, sample_graph_data, sample_data_dictionary
    )

    # Check that the CLD data was updated with node_var_def_dict
    assert "node_var_def_dict" in updated_cld_data
    assert isinstance(updated_cld_data["node_var_def_dict"], dict)

    # Check that matches were found for all nodes
    expected_nodes = ["climate change", "economic growth", "population size"]
    expected_node_var_def_dict = {
        "climate change": [["climate change", "Rise in Earth's temperature"]], 
        "economic growth": [["economic growth", "Increase in economic output"]], 
        "population size": [["population size", "Study of population characteristics"]]
    }

    assert set(updated_cld_data["node_var_def_dict"].keys()) == set(expected_nodes)
    
    assert updated_cld_data["node_var_def_dict"] == expected_node_var_def_dict

#TODO: fix this test
def test_process_all_clds(semantic_processor, sample_graph_data, sample_data_dictionary):
    """Test processing multiple CLDs."""

    clds_dict = OrderedDict([1, sample_graph_data])
    clds_dict.update([2, sample_graph_data_2])
    
    # combine the two data dictionaries
    data_dict = sample_data_dictionary + sample_data_dictionary_2
    

    updated_clds_dict = semantic_processor.process_all_clds(
        clds_dict, data_dict
    )

    # Check that all CLDs were processed
    assert len(updated_clds_dict) == 2
    assert all(
        "node_var_def_dict" in cld_data for cld_data in updated_clds_dict.values())

    # # Check that the combined variable definitions dictionary was created
    # assert isinstance(, dict)
    # assert len(vars_def_dict) > 0


def test_process_cld_with_empty_graph(semantic_processor, sample_data_dictionary):
    """Test processing a CLD with an empty graph."""
    empty_cld_data = {
        "cld_graph": nx.DiGraph(),
        "node_var_def_dict": {}
    }

    updated_cld_data, node_var_dict = semantic_processor.process_cld(
        "cld1", empty_cld_data, sample_data_dictionary
    )

    assert "node_var_def_dict" in updated_cld_data
    assert isinstance(updated_cld_data["node_var_def_dict"], dict)
    assert len(updated_cld_data["node_var_def_dict"]) == 0
    assert len(node_var_dict) == 0


def test_process_cld_with_empty_dictionary(semantic_processor, sample_graph_data):
    """Test processing a CLD with an empty data dictionary."""
    empty_data_dictionary = {"cld1": pd.DataFrame(
        columns=["Variable", "Definition"])}

    updated_cld_data, node_var_dict = semantic_processor.process_cld(
        "cld1", sample_graph_data, empty_data_dictionary
    )

    assert "node_var_def_dict" in updated_cld_data
    assert isinstance(updated_cld_data["node_var_def_dict"], dict)
    assert len(updated_cld_data["node_var_def_dict"]) == 0
    assert len(node_var_dict) == 0


def test_process_cld_with_missing_cld_id(semantic_processor, sample_graph_data, sample_data_dictionary):
    """Test processing a CLD with a missing CLD ID in the data dictionary."""
    with pytest.raises(KeyError):
        semantic_processor.process_cld(
            "missing_cld", sample_graph_data, sample_data_dictionary
        )


def test_process_all_clds_with_empty_input(semantic_processor, sample_data_dictionary):
    """Test processing an empty CLDs dictionary."""
    empty_clds_dict = {}
    updated_clds_dict, vars_def_dict = semantic_processor.process_all_clds(
        empty_clds_dict, sample_data_dictionary
    )

    assert len(updated_clds_dict) == 0
    assert len(vars_def_dict) == 0


def test_process_all_clds_with_empty_dictionary(semantic_processor, sample_graph_data):
    """Test processing CLDs with an empty data dictionary."""
    clds_dict = {
        "cld1": sample_graph_data.copy(),
        "cld2": sample_graph_data.copy()
    }
    empty_data_dictionary = {}

    updated_clds_dict, vars_def_dict = semantic_processor.process_all_clds(
        clds_dict, empty_data_dictionary
    )

    assert len(updated_clds_dict) == 2
    assert all(
        "node_var_def_dict" in cld_data for cld_data in updated_clds_dict.values())
    assert all(len(cld_data["node_var_def_dict"]) ==
               0 for cld_data in updated_clds_dict.values())
    assert len(vars_def_dict) == 0
