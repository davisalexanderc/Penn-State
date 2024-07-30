import json
import cv2
import numpy as np
from pycocotools import mask

def rle_to_polygon(segmentation):
    """Convert RLE to polygon."""
    if isinstance(segmentation, dict):
        rle = mask.frPyObjects(segmentation, segmentation['size'][0], segmentation['size'][1])
        masks = mask.decode(rle)
        polygons = []
        for i in range(masks.shape[-1]):
            contours, _ = cv2.findContours(masks[:, :, i].astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                contour = contour.flatten().tolist()
                if len(contour) >= 6:
                    polygons.append(contour)
        return polygons
    return segmentation

def convert_annotations(input_annotation_path, output_annotation_path):
    """Convert segmentations to polygons and save to a new JSON file."""
    with open(input_annotation_path, 'r') as f:
        annotations = json.load(f)

    # Convert segmentations to polygons
    for annotation in annotations['annotations']:
        if 'segmentation' in annotation:
            annotation['segmentation'] = rle_to_polygon(annotation['segmentation'])
            image_id = annotation['image_id']
            # Find the corresponding image filename
            image_filename = next(img['file_name'] for img in annotations['images'] if img['id'] == image_id)
            print(f"Processed segmentation for file: {image_filename}")

    # Save the updated annotations
    with open(output_annotation_path, 'w') as f:
        json.dump(annotations, f)

    print("Conversion completed and saved to:", output_annotation_path)

if __name__ == "__main__":
    # Set the input and output paths directly in the script
    input_annotation_path = './data/annotations/train_annotations.json'
    output_annotation_path = './data/annotations/train_annotations_converted.json'
    
    # Convert the annotations
    convert_annotations(input_annotation_path, output_annotation_path)
