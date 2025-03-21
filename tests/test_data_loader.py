import json
import pickle
from collections import OrderedDict
from pathlib import Path

import networkx as nx
import pandas as pd
import pytest

from src.data_management.data_loader import DataLoader


@pytest.fixture
def data_loader():
    return DataLoader()


@pytest.fixture
def test_data_dir(tmp_path):
    # Create test data directory
    data_dir = tmp_path / "sample_files"
    data_dir.mkdir()
    return data_dir


@pytest.fixture
def test_sample_data_dir():
    """Get the path to the test data directory."""
    # Get the project root directory (where the tests directory is located)
    project_root = Path(__file__).parent.parent
    return project_root / "test_data"


@pytest.fixture
def test_model_files(test_data_dir):
    """Get paths to test model files."""
    return {
        "model1": test_data_dir / "test_model.mdl",
        "model2": test_data_dir / "test_model2.mdl"
    }


@pytest.fixture
def sample_json_file(test_data_dir):
    # Create a sample JSON file
    test_data = {
        "variables": {"1": "var1", "2": "var2"},
        "relationships": {"1": {"2": {"weight": 1}}}
    }
    file_path = test_data_dir / "test.json"
    with open(file_path, 'w') as f:
        json.dump(test_data, f)
    return file_path


@pytest.fixture
def sample_pickle_file(test_data_dir):
    # Create a sample pickle file
    test_data = [
        {"1": "var1", "2": "var2"},  # node mapping
        {"1": {"2": {"weight": 1}}}  # graph data
    ]
    file_path = test_data_dir / "test.pkl"
    with open(file_path, 'wb') as f:
        pickle.dump(test_data, f)
    return file_path


def test_load_file_json(data_loader, sample_json_file):
    data = data_loader.load_file(sample_json_file)

    assert isinstance(data, dict)
    assert "variables" in data
    assert "relationships" in data


def test_load_file_pickle(data_loader, sample_pickle_file):
    data = data_loader.load_file(sample_pickle_file)
    assert isinstance(data, list)
    assert len(data) == 2
    assert isinstance(data[0], dict)
    assert isinstance(data[1], dict)


def test_load_clds_from_directory(data_loader, test_sample_data_dir):
    """Test loading multiple CLDs from a directory."""
    # Load CLDs from test directory
    clds_dict = data_loader.load_clds_from_directory(test_sample_data_dir)

    # Check we got the expected number of CLDs
    assert isinstance(clds_dict, OrderedDict)
    assert len(clds_dict) == 2

    # Check structure of first CLD
    first_cld_name = list(clds_dict.keys())[0]
    first_cld = clds_dict[first_cld_name]

    # Verify dictionary structure
    assert isinstance(first_cld, dict)
    assert 'name' in first_cld
    assert 'nx_graph' in first_cld

    # Verify graph object
    assert isinstance(first_cld['nx_graph'], nx.DiGraph)

    # Verify name matches file name
    assert first_cld['name'] == first_cld_name


def test_load_file_invalid_format(data_loader, test_data_dir):
    # Create a file with invalid format
    invalid_file = test_data_dir / "test.invalid"
    invalid_file.touch()

    with pytest.raises(ValueError):
        data_loader.load_file(invalid_file)


def test_load_file_nonexistent(data_loader):
    with pytest.raises(FileNotFoundError):
        data_loader.load_file("nonexistent_file.json")


def test_load_data_dictionary_from_excel(data_loader, test_data_dir):
    # Create a test Excel file with sample data
    test_excel_path = test_data_dir / "test_dictionary.xlsx"
    df1 = pd.DataFrame({
        'Variable': ['var1', 'var2'],
        'Definition': ['def1', 'def2']
    })
    df2 = pd.DataFrame({
        'Variable': ['var3', 'var4'], 
        'Definition': ['def3', 'def4']
    })
    with pd.ExcelWriter(test_excel_path) as writer:
        df1.to_excel(writer, sheet_name='Sheet1', index=False)
        df2.to_excel(writer, sheet_name='Sheet2', index=False)

    data_dict = data_loader.load_data_dictionary_from_excel(test_excel_path)

    assert isinstance(data_dict, OrderedDict)
    assert len(data_dict) == 2  # Two sheets

    # Check first sheet
    assert isinstance(data_dict['Sheet1'], OrderedDict)
    assert data_dict['Sheet1']['name'] == 'Sheet1'
    assert data_dict['Sheet1']['definition']['var1'] == 'def1'
