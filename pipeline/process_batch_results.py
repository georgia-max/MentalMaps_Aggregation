import json
import os
from pathlib import Path

import openai
import pandas as pd
from dotenv import load_dotenv


def load_api_keys():
    """Load API keys from environment variables."""
    # Load environment variables from .env file
    load_dotenv()

    # Get OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    # Initialize OpenAI client
    return openai.OpenAI(api_key=api_key)


def load_results(result_file_path):
    """Load and parse results from the JSONL file."""
    results = []
    with open(result_file_path, 'r') as file:
        for line_number, line in enumerate(file, 1):
            try:
                # Remove any whitespace and check if line is empty
                line = line.strip()
                if not line:
                    continue

                # Parsing the JSON string into a dict and appending to the list of results
                json_object = json.loads(line)
                results.append(json_object)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON on line {line_number}:")
                print(f"Line content: {line}")
                print(f"Error details: {str(e)}")
                print("---")
                continue  # Skip this line and continue with the next one

    print(f"Successfully parsed {len(results)} results")
    return results


def process_results(results, df):
    """Extract categories from results and add them to the DataFrame."""
    categories = []
    indices = []

    for res in results:
        try:
            # Get the task ID and content
            task_id = res['custom_id']
            index = int(task_id.split('-')[-1])

            indices.append(index)

            # Parse the content as JSON and extract category
            content = res['response']['body']['choices'][0]['message']['content']
            result_dict = json.loads(content)
            category = result_dict['categories'][0]
            categories.append(float(category))

        except (KeyError, json.JSONDecodeError, IndexError, ValueError) as e:
            print(f"Error processing result for task {task_id}: {str(e)}")
            print(f"Problematic content: {content}")
            categories.append(None)

    # Create a Series with the categories
    category_series = pd.Series(categories, index=indices)

    # Add categories to the DataFrame
    df['category'] = category_series

    return df


def main():
    try:

        # File paths
        result_file = "notebook/result_0307.jsonl"
        # Update this path as needed
        input_csv = "data/read_for_label/all_definition_pairs.csv"
        output_csv = "notebook/processed_results.csv"

        # Load the original DataFrame
        df = pd.read_csv(input_csv, index_col=0)
        df.rename(columns={"Variable 1": "sentence1",
                  "Variable 2": "sentence2"}, inplace=True)

        # Load and process results
        results = load_results(result_file)
        df = process_results(results, df)

        # Save processed results
        df.to_csv(output_csv)

        # Print statistics
        print("\nCategory distribution:")
        print(df['category'].value_counts(dropna=False))
        print("\nFirst few rows of processed data:")
        print(df.head())

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    main()
