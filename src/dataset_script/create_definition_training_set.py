# deprecated
# Create training set based on definitions

import pandas as pd
from itertools import combinations
# from ..utils.data_io import read_json
import json
import os
from collections import ChainMap

# Step 1: Define the file paths
input_csv = 'data/processed/SYNCH/training_set/training_set_0625.csv'  
output_dataset_path = 'data/processed/SYNCH/training_set/training_set_def_0625.csv'  

# Step 2: Read the CSV file into a DataFrame
df = pd.read_csv(input_csv)

cld_list =[]

# Open the JSON file
data_dictionary_path = "/Users/gl665/PycharmProjects/Phrame_MentalMaps/data/interim/RC/results sheets/data_dictionary/"

for filename in os.listdir(data_dictionary_path):
    if filename.endswith('.json'):
        file_path = os.path.join(data_dictionary_path, filename)
        with open(file_path, 'r',  encoding='utf-8') as f:
            print("load:",filename)
            data = json.load(f)
            cld_list.append(data)



final_dict = ChainMap(*cld_list)

new_df = df.copy()  # Create a copy of the original DataFrame

for index, row in df.iterrows():
    sentence1 = row['sentence1']  # Assuming 'sentence1' is a column in your DataFrame
    if sentence1 in final_dict:
        new_df.at[index, 'def1'] = final_dict[sentence1]
    else:
        pass
    
    sentence2 = row['sentence2']  # Assuming 'sentence1' is a column in your DataFrame
    if sentence2 in final_dict:
        new_df.at[index, 'def2'] = final_dict[sentence2]
    else:
        pass
        

    
# Step 4: export the dataframe as a csv file 
new_df.to_csv(output_dataset_path, index=False)


