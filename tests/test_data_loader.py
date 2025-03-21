import json
import pickle
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
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()
    return data_dir


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


def test_load_clds_from_directory(data_loader, test_data_dir, sample_pickle_file):
    # Create a second pickle file
    test_data2 = [
        {"3": "var3", "4": "var4"},
        {"3": {"4": {"weight": 1}}}
    ]
    file_path2 = test_data_dir / "test2.pkl"
    with open(file_path2, 'wb') as f:
        pickle.dump(test_data2, f)

    clds_dict = data_loader.load_clds_from_directory(test_data_dir)
    assert len(clds_dict) == 2
    assert all(isinstance(cld['cld_graph'], nx.DiGraph)
               for cld in clds_dict.values())


def test_load_file_invalid_format(data_loader, test_data_dir):
    # Create a file with invalid format
    invalid_file = test_data_dir / "test.invalid"
    invalid_file.touch()

    with pytest.raises(ValueError):
        data_loader.load_file(invalid_file)


def test_load_file_nonexistent(data_loader):
    with pytest.raises(FileNotFoundError):
        data_loader.load_file("nonexistent_file.json")
