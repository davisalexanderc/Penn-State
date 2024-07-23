import os
import json

# Define the paths to the directories and annotation files
data_dir = './data'
image_dirs = {
    'train': os.path.join(data_dir, 'images/train'),
    'val': os.path.join(data_dir, 'images/val'),
    'test': os.path.join(data_dir, 'images/test')
}
annotation_files = {
    'train': os.path.join(data_dir, 'annotations/instances_train.json'),
    'val': os.path.join(data_dir, 'annotations/instances_val.json'),
    'test': os.path.join(data_dir, 'annotations/instances_test.json')
}

# Check if directories exist
for key, dir_path in image_dirs.items():
    if not os.path.exists(dir_path):
        print(f"Directory {dir_path} does not exist.")
    else:
        print(f"Directory {dir_path} exists.")

# Check if annotation files exist and are in COCO format
for key, ann_path in annotation_files.items():
    if not os.path.exists(ann_path):
        print(f"Annotation file {ann_path} does not exist.")
    else:
        print(f"Annotation file {ann_path} exists.")
        # Check COCO format
        with open(ann_path, 'r') as f:
            data = json.load(f)
            if 'images' in data and 'annotations' in data and 'categories' in data:
                print(f"Annotation file {ann_path} is in COCO format.")
            else:
                print(f"Annotation file {ann_path} is not in COCO format.")

# Check if each image folder contains the required files
for key, dir_path in image_dirs.items():
    print(f"\nChecking files in {dir_path}:")
    if os.path.exists(dir_path):
        files = os.listdir(dir_path)
        original_files = [f for f in files if '_original' in f]
        semantic_files = [f for f in files if '_semantic' in f]
        instance_files = [f for f in files if '_instance' in f]
        
        print(f"Found {len(original_files)} original files.")
        print(f"Found {len(semantic_files)} semantic files.")
        print(f"Found {len(instance_files)} instance files.")
        
        # Check if the counts match
        if len(original_files) == len(semantic_files) == len(instance_files):
            print(f"All files are correctly paired in {dir_path}.")
        else:
            print(f"Mismatch in file counts in {dir_path}.")
    else:
        print(f"Directory {dir_path} does not exist.")
