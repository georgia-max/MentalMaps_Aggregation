import regex as re
import pandas as pd 
import os
import pickle


def read_cld_file(cld_path) -> pd.DataFrame:
    """
    Reads a Vensim .txt file and extracts the content on variable names and links.
    :param: file_path
    :return: pandas.DataFrame
    """
    with open(cld_path, 'r') as f:
        lines = f.readlines()

    start_pattern = re.compile(r".*\*View 1.*")
    view2_pattern = re.compile(r".*\*View 2.*")
    end_pattern = view2_pattern if any(view2_pattern.match(line) for line in lines) else re.compile(r'/{3}-+\\{3}')
    extracted = []
    extract = False

    

    for line in lines:

        
        if start_pattern.match(line):
            extract = True
            extracted = []
            continue

        if extract:
            if end_pattern.match(line):
                extract = False
                break

            extracted.append(line)


    if end_pattern == view2_pattern:
        extracted = extracted[1:-2]
    else:
        extracted = extracted[1:]

    df = pd.DataFrame(extracted)
    df = df[0].str.split(',', expand=True)


    df = df[df[0].str.isdigit()]

    df[0] = df[0].astype(int)

    return df 

def read_json(folder_path, data_dict):

    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'rb') as f:
                print("load:",filename)
                data = pickle.load(f)
                # store the loaded data in a dictionary for further processing, the key is the file name, the dictionary is data
                data_dict[filename] = data

    return data_dict


# def get_dict_of_cld(data_dict, df_aggregate_names, dict_file_rename):
#     """
#     Generates a dictionary of NetworkX graphs representing the Causal Loop Diagrams (CLDs) for a given data dictionary.
    
#     Args:
#         data_dict (dict): A dictionary containing the data for each CLD.
#         df_aggregate_names (pandas.DataFrame): A DataFrame containing the theme names for each CLD.
#         dict_file_rename (dict): A dictionary mapping the original CLD names to the desired renamed CLD names.
    
#     Returns:
#         dict: A dictionary where the keys are the renamed CLD names and the values are the corresponding NetworkX graphs.
#     """


#     dict_cld = {}

#     for k, v in data_dict.items():

#         merge_df,  theme_dict = parse_cld.get_theme_cld(v, df_aggregate_names)

#         unique_theme_names = set(df_aggregate_names['theme'])

    
#         df_subset = merge_df[['from', 'to', 'polarity_type']]
#         df_subset = df_subset.rename(columns={'polarity_type': 'weight'})


#         d = parse_cld.get_dict_of_dicts(df_subset)
#         # cld_name = k
#         cld_name = dict_file_rename.get(k)

#         g = get_nx_graph(d, theme_dict, cld_name, unique_theme_names)
#         dict_cld[cld_name] = g

#         return dict_cld
