#!/bin/bash

# Directory containing your .docx files
INPUT_DIR="faculty/"

# Directory where .txt files will be saved
OUTPUT_DIR="faculty/txt_files"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Loop through all .docx files in the input directory
for FILE in "$INPUT_DIR"/*.docx; do
  # If no .docx files exist, skip
  [ -e "$FILE" ] || continue

  # Extract the base filename (without .docx extension)
  BASENAME=$(basename "$FILE" .docx)

  # Use Pandoc to convert .docx to .txt
  pandoc "$FILE" -t plain -o "$OUTPUT_DIR/$BASENAME.txt"

  echo "Converted: $FILE -> $OUTPUT_DIR/$BASENAME.txt"
done
