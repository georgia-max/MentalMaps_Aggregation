"""
get semantic matching from NLP model using untrained sentence transformers.

Do this to reduce the number of pairing nodes that needs to be inferenced on the fined-tuned model.

Input:
    - df = all_definition_pairs.csv

output:
    - nlp_pairs = nlp_not_matched_pairs.csv
    - all_definition_pairs_llm.csv = the rest of the dataset that needs to be inferenced on the fined-tuned model..
"""
import glob
import os
import time
from functools import partial
from multiprocessing import Pool, cpu_count

import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer

# INPUT_FILE = "/Users/gl665/Documents/Phrame-MentalMaps-1/data/read_for_label/all_definition_pairs.csv"
# OUTPUT_DIR = "/Users/gl665/Documents/Phrame-MentalMaps-1/data/read_for_label/batch_results"
# OUTPUT_ALL_FILE = "/Users/gl665/Documents/Phrame-MentalMaps-1/data/read_for_label/nlp_not_matched_pairs.csv"
# OUTPUT_LLM_PAIRS_FILE = "/Users/gl665/Documents/Phrame-MentalMaps-1/data/read_for_label/all_definition_pairs_llm.csv"

INPUT_FILE = "C:\\Users\\GL665\\Documents\\Phrame-MentalMaps\\data\\read_for_label\\all_definition_pairs.csv"
OUTPUT_DIR = "C:\\Users\\GL665\\Documents\\Phrame-MentalMaps\\data\\read_for_label\\batch_results"
OUTPUT_ALL_FILE = "C:\\Users\\GL665\\Documents\\Phrame-MentalMaps\\data\\read_for_label\\nlp_not_matched_pairs.csv"
OUTPUT_LLM_PAIRS_FILE = "C:\\Users\\GL665\\Documents\\Phrame-MentalMaps\\data\\read_for_label\\all_definition_pairs_llm.csv"


BATCH_NUM = [388, 267, 769, 520, 29, 183, 35, 255, 667, 337, 997, 7, 1009, 775, 347, 826, 649, 639, 1027, 512, 833, 135, 843, 507, 498, 20, 672, 890, 352, 1000, 177, 129, 12, 640, 1019, 895, 765, 987, 677, 25, 384, 502, 130, 659, 836, 645, 17, 259, 39, 172, 1005, 683, 167, 1010, 262, 139, 494, 1022, 517, 823, 342, 40, 770, 992, 662, 332, 2, 30, 773, 341, 33, 185, 1, 178, 661, 331, 991, 1021, 514, 261, 497, 508, 680, 1013, 998, 338, 668, 171, 8, 348, 1006, 14, 646, 829, 1028, 636, 133, 501, 387, 835, 766, 896, 354, 26, 674, 518, 643, 11, 1003, 174, 168, 671, 23, 351, 893, 763, 830, 504, 1031, 382, 840, 136, 18, 825, 1024, 511, 4, 994, 664, 334, 36, 256, 180, 344, 523, 678, 988, 839, 264, 822,
             516, 1023, 31, 3, 993, 333, 663, 771, 343, 524, 1011, 166, 682, 495, 138, 263, 16, 644, 1004, 173, 38, 258, 24, 986, 676, 894, 764, 1018, 837, 658, 131, 503, 385, 176, 1001, 641, 13, 128, 499, 506, 842, 134, 832, 353, 891, 673, 21, 346, 774, 1008, 6, 336, 666, 996, 34, 182, 513, 1026, 638, 648, 827, 266, 28, 521, 1014, 768, 329, 679, 989, 684, 522, 1017, 265, 657, 838, 493, 510, 1025, 824, 19, 345, 181, 257, 37, 995, 335, 665, 5, 892, 350, 22, 670, 169, 137, 841, 383, 1030, 505, 831, 10, 642, 519, 175, 1002, 834, 386, 500, 132, 675, 985, 27, 767, 1007, 349, 9, 170, 999, 669, 339, 637, 1029, 828, 647, 15, 509, 496, 260, 1012, 681, 165, 330, 660, 990, 179, 184, 32, 340, 772, 821, 515, 1020]
# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)


def process_batch(batch_tuple, model_name='all-mpnet-base-v2'):
    """Process a single batch of data using a fresh model instance"""
    batch_id, df_batch = batch_tuple

    # Create a new model instance for each process
    # This is important for multiprocessing to avoid sharing model objects between processes
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    if device == "cuda":

        model = SentenceTransformer(model_name).to(device)
    else:
        model = SentenceTransformer(model_name)

    start_time = time.time()

    sentence1 = df_batch['sentence1'].tolist()
    sentence2 = df_batch['sentence2'].tolist()

    # Encode sentences
    embeddings1 = model.encode(
        sentence1, batch_size=32, show_progress_bar=False, convert_to_numpy=True, device=device)
    embeddings2 = model.encode(
        sentence2, batch_size=32, show_progress_bar=False, convert_to_numpy=True, device=device)

    # Calculate similarities
    similarities = []
    for i in range(len(embeddings1)):
        similarity = np.dot(embeddings1[i], embeddings2[i]).round(4)
        similarities.append(similarity)

    df_batch['similarity'] = similarities

    # Save batch results
    batch_output_file = os.path.join(
        OUTPUT_DIR, f"batch_{batch_id}_results.csv")
    df_batch.to_csv(batch_output_file, index=False)

    batch_time = time.time() - start_time
    print(
        f"Batch {batch_id} processed in {batch_time:.2f} seconds. Results saved to {batch_output_file}")

    return batch_output_file


def main():

    # Check if GPU is available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    # Start timing the entire process

    start_time_total = time.time()

    print("Loading and preprocessing data...")
    df = pd.read_csv(INPUT_FILE)
    df = df.dropna()

    # Uncomment this line
    # df = df.sample(n=20000, random_state=42)

    # Determine number of cores to use (leave 1-2 cores free for system processes)]
    if device == 'cpu':
        num_processes = max(1, cpu_count() - 5)
        print(f"Using {num_processes} CPU cores for parallel processing")
    else:
        num_processes = 1
        print("Using 1 GPU for parallel processing")

    # Batch parameters - smaller batches for better load balancing
    batch_size = 5000  # Smaller batch size for parallel processing # use 500 for cpu

    # Create batches
    batches = []
    for i in range(0, len(df), batch_size):
        batch_id = i // batch_size + 1
        # if batch_id not in BATCH_NUM:
        batch_output_file = os.path.join(
            OUTPUT_DIR, f"batch_{batch_id}_results.csv")
        if not os.path.exists(batch_output_file):
            df_batch = df.iloc[i:i+batch_size].copy()

            batches.append((batch_id, df_batch))

    print(
        f"Created {len(batches)} batches of size {batch_size} that need processing")

    # Process batches in parallel
    print("\n--- Starting parallel processing ---")
    batch_files = []

    if batches:
        with Pool(processes=num_processes) as pool:
            batch_files = pool.map(process_batch, batches)

    # Add existing batch files that were skipped
    for i in range(1, len(df) // batch_size + 2):
        existing_file = os.path.join(OUTPUT_DIR, f"batch_{i}_results.csv")
        if os.path.exists(existing_file) and existing_file not in batch_files:
            batch_files.append(existing_file)

    # Combine all batch results
    print("\nCombining all processed batches...")
    all_results = []
    for file in batch_files:
        if file and os.path.exists(file):
            batch_df = pd.read_csv(file)
            all_results.append(batch_df)

    combined_df = pd.concat(all_results, ignore_index=True)

    # Save final results
    print("Saving final combined results...")
    combined_df.to_csv(OUTPUT_ALL_FILE, index=False)

    # Create LLM subset
    df_llm_pairs = combined_df[combined_df['similarity'] >= 0.4]
    df_llm_pairs.to_csv(OUTPUT_LLM_PAIRS_FILE, index=False)

    # Summary statistics
    print("\n--- Summary Statistics ---")
    print("Total number of pairs processed: ", len(combined_df))
    print("Number of pairs with similarity >= 0.4 (to inference on the LLM model): ", len(
        df_llm_pairs))
    print(
        f"Percentage of pairs to inference on the fine-tuned model: {100*(len(df_llm_pairs) / len(combined_df)):.2f}%")

    # Total runtime
    total_time = time.time() - start_time_total
    print(
        f"\n--- Total runtime: {total_time:.2f} seconds ({total_time/60:.2f} minutes) ---")
    print(f"Average time per batch: {total_time/len(batches):.2f} seconds")


if __name__ == "__main__":
    main()
