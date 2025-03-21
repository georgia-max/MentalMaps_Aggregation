from pathlib import Path
from typing import Dict, Optional

from src.data_management.data_loader import DataLoader
from src.data_management.data_saver import DataSaver
from src.semantic_matching.semantic_matching import SemanticMatchingProcessor

# from src.parsers.json_parser import JSONParser
# from src.graph_processing.graph_builder import GraphBuilder


# def main():
#     # Initialize data handlers
#     loader = DataLoader()
#     saver = DataSaver()


#     # Load data
#     clds_dict = loader.load_clds_from_directory(INPUT_CLD_FOLDER)
#     # data_dictionary = loader.load_data_dictionary(INPUT_FILE)

#     # Process data...

#     # Save results
#     saver.save_clds_dictionary(clds_dict, OUTPUT_CLD_FOLDER)
#     # saver.save_variables_dictionary(vars_def_dict, OUTPUT_FILE)


class Pipeline:
    """Main pipeline for CLD processing"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.loader = DataLoader()
        self.saver = DataSaver()
        self.semantic_processor = SemanticMatchingProcessor()
        # self.parser = JSONParser()
        # self.graph_builder = GraphBuilder()

    def run(self,
            input_dir: Path,
            data_dict_path: Path,
            output_dir: Path) -> None:
        """
        Run the complete pipeline

        Args:
            input_dir: Directory containing CLD files
            data_dict_path: Path to data dictionary file
            output_dir: Directory for output files
        """
        # Load data
        clds_dict = self.loader.load_clds_from_directory(input_dir)
        # print(clds_dict)

        data_dictionary = self.loader.load_data_dictionary_from_excel(
            data_dict_path)
        print(data_dictionary)

        # # # Process CLDs with semantic matching
        # clds_dict, vars_def_dict = self.semantic_processor.process_all_clds(
        #     clds_dict, data_dictionary)

        # Save results
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # self.saver.save_variables_dictionary(
        #     vars_def_dict,
        #     output_dir / "all_vars_def_dictionary.pkl"
        # )
        # self.saver.save_clds_dictionary(
        #     clds_dict,
        #     output_dir / "clds_dictionary.pkl"
        # )


def main():
    """Entry point for the pipeline"""
    # Define paths

    base_dir = Path(__file__).parent.parent.parent
    INPUT_CLD_FOLDER = base_dir / \
        "data/raw/rc_mental_models_clean"

    data_dict_path = base_dir / "data/data_dictionary/Data_Dictionary.xlsx"

    OUTPUT_CLD_FOLDER = base_dir / "data/just_testing"

    # output_dir = base_dir / "data/output"

    # Run pipeline
    pipeline = Pipeline()
    pipeline.run(INPUT_CLD_FOLDER, data_dict_path,  OUTPUT_CLD_FOLDER)


if __name__ == "__main__":
    main()
