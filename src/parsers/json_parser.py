# src/parsers/json_parser.py

from pathlib import Path
from typing import Dict, List, Tuple, Union
import pickle
import json
from dataclasses import dataclass
import networkx as nx
from collections import OrderedDict


@dataclass
class CLDData:
    """Data structure for CLD information"""
    node_mapping: Dict[int, str]  # Maps node IDs to names
    graph_data: Dict  # Graph structure in dict-of-dicts format
    metadata: Dict = None  # Optional metadata


class JSONParser:
    """Parser for CLD JSON files"""

    def __init__(self):
        self.supported_formats = ['.json', '.pkl']

    def load_cld(self, file_path: Union[str, Path]) -> CLDData:
        """
        Load a CLD from a JSON or pickle file.
        
        Args:
            file_path: Path to the CLD file
            
        Returns:
            CLDData object containing the parsed data
            
        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file doesn't exist
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.suffix not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")

        if file_path.suffix == '.pkl':
            return self._load_pickle(file_path)
        else:
            return self._load_json(file_path)

    def _load_pickle(self, file_path: Path) -> CLDData:
        """Load CLD data from a pickle file"""
        with open(file_path, 'rb') as f:
            data = pickle.load(f)

        if not isinstance(data, (list, tuple)) or len(data) != 2:
            raise ValueError("Invalid pickle file format")

        return CLDData(
            node_mapping=data[0],
            graph_data=data[1],
            metadata={'source': str(file_path)}
        )

    def _load_json(self, file_path: Path) -> CLDData:
        """Load CLD data from a JSON file"""
        with open(file_path, 'r') as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError("Invalid JSON format")

        return CLDData(
            node_mapping=data.get('nodes', {}),
            graph_data=data.get('graph', {}),
            metadata=data.get('metadata', {})
        )

    def save_cld(self, cld_data: CLDData, file_path: Union[str, Path],
                 format: str = 'pkl') -> None:
        """
        Save CLD data to a file.
        
        Args:
            cld_data: CLDData object to save
            file_path: Path where to save the file
            format: Output format ('pkl' or 'json')
            
        Raises:
            ValueError: If format is not supported
        """
        file_path = Path(file_path)

        if format == 'pkl':
            self._save_pickle(cld_data, file_path)
        elif format == 'json':
            self._save_json(cld_data, file_path)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _save_pickle(self, cld_data: CLDData, file_path: Path) -> None:
        """Save CLD data as pickle file"""
        with open(file_path, 'wb') as f:
            pickle.dump([cld_data.node_mapping, cld_data.graph_data], f)

    def _save_json(self, cld_data: CLDData, file_path: Path) -> None:
        """Save CLD data as JSON file"""
        data = {
            'nodes': cld_data.node_mapping,
            'graph': cld_data.graph_data,
            'metadata': cld_data.metadata or {}
        }
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def load_clds_from_directory(self, directory: Union[str, Path]) -> OrderedDict:
        """
        Load multiple CLDs from a directory.
        
        Args:
            directory: Path to directory containing CLD files
            
        Returns:
            OrderedDict mapping IDs to CLD graphs and metadata
        """
        directory = Path(directory)
        clds_dict = OrderedDict()
        count = 1

        for file_path in directory.glob('*'):
            if file_path.suffix in self.supported_formats:
                try:
                    cld_data = self.load_cld(file_path)
                    G = nx.from_dict_of_dicts(
                        cld_data.graph_data, create_using=nx.DiGraph)
                    G = nx.relabel_nodes(G, cld_data.node_mapping)

                    clds_dict[count] = {
                        'name': file_path.name,
                        'cld_graph': G,
                        'metadata': cld_data.metadata
                    }
                    count += 1
                except Exception as e:
                    print(f"Error loading {file_path}: {str(e)}")

        return clds_dict


# Example usage:
if __name__ == "__main__":
    parser = JSONParser()

    # Load a single CLD
    cld_data = parser.load_cld('path/to/cld.json')

    # Load multiple CLDs from directory
    clds_dict = parser.load_clds_from_directory('path/to/clds/directory')

    # Save a CLD
    parser.save_cld(cld_data, 'path/to/output.pkl', format='pkl')


# from tqdm import tqdm
# import matplotlib.pyplot as plt
# import networkx as nx
# import pickle
# import sys
# import time
# import os

# import gravis
# import pandas as pd

# from vensim_parser import CLDParser

# from data_io import read_json, read_cld_file

# import traceback

# def main():

#     try:

#         # Check if the file exists
#         if not os.path.isfile(sys.argv[1]):
#             print(sys.argv[1], "does not exist or is not a file.")

#             raise FileNotFoundError(f"File not found: {sys.argv[1]}")


#         #  Open the file and read its contents
#         input_file = sys.argv[1]
#         output_file = sys.argv[2]

#         df = read_cld_file(input_file)
        
#         cld = CLDParser(df)

#         cld_data = cld.get_cld_dict()

#         with open(output_file, 'wb') as f:
#             pickle.dump(cld_data, f)

#         # G = nx.MultiDiGraph(d)

#         # cld_nx.draw_labeled_multigraph(G, "weight", dict_vars_name)
#         # # plt.show()
#         # plt.savefig(file_name + ".png")

#     except Exception as e:

#         traceback.print_exc()  # This will print the error traceback

#         if len(sys.argv) != 3:
#             print("Type in the .mdl file and the output file name. Example: python3 main.py input.mdl output.json")

#         sys.exit(1)
# if __name__ == "__main__":

#     for i in tqdm(range(100), desc=f"Loading..."):
#         pass
#     main()
