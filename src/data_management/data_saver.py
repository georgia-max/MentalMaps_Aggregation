from pathlib import Path
from typing import Dict, Union, Any
import pickle
import json
import pandas as pd
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class SaveConfig:
    """Configuration for saving data"""
    format: str = 'pkl'
    indent: int = 2
    encoding: str = 'utf-8'
    compression: bool = False


class DataSaver:
    """Handles saving of various data types used in the pipeline"""

    def __init__(self):
        self.supported_formats = {
            'pkl': self._save_pickle,
            'json': self._save_json,
            'excel': self._save_excel,
            'csv': self._save_csv
        }

    def save_data(self, data: Any, file_path: Union[str, Path],
                  config: Optional[SaveConfig] = None) -> None:
        """
        Save data to a file.
        
        Args:
            data: Data to save
            file_path: Path where to save the file
            config: Optional save configuration
            
        Raises:
            ValueError: If format is not supported
        """
        file_path = Path(file_path)
        config = config or SaveConfig()

        if config.format not in self.supported_formats:
            raise ValueError(f"Unsupported format: {config.format}")

        self.supported_formats[config.format](data, file_path, config)

    def save_clds_dictionary(self, clds_dict: Dict, file_path: Union[str, Path]) -> None:
        """
        Save CLDs dictionary to file.
        
        Args:
            clds_dict: Dictionary of CLDs to save
            file_path: Path where to save the file
        """
        self.save_data(clds_dict, file_path)

    def save_variables_dictionary(self, vars_dict: Dict, file_path: Union[str, Path]) -> None:
        """
        Save variables dictionary to file.
        
        Args:
            vars_dict: Dictionary of variables to save
            file_path: Path where to save the file
        """
        self.save_data(vars_dict, file_path)

    def _save_pickle(self, data: Any, file_path: Path, config: SaveConfig) -> None:
        """Save data as pickle file"""
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)

    def _save_json(self, data: Any, file_path: Path, config: SaveConfig) -> None:
        """Save data as JSON file"""
        with open(file_path, 'w', encoding=config.encoding) as f:
            json.dump(data, f, indent=config.indent)

    def _save_excel(self, data: pd.DataFrame, file_path: Path, config: SaveConfig) -> None:
        """Save data as Excel file"""
        data.to_excel(file_path, index=False)

    def _save_csv(self, data: pd.DataFrame, file_path: Path, config: SaveConfig) -> None:
        """Save data as CSV file"""
        data.to_csv(file_path, index=False)
