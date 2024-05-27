
import os
import pickle
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

