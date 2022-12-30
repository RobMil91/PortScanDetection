#this pipeline is used to work on a labeled csv created by the attack injection labeling generator
echo READING CONFIG

#CONFIGURE:
#INPUT
LABELD_CSV=$1
#OUTPUTFOLDER
FOLDER_PATH=$2

ALL_SECONDS=$3

MAP_THRESHOLD_PORTSCAN=$4
#RESOLUTION
MAP_RES_X=$5
MAP_RES_Y=$5
#65536
#Given to decide the range of the y-axis in port totals -> std is all ports, if 1000 ports all above ports are ignored.
MAX_CHECKED_PORTS=$6
# FIXED_EXPOSURE_TIME=60

diff_exposure_times=22
timing_list=("0.1" "0.2" "0.3" "0.4" "0.5" "0.6" "0.7" "0.8" "0.9" "1" "5" "10" "15" "20" "25" "30" "35" "40" "45" "50" "55" "60")

echo Input
echo "---LOG: Aggregation OUTPUT PATH: $FOLDER_PATH"
echo "---LOG: INPUT: $LABELD_CSV"

echo "---LOG: Out Maps Specified: $FOLDER_PATH"
echo "---LOG: Map Threshold: $MAP_THRESHOLD_PORTSCAN"
echo "---LOG: MAX_CHECKED_PORTS: $MAX_CHECKED_PORTS"
echo "---LOG: Different Exposure times: $diff_exposure_times"
echo "---LOG: timing_list: $timing_list"




mkdir "$FOLDER_PATH/maps";



echo "WRITING AGGREGATION MAPS"


MAPS_CURRENT=1
CURRENT_OUT_PATH=""

for ((i=0; i<$diff_exposure_times; i++))

do
echo "------------------------------------------------------------------------------Writing MAPS $i ---------------------------------------------------"

echo "Current Exposure Time: ${timing_list[$i]}"
echo "Total Maps Created: "
echo "$ALL_SECONDS / ${timing_list[$i]}" | bc

# 8h got 28800 seconds 
# so 1 second means necessary to get 28800 maps
# 5 seconds means we cut down to 28800 / 5
# 10 seconds ... 28800 / 10
# This means always the complete traffic is used for aggregation relativ to the amount of seconds given
MAPS_CURRENT=`echo "$ALL_SECONDS / ${timing_list[$i]}" | bc`

# MAPS_CURRENT=""$ALL_SECONDS / ${timing_list[$i]}" | bc" 
CURRENT_OUT_PATH="${FOLDER_PATH}maps/exposure_time_${timing_list[$i]}seconds"
mkdir $CURRENT_OUT_PATH
CURRENT_OUT_PATH="${FOLDER_PATH}maps/exposure_time_${timing_list[$i]}seconds/"

echo "Writing MAPS to path"

echo "../build_maps.py $LABELD_CSV $CURRENT_OUT_PATH $MAPS_CURRENT $THRESHOLD_PORTSCAN $MAP_RES_X $MAP_RES_Y $MAX_CHECKED_PORTS "

python3 ../Data/Aggregation/build_maps.py $LABELD_CSV $CURRENT_OUT_PATH $MAPS_CURRENT $MAP_THRESHOLD_PORTSCAN $MAP_RES_X $MAP_RES_Y $MAX_CHECKED_PORTS 

echo "---LOG: Aggregated CSV $LABELD_CSV to file $CURRENT_OUT_PATH ; $MAPS_CURRENT aggregation maps got created; Threshold is: $MAP_THRESHOLD_PORTSCAN; Resolution is: $MAP_RES_X; $MAX_CHECKED_PORTS ports got checked"

echo "------------------------------------------------------------------------------end $i ---------------------------------------------------"
done

#needed to save the configuration
# cp secMIN_aggregation.sh "$FOLDER_PATH/"