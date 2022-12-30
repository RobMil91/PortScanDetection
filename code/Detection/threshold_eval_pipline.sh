

echo READING CONFIG

#this can be used as a basic pipeline for detection, since there are no special parameters needed, the threshold is set during the Data synthesis


BASE_PATH=~/workspace/data/experiment1/1threshold_diff/maps/

OUT_PATH=~/workspace/data/experiment1/1threshold_diff/results/

RUNS=12
MAP_FOLDERS=("threshold_1" "threshold_100" "threshold_25" 
"threshold_5" "threshold_600" "threshold_800"
"threshold_10" "threshold_200" "threshold_400" 
"threshold_50" "threshold_75" "threshold_1000")

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

fi

for ((i=0; i<$RUNS; i++))

do
    echo "------------------------------------------------------------------------------DETECTION ATTEMPT on ${MAP_FOLDERS[$i]} ---------------------------------------------------"


    echo "Current Exposure Time: ${MAP_FOLDERS[$i]}"

    echo "$BASE_PATH${MAP_FOLDERS[$i]}"

    echo "$OUT_PATH${MAP_FOLDERS[$i]}/"


    mkdir "$OUT_PATH${MAP_FOLDERS[$i]}/"

    python3 NN_WORKFLOWS/train_model.py "$BASE_PATH${MAP_FOLDERS[$i]}" $RESOLUTION $EPOCHS $BATCH_SIZE $VALIDATION_SPLIT "$OUT_PATH${MAP_FOLDERS[$i]}/" "$NAME${MAP_FOLDERS[$i]}"

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
cp threshold_eval_pipline.sh "$OUT_PATH/"












