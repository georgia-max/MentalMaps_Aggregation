import unittest
import pandas as pd
import pickle

from parse_cld import read_cld_file, get_cld_df, get_dict_to_vars
from parse_cld import get_adjacency_matrix, get_polarity_matrix, generate_dataframe


class TestParseCLD(unittest.TestCase):
    #TODO: fix the test case

    def setUp(self):
        self.cld_data = read_cld_file('Testing/rabbit_example.mdl')
        # self.cld_data = read_cld_file('Dataset/SYNCH/Pine_Ridge/ME_10_5_2021_X2.mdl')

    def test_read_cld_file(self):
        expected_output = 'rabbit population'
        # acutal_output= read_cld_file('Dataset/test.mdl')
        output_line = self.cld_data.iloc[0]
        
        output_line_list = output_line.tolist()
        print(output_line_list)
        self.assertEqual(output_line_list[2], expected_output)

    def test_get_cld_df(self):
        # df = read_cld_file('Dataset/test.mdl')
        df_cld = get_cld_df(self.cld_data)

        expected_columns = ['type', 'index', 'from', 'to', 'polarity', 'links', 'polarity_type']
        # print(df_cld.iloc[0])
        self.assertEqual(list(df_cld.columns), expected_columns)
        self.assertEqual(df_cld.iloc[0, 4], 43)

    def test_get_dict_to_vars(self):
        """
        Tests the get_dict_to_vars function.
        :return: None
        """
        # df = read_cld_file('Dataset/test.mdl')
        my_dict = get_dict_to_vars(self.cld_data)
        expected_dict = {'1': 'rabbit population', '2': 'birth', '5': 'd[65 chars]nts'}
        self.assertEqual(my_dict, expected_dict)

    def test_get_adjacency_matrix(self):
        df_cld = get_cld_df(self.cld_data)
        my_dict = get_dict_to_vars(self.cld_data)
        adj_matrix = get_adjacency_matrix(df_cld)

        # Assert the shape of the adjacency matrix
        self.assertEqual(adj_matrix.shape, (len(my_dict), len(my_dict)))

    def test_get_polarity_matrix(self):
        df_cld = get_cld_df(self.cld_data)
        my_dict = get_dict_to_vars(self.cld_data)
        pol_matrix = get_polarity_matrix(df_cld)
        # Assert the shape of the polarity matrix
        self.assertEqual(pol_matrix.shape, (len(my_dict), len(my_dict)))

    def test_df_to_adjacency_list(self):
        none



# src/test_parse_cld.py
class TestGenerateDataframe(unittest.TestCase):

    def setUp(self):
        self.cld_data = (
        {
            '1': 'rabbit population',
            '2': 'birth',
            '5': 'deaths',
            '8': 'food',
            '10': 'fox population',
            '12': 'numbers of hunts'
        }, 
        {
            '1': {
                '2': {'weight': 1},
                '5': {'weight': 1},
                '10': {'weight': 3}
            },
            '10': {
                '12': {'weight': 1}
            },
            '2': {
                '1': {'weight': 1}
            }, 
            '5': {
                '1': {'weight': -1}
            }, 
            '8': {
                '1': {'weight': 3}
            }
        }
)

    def test_generate_dataframe_columns(self):
        df = generate_dataframe(self.cld_data)
        expected_columns = ['source', 'target', 'weight', 'source_name', 'target_name']
        print(df)
        self.assertEqual(list(df.columns), expected_columns)

    def test_generate_dataframe_shape(self):
        df = generate_dataframe(self.cld_data)
        expected_shape = (7, 5)
        self.assertEqual(df.shape, expected_shape)

    def test_generate_dataframe_values(self):
        df = generate_dataframe(self.cld_data)

        expected_values = ['1', '2', {'weight': 1}, 'rabbit population', 'birth']
  
        self.assertEqual(list(df.iloc[0]), expected_values)

    def test_generate_dataframe_empty_input(self):
        cld_data = ({}, {})
        df = generate_dataframe(cld_data)
        self.assertTrue(df.empty)


if __name__ == '__main__':

    unittest.main()
