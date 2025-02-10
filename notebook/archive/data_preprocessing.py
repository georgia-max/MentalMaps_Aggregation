import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

training_dataset_path = "C:/Users/GL665/Code/Phrame-MentalMaps/data/processed/SYNCH/training_set/training_set_0715_var_A0729.csv"

# %%
# When training and test set is in one dataset
my_dataset = pd.read_csv(training_dataset_path)
my_dataset = my_dataset[['sentence1', 'sentence2', 'label', 'idx']]
print("Read dataset.....")
print("Originial dataset head")
print(my_dataset.head())
# delete rows with missing values
my_dataset = my_dataset.dropna()
# print(my_dataset.isna().sum())

# %%
# delete rows if the row does not equal to "1" or "0"
my_dataset = my_dataset[my_dataset['label'].isin(['0', '1'])]
print("Dataset shape after deleting rows that are not 0 or 1:", my_dataset.shape)
# Assuming my_dataset is your DataFrame
label_counts = my_dataset['label'].value_counts()

plt.figure(figsize=(8, 6))
ax = label_counts.plot(kind='bar')
label_counts.plot(kind='bar')
plt.title('Distribution of Labels in Dataset')
plt.xlabel('Label')
plt.ylabel('Count')
plt.xticks(rotation=0)

# Add numbers on top of each bar
for i, v in enumerate(label_counts):
    ax.text(i, v, str(v), ha='center', va='bottom')
plt.tight_layout()
plt.show()

print("Label distribution:")
print(label_counts)
