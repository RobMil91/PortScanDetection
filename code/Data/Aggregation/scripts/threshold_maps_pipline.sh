

#this pipeline is used to work on a labeled csv!
echo READING CONFIG

#input for the pipeline
LABELD_OUT_CSV=~/workspace/data/experiment1/injected_attack_labeled.csv

ALL_SECONDS=900

FOLDER_PATH=~/workspace/data/experiment1/1threshold_diff/

MAP_RES_X=32
#this is removed cause it is quadratic resolution 

#65536
MAX_CHECKED_PORTS=2000
# FIXED_EXPOSURE_TIME=60



# diff_exposure_times=1


echo Input

echo "FOLDER_PATH: $FOLDER_PATH"
echo $LABELD_OUT_CSV
echo $OUT_PATH_MAPs

echo $TOTAL_MAPS
echo $THRESHOLD_PORTSCAN
echo $MAP_RES_X
echo $MAP_RES_Y
echo $MAX_CHECKED_PORTS

echo "FIXED_EXPOSURE_TIME: $FIXED_EXPOSURE_TIME"


if [ ! -d $FOLDER_PATH ]; then
echo "CREATING data temp and result folder at $FOLDER_PATH"
mkdir -p $FOLDER_PATH;
mkdir "$FOLDER_PATH/maps";
fi



diff_thresholds=12

threshold_list=("1" "5" "10"
 "25" "50" "75" 
 "100" "200" "400" 
 "600" "800" "1000")


#if needed start loop here---------------------------------

# 8h got 28800 seconds 
# so 1 second means necessary to get 28800 maps
#5 seconds means we cut down to 28800 / 5
# 10 seconds ... 28800 / 10
#we adjust to the following we just provide the total maps, because the traffic should always be completly checked, otherwise comparability suffers
#this obviously should be fine tuned to exact seconds, that can be read out by starting this program.


echo "WRITING AGGREGATION MAPS in loops"


MAPS_CURRENT=$ALL_SECONDS
CURRENT_OUT_PATH=""


for ((i=0; i<$diff_thresholds; i++))

do
echo "------------------------------------------------------------------------------Writing MAPS $i ---------------------------------------------------"

#forced to take entire time range!

echo "threshold current"
echo "${threshold_list[$i]}"

CURRENT_OUT_PATH="${FOLDER_PATH}maps/threshold_${threshold_list[$i]}"

mkdir $CURRENT_OUT_PATH



CURRENT_OUT_PATH="${FOLDER_PATH}maps/threshold_${threshold_list[$i]}/"

echo "CURRENT_OUT_PATH: $CURRENT_OUT_PATH"



THRESHOLD_PORTSCAN="${threshold_list[$i]}"

echo "----------------------Writing MAPS to path!----------------------------------------------------------"


python3 Workflow.py $LABELD_OUT_CSV $CURRENT_OUT_PATH $MAPS_CURRENT $THRESHOLD_PORTSCAN $MAP_RES_X $MAP_RES_X $MAX_CHECKED_PORTS 

echo "------------------------------------------------------------------------------end $i ---------------------------------------------------"

done



# echo "CLEANUP tmp files"

# rm -r "$FOLDER_PATH/tmp";

#needed to save the configuration
cp threshold_maps_pipline.sh "$FOLDER_PATH/"