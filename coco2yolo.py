import json
import cv2
import os
import numpy as np
from shutil import copyfile

with open("data_task2/train/annotations/COCO_json/coco_annotations_train.json", "r") as f:
    training_data = json.load(f)


def get_shape(path):
    return cv2.imread(path).shape


def convert(path, x1, y1, x2, y2):
    def sorting(l1, l2):
        if l1 > l2:
            lmax, lmin = l1, l2
            return lmax, lmin
        else:
            lmax, lmin = l2, l1
            return lmax, lmin

    frame_shape = get_shape(path)
    xmax, xmin = sorting(x1, x2)
    ymax, ymin = sorting(y1, y2)
    dw = 1. / frame_shape[1]
    dh = 1. / frame_shape[0]
    x = (xmin + xmax) / 2.0
    y = (ymin + ymax) / 2.0
    w = xmax - xmin
    h = ymax - ymin
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def make_yolo_folders(yolo_dataset_path):
    img_train_path = os.path.join(yolo_dataset_path, "images/train")
    img_val_path = os.path.join(yolo_dataset_path, "images/val")

    labels_train_path = os.path.join(yolo_dataset_path, "labels/train")
    labels_val_path = os.path.join(yolo_dataset_path, "labels/val")
    
    for d in [img_train_path, img_val_path, labels_train_path, labels_val_path]:
        os.makedirs(d)
    
    return img_train_path, img_val_path, labels_train_path, labels_val_path


if __name__ == "__main__":
    #################### Params Start ##################################
    np.random.seed(55)

    coco_label_path = "/home/akhafizov/Desktop/data_Evraz/train/annotations/COCO_json/coco_annotations_train.json"
    image_folder_path = "/home/akhafizov/Desktop/data_Evraz/train/images"
    yolo_dataset_path = "./yolo_data"
    val_train_ratio = 10/90


    #################### Params End ##################################

    img_train_path, img_val_path, labels_train_path, labels_val_path = make_yolo_folders(yolo_dataset_path)
    val_proba = 1 / (1 + val_train_ratio)
    print("val_proba:", val_proba)
    with open(coco_label_path, "r") as f:
        training_data = json.load(f)

    N = len(training_data["annotations"])
    print("framse:", N)
    is_val_folder_array = np.random.choice([False, True], size=N, p = [val_proba, 1-val_proba])
    print(np.sum(is_val_folder_array), np.sum(~is_val_folder_array), np.sum(is_val_folder_array)/ np.sum(~is_val_folder_array))

    for i, is_val_folder in enumerate(is_val_folder_array):
        image_id = training_data["annotations"][i]["image_id"]
        category_id = str(0)
        bbox = training_data["annotations"][i]["bbox"]
        for img in training_data["images"]:
            if img["id"] == image_id:
                img_name = img["file_name"]
                image_path = os.path.join(image_folder_path, img_name)
        kitti_bbox = [bbox[0], bbox[1], bbox[2] + bbox[0], bbox[3] + bbox[1]]
        yolo_bbox = convert(image_path, kitti_bbox[0], kitti_bbox[1], kitti_bbox[2], kitti_bbox[3])
        
        content = category_id + " " + str(yolo_bbox[0]) + " " + str(yolo_bbox[1]) + " " + str(yolo_bbox[2]) + " " + str(yolo_bbox[3])

        label_dst_path = labels_val_path if is_val_folder else labels_train_path
        label_dst_path = os.path.join(label_dst_path, img_name.replace("jpg", "txt"))
        file = open(label_dst_path, "a")
        file.write("\n")
        file.write(content)

        image_dst_path = img_val_path if is_val_folder else img_train_path
        image_dst_path = os.path.join(image_dst_path, img_name)
        copyfile(image_path, image_dst_path)