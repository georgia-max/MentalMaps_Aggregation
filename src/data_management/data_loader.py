# src/data_management/data_loader.py

import json
import pickle
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Union

from src.parsers.vensim_parser import VensimParser, CLDParser


import networkx as nx
import pandas as pd


@dataclass
class DataDictionary:
    """Data structure for data dictionary"""
    variables: Dict[str, str]  # variable name to definition mapping
    metadata: Dict = None  # Optional metadata


class DataLoader:
    """Handles loading of various data types used in the pipeline"""

    def __init__(self):
        self.supported_formats = {
            '.json': self._load_json,
            '.pkl': self._load_pickle,
            '.xlsx': self._load_excel,
            '.csv': self._load_csv, 
            '.mdl': self._load_vensim
        }

    def load_file(self, file_path: Union[str, Path],
                  format: Optional[str] = None) -> Union[Dict, pd.DataFrame]:
        """
        Load data from a file, automatically detecting format if not specified.

        Args:
            file_path: Path to the file
            format: Optional format specification

        Returns:
            Loaded data in appropriate format

        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file doesn't exist
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if format is None:
            format = file_path.suffix.lower()

        if format not in self.supported_formats:
            raise ValueError(f"Unsupported format: {format}")

        return self.supported_formats[format](file_path)

    def load_data_dictionary(self, file_path: Union[str, Path]) -> Dict[int, pd.DataFrame]:
        """
        Load data dictionary from Excel file.

        Args:
            file_path: Path to Excel file

        Returns:
            Dictionary mapping sheet numbers to DataFrames
        """
        excel_data = pd.read_excel(file_path, sheet_name=None)
        data_dictionary = {}

        for k, v in excel_data.items():
            v.columns.values[0] = "variable"
            v.columns.values[1] = "definition"
            data_dictionary[int(k)] = v

        return data_dictionary

    def load_clds_from_directory(self, directory: Union[str, Path]) -> OrderedDict:
        """
        Load multiple CLDs from a directory.

        Args:
            directory: Path to directory containing CLD files

        Returns:
            OrderedDict mapping IDs, name and cld_graph
            e.g. {1: {'name': 'test.mdl', 'cld_graph': <networkx.classes.digraph.DiGraph object at 0x7f911c177190>}}
            
        """
        directory = Path(directory)
        clds_dict = OrderedDict()
        count = 1

        for file_path in directory.glob('*'):
            if file_path.suffix in ['.json', '.pkl', '.mdl']:
                try:
                    data = self.load_file(file_path)
                    if isinstance(data, (list, tuple)) and len(data) == 2:
                        G = nx.from_dict_of_dicts(
                            data[1], create_using=nx.DiGraph)
                        G = nx.relabel_nodes(G, data[0])

                        clds_dict[count] = {
                            'name': file_path.name,
                            'cld_graph': G
                        }
                        count += 1
                except Exception as e:
                    print(f"Error loading {file_path}: {str(e)}")

        return clds_dict

    def _load_json(self, file_path: Path) -> Dict:
        """Load data from JSON file"""
        with open(file_path, 'r') as f:
            return json.load(f)

    def _load_pickle(self, file_path: Path) -> Dict:
        """Load data from pickle file"""
        with open(file_path, 'rb') as f:
            return pickle.load(f)

    def _load_excel(self, file_path: Path) -> pd.DataFrame:
        """Load data from Excel file"""
        return pd.read_excel(file_path)

    def _load_csv(self, file_path: Path) -> pd.DataFrame:
        """Load data from CSV file"""
        return pd.read_csv(file_path)

    def _load_vensim(self, file_path: Path) -> Dict:
        """Load data from Vensim file and parse it into a dictionary"""
        parser = CLDParser()
        return parser.parse(file_path)

