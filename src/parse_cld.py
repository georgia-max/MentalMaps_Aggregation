import pandas as pd
import regex as re
import numpy as np
import networkx as nx
import itertools as it

def read_cld_file(file_path: str) -> pd.DataFrame:
    """
    Reads a Vensim .txt file and extracts the content on variable names and links.
    :param: file_path
    :return: pandas.DataFrame
    """

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # # Compile regex to match line with sketch info
    start_pattern = re.compile(r".*\*View 1.*")
    view2_pattern = re.compile(r".*\*View 2.*")
    end_pattern = view2_pattern if any(view2_pattern.match(line) for line in lines) else re.compile(r'/{3}-+\\{3}')
    extracted = []
    extract = False

    for line in lines:
        if start_pattern.match(line):
            # Start new extraction when "View 1" is found
            extract = True
            extracted = []  # Reset extracted lines for new block
            continue  # Skip to next iteration to avoid appending the start line itself

        if extract:
            if end_pattern.match(line):
                # Stop extracting if end pattern found and break if you only need the first block
                extract = False
                break
            extracted.append(line)  # Append current line to extracted

    # check the end_pattern what is the pattern.
    if end_pattern == view2_pattern:
        extracted = extracted[1:-2]  # Remove the first and last two lines
    else:
        extracted = extracted[1:]
    df = pd.DataFrame(extracted)
    df = df[0].str.split(',', expand=True)
    # change column 0 dytpe to int
    df[0] = df[0].astype(int)

    # print(df)

    return df


def get_cld_df(df):
    """
    Extracts organize and transform the CLD data from the input DataFrame.
    :param df:
    :return: df_new
    """

    # Grab dependencies
    df_new = df.loc[df[0]== 1,  ]
    df_new = df_new[[0, 1, 2, 3, 6]]
    # Give dataframe new column names
    df_new = df_new.rename(columns={0: 'type', 1: 'index',2: 'from', 3: 'to', 6: 'polarity'})
    df_new['polarity'] = df_new['polarity'].astype(int)
    df_new['links'] = 1
    df_new['polarity_type'] = np.where(df_new['polarity'] == 43, 1,
                                         np.where(df_new['polarity'] == 45, -1, 3))
    return df_new

def get_dict_to_vars(df):
    """
    Creates a dictionary mapping variable names to their index in the DataFrame.
    :param df_vars: DataFrame containing variable information
    :return: dictionary mapping variable names to their index
    """
    # in the txt file, 10 means it is a variable.
    if df[0].eq(10).any():
        return df.loc[df[0] == 10].set_index(1)[2].to_dict()
    else:
        return {}

def get_adjacency_matrix(df_new):
    """
    Generates an adjacency matrix of links from the input DataFrame containing CLD data.
    :param df_new:
    :param dict_var:
    :return: ad_matrix, row is from and column is to.
    """

    # Make a adjacency matrix from df_links column from, to and links
    link_matrix = df_new.pivot(index='from', columns='to', values='links').fillna(0).astype(int)

    missing_cols = set(link_matrix.index) - set(link_matrix.columns)
    missing_rows = set(link_matrix.columns) - set(link_matrix.index)

    if len(missing_cols) > 0:
        for col in missing_cols:
            link_matrix[col] = 0
    if len(missing_rows) > 0:
        for row in missing_rows:
            link_matrix.loc[row] = 0

    # Sort rows and cols by the index of dict_var
    link_matrix = link_matrix.sort_index(axis=1)
    link_matrix = link_matrix.sort_index(axis=0)

    return link_matrix


def get_polarity_matrix(df_new):
    """
    Generates a polarity matrix from the input DataFrame containing CLD data.
    :param df_new:
    :param dict_var:
    :return: polarity_matrix, +1 is positive, -1 is negative
    """
    polarity_matrix = df_new.pivot(index='from', columns='to', values='polarity_type').fillna(0).astype(int)

    missing_cols = set(polarity_matrix.index) - set(polarity_matrix.columns)
    missing_rows = set(polarity_matrix.columns) - set(polarity_matrix.index)

    if len(missing_cols) > 0:
        for col in missing_cols:
            polarity_matrix[col] = 0
    if len(missing_rows) > 0:
        for row in missing_rows:
            polarity_matrix.loc[row] = 0

    # Sort rows and cols by the index of dict_var
    polarity_matrix = polarity_matrix.sort_index(axis=1)
    polarity_matrix = polarity_matrix.sort_index(axis=0)

    return polarity_matrix


def get_dict_of_dicts(df_subset):
    """
    Creates a dictionary of dictionaries from the input DataFrame, where the outer dictionary keys are the 'from'
    values and the inner dictionary keys are the 'to' values.
    This function stores the link information in a more efficient data structure for further processing.

    The dataset should only have three columns, from, to and weight
    :param df:
    :return: dictionary of dictionaries

    """
    d = df_subset.groupby('from').apply(lambda x: x.set_index('to').to_dict(orient='index'),
                                        include_groups=False).to_dict()
    return d

def get_cld(df):
    """
    Extracts, organizes, and transforms the CLD data from the input DataFrame to a dict-of-dicts data structure.
    :param df:
    :return:
    """
    df_cld = get_cld_df(df)

    # my_dict = get_dict_to_vars(df)

    df_subset = df_cld[['from', 'to', 'polarity_type']]

    # Change the column name polarity type of weight
    df_subset = df_subset.rename(columns={'polarity_type': 'weight'})
    d = get_dict_of_dicts(df_subset)
    return d



def get_dataframe(cld_dict):
    """
    Generates a DataFrame from the CLD data in the format (source, target, weight, source_name, target_name).
    Args: 
        cld_data (dictionary): A dictionary that represents the CLD matrix 
    Returns:
        pd.DataFrame: A DataFrame containing the CLD data in the specified format.
    """
    # Unpack the cld_data
    dict_var_name, d = cld_dict
    # print(dict_vars_name)
    # print(d)
    # get the second dictionary, where it stored the links and weights


    # Create a list of tuples (source, target, weight)
    edges = []
    for source, targets in d.items():
        for target, weight_dict in targets.items():
            weight = weight_dict['weight']
            
            edges.append((source, target, weight))

    # Create a DataFrame from the list of edges
    df = pd.DataFrame(edges, columns=['from', 'to', 'polarity_type'])
    df['links'] = 1
    # get column weight as int 
    # df['weight'] = df['weight'].astype(int)
    # print(df)
    # print(df.info())

    # # Add variable names
    # df['source_name'] = df['source'].map(dict_vars_name)
    # df['target_name'] = df['target'].map(dict_vars_name)

    return dict_var_name, df


def get_duplicate_theme_no(df):
    """
    Get the list of duplicate theme from the input DataFrame.
    :param df:
    :return:
    """
    # get all the duplicate theme no 
    df_theme_no = df['theme'].value_counts()
    duplicate_theme_no = df_theme_no[df_theme_no > 1].index.tolist()
    return duplicate_theme_no


# functions for aggregateCLD.ipynb 

def get_theme_cld(cld_dict, df_theme ): 
    """
    Get the single theme CLD from the input DataFrame.
    :param df:
    :return:
    """
    dict_vars, df = get_dataframe(cld_dict)

    vars_cld = pd.DataFrame.from_dict(dict_vars, orient='index').reset_index()#.columns(['Vensim Var No.', 'Var Name'])
    # rename columns 
    vars_cld.columns = ['vensim_var_no','var_name']
    # turn all the variable names to lowercap 
    vars_cld['var_name'] = vars_cld['var_name'].str.lower()
    # delete the "" sign 
    vars_cld['var_name'] = vars_cld['var_name'].str.replace('"', '')

    df_aggregate_merge = pd.merge(df_theme, vars_cld, left_on='variable', right_on='var_name', how='right')
    # print(df_aggregate_merge)
    

    df_aggregate_merge['vensim_var_no'] = df_aggregate_merge['vensim_var_no'].astype(int)
    list_of_duplicate_themes = get_duplicate_theme_no(df_aggregate_merge)

    theme_no_dict = {}
    for i, val in enumerate(list_of_duplicate_themes):
        theme_no_dict[val] = max(df_aggregate_merge['vensim_var_no']) + i + 1

    df_aggregate_merge['theme_no'] = df_aggregate_merge['theme'].map(theme_no_dict)


    for i, row in df_aggregate_merge.iterrows():
        if pd.isna(row['theme_no']):
            df_aggregate_merge.at[i, 'theme_no'] = row['vensim_var_no']


    df_aggregate_merge['theme_no'] = df_aggregate_merge['theme_no'].astype(int)

    theme_dict = {}
    for index, row in df_aggregate_merge.iterrows():
        if pd.isna(row['theme']):
            theme_dict[row['theme_no']] = row['var_name']
        else:
            theme_dict[row['theme_no']] = row['theme']

    theme_dict = {int(k): v for k, v in theme_dict.items()}



    theme_org_new_dict = dict(zip(df_aggregate_merge['vensim_var_no'], df_aggregate_merge['theme_no']))
    theme_org_new_dict = {int(k): v for k, v in theme_org_new_dict.items()}


    new_df = df.copy()
    # change all data in df to int 
    new_df = new_df.astype(int)
    #swap the from column in df to new number based on theme_no_number_dict
    new_df['from'] = new_df['from'].map(theme_org_new_dict)
    new_df['to'] = new_df['to'].map(theme_org_new_dict)

    merge_df = new_df.groupby(['from', 'to']).sum().reset_index()
    
    return merge_df, theme_dict


def get_aggregate_adjacency_mx(merge_df, theme_dict): 

    adj_mx = get_adjacency_matrix(merge_df)
    # change theme dict keys to int 
    theme_dict = {int(k): v for k, v in theme_dict.items()}
    adj_mx.columns = adj_mx.columns.map(theme_dict)

    adj_mx.index = adj_mx.index.map(theme_dict)

    return adj_mx

def get_aggregate_polarity_mx(merge_df, theme_dict): 

    pol_mx = get_polarity_matrix(merge_df)
    # change theme dict keys to int 
    theme_dict = {int(k): v for k, v in theme_dict.items()}
    pol_mx.columns = pol_mx.columns.map(theme_dict)

    pol_mx.index = pol_mx.index.map(theme_dict)

    return pol_mx


def get_combine_matrix(matrix1, matrix2): 


    def combine_non_nan(s1, s2):

        if pd.isna(s1).all():
            return s2
        elif pd.isna(s2).all():
            return s1
        else:
            return s1 + s2

    if matrix2.empty :
        return matrix1

    else: 
        combined_matrix = matrix1.combine(matrix2, combine_non_nan, overwrite = False)
        combined_matrix = combined_matrix.fillna(matrix1)
        combined_matrix = combined_matrix.fillna(matrix2)

        return combined_matrix 
