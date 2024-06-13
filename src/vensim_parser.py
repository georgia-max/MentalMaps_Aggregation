import re
import pandas as pd
import numpy as np
import networkx as nx
from src.cld_aggregator import CLDGraph

class CLDParser:

    def __init__(self, df):
        self.df = df


    def get_cld_dict(self):
        """
        Extracts, organizes, and transforms the CLD data from the input DataFrame to a dict-of-dicts data structure.
        :param df:
        :return: dictionary 

        
        """
        # get variables
        df_vars = self.df.loc[self.df[0] == 10]
        dict_var = df_vars.set_index(1)[2].to_dict()

        dict_var = {k: v.lower() for k, v in dict_var.items()}
        dict_var = {int(k): v.replace('"', '') for k, v in dict_var.items()}

        unique_var_values = sorted(set(dict_var.values()))
        dict_var_final = {int(k): v for k, v in enumerate(unique_var_values, 1)}

        # get cld data 
        df_cld = self.get_cld_df(dict_var, dict_var_final)


        d = self.get_dict_of_dicts(df_cld)
        cld_data = [dict_var_final, d]

        return cld_data
    
    def get_dict_of_dicts(self, df_subset):

        """
        Creates a dictionary of dictionaries from the input DataFrame, where the outer dictionary keys are the 'from'
        values and the inner dictionary keys are the 'to' values.
        :param df_subset:
        :return: dictionary of dictionaries
        """
        nested_dict = {}
        df_subset = df_subset.drop_duplicates()
        df_subset = df_subset.dropna()

        for index, row in df_subset.iterrows():
            from_value = row['from']
            to_value = row['to']
            weight_value = row['weight']

            if from_value not in nested_dict:
                nested_dict[from_value] = {}

            nested_dict[from_value][to_value] = {'weight': weight_value}
        
        return nested_dict
    
    def get_cld_df(self, dict_var, dict_var_final):
        """
        Extracts, organizes, and transforms the CLD data from the input DataFrame.
        Get the polarity type, when = 32, the polarity is positive(+),
        when = 33, the polarity is negative (-1), when = 34, the polarity is neutral(3).
        :param df:
        :return: df_new
        """
        df_new = self.df.loc[self.df[0] == 1]
        df_new = df_new[[0, 1, 2, 3, 6]]
        df_new = df_new.rename(columns={0: 'type', 1: 'index', 2: 'from_org', 3: 'to_org', 6: 'polarity'})
        df_new['polarity'] = df_new['polarity'].astype(int)
        df_new['from_org'] = df_new['from_org'].astype(int)
        df_new['to_org'] = df_new['to_org'].astype(int)
        df_new['links'] = 1
        df_new['polarity_type'] = np.where(df_new['polarity'] == 43, 1,
                                           np.where(df_new['polarity'] == 45, -1, 3))

        df_new['from_var'] = df_new['from_org'].map(dict_var)
        df_new['to_var'] = df_new['to_org'].map(dict_var)

        df_new['from'] = df_new['from_var'].map({v: k for k, v in dict_var_final.items()})
        df_new['to'] = df_new['to_var'].map({v: k for k, v in dict_var_final.items()})
        df_new = df_new.drop(columns=['from_org', 'to_org'])


        df_t = df_new[['from', 'to', 'polarity_type']]
        df_t = df_t.rename(columns={'polarity_type': 'weight'})

        return df_t

    def get_adjacency_matrix(self, df_new):
        """
        Generates an adjacency matrix of links from the input DataFrame containing CLD data.
        :param df_new:
        :return: ad_matrix, row is from and column is to.
        """
        link_matrix = df_new.pivot(index='from', columns='to', values='links').fillna(0).astype(int)

        missing_cols = set(link_matrix.index) - set(link_matrix.columns)
        missing_rows = set(link_matrix.columns) - set(link_matrix.index)

        if len(missing_cols) > 0:
            for col in missing_cols:
                link_matrix[col] = 0
        if len(missing_rows) > 0:
            for row in missing_rows:
                link_matrix.loc[row] = 0

        link_matrix = link_matrix.sort_index(axis=1)
        link_matrix = link_matrix.sort_index(axis=0)

        return link_matrix

    def get_polarity_matrix(self, df_new):
        """
        Generates a polarity matrix from the input DataFrame containing CLD data.
        :param df_new:
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

        polarity_matrix = polarity_matrix.sort_index(axis=1)
        polarity_matrix = polarity_matrix.sort_index(axis=0)

        return polarity_matrix





    def get_cld_dataframe(self, cld_dict):
        """
        Generates a DataFrame from the CLD data in the format (source, target, weight, source_name, target_name).
        Args:
            cld_data (dictionary): A dictionary that represents the CLD matrix
        Returns:
            pd.DataFrame: A DataFrame containing the CLD data in the specified format.
        """
        dict_var_name, d = cld_dict

        edges = []
        for source, targets in d.items():
            for target, weight_dict in targets.items():
                weight = weight_dict['weight']
                edges.append((source, target, weight))

        df = pd.DataFrame(edges, columns=['from', 'to', 'polarity_type'])
        df['links'] = 1

        return dict_var_name, df

    def get_duplicate_theme_no(self, df):
        """
        Get the list of duplicate theme from the input DataFrame.
        :param df:
        :return:
        """
        df_theme_no = df['theme'].value_counts()
        duplicate_theme_no = df_theme_no[df_theme_no > 1].index.tolist()
        return duplicate_theme_no
    
    def get_theme_cld(self, cld_dict, df_theme ): 
        """
        Get the single theme CLD from the input DataFrame.
        
        Args:
            cld_dict (dict): A dictionary containing the CLD data.
            df_theme (pandas.DataFrame): A DataFrame containing the theme information.
        
        Returns:
            tuple: A tuple containing the following:
                - merge_df (pandas.DataFrame): A DataFrame containing the merged CLD data.
                - theme_dict (dict): A dictionary mapping theme numbers to theme names.

        """
        dict_vars, df = self.get_cld_dataframe(cld_dict)

        vars_cld = pd.DataFrame.from_dict(dict_vars, orient='index').reset_index()#.columns(['Vensim Var No.', 'Var Name'])
        # rename columns 
        vars_cld.columns = ['vensim_var_no','var_name']
        # turn all the variable names to lowercap 
        vars_cld['var_name'] = vars_cld['var_name'].str.lower()
        # delete the "" sign 
        vars_cld['var_name'] = vars_cld['var_name'].str.replace('"', '')

        df_aggregate_merge = pd.merge(df_theme, vars_cld, left_on='variable', right_on='var_name', how='right')
        

        df_aggregate_merge['vensim_var_no'] = df_aggregate_merge['vensim_var_no'].astype(int)
        list_of_duplicate_themes = self.get_duplicate_theme_no(df_aggregate_merge)

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


        # get dictionary of the origininla vensim var number and the new theme number
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
    

    # def get_aggregate_adjacency_mx(merge_df, theme_dict): 

    #     adj_mx = get_adjacency_matrix(merge_df)
    #     # change theme dict keys to int 
    #     theme_dict = {int(k): v for k, v in theme_dict.items()}
    #     adj_mx.columns = adj_mx.columns.map(theme_dict)

    #     adj_mx.index = adj_mx.index.map(theme_dict)

    #     return adj_mx

    # def get_aggregate_polarity_mx(merge_df, theme_dict): 

    #     pol_mx = get_polarity_matrix(merge_df)
    #     # change theme dict keys to int 
    #     theme_dict = {int(k): v for k, v in theme_dict.items()}
    #     pol_mx.columns = pol_mx.columns.map(theme_dict)

    #     pol_mx.index = pol_mx.index.map(theme_dict)

    #     return pol_mx


