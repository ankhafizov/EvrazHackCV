import json
import cv2
import os

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


check_set = set()
for i in range(len(training_data["annotations"])):
    image_id = training_data["annotations"][i]["image_id"]
    category_id = str(0)
    bbox = training_data["annotations"][i]["bbox"]
    for img in training_data["images"]:
        if img["id"] == image_id:
            img_name = img["file_name"]
            image_path = os.path.join("data_task2", "train", "images", img_name)
    kitti_bbox = [bbox[0], bbox[1], bbox[2] + bbox[0], bbox[3] + bbox[1]]

    yolo_bbox = convert(image_path, kitti_bbox[0], kitti_bbox[1], kitti_bbox[2], kitti_bbox[3])
    filename = os.path.join("data_task2", "train", "labels", img_name.replace("jpg", "txt"))
    content = category_id + " " + str(yolo_bbox[0]) + " " + str(yolo_bbox[1]) + " " + str(yolo_bbox[2]) + " " + str(
        yolo_bbox[3])

    if image_id in check_set:
        file = open(filename, "a")
        file.write("\n")
        file.write(content)
        file.close()
    elif image_id not in check_set:
        check_set.add(image_id)
        file = open(filename, "w")
        file.write(content)
        file.close()
