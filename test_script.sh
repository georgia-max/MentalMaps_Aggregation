#!/bin/bash

# Run  ./test_script.sh

# Define the directories
INPUT_DIR="Dataset/Overcome/SF_Models"
OUTPUT_DIR="Output/Overcome/SF_Models"

# Create the output directory if it doesn't already exist
mkdir -p "$OUTPUT_DIR"

# Loop through all .mdl files in the input directory
for mdl_file in "$INPUT_DIR"/*.mdl; do
    # Extract the base filename without the extension
    base_name=$(basename "$mdl_file" .mdl)

    # Define the output file path
    json_file="$OUTPUT_DIR/${base_name}.json"

    # Run the Python script with the current file and the output file as arguments
    python3 main.py "$mdl_file" "$json_file"

done

echo "All files processed."

