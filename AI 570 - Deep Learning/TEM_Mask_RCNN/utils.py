import os
import json
import numpy as np
import matplotlib.pyplot as plt
from detectron2 import model_zoo
from detectron2.engine import DefaultTrainer, DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.data.datasets import register_coco_instances, load_coco_json

class Model:
    def __init__(self, predictor):
        self.predictor = predictor

    def _convert_to_segments_format(self, image, outputs):
        segmentation_bitmap = np.zeros((image.shape[0], image.shape[1]), np.uint32)
        annotations = []
        counter = 1
        instances = outputs['instances']
        for i in range(len(instances.pred_classes)):
            category_id = int(instances.pred_classes[i])
            instance_id = counter
            mask = instances.pred_masks[i].cpu().numpy()
            segmentation_bitmap[mask] = instance_id
            annotations.append({'id': instance_id, 'category_id': category_id})
            counter += 1
        return segmentation_bitmap, annotations

    def __call__(self, image):
        image = np.array(image)
        outputs = self.predictor(image)
        label, label_data = self._convert_to_segments_format(image, outputs)
        return label, label_data

def train_model(data_dir):
    # Register the dataset in Detectron2
    #register_coco_instances('my_dataset_train', {}, os.path.join(data_dir, 'annotations/instances_train.json'), os.path.join(data_dir, 'images/train'))
    #register_coco_instances('my_dataset_val', {}, os.path.join(data_dir, 'annotations/instances_val.json'), os.path.join(data_dir, 'images/val'))
    
    train_metadata = MetadataCatalog.get('my_dataset_train')  
    val_metadata = MetadataCatalog.get('my_dataset_val')

    print(train_metadata) # For Testing
    print(len(train_metadata.thing_classes)) # For Testing

    # Configure the training run
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file('COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml'))
    cfg.DATASETS.TRAIN = ('my_dataset_train',)
    cfg.DATASETS.TEST = ('my_dataset_val',)
    cfg.INPUT.MASK_FORMAT = 'bitmask'
    cfg.DATALOADER.NUM_WORKERS = 2
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url('COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml')
    cfg.SOLVER.IMS_PER_BATCH = 2
    cfg.SOLVER.BASE_LR = 0.00025
    cfg.SOLVER.MAX_ITER = 300
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2 # [Rods, Spheres] The original code is: len(train_metadata.thing_classes)
    
    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    trainer = DefaultTrainer(cfg)
    trainer.resume_or_load(resume=False)
    trainer.train()

    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, 'model_final.pth')
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
    cfg.DATASETS.TEST = ('my_dataset_val',)
    cfg.TEST.DETECTIONS_PER_IMAGE = 1000
    predictor = DefaultPredictor(cfg)
    model = Model(predictor)
    
    return model

def visualize(*args):
    images = args
    for i, image in enumerate(images):
        plt.subplot(1, len(images), i+1)
        plt.imshow(np.array(image))
    plt.show()

def unregister_dataset(name):
    if name in DatasetCatalog.list():
        DatasetCatalog.remove(name)
    if name in MetadataCatalog.list():
        del MetadataCatalog._metadata[name]