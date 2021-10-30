## Parameters

freeze_layers=18

test_images_location=yolo_data/images/test
dataset_in_yolo_form_location=yolo_data/dataset.yaml
train_tag=yolov5x_freeze_${freeze_layers}_adam_hypl_decay_lf0005

epochs=300

# Train

echo $train_tag
rm -rf yolov5/runs/train/$train_tag

python3 yolov5/train.py \
--img 640 \
--batch 25 \
--epochs $epochs  \
--data $dataset_in_yolo_form_location \
--weights yolov5x.pt \
--name $train_tag \
--workers 12 \
--freeze $freeze_layers \
--hyp yola_hyp.scratch-low_custom.yaml \
--adam

# Test
rm -rf yolov5/runs/detect/$train_tag

python yolov5/detect.py \
--img 640 \
--conf-thres 0.5 \
--save-txt \
--name $train_tag \
--weights yolov5/runs/train/${train_tag}/weights/best.pt \
--source $test_images_location

mkdir -p output

python ./yolo2coco.py \
--path yolov5/runs/detect/$train_tag/ \
--yolo-subdir \
--output $train_tag.json