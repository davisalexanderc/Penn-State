# File: File_puller.py
# Description: The purpose of this script it to extract the TEM images from Dr. Plass' research database.
# This script finds and copies all .tif files from subdirectories named 'TEM' to a new directory named 
# 'data' in the same directory as the script.

import os
import shutil
import sys

# Set the output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Get the directory where the Python script is located
base_directory = os.path.dirname(os.path.abspath(__file__))
destination_directory = os.path.join(base_directory, 'data')

# Create the destination directory if it doesn't exist
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

# Walk through the subdirectories in the base directory
for root, dirs, files in os.walk(base_directory):
    if os.path.basename(root).lower() == 'tem':
        for file in files:
            if file.lower().endswith('.tif'):
                # Construct full file path
                file_path = os.path.join(root, file)
                try:
                    # Copy file to the destination directory
                    shutil.copy2(file_path, destination_directory)
                    # Print the name of the file
                    print(f"Copied: {file_path}")
                except Exception as e:
                    print(f"Failed to copy {file_path}: {e}")

print("All .tif files in 'TEM' directories have been copied.")