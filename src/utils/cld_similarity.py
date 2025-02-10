#TODO: Need to clean this file. Do NOT RUN THIS!
import sentencepiece
from sentence_transformers import SentenceTransformer, util
import torch
import pickle
import seaborn as sns
import nltk
from absl import logging
from kmeans_pytorch import kmeans

import tensorflow as tf

# TODO : Implement CLD similarity calculation using sentence transformers
import tensorflow_hub as hub
# module = hub.Module("https://tfhub.dev/google/universal-sentence-encoder-lite/2")

import tensorflow_hub as hub

from absl import logging
import tensorflow as tf
import tensorflow_hub as hub

module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)
print("module %s loaded" % module_url)


def embed(input):
    return model(input)


# embed = hub.load("https://www.kaggle.com/models/google/universal-sentence-encoder/TensorFlow2/universal-sentence-encoder/2")

# %%
def plot_similarity(labels, features, rotation):
    corr = np.inner(features, features)
    sns.set(font_scale=1.2)
    g = sns.heatmap(
        corr,
        xticklabels=labels,
        yticklabels=labels,
        vmin=0,
        vmax=1,
        cmap="YlOrRd")
    g.set_xticklabels(labels, rotation=rotation)
    g.set_title("Semantic Textual Similarity")


def run_and_plot(messages_):
    message_embeddings_ = embed(messages_)
    plot_similarity(messages_, message_embeddings_, 90)


run_and_plot(string_list)
#
# model = hub.KerasLayer("https://tfhub.dev/google/nnlm-en-dim128/2")
# embeddings = model(["The rain in Spain.", "falls",
#                     "mainly", "In the plain!"])
#
# print(embeddings.shape)  # (4,128)
# embed = hub.load("https://www.kaggle.com/models/google/universal-sentence-encoder/TensorFlow2/universal-sentence-encoder/2")
# embeddings = embed([
#     "The quick brown fox jumps over the lazy dog.",
#     "I am a sentence for which I would like to get its embedding"])
#
# print(embeddings)
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