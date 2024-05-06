from parse_cld import read_cld_file, get_cld_df, get_dict_to_vars, get_adjacency_matrix, get_polarity_matrix

df = read_cld_file('Dataset/clean models/aggregate reentry DSS model.mdl')

# df = read_cld_file('Testing/rabbit_example.mdl')
df_cld = get_cld_df(df)
# df_cld.to_csv('Output/df_cld.csv')

my_dict = get_dict_to_vars(df)
print(my_dict)
print(len(my_dict))

adj_matrix = get_adjacency_matrix(df_cld)
print(adj_matrix)
print(adj_matrix.shape)
pol_matrix = get_polarity_matrix(df_cld)

print(pol_matrix)


# adj_matrix.to_csv('Output/adjacency_matrix.csv')
# pol_matrix.to_csv('Output/polarity_matrix.csv')
