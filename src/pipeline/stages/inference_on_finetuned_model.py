# %%
import json
import os
from pprint import pprint

import openai
import pandas as pd
import tqdm as tqdm
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split

load_dotenv()
client = openai.OpenAI(api_key=os.getenv(
    "OPENAI_API_KEY"))

FILE_PATH = "C:\\Users\\GL665\\Documents\\Phrame-MentalMaps\\notebook\\all_definition_pairs.csv"
OUTPUT_FILE_PATH = "C:\\Users\\GL665\\Documents\\Phrame-MentalMaps\\notebook\\all_definition_pairs_predictions.csv"

system_message = """

You are a helpful assistant. You will be given two sentencs, and you will have to label the semantic relationship between them. 
If the two sentences are semantically related, you will label them as 1. If they are not semantically related, you will label them as 0. 

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


# # predict the rest of the data
job_id = "ftjob-dttfKWZEbLqmzRJXLXtaYEbM"


response = client.fine_tuning.jobs.retrieve(job_id)
fine_tuned_model_id = response.fine_tuned_model

if fine_tuned_model_id is None:
    raise RuntimeError(
        "Fine-tuned model ID not found. Your job has likely not been completed yet."
    )

print("Fine-tuned model ID:", fine_tuned_model_id)

# # %%
# test_mes = [{'content': '\n'
#              '\n'
#              'You are a helpful assistant. You will be given two sentencs, and '
#              'you will have to label the semantic relationship between them. \n'
#              'If the two sentences are semantically related, you will label '
#              'them as 1. If they are not semantically related, you will label '
#              'them as 0. \n'
#              '\n',
#              'role': 'system'},
#             {'content': 'Sentence: trust in police\n\nSentence: fear of police\n',
#              'role': 'user'}]

# response = client.chat.completions.create(
#     model=fine_tuned_model_id, messages=test_mes, temperature=0, max_tokens=500
# )
# print(response.choices[0].message.content)


def main():
    # all_variables_pairs_df = pd.read_csv("all_variable_pairs.csv")
    all_variables_pairs_df = pd.read_csv(FILE_PATH)

    all_variables_pairs_df.rename(
        columns={"Variable 1": "sentence1", "Variable 2": "sentence2"}, inplace=True)

    all_messages = [
        [
            {"role": "system", "content": system_message},
            {"role": "user", "content": create_user_message(row)}
        ]
        for row in all_variables_pairs_df.to_dict('records')
    ]

    batch_size = 200
    total_batches = len(all_messages) // batch_size + \
        (1 if len(all_messages) % batch_size else 0)
    print(f"Total batches: {total_batches}")

    for batch_num in range(534, total_batches):
        print("Batch:", batch_num, "/ ",  total_batches)
        start_idx = batch_num * batch_size
        end_idx = min((batch_num + 1) * batch_size, len(all_messages))
        batch = all_messages[start_idx:end_idx]
        # input messages
        input_messages = [msg[1]['content'] for msg in batch]

        # Process batch
        responses = [
            client.chat.completions.create(
                model=fine_tuned_model_id,
                messages=msg,
                temperature=0,
                max_tokens=500
            ) for msg in batch
        ]

        batch_results = [
            response.choices[0].message.content for response in responses]

        # Save batch results
        batch_df = pd.DataFrame({
            'input_message': input_messages,
            'predicted_label': batch_results,
            'batch_number': batch_num
        })
        # print(batch_df)
        # create folder if it doesn't exist
        if not os.path.exists('results'):
            os.makedirs('results')

        batch_df.to_csv(f'results/batch_{batch_num}.csv', index=False)

        print(f"Completed batch {batch_num + 1}/{total_batches}")


if __name__ == "__main__":

    main()
