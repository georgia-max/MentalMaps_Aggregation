
import glob
import os
import time
from functools import partial
from multiprocessing import Pool, cpu_count

import numpy as np
import pandas as pd

INPUT_DIR = "/Users/gl665/Documents/Phrame-MentalMaps-1/data/read_for_label/batch_results"


def main():

    print("Loading and preprocessing data...")
    # read all the files names in the output directory
    
    all_files = glob.glob(os.path.join(INPUT_DIR, "*.csv"))
    print(all_files)
    
    all_files = [file.split("/")[-1] for file in all_files]
    print(all_files)
    all_files_num = [int(file.split("_")[1]) for file in all_files]
    print(all_files_num)
    

    # get all the numbers of the files
    # all_files = [int(file.split("_")[1]) for file in all_files]
    # print(all_files)


if __name__ == "__main__":
    main()
