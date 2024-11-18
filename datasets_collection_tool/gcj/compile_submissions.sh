#!/bin/bash

top_dir="gcj2017/"
# Directory containing the source files
source_dir="$top_dir/train"

# Directory to store the compiled solutions
output_dir="$top_dir/train_compiled"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Loop over all files in the source directory
for file in "$source_dir"/*; do
    # Check if the file is a regular file
    if [ -f "$file" ]; then
        # Get the filename without the extension
        filename=$(basename "$file")
        filename="${filename%.*}"

        # Compile the file using gcc
        g++ "$file" -O0 -gdwarf-4 -o "$output_dir/$filename"
    fi
done
