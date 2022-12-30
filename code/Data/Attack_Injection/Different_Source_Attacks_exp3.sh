

echo READING CONFIG

#need to be changed acc to system
IDT_LOC=/home/robin/workspace/MA_Thesis/ID2T/id2t
PCAP_PATH_ORG=~/data/background_traffic_14-14-30.pcap

#line is given and can be written as needed --------------------------need to be changed!
FOLDER_PATH=~/pip_workflow/9_diff_ip_attacks/exp_3_tmp/


#config the attack

# monday: start 1499082958.598308
ATTACK_START_TIMESTAMP=1499082959



IP_DST_VICTIM="9.8.7.6"
#this is the time between each attack!
FIXED_EXPOSURE_TIME=2


IP_SRC_ATTACK_list=('3.255.255.255' '11.255.255.255' '19.255.255.255' '27.255.255.255' '35.255.255.255' '43.255.255.255' '51.255.255.255' '59.255.255.255' '67.255.255.255' '75.255.255.255' '83.255.255.255' '91.255.255.255' '99.255.255.255' '107.255.255.255' '115.255.255.255' '123.255.255.255' '131.255.255.255' '139.255.255.255' '147.255.255.255' '155.255.255.255' '163.255.255.255' '171.255.255.255' '179.255.255.255' '187.255.255.255' '195.255.255.255' '203.255.255.255' '211.255.255.255' '219.255.255.255' '227.255.255.255' '235.255.255.255' '243.255.255.255' '251.255.255.255')




# THRESHOLD_PORTSCAN=1
MAP_RES_X=32
MAP_RES_Y=32
#65536
MAX_CHECKED_PORTS=65536
TOTAL_MAPS=29135 
#from each bucket
AMMOUNT_ATTACKS=32
AMMOUNT_ATTACKS_PER_IP=455
PORT_RANGE=3




# DO NOT CHANGE!

START_PORT=1
END_PORT=1000
CURRENT_PORT=""

# "${VAR1}World"
OUTPATH="${FOLDER_PATH}tmp/injected_attack.pcap"
OUT_CSV="${FOLDER_PATH}tmp/injected_attack.csv"
LABELD_OUT_CSV="${FOLDER_PATH}tmp/injected_attack_labeled.csv"
OUT_PATH_MAPs="${FOLDER_PATH}maps/"

echo Input

echo "FOLDER_PATH: $FOLDER_PATH"
echo "IDT_LOC: $IDT_LOC"
echo "PCAP_PATH_ORG : $PCAP_PATH_ORG"
echo "OUTPATH : $OUTPATH"
echo $OUT_CSV13
echo $PORTS
echo $TOTAL_MAPS
echo $THRESHOLD_PORTSCAN
echo $MAP_RES_X
echo $MAP_RES_Y
echo $MAX_CHECKED_PORTS
echo $FIXED_EXPOSURE_TIME
echo $AMMOUNT_ATTACKS
echo $AMMOUNT_ATTACKS_PER_IP





if [ ! -d $FOLDER_PATH ]; then
echo "CREATING data temp and result folder at $FOLDER_PATH"
mkdir -p $FOLDER_PATH;
mkdir "$FOLDER_PATH/tmp";
mkdir "$FOLDER_PATH/maps";
fi




PCAP_PATH=$PCAP_PATH_ORG


for ((i=0; i<$AMMOUNT_ATTACKS; i++))

do
    echo "------------------------------------------------------------------------------INJECTING Attcker $i ---------------------------------------------------"

    echo "ATTACK_START_TIMESTAMP: $ATTACK_START_TIMESTAMP"
    echo "$i"

    IP_SRC_ATTACK="${IP_SRC_ATTACK_list[$i]}"

    echo "current attack ip: "
    echo "$IP_SRC_ATTACK"


    #new loop keep ip and do 45 times with different ports!


for ((j=0; j<$AMMOUNT_ATTACKS_PER_IP; j++))
do 

# echo "$START_PORT" 
# echo "$END_PORT" 
    echo "------------------------------------------------------------------------------INJECTING attack $j ---------------------------------------------------"




CURRENT_PORT="$START_PORT-$END_PORT" 
echo $CURRENT_PORT


# echo $IDT_LOC -i $PCAP_PATH -ry -a PortscanAttack ip.src=$IP_SRC_ATTACK ip.dst=$IP_DST_VICTIM port.dst=$CURRENT_PORT inject.at-timestamp=$ATTACK_START_TIMESTAMP -o $OUTPATH

$IDT_LOC -i $PCAP_PATH -ry -a PortscanAttack ip.src=$IP_SRC_ATTACK ip.dst=$IP_DST_VICTIM port.dst=$CURRENT_PORT inject.at-timestamp=$ATTACK_START_TIMESTAMP -o $OUTPATH

START_PORT=$(($END_PORT + 1)) 
END_PORT=$(($END_PORT + PORT_RANGE + 1)) 


#updating the attack start time
ATTACK_START_TIMESTAMP=$(($ATTACK_START_TIMESTAMP + $FIXED_EXPOSURE_TIME))  

PCAP_PATH=$OUTPATH


done

START_PORT=0
END_PORT=0




done




if [ $AMMOUNT_ATTACKS == 0 ]; then
    echo "------------------------------------------------------------------------------Copying Traffic without attacks ---------------------------------------------------"
    cp $PCAP_PATH_ORG $OUTPATH;
    IP_SRC_ATTACK=-1
    IP_DST_VICTIM=-1
fi


echo CONVERTING TO CSV 

tshark -r $OUTPATH -t ud -T fields -e ip.src -e ip.dst -e tcp.srcport  -e tcp.dstport  -e udp.srcport  -e udp.dstport -e ip.proto -e frame.time -e _ws.col.Time -e frame.time_epoch -e frame.protocols -E separator=, -E quote=d, -E header=y > $OUT_CSV

echo "OUT_CSV Name from tshark: $OUT_CSV"

echo Packet LABELING

python3 ../Label_Generator/ONE_TARGET_LABEL.py $IP_DST_VICTIM $OUT_CSV $LABELD_OUT_CSV

# echo WRITING AGGREGATION MAPS

# python3 ../Detection_workflow/Workflow.py $LABELD_OUT_CSV $OUT_PATH_MAPs $TOTAL_MAPS $THRESHOLD_PORTSCAN $MAP_RES_X $MAP_RES_Y $MAX_CHECKED_PORTS

# echo "CLEANUP tmp files"

# rm -r "$FOLDER_PATH/tmp";

#needed to save the configuration
cp Different_Source_Attacks_exp3.sh "$FOLDER_PATH/"
