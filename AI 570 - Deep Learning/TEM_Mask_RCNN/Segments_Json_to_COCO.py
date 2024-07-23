# pip install tensorflow
# pip install segments-ai
# pip install pycocotools

import sys
import os
import tensorflow as tf
import torch
from segments import SegmentsClient, SegmentsDataset
from segments.utils import export_dataset

# Initialize a SegmentsDataset from the release file
API_folder = "C:/Users/alex/Desktop/API_keys/"
API_file = "Segments_API.txt"
api_key = open(API_folder + API_file, "r").readline().strip()
client = SegmentsClient(api_key)
release = client.get_release('davis_alexander/TEM_Project4', 'TEM_V01')   # Alternatively: release = 'flowers-v1.0.json'
dataset = SegmentsDataset(release, labelset='ground-truth', filter_by=['labeled', 'reviewed'])

# Export to COCO panoptic format
export_dataset(dataset, export_format='coco-instance')