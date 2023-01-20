#gc = global call -> this script is used from top level folder

echo READING CONFIG

RUNS=13

MAP_FOLDERS=('exposure_time_1seconds' 'exposure_time_5seconds' 'exposure_time_10seconds'
    'exposure_time_15seconds' 'exposure_time_20seconds' 'exposure_time_25seconds'
    'exposure_time_30seconds' 'exposure_time_35seconds' 'exposure_time_40seconds'
    'exposure_time_45seconds' 'exposure_time_50seconds' 'exposure_time_55seconds' 'exposure_time_60seconds')

#of the above mentioned folder names (map folder array)
BASE_PATH=~/sec_Min_Aggregation/maps/

#output path of histories, model
OUT_PATH=~/sec_Min_Aggregation/results/

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
    mkdir -p "$OUT_PATH"
    mkdir "$HISTORY_PATH"
fi

for ((i = 0; i < $RUNS; i++)); do
    echo "------------------------------------------------------------------------------DETECTION ATTEMPT on ${MAP_FOLDERS[$i]} ---------------------------------------------------"
    echo "Current Exposure Time: ${MAP_FOLDERS[$i]}"
    echo "$BASE_PATH${MAP_FOLDERS[$i]}"
    echo "$OUT_PATH${MAP_FOLDERS[$i]}/"
    mkdir "$OUT_PATH${MAP_FOLDERS[$i]}/"

    python3 Detection/NN_WORKFLOWS/classify_aggregation_maps.py "$BASE_PATH${MAP_FOLDERS[$i]}" $RESOLUTION $EPOCHS $BATCH_SIZE $VALIDATION_SPLIT "$OUT_PATH${MAP_FOLDERS[$i]}/" "$NAME${MAP_FOLDERS[$i]}"

    echo "$OUT_PATH${MAP_FOLDERS[$i]}/$NAME${MAP_FOLDERS[$i]}.pkl"
done

#needed to save the configuration
# cp sec_to_min_eval_NN.sh "$OUT_PATH/"
