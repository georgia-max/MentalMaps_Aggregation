# Last update: 2024-07-30
# read the excel file of the variables that are labeled by arielle and create
# two new columns that are the definitions of the variables by using the dictionary from the 
# raw data dictionary sheet. 

# %%
import pandas as pd 
import numpy as np 
# %%
input_data_dict_path = "/Users/gl665/PycharmProjects/Phrame_MentalMaps/data/raw/SYNCH/RC/excel_sheets/Rapid City SYNCH Models data dictionary0715.xlsx"

data_labeled_path = "/Users/gl665/PycharmProjects/Phrame_MentalMaps/data/processed/SYNCH/training_set/training_set_0715_var_A0729.csv"
# Create an empty dictionary to store the data frames
excel_sheets = {}

cld_dataframe = {}

# Read all sheets into the dictionary
for sheet_name in pd.ExcelFile(input_data_dict_path).sheet_names:
    excel_sheets[sheet_name] = pd.read_excel(
        input_data_dict_path, sheet_name=sheet_name)
    if "changed variable names" in excel_sheets[sheet_name].columns:
        print("Geting Sheet: ", sheet_name)

        cld_dataframe[sheet_name] = excel_sheets[sheet_name][[
            'variable', 'changed variable names', 'definition']]
        cld_dataframe[sheet_name] = cld_dataframe[sheet_name].dropna()
    else:
        pass

#%%
final_vars_def_dict = {}
for sheet_name, data in cld_dataframe.items():
    vars_def_dict = dict(
        zip(data['changed variable names'], data['definition']))
    
    # append a dictionary to the final dictionary
    final_vars_def_dict.update(vars_def_dict)    
# %%

labeled_df = pd.read_csv(data_labeled_path)
labeled_df.head()

# %%

labeled_df['definition1'] = labeled_df['sentence1'].map(final_vars_def_dict)
labeled_df['definition2'] = labeled_df['sentence2'].map(final_vars_def_dict)
# reorider the columns  where definition 1 and definition 2 are the 2nd and 4th column 
labeled_df = labeled_df[['sentence1', 'definition1',
                         'sentence2', 'definition2', 'label','idx','notes']]
print("export the labeled data frame to a csv file")

# export the labeled data frame to a csv file
labeled_df.to_csv("/Users/gl665/PycharmProjects/Phrame_MentalMaps/data/processed/SYNCH/training_set/training_set_0715_var_def_A0729.csv", index=False)


# %%
