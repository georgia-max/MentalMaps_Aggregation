import unittest
import pandas as pd
from parse_cld import read_cld_file, get_cld_df, get_dict_to_vars, get_adjacency_matrix, get_polarity_matrix


class TestParseCLD(unittest.TestCase):
    #TODO: fix the test case

    def setUp(self):
        self.cld_data = read_cld_file('Testing/rabbit_example.mdl.mdl')
        print(self.cld_data.head())

    def test_read_cld_file(self):
        expected_output = [
            10, '1', 'egg', '276', '168', '11', '8', '8', '3', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
            '0\n'  #,
        ]

        # acutal_output= read_cld_file('Dataset/test.mdl')
        output_line = self.cld_data.iloc[0]
        output_line_list = output_line.tolist()
        self.assertEqual(output_line_list, expected_output)

    def test_get_cld_df(self):
        # df = read_cld_file('Dataset/test.mdl')
        df_cld = get_cld_df(self.cld_data)

        expected_columns = ['type', 'index', 'from', 'to', 'polarity', 'links', 'polarity_type']
        print(df_cld.iloc[0])
        self.assertEqual(list(df_cld.columns), expected_columns)
        self.assertEqual(df_cld.iloc[0, 4], 45)

    def test_get_dict_to_vars(self):
        """
        Tests the get_dict_to_vars function.
        :return: None
        """
        # df = read_cld_file('Dataset/test.mdl')
        my_dict = get_dict_to_vars(self.cld_data)
        expected_dict = {'1': 'egg', '2': 'water', '3': 'food', '7': 'chicken'}
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



if __name__ == '__main__':
    unittest.main()
