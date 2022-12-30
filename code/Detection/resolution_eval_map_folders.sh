

echo READING CONFIG

BASE_PATH=~/workspace/data/experiment1/1run_diff_resolution/maps/

OUT_PATH=/home/robin/workspace/data/experiment1/1run_diff_resolution/results/

#pkl naming --> each new result name will be saved individually, therefore more histories and models can be created
NAME="ROUND_1"


EPOCHS=100
BATCH_SIZE=128
VALIDATION_SPLIT=0.2

RUNS=16

# MAP_FOLDERS=("resolution_8"  "resolution_10"  "resolution_12"
# "resolution_14"  "resolution_16"  "resolution_18"  "resolution_20"  "resolution_22"
# "resolution_24"  "resolution_26"   "resolution_28"  "resolution_30"  "resolution_32")

# RESOLUTIONS=("8" "10" "12" "14" "16" "18" "20" "22" "24" "26" "28" "30" "32")


MAP_FOLDERS=("resolution_2" "resolution_4" "resolution_6"
 "resolution_8" "resolution_10" "resolution_12"
 "resolution_14" "resolution_16" "resolution_18" 
 "resolution_20" "resolution_22" "resolution_24"  
 "resolution_26"   "resolution_28"  "resolution_30" 
 "resolution_32")

RESOLUTIONS=("2" "4" "6" "8" "10" "12" "14" "16" "18" "20"  "22" "24" "26" "28" "30" "32")


echo $IN_PATH
echo $OUT_PATH



if [ ! -d $OUT_PATH ]; then
echo "CREATING results folder $FOLDER_PATH"
mkdir -p "$OUT_PATH";

fi



for ((i=0; i<$RUNS; i++))

do
    echo "------------------------------------------------------------------------------DETECTION ATTEMPT on ${MAP_FOLDERS[$i]} ---------------------------------------------------"


    echo "Current Resolution: ${RESOLUTIONS[$i]}"

    echo "$BASE_PATH${MAP_FOLDERS[$i]}"

    echo "$OUT_PATH${MAP_FOLDERS[$i]}/"


    mkdir "$OUT_PATH${MAP_FOLDERS[$i]}/"

    # tools/Evaluation/NN_WORKFLOWS/train_model _padded.py

    # echo NN_WORKFLOWS/train_model.py "$BASE_PATH${MAP_FOLDERS[$i]}" "${RESOLUTIONS[$i]}" $EPOCHS $BATCH_SIZE $VALIDATION_SPLIT "$OUT_PATH${MAP_FOLDERS[$i]}/" $NAME

    python3 NN_WORKFLOWS/train_model_padded.py "$BASE_PATH${MAP_FOLDERS[$i]}" "${RESOLUTIONS[$i]}" $EPOCHS $BATCH_SIZE $VALIDATION_SPLIT "$OUT_PATH${MAP_FOLDERS[$i]}/" "$NAME${RESOLUTIONS[$i]}"

    echo "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/"

    mkdir "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/"

    echo "$OUT_PATH${MAP_FOLDERS[$i]}/$NAME.pkl"


    bool=$(echo "$VALIDATION_SPLIT > 0.0" | bc)
    if [ $bool = '1' ]; then

    # python3 ../Plotting/plot_1_history.py "$OUT_PATH${MAP_FOLDERS[$i]}/$NAME.pkl" "$OUT_PATH${MAP_FOLDERS[$i]}/metrics/"
    python3 ../Plotting/plot_from_histories.py "$OUT_PATH${MAP_FOLDERS[$i]}/" $EPOCHS "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/" 'val_accuracy'
    python3 ../Plotting/plot_from_histories.py "$OUT_PATH${MAP_FOLDERS[$i]}/" $EPOCHS "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/" 'val_precision'
    python3 ../Plotting/plot_from_histories.py "$OUT_PATH${MAP_FOLDERS[$i]}/" $EPOCHS "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/" 'val_recall'
    python3 ../Plotting/plot_from_histories.py "$OUT_PATH${MAP_FOLDERS[$i]}/" $EPOCHS "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/" 'val_FP'
    python3 ../Plotting/plot_from_histories.py "$OUT_PATH${MAP_FOLDERS[$i]}/" $EPOCHS "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/" 'val_FN'

    fi
    python3 ../Plotting/plot_from_histories.py "$OUT_PATH${MAP_FOLDERS[$i]}/" $EPOCHS "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/" 'FN'
    python3 ../Plotting/plot_from_histories.py "$OUT_PATH${MAP_FOLDERS[$i]}/" $EPOCHS "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/" 'accuracy'
    python3 ../Plotting/plot_from_histories.py "$OUT_PATH${MAP_FOLDERS[$i]}/" $EPOCHS "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/" 'precision'
    python3 ../Plotting/plot_from_histories.py "$OUT_PATH${MAP_FOLDERS[$i]}/" $EPOCHS "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/" 'recall'
    python3 ../Plotting/plot_from_histories.py "$OUT_PATH${MAP_FOLDERS[$i]}/" $EPOCHS "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/" 'FP'








done

#needed to save the configuration
cp resolution_eval_map_folders.sh "$OUT_PATH/"












