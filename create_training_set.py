import pandas as pd
from itertools import combinations


# Step 1: Define the file paths
input_csv = 'fine_tuning_dataset_repository/dataset/manual_grouping_0625.csv'  
output_dataset_path = 'fine_tuning_dataset_repository/dataset/XXX.csv'  

# Step 2: Read the CSV file into a DataFrame
df = pd.read_csv(input_csv)

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

