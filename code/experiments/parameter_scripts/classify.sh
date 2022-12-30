

echo READING CONFIG

RUNS=22

MAP_FOLDERS=("exposure_time_0.1seconds"  "exposure_time_0.3seconds"  "exposure_time_0.5seconds" 
"exposure_time_0.7seconds"  "exposure_time_0.9seconds" "exposure_time_0.2seconds" 
"exposure_time_0.4seconds"  "exposure_time_0.6seconds"  "exposure_time_0.8seconds" 'exposure_time_1seconds' 'exposure_time_5seconds' 'exposure_time_10seconds' 
'exposure_time_15seconds' 'exposure_time_20seconds' 'exposure_time_25seconds' 
'exposure_time_30seconds' 'exposure_time_35seconds' 'exposure_time_40seconds' 
'exposure_time_45seconds' 'exposure_time_50seconds' 'exposure_time_55seconds' 'exposure_time_60seconds')

BASE_PATH=$1

OUT_PATH=$2

#pkl naming --> each new result name will be saved individually, therefore more histories and models can be created
NAME="ROUND_1"

RESOLUTION=32
EPOCHS=100
BATCH_SIZE=128
VALIDATION_SPLIT=0.2

echo $IN_PATH
echo $OUT_PATH


if [ ! -d $OUT_PATH ]; then
echo "CREATING results folder $FOLDER_PATH"
mkdir -p "$OUT_PATH";
mkdir "$HISTORY_PATH";
fi



for ((i=0; i<$RUNS; i++))

do
    echo "------------------------------------------------------------------------------DETECTION ATTEMPT on ${MAP_FOLDERS[$i]} ---------------------------------------------------"


    echo "Current Exposure Time: ${MAP_FOLDERS[$i]}"
    echo "$BASE_PATH${MAP_FOLDERS[$i]}"
    echo "$OUT_PATH${MAP_FOLDERS[$i]}/"


    mkdir "$OUT_PATH${MAP_FOLDERS[$i]}/"

    python3 ../Detection/NN_WORKFLOWS/classify_aggregation_maps.py "$BASE_PATH${MAP_FOLDERS[$i]}" $RESOLUTION $EPOCHS $BATCH_SIZE $VALIDATION_SPLIT "$OUT_PATH${MAP_FOLDERS[$i]}/" "$NAME${MAP_FOLDERS[$i]}"


done

#needed to save the configuration
cp split_seconds_classify_eval.sh "$OUT_PATH/"



