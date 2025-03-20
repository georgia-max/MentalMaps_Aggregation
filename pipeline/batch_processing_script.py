"""

The script takes the batch tasks data and processes it to create a batch job.
"""
import json
import os
from pprint import pprint

import openai
import pandas as pd
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split

INPUT_SENTENCE_PAIRS_FILE_PATH = "/Users/gl665/Documents/Phrame-MentalMaps-1/data/read_for_label/batch_sum_nlp_results/all_definition_pairs_llm.csv"

OUTPUR_DIR = "/Users/gl665/Documents/Phrame-MentalMaps-1/data/read_for_label/batch_tasks_LLM"


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


system_message = """

Your goal is to label the semantic similarity relationship between two sentences.
You will be given two sentencs. You will output a json object containing the following information:
{
  "categories": [/* integers, 1 if related, 0 otherwise */]
}

The categories field should be an integer between 0 and 1. 1 means the two sentences are semantically related, 0 means they are not semantically related.
"""


def create_user_message(row):
    return f"Sentence: {row['sentence1']}\n\nSentence: {row['sentence2']}\n"


def prepare_example_conversation(row):
    return {
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": create_user_message(row)},
            {"role": "assistant", "content": row["label"]},
        ]
    }


def create_tasks(df):

    tasks = []

    for index, row in df.iterrows():

        two_sentences = "sentence 1: " + \
            str(row['sentence1']) + "\nSentence 2:" + str(row['sentence2'])
        # print(two_sentences)

        task = {
            "custom_id": f"task-{index}",
            "method": "POST",  # TODO: chechk this
            "url": "/v1/chat/completions",
            "body": {

                "model": "ft:gpt-4o-mini-2024-07-18:personal:recipe-ner:B6fnKJqs",
                "temperature": 0.1,
                "response_format": {"type": "json_object"},
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": two_sentences}
                ],
            }
        }

        tasks.append(task)

    return tasks

# Creating the file


def create_batch_job(tasks, file_name: str):
    """
    Creates a batch job from a list of tasks.

    Args:
        tasks: List of task dictionaries to process in batch
        file_name: Name of the JSONL file to create (default: batch_tasks_mentalmap_all_data.jsonl)

    Returns:
        batch_job: The created batch job object
    """
    # Write tasks to JSONL file
    client = load_api_keys()

    file_name = os.path.join(OUTPUR_DIR, file_name)

    with open(file_name, 'w') as file:
        for obj in tasks:
            file.write(json.dumps(obj) + '\n')

    # Create batch file
    batch_file = client.files.create(
        file=open(file_name, "rb"),
        purpose="batch"
    )

    print(batch_file)

    # Create and return batch job
    batch_job = client.batches.create(
        input_file_id=batch_file.id,
        endpoint="/v1/chat/completions",
        completion_window="24h"
    )

    return batch_job


def main():

    # %%
    # all_variables_pairs_df = pd.read_csv("all_variable_pairs.csv")
    all_variables_pairs_df = pd.read_csv(
        INPUT_SENTENCE_PAIRS_FILE_PATH)

    all_variables_pairs_df.rename(
        columns={"Variable 1": "sentence1", "Variable 2": "sentence2"}, inplace=True)
    all_variables_pairs_df.head()

    # all_variables_pairs_df = all_variables_pairs_df.iloc[400000:-40000]
    print(f"total number of rows: {all_variables_pairs_df.shape[0]}")

    # split the dataframe into 20000 rows each and create a list of dataframes for batch processing the tasks
    df_list = [all_variables_pairs_df[i:i+20000]
               for i in range(0, all_variables_pairs_df.shape[0], 20000)]

    print(f"Number of dataframes: {len(df_list)}")

    i = 0
    for df in df_list:
        file_name = f"batch_tasks_mentalmap_{i}.jsonl"
        tasks = create_tasks(df)
        batch_job = create_batch_job(tasks, file_name)
        i += 1
        # print the indx of the number of rows processed
        print(f"Batch job {i} created")
        print(batch_job)
        print("\n----------------------------------\n")
        # check the status of the batch job
        # batch_job = client.batches.retrieve(batch_job.id)
        # print(batch_job)


if __name__ == "__main__":
    main()
