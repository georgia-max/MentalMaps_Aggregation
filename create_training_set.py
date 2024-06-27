import pandas as pd
import pickle
from itertools import combinations
from datasets import Dataset 


# Step 1: Define the file paths
input_csv = 'results/SYNCH/training_set/SYNCH_grouping_by_definition_0627.xlsx'  # Replace with your input CSV file path
output_dataset_path = 'fine_tuning_dataset_repository/dataset/preprocess_SYNCH_grouping_by_definition_0627.csv'  # Replace with your desired output file path

# Step 2: Read the CSV file into a DataFrame
df = pd.read_excel(input_csv, sheet_name= "manual grouping_0625")

# Step 3: Convert the DataFrame to a dictionary

# Each pair in each row is consider a training sample. create a new dataframe with the pair that include two examples. 
total_pairs ={}

for i, row in df.iterrows():
    my_row = row.dropna().tolist()
    if len(my_row) >= 2:
        pairs = list(combinations(my_row, 2))
        total_pairs.update(pairs)
    else: 
        pass

print(total_pairs)
# turn the total pairs dictionary to columns in dataframe 
df_training = pd.DataFrame(total_pairs.items(), columns=['sentence1', 'sentence2'])
df_training['label'] = 1 
df_training['idx'] = df_training.index

# Step 4: export the dataframe as a csv file 
df_training.to_csv(output_dataset_path, index=False)


# ds.save_to_disk("")
# ds = Dataset.from_pandas(df_training)

# print(ds)
# print(ds[0])

