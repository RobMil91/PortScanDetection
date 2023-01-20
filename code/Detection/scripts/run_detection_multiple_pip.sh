echo READING CONFIG

DETECTIONS=2
IN_PATH=~/sec_Min_Aggregation/maps/exposure_time_1seconds/
OUT_PATH=~/sec_Min_Aggregation/classification_results_1second/

RESOLUTION=32
EPOCHS=100
BUCKET_SIZE=128
VALIDATION_SPLIT=0.2

echo $IN_PATH
echo $OUT_PATH

if [ ! -d $OUT_PATH ]; then
    echo "CREATING results folder $FOLDER_PATH"
    mkdir -p "$OUT_PATH"
    mkdir "$OUT_PATH/metrics"

fi

for ((i = 1; i <= $DETECTIONS; i++)); do
    echo "------------------------------------------------------------------------------DETECTION ATTEMPT attack $i ---------------------------------------------------"

    NAME="ROUND_$i"

    python3 NN_WORKFLOW/train_model.py $IN_PATH $RESOLUTION $EPOCHS $BUCKET_SIZE $VALIDATION_SPLIT $OUT_PATH $NAME

done

#needed to save the configuration
cp run_detection_multiple_pip.sh "$OUT_PATH/"
