

#this pipeline is used to work on a labeled csv!
echo READING CONFIG

#input for the pipeline
LABELD_OUT_CSV=~/workspace/data/experiment1/injected_attack_labeled.csv

ALL_SECONDS=900

FOLDER_PATH=~/workspace/data/experiment1/2run_test_split_seconds/

THRESHOLD_PORTSCAN=1
MAP_RES_X=32
MAP_RES_Y=32
#65536
MAX_CHECKED_PORTS=2000
# FIXED_EXPOSURE_TIME=60



diff_exposure_times=9
# diff_exposure_times=13
timing_list=("0.1" "0.2" "0.3" "0.4" "0.5" "0.6" "0.7" "0.8" "0.9")
# timing_list=("1" "5" "10" "15" "20" "25" "30" "35" "40" "45" "50" "55" "60")


echo Input

echo "FOLDER_PATH: $FOLDER_PATH"
echo $LABELD_OUT_CSV
echo $OUT_PATH_MAPs

echo $TOTAL_MAPS
echo $THRESHOLD_PORTSCAN
echo $MAP_RES_X
echo $MAP_RES_Y
echo $MAX_CHECKED_PORTS

# echo "FIXED_EXPOSURE_TIME: $FIXED_EXPOSURE_TIME"


if [ ! -d $FOLDER_PATH ]; then
echo "CREATING data temp and result folder at $FOLDER_PATH"
mkdir -p $FOLDER_PATH;
mkdir "$FOLDER_PATH/maps";
fi




#if needed start loop here---------------------------------

# 8h got 28800 seconds 
# so 1 second means necessary to get 28800 maps
#5 seconds means we cut down to 28800 / 5
# 10 seconds ... 28800 / 10
#we adjust to the following we just provide the total maps, because the traffic should always be completly checked, otherwise comparability suffers
#this obviously should be fine tuned to exact seconds, that can be read out by starting this program.


echo "WRITING AGGREGATION MAPS in loops"


MAPS_CURRENT=1
CURRENT_OUT_PATH=""


for ((i=0; i<$diff_exposure_times; i++))

do
echo "------------------------------------------------------------------------------Writing MAPS $i ---------------------------------------------------"

echo "Current Exposure Time: ${timing_list[$i]}"

#forced to take entire time range!

# echo "${timing_list[$i]}"

echo "$ALL_SECONDS / ${timing_list[$i]}" | bc

MAPS_CURRENT=`echo "$ALL_SECONDS / ${timing_list[$i]}" | bc`


# MAPS_CURRENT=""$ALL_SECONDS / ${timing_list[$i]}" | bc" 
CURRENT_OUT_PATH="${FOLDER_PATH}maps/exposure_time_${timing_list[$i]}seconds"

mkdir $CURRENT_OUT_PATH


# echo "${FOLDER_PATH}maps/exposure_time_$counter"

CURRENT_OUT_PATH="${FOLDER_PATH}maps/exposure_time_${timing_list[$i]}seconds/"

echo "CURRENT_OUT_PATH: $CURRENT_OUT_PATH"


echo "MAPS_CURRENT: $MAPS_CURRENT"

echo "Writing MAPS to path"

python3 Workflow.py $LABELD_OUT_CSV $CURRENT_OUT_PATH $MAPS_CURRENT $THRESHOLD_PORTSCAN $MAP_RES_X $MAP_RES_Y $MAX_CHECKED_PORTS 

#todo balance dataset
echo "------------------------------------------------------------------------------end $i ---------------------------------------------------"

done



# echo "CLEANUP tmp files"

# rm -r "$FOLDER_PATH/tmp";

#needed to save the configuration
cp subSeconds_aggregation.sh "$FOLDER_PATH/"