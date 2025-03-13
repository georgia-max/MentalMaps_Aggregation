"""
get semantic matching from NLP model using untrained sentence transformers. 

Do this to reduce the number of pairing nodes that needs to be inferenced on the fined-tuned model. 

Input:
    - df = all_definition_pairs.csv 
    
output: 
    - nlp_pairs = nlp_not_matched_pairs.csv
    - all_definition_pairs_llm.csv = the rest of the dataset that needs to be inferenced on the fined-tuned model.. 
"""

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

INPUT_FILE = "/Users/gl665/Documents/Phrame-MentalMaps-1/data/read_for_label/all_definition_pairs.csv"
OUTPUT_ALL_FILE = "/Users/gl665/Documents/Phrame-MentalMaps-1/data/read_for_label/nlp_not_matched_pairs.csv"
OUTPUT_LLM_PAIRS_FILE = "/Users/gl665/Documents/Phrame-MentalMaps-1/data/read_for_label/all_definition_pairs_llm.csv"


def main():
    df = pd.read_csv(INPUT_FILE)#.iloc[1:2000]

    # Load transformer model
    model = SentenceTransformer('all-mpnet-base-v2')
    # Compute embeddings for all pairs

    sentence1 = df['sentence1'].tolist()
    sentence2 = df['sentence2'].tolist()

    embeddings1 = model.encode(
        sentence1, batch_size=32, show_progress_bar=True)
    embeddings2 = model.encode(
        sentence2, batch_size=32, show_progress_bar=True)

    similarities = []
    
    for i in range(len(embeddings1)):
        
        similarity = model.similarity(
            embeddings1[i], embeddings2[i])[0][0].item()
        similarities.append(similarity)
        
    df['similarity'] = similarities
    
    print(df.head())
    df_llm_pairs = df[df['similarity'] >= 0.4]


    df.to_csv(OUTPUT_ALL_FILE, index=False)
    df_llm_pairs.to_csv(OUTPUT_LLM_PAIRS_FILE, index=False)
    
    print("Total number of pairs: ", len(df))
    print("Number of pairs with similarity >= 0.5 (to inference on the LLM model): ", len(df_llm_pairs))
    print(f"Percentage of pairs to inference on the fine-tuned model: {100*(len(df_llm_pairs) / len(df)):.2f}%")
    
    

if __name__ == "__main__":
    main()
