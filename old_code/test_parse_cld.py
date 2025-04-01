# import unittest
# import pandas as pd
# import pickle

# from src import parse_cld

# class TestParseCLD(unittest.TestCase):

#     def setUp(self):
#         self.cld_data = parse_cld.read_cld_file('toy_example/rabbit_example.mdl')
#         # self.cld_data = read_cld_file('Dataset/SYNCH/Pine_Ridge/ME_10_5_2021_X2.mdl')

#     def test_read_cld_file(self):
#         expected_output = 'rabbit population'
#         # acutal_output= read_cld_file('Dataset/test.mdl')
#         output_line = self.cld_data.iloc[0]
        
#         output_line_list = output_line.tolist()
#         print(output_line_list)
#         self.assertEqual(output_line_list[2], expected_output)

#     def test_get_cld_df(self):
#         dict_var_final, dict_var = parse_cld.get_dict_to_vars(self.cld_data)
#         df_cld = parse_cld.get_cld_df(self.cld_data, dict_var, dict_var_final)

#         expected_columns = ['type', 'index', 'polarity', 'links', 'polarity_type', 'from_var', 'to_var', 'from', 'to']
#         # print(df_cld.iloc[0])
#         self.assertEqual(list(df_cld.columns), expected_columns)

#     def test_get_dict_to_vars(self):
#         """
#         Tests the get_dict_to_vars function.
#         :return: None
#         """
#         dict_var_final, dict_var = parse_cld.get_dict_to_vars(self.cld_data)
#         expected_dict = {1: 'birth', 2: 'deaths', 3: 'food', 4: 'fox population', 5: 'numbers of hunts', 6: 'rabbit population'}
#         self.assertEqual(dict_var_final, expected_dict)

#     def test_get_adjacency_matrix(self):
#         dict_var_final, dict_var = parse_cld.get_dict_to_vars(self.cld_data)
#         df_cld = parse_cld.get_cld_df(self.cld_data, dict_var, dict_var_final)

#         adj_matrix = parse_cld.get_adjacency_matrix(df_cld)

#         # Assert the shape of the adjacency matrix
#         self.assertEqual(adj_matrix.shape, (len(dict_var_final), len(dict_var_final)))

#     def test_get_polarity_matrix(self):
#         dict_var_final, dict_var = parse_cld.get_dict_to_vars(self.cld_data)
#         df_cld = parse_cld.get_cld_df(self.cld_data, dict_var, dict_var_final)
#         pol_matrix = parse_cld.get_polarity_matrix(df_cld)
#         # Assert the shape of the polarity matrix
#         self.assertEqual(pol_matrix.shape, (len(dict_var_final), len(dict_var_final)))

# class TestGetDictOfDicts(unittest.TestCase):

#     def setUp(self):
#         self.df = pd.DataFrame({
#             'from': [1, 2, 3, 1, 2],
#             'to': [2, 3, 1, 3, 1],
#             'weight': [1, 2, 3, 4, 5]
#         })

#     def test_get_dict_of_dicts_output_type(self):
#         result = parse_cld.get_dict_of_dicts(self.df)
#         self.assertIsInstance(result, dict)

#     def test_get_dict_of_dicts_output_structure(self):
#         result = parse_cld.get_dict_of_dicts(self.df)
#         self.assertTrue(all(isinstance(v, dict) for v in result.values()))

#     def test_get_dict_of_dicts_output_values(self):
#         expected_output = {
#             1: {2: {'weight': 1}, 3: {'weight': 4}},
#             2: {3: {'weight': 2}, 1: {'weight': 5}},
#             3: {1: {'weight': 3}}
#         }
#         result = parse_cld.get_dict_of_dicts(self.df)
#         self.assertEqual(result, expected_output)

#     def test_get_dict_of_dicts_empty_input(self):
#         df_empty = pd.DataFrame(columns=['from', 'to', 'weight'])
#         result = parse_cld.get_dict_of_dicts(df_empty)
#         self.assertEqual(result, {})

#     def test_get_dict_of_dicts_duplicate_entries(self):
#         df_duplicate = pd.DataFrame({
#             'from':     [1, 2, 3, 1, 2, 1, 2, 2],
#             'to':       [2, 3, 1, 3, 1, 2, 3, 3],
#             'weight':   [1, 2, 3, 4, 5, 6, 7, 2]
#         })
#         expected_output = {
#             1: {2: {'weight': 6}, 3: {'weight': 4}},
#             2: {3: {'weight': 7}, 1: {'weight': 5}},
#             3: {1: {'weight': 3}}
#         }
#         result = parse_cld.get_dict_of_dicts(df_duplicate)
#         self.assertEqual(result, expected_output)
#     def test_get_dict_of_dicts_nan_values(self):
#         df_nan = pd.DataFrame({
#             'from': [1, 2, 3, 1, 2, 1, 2],
#             'to': [2, 3, 1, None, 1, 2, 3],
#             'weight': [1, 2, 3, 4, 5, 6, 7]
#         })
            
#         expected_output = {
#             1: {2: {'weight': 6}},
#             2: {3: {'weight': 7}, 1: {'weight': 5}},
#             3: {1: {'weight': 3}}
#         }
#         result = parse_cld.get_dict_of_dicts(df_nan)
#         self.assertEqual(result, expected_output)

# class TestGenerateDataframe(unittest.TestCase):

#     def setUp(self):
#         self.cld_data = (
#         {
#             '1': 'rabbit population',
#             '2': 'birth',
#             '5': 'deaths',
#             '8': 'food',
#             '10': 'fox population',
#             '12': 'numbers of hunts'
#         }, 
#         {
#             '1': {
#                 '2': {'weight': 1},
#                 '5': {'weight': 1},
#                 '10': {'weight': 3}
#             },
#             '10': {
#                 '12': {'weight': 1}
#             },
#             '2': {
#                 '1': {'weight': 1}
#             }, 
#             '5': {
#                 '1': {'weight': -1}
#             }, 
#             '8': {
#                 '1': {'weight': 3}
#             }
#         }
# )

#     def test_generate_dataframe_columns(self):
#         dict_var_name, df = parse_cld.get_dataframe(self.cld_data)
#         expected_columns = ['source', 'target', 'weight', 'source_name', 'target_name']
#         print(df)
#         self.assertEqual(list(df.columns), expected_columns)

#     def test_generate_dataframe_shape(self):
#         df = parse_cld.get_dataframe(self.cld_data)
#         expected_shape = (7, 5)
#         self.assertEqual(df.shape, expected_shape)

#     def test_generate_dataframe_values(self):
#         dict_var_name, df = parse_cld.get_dataframe(self.cld_data)

#         expected_values = ['1', '2', {'weight': 1}, 'rabbit population', 'birth']
  
#         self.assertEqual(list(df.iloc[0]), expected_values)

#     def test_generate_dataframe_empty_input(self):
#         cld_data = ({}, {})
#         dict_var_name, df = parse_cld.get_dataframe(cld_data)
#         self.assertTrue(df.empty)

#     def test_generate_dataframe_dict_var(self): 
#         dict_var_name, df = parse_cld.get_dataframe(self.cld_data)
#         expected_dict = {'1': 'rabbit population', '2': 'birth', '5': 'deaths', '8': 'food', '10': 'fox population', '12': 'numbers of hunts'}
#         self.assertEqual(dict_var_name, expected_dict)


# class TestGetCombineMatrix(unittest.TestCase):
#     def setUp(self): 

#         self.matrix1 = [[ 1, 1, 1, 0, 1],
#                         [1, 0, 1, 1, 1],
#                         [ 1, 0, 0, 0, 0],
#                         [1, 1, 0, 1, 0],
#                         [1, 0, 0, 1, 0]]

#         self.matrix1 = pd.DataFrame(self.matrix1, columns=['a', 'b', 'c', 'd', 'e'])
#         self.matrix1.index = ['a', 'b', 'c', 'd', 'e']

#         self.matrix2 = [[ 0, 1, 1, 0, 1],
#                         [1, 0, 1, 1, 1],
#                         [ 1, 0, 0, 0, 0],
#                         [1, 1, 0, 1, 0],
#                         [1, 0, 0, 1, 1]]

#         self.matrix2 = pd.DataFrame(self.matrix2, columns=['z', 'd', 'c', 'b', 'a'])
#         self.matrix2.index = ['z', 'd', 'c', 'b', 'a']        
    
#     def test_get_combine_matrix(self): 
#         combined_matrix = parse_cld.get_combine_matrix(self.matrix1, self.matrix2)
#         self.assertEqual(combined_matrix.shape, (6,6) )



# # class TestGetDictOfDicts(unittest.TestCase):

# #     def setUp(self):
# #         self.df = pd.DataFrame({
# #             'from': [1, 2, 3, 1, 2],
# #             'to': [2, 3, 1, 3, 1],
# #             'weight': [1, 2, 3, 4, 5]
# #         })

# #     def test_get_dict_of_dicts_output_type(self):
# #         result = parse_cld.get_dict_of_dicts(self.df)
# #         self.assertIsInstance(result, dict)

# #     def test_get_dict_of_dicts_output_structure(self):
# #         result = parse_cld.get_dict_of_dicts(self.df)
# #         self.assertTrue(all(isinstance(v, dict) for v in result.values()))

# #     def test_get_dict_of_dicts_output_values(self):
# #         expected_output = {
# #             1: {2: {'weight': 1}, 3: {'weight': 4}},
# #             2: {3: {'weight': 2}, 1: {'weight': 5}},
# #             3: {1: {'weight': 3}}
# #         }
# #         result = parse_cld.get_dict_of_dicts(self.df)
# #         self.assertEqual(result, expected_output)

# #     def test_get_dict_of_dicts_empty_input(self):
# #         df_empty = pd.DataFrame(columns=['from', 'to', 'weight'])
# #         result = parse_cld.get_dict_of_dicts(df_empty)
# #         self.assertEqual(result, {})

# #     def test_get_dict_of_dicts_duplicate_entries(self):
# #         df_duplicate = pd.DataFrame({
# #             'from': [1, 2, 3, 1, 2, 1, 2],
# #             'to': [2, 3, 1, 3, 1, 2, 3],
# #             'weight': [1, 2, 3, 4, 5, 6, 7]
# #         })
# #         expected_output = {
# #             1: {2: {'weight': 6}, 3: {'weight': 4}},
# #             2: {3: {'weight': 7}, 1: {'weight': 5}},
# #             3: {1: {'weight': 3}}
# #         }
# #         result = parse_cld.get_dict_of_dicts(df_duplicate)
# #         self.assertEqual(result, expected_output)


# if __name__ == '__main__':

#     unittest.main()