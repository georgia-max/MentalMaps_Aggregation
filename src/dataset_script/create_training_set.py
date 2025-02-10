import pandas as pd
from itertools import combinations


# Step 1: Define the file paths
input_csv = 'data/interim/RC/manual_label_data/manual_grouping_var_0710.csv'  
output_dataset_path = 'fine_tuning_dataset_repository/dataset/training_set_var_0710.csv'  

# Step 2: Read the CSV file into a DataFrame
df = pd.read_csv(input_csv)

df = df.dropna(axis=0, how='all')

# print(df)

total_pairs ={}

df_copy = df.copy()
if 'label' in df_copy.columns:
    df_copy = df_copy.drop(columns=['label'])
    
else:
    pass
for i, row in df_copy.iterrows():
    my_row = row.dropna().tolist()
    if len(my_row) >= 2:
        pairs = list(combinations(my_row, 2))
        print(pairs)
        dict_pairs = {pairs: }
        total_pairs.update(pairs)
    else: 
        pass

# print(total_pairs)
# turn the total pairs dictionary to columns in dataframe 
df_training = pd.DataFrame(total_pairs.items(), columns=['sentence1', 'sentence2'])
# df_training['label'] = 1 
df_training['idx'] = df_training.index

# print(df_training.head())
# Step 4: export the dataframe as a csv file 
# df_training.to_csv(output_dataset_path, index=False)


