## Parameters
test_images_location=/home/akhafizov/Desktop/data_Evraz/test/images
dataset_in_coco_form_location=yolo_data/dataset.yaml

freeze_layers=18

train_tag=yolov5x_freeze_${freeze_layers}_adam_hypl_decay_lf0005


# Train

echo $train_tag
rm -rf yolov5/runs/train/$train_tag

python3 yolov5/train.py \
--img 640 \
--batch 25 \
--epochs 100  \
--data $dataset_in_coco_form_location \
--weights yolov5x.pt \
--name $train_tag \
--workers 12 \
--freeze $freeze_layers \
--hyp hyp.scratch-low.yaml \
--adam

# Test

python yolov5/detect.py \
--img 640 \
--conf-thres 0.5 \
--save-txt \
--name $train_tag \
--weights yolov5/runs/train/${train_tag}/weights/best.pt \
--source $test_images_location

python ./yolo2coco.py \
--path yolov5/runs/detect/$train_tag/ \
--yolo-subdir \
--output $train_tag.json