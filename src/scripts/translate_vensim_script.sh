#!/bin/bash

# Run  ./translate_vensim_script.sh
# Change the directories 

INPUT_DIR="data/raw/rc_mental_models_clean"
OUTPUT_DIR="data/jsonfiles"

# Create the output directory if it doesn't already exist
mkdir -p "$OUTPUT_DIR"

# Loop through all .mdl files in the input directory
for mdl_file in "$INPUT_DIR"/*.mdl; do
    # Extract the base filename without the extension
    base_name=$(basename "$mdl_file" .mdl)

    # Define the output file path
    json_file="$OUTPUT_DIR/${base_name}.json"

    # Run the Python script with the current file and the output file as arguments
    python3 src/utils/export_cld_json.py "$mdl_file" "$json_file"

done

echo "All files processed."


