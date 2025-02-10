# last update 2024-07-30
# this file look into the data dictionary csv file and creates a list of pairs of sentences
# for labeling.

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer


# read in data dictionary excel file as a for loop for each variable in the data dictionary
input_file_path = "data/raw/SYNCH/RC/excel_sheets/Rapid City SYNCH Models data dictionary0715.xlsx"
# Create an empty dictionary to store the data frames
excel_sheets = {}

cld_dataframe = {}

# Read all sheets into the dictionary
for sheet_name in pd.ExcelFile(input_file_path).sheet_names:
    excel_sheets[sheet_name] = pd.read_excel(
        input_file_path, sheet_name=sheet_name)
    if "changed variable names" in excel_sheets[sheet_name].columns:
        print("Geting Sheet: ", sheet_name)

        cld_dataframe[sheet_name] = excel_sheets[sheet_name][[
            'variable', 'changed variable names', 'definition']]
        cld_dataframe[sheet_name] = cld_dataframe[sheet_name].dropna()
    else:
        pass


# concatenate all the variable names into a single list
all_variable_names = []
for sheet_name, data in cld_dataframe.items():
    all_variable_names.extend(data['changed variable names'].tolist())

print("number of all the variables", len(all_variable_names))
# get only uniquee variable names
unique_variable_names = list(set(all_variable_names))
print("numbers of the unique variables", len(unique_variable_names))


# run a sentence transformer to group the sentences into pairs
model = SentenceTransformer("all-mpnet-base-v2")
embeddings_cld = model.encode(unique_variable_names)
similarities = model.similarity(embeddings_cld, embeddings_cld)



high_similarity_pairs = {}
high_similarity_dictionary = {}
for idx_i, sentence1 in enumerate(unique_variable_names):
    for idx_j, sentence2 in enumerate(unique_variable_names):
        if (similarities[idx_i][idx_j] > 0.6) and (similarities[idx_i][idx_j] < 0.95):
            score = similarities[idx_i][idx_j].numpy().max()
            high_similarity_dictionary[(idx_i, idx_j)] = {
                'sentence1': sentence1,
                'sentence2': sentence2,
                'score': score
            }
high_similarity_df = pd.DataFrame(high_similarity_dictionary).T
high_similarity_df = high_similarity_df.reset_index()
# print(high_similarity_df.head())

# low_similarity_pairs = {}
# low_similarity_dictionary = {}
# for idx_i, sentence1 in enumerate(unique_variable_names):
#     for idx_j, sentence2 in enumerate(unique_variable_names):
#         if (similarities[idx_i][idx_j] > 0.5) and (similarities[idx_i][idx_j] < 0.6):
#             score = similarities[idx_i][idx_j].numpy().max()
#             low_similarity_dictionary[(idx_i, idx_j)] = {
#                 'sentence1': sentence1,
#                 'sentence2': sentence2,
#                 'score': score
#             }

# low_similarity_df = pd.DataFrame(low_similarity_dictionary).T
# low_similarity_df = low_similarity_df.reset_index()
# print(low_similarity_df.head())

# concatenate the high and low similarity df

all_similarity_df = high_similarity_df
# all_similarity_df = pd.concat(
#     [high_similarity_df, low_similarity_df], ignore_index=True)
all_similarity_df['idx'] = all_similarity_df.index
all_similarity_df = all_similarity_df.drop(['level_0', 'level_1'], axis=1)
print(all_similarity_df.shape)


# export the df to csv file
# all_similarity_df.to_csv(
#     "data/interim/RC/ready_for_labeling/training_set_forlabel_var_0715.csv", index=False)
# all_similarity_df.to_csv(
#     "data/interim/RC/ready_for_labeling/training_set_forlabel_var_0715.csv", index=False)
