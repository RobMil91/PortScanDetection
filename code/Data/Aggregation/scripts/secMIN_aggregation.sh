#this pipeline is used to work on a labeled csv created by the attack injection labeling generator
echo READING CONFIG

#CONFIGURE:
#INPUT
LABELD_CSV=$1
#OUTPUTFOLDER
FOLDER_PATH=~/sec_Min_Aggregation/

ALL_SECONDS=933

MAP_THRESHOLD_PORTSCAN=1
#RESOLUTION
MAP_RES_X=32
MAP_RES_Y=32
#65536
#Given to decide the range of the y-axis in port totals -> std is all ports, if 1000 ports all above ports are ignored.
MAX_CHECKED_PORTS=65536
# FIXED_EXPOSURE_TIME=60

diff_exposure_times=13
timing_list=("1" "5" "10" "15" "20" "25" "30" "35" "40" "45" "50" "55" "60")

echo Input
echo "---LOG: Aggregation OUTPUT PATH: $FOLDER_PATH"
echo "---LOG: INPUT: $LABELD_CSV"

echo "---LOG: Out Maps Specified: $FOLDER_PATH"
echo "---LOG: Map Threshold: $MAP_THRESHOLD_PORTSCAN"
echo "---LOG: MAX_CHECKED_PORTS: $MAX_CHECKED_PORTS"

if [ ! -d $FOLDER_PATH ]; then
    echo "CREATING data temp and result folder at $FOLDER_PATH"
    mkdir -p $FOLDER_PATH
    mkdir "$FOLDER_PATH/maps"
fi

echo "WRITING AGGREGATION MAPS"

MAPS_CURRENT=1
CURRENT_OUT_PATH=""

for ((i = 0; i < $diff_exposure_times; i++)); do
    echo "------------------------------------------------------------------------------Writing MAPS $i ---------------------------------------------------"

    echo "Current Exposure Time: ${timing_list[$i]}"
    echo "Total Maps Created: "
    echo "$ALL_SECONDS / ${timing_list[$i]}" | bc

    # 8h got 28800 seconds
    # so 1 second means necessary to get 28800 maps
    # 5 seconds means we cut down to 28800 / 5
    # 10 seconds ... 28800 / 10
    # This means always the complete traffic is used for aggregation relativ to the amount of seconds given
    MAPS_CURRENT=$(echo "$ALL_SECONDS / ${timing_list[$i]}" | bc)

    # MAPS_CURRENT=""$ALL_SECONDS / ${timing_list[$i]}" | bc"
    CURRENT_OUT_PATH="${FOLDER_PATH}maps/exposure_time_${timing_list[$i]}seconds"
    mkdir $CURRENT_OUT_PATH
    CURRENT_OUT_PATH="${FOLDER_PATH}maps/exposure_time_${timing_list[$i]}seconds/"

    echo "Writing MAPS to path"

    echo "../build_maps.py $LABELD_CSV $CURRENT_OUT_PATH $MAPS_CURRENT $THRESHOLD_PORTSCAN $MAP_RES_X $MAP_RES_Y $MAX_CHECKED_PORTS "

    python3 ../build_maps.py $LABELD_CSV $CURRENT_OUT_PATH $MAPS_CURRENT $MAP_THRESHOLD_PORTSCAN $MAP_RES_X $MAP_RES_Y $MAX_CHECKED_PORTS

    echo "---LOG: Aggregated CSV $LABELD_CSV to file $CURRENT_OUT_PATH ; $MAPS_CURRENT aggregation maps got created; Threshold is: $MAP_THRESHOLD_PORTSCAN; Resolution is: $MAP_RES_X; $MAX_CHECKED_PORTS ports got checked"

    echo "------------------------------------------------------------------------------end $i ---------------------------------------------------"
done

#needed to save the configuration
cp secMIN_aggregation.sh "$FOLDER_PATH/"
