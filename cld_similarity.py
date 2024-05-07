from sentence_transformers import SentenceTransformer, util
import torch
import pickle

# TODO : Implement CLD similarity calculation using sentence transformers

#https://medium.com/aimonks/text-similarity-building-a-text-similarity-checker-with-hugging-face-and-streamlit-db0eaf66048c
#https://medium.com/@ahmedmellit/text-similarity-implementation-using-bert-embedding-in-python-1efdb5194e65

#Load model
# model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
#
# # read json file with CLD variable names .
#
# with open('Output/Overcome RC1 4-5-2023.json', 'rb') as f:
#     loaded_dict = pickle.load(f)
#
# print(loaded_dict)
# # Define two example sentences
# sentence1 = loaded_dict
# sentence2 = "A quick brown dog jumps over the lazy fox"
#
# # Encode sentences and compute similarity score
# embeddings1 = model.encode([sentence1], convert_to_tensor=True)
# embeddings2 = model.encode([sentence2], convert_to_tensor=True)
# cosine_similarities = torch.nn.functional.cosine_similarity(embeddings1, embeddings2)
#
# # Print similarity score
# print(f"Similarity score: {cosine_similarities.item()}")