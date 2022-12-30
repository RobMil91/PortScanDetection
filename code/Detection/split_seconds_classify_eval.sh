

echo READING CONFIG

RUNS=9
MAP_FOLDERS=("exposure_time_0.1seconds"  "exposure_time_0.3seconds"  "exposure_time_0.5seconds" 
"exposure_time_0.7seconds"  "exposure_time_0.9seconds" "exposure_time_0.2seconds" 
"exposure_time_0.4seconds"  "exposure_time_0.6seconds"  "exposure_time_0.8seconds")

BASE_PATH=~/workspace/data/experiment1/1run_test_split_seconds/maps/

OUT_PATH=~/workspace/data/experiment1/1run_test_split_seconds/results/

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

    python3 NN_WORKFLOWS/train_model.py "$BASE_PATH${MAP_FOLDERS[$i]}" $RESOLUTION $EPOCHS $BATCH_SIZE $VALIDATION_SPLIT "$OUT_PATH${MAP_FOLDERS[$i]}/" "$NAME${MAP_FOLDERS[$i]}"

    echo "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/"

    mkdir "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/"

    echo "$OUT_PATH${MAP_FOLDERS[$i]}/$NAME${MAP_FOLDERS[$i]}.pkl"

    # cp "$OUT_PATH${MAP_FOLDERS[$i]}/$NAME${MAP_FOLDERS[$i]}.pkl" "$HISTORY_PATH$NAME${MAP_FOLDERS[$i]}.pkl"
    # bool=$(echo "$VALIDATION_SPLIT > 0.0" | bc)
    # if [ $bool = '1' ]; then

    # # python3 ../Plotting/plot_1_history.py "$OUT_PATH${MAP_FOLDERS[$i]}/$NAME.pkl" "$OUT_PATH${MAP_FOLDERS[$i]}/metrics/"
    # python3 ../Plotting/plot_from_histories.py "$OUT_PATH${MAP_FOLDERS[$i]}/" $EPOCHS "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/" 'val_accuracy'
    # python3 ../Plotting/plot_from_histories.py "$OUT_PATH${MAP_FOLDERS[$i]}/" $EPOCHS "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/" 'val_precision'
    # python3 ../Plotting/plot_from_histories.py "$OUT_PATH${MAP_FOLDERS[$i]}/" $EPOCHS "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/" 'val_recall'
    # python3 ../Plotting/plot_from_histories.py "$OUT_PATH${MAP_FOLDERS[$i]}/" $EPOCHS "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/" 'val_FP'
    # python3 ../Plotting/plot_from_histories.py "$OUT_PATH${MAP_FOLDERS[$i]}/" $EPOCHS "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/" 'val_FN'

    # fi
    # python3 ../Plotting/plot_from_histories.py "$OUT_PATH${MAP_FOLDERS[$i]}/" $EPOCHS "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/" 'FN'
    # python3 ../Plotting/plot_from_histories.py "$OUT_PATH${MAP_FOLDERS[$i]}/" $EPOCHS "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/" 'accuracy'
    # python3 ../Plotting/plot_from_histories.py "$OUT_PATH${MAP_FOLDERS[$i]}/" $EPOCHS "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/" 'precision'
    # python3 ../Plotting/plot_from_histories.py "$OUT_PATH${MAP_FOLDERS[$i]}/" $EPOCHS "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/" 'recall'
    # python3 ../Plotting/plot_from_histories.py "$OUT_PATH${MAP_FOLDERS[$i]}/" $EPOCHS "$OUT_PATH${MAP_FOLDERS[$i]}/metrics_ROUND_$NAME/" 'FP'


done

#needed to save the configuration
cp split_seconds_classify_eval.sh "$OUT_PATH/"



