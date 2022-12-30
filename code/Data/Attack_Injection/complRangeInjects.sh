
echo READING CONFIG
#need to be changed detection to system
#line is given and can be written as needed --------------------------need to be changed!
OUTPUT_FOLDER_PATH=~/workspace/data/LEARN10/
IDT_LOC=/home/robin/workspace/MA_Thesis/ID2T/id2t
PCAP_PATH_ORG=~/workspace/MA_Thesis/datasets/pcaps/portscan_10_min.pcap

#------------------------------------------------------------config the attack here:
ATTACK_START_TIMESTAMP=1499443200
AMMOUNT_ATTACKS=4
AMMOUNT_ATTACKS_PER_IP=1
Start_Port=1
End_Port=500
#End_Port=65535
IP_DST_VICTIM="9.8.7.6"
#time between each attack!
NO_Attack_Timer=120


echo "---LOG: Input is file at $PCAP_PATH_ORG"
echo "---LOG: Destination folder is $OUTPUT_FOLDER_PATH"

#get general info
capinfos $PCAP_PATH_ORG | grep "First packet time:"
tshark -r $PCAP_PATH_ORG -T fields -e frame.time_epoch -c 1 > tmp.csv
echo "Measured Start of PCAP FILE:"
head -1 tmp.csv 
rm tmp.csv

echo "---LOG: Start Time used: $ATTACK_START_TIMESTAMP"

IP_SRC_ATTACK_list=('3.255.255.255' '11.255.255.255' '19.255.255.255' '27.255.255.255' '35.255.255.255' '43.255.255.255' '51.255.255.255' '59.255.255.255' '67.255.255.255' '75.255.255.255' '83.255.255.255' '91.255.255.255' '99.255.255.255' '107.255.255.255' '115.255.255.255' '123.255.255.255' '131.255.255.255' '139.255.255.255' '147.255.255.255' '155.255.255.255' '163.255.255.255' '171.255.255.255' '179.255.255.255' '187.255.255.255' '195.255.255.255' '203.255.255.255' '211.255.255.255' '219.255.255.255' '227.255.255.255' '235.255.255.255' '243.255.255.255' '251.255.255.255')

OUTPATH="${OUTPUT_FOLDER_PATH}tmp/injected_attack.pcap"
OUT_CSV="${OUTPUT_FOLDER_PATH}tmp/injected_attack.csv"
LABELD_OUT_CSV="${OUTPUT_FOLDER_PATH}tmp/injected_attack_labeled.csv"

#needed to generate folder structure
if [ ! -d $OUTPUT_FOLDER_PATH ]; then
echo "CREATING data temp and result folder at $OUTPUT_FOLDER_PATH"
mkdir -p $OUTPUT_FOLDER_PATH;
mkdir "$OUTPUT_FOLDER_PATH/tmp";
fi


PCAP_PATH=$PCAP_PATH_ORG

CURRENT_PORTs="$Start_Port-$End_Port"

for ((i=0; i<$AMMOUNT_ATTACKS; i++))

do
    echo "------------------------------------------------------------------------------INJECTING Attacker $i ---------------------------------------------------"

    IP_SRC_ATTACK="${IP_SRC_ATTACK_list[$i]}"

for ((j=0; j<$AMMOUNT_ATTACKS_PER_IP; j++))
do 

    echo "------------------------------------------------------------------------------INJECTING attack $j ---------------------------------------------------"

$IDT_LOC -i $PCAP_PATH -a PortscanAttack ip.src=$IP_SRC_ATTACK ip.dst=$IP_DST_VICTIM port.dst="$CURRENT_PORTs" inject.at-timestamp=$ATTACK_START_TIMESTAMP -o $OUTPATH

echo "---LOG: Injected Attack in $PCAP_PATH from $IP_SRC_ATTACK to $IP_DST_VICTIM with ports $CURRENT_PORTs at timestamp: $ATTACK_START_TIMESTAMP written to: $OUTPATH"

ATTACK_START_TIMESTAMP=$(($ATTACK_START_TIMESTAMP + $NO_Attack_Timer))  
PCAP_PATH=$OUTPATH

done

done

if [ $AMMOUNT_ATTACKS == 0 ]; then
    echo "------------------------------------------------------------------------------Copying Traffic without attacks ---------------------------------------------------"
    cp $PCAP_PATH_ORG $OUTPATH;
    IP_SRC_ATTACK=-1
    IP_DST_VICTIM=-1
fi

echo CONVERTING TO CSV 
tshark -r $OUTPATH -t ud -T fields -e ip.src -e ip.dst -e tcp.dstport -e frame.time_epoch -E separator=, -E quote=d, -E header=y > $OUT_CSV

echo "OUT_CSV Name from tshark: $OUT_CSV"
python3 ../Label_Generator/ONE_TARGET_LABEL.py $IP_DST_VICTIM $OUT_CSV $LABELD_OUT_CSV
echo "LOG: labeled all packets in $OUT_CSV that got destination $IP_DST_VICTIM are labeled 1 (port scan), written to $LABELD_OUT_CSV"

#save the configuration
cp complRangeInjects.sh "$OUTPUT_FOLDER_PATH/"
