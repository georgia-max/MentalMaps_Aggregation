import pandas as pd
import pickle
from itertools import combinations
import json
import os 

# Step 1: Define the file paths
# folder_path ='results/SYNCH/JSON_file/RC/results sheets/data_dictionary/'  # Replace with your input CSV file path
# output_dataset_path = 'fine_tuning_dataset_repository/test_set/test_set_four_cld.csv'  # Replace with your desired output file path

# Step 2: Read the json file 
dict_def = {}
for file in os.listdir(folder_path):
    if file.endswith(".json"):
        with open(folder_path + "/" + file, 'r') as f:
            data = json.load(f)
            dict_def[file] = data
            
list_of_vars = []

for k, v in dict_def.items():
    cld_new_vars_name = []
    cld_var_names = list(v.keys())

    list_of_vars.extend(cld_var_names)
    
# Create pairs 
# Create all possible pairs of variables
pairs = combinations(list_of_vars, 2)
# print(pairs)

df = pd.DataFrame(pairs, columns=['sentence1', 'sentence2'])
df['label'] = 0
df['idx'] = df.index

# Delete all the rows if contains Nan
df = df.dropna()

print(df.isna().sum())

# Step 4: export the dataframe as a csv file 
# df.to_csv(output_dataset_path, index=False)


# ds.save_to_disk("")
# ds = Dataset.from_pandas(df_training)

# print(ds)
# print(ds[0])

