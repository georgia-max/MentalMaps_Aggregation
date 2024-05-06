import pandas as pd
import regex as re
import numpy as np

def read_cld_file(file_path):
    """
    Reads a Vensim .txt file and extracts the content on variable names and links.
    :param: file_path
    :return: pandas.DataFrame
    """

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Compile regex to match line with sketch info
    start_pattern = re.compile(r"\\\---///*")
    end_pattern = re.compile(r'\/{3}-+\\{3}')

    extracted = []
    extract = False

    for line in lines:
        if end_pattern.search(line):
            # Stop extracting if end pattern found
            extract = False

        elif start_pattern.search(line):
            # Start new extraction
            extracted = []
            extract = True

        elif extract:
            # Append to extracted lines
            extracted.append(line)

    extracted = extracted[3:]
    df = pd.DataFrame(extracted)
    df = df[0].str.split(',', expand=True)
    # change column 0 dytpe to int
    df[0] = df[0].astype(int)

    return df


def get_cld_df(df):
    """
    Extracts organize and transform the CLD data from the input DataFrame.
    :param df:
    :return: df_new
    """

    # Grab dependencies
    df_new = df.loc[df[0]==1,  ]
    df_new = df_new[[0,1, 2,3,6]]
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

