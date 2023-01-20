echo READING CONFIG
#need to be changed detection to system
#line is given and can be written as needed --------------------------need to be changed!
OUTPUT_FOLDER_PATH=~/workspace/data/learnPlot/
IDT_LOC=
PCAP_PATH_ORG=~/workspace/data/control_exp/portscan_2_min_20221017-155525.pcap

#config the attack
ATTACK_START_TIMESTAMP=1499449381
AMMOUNT_ATTACKS=1
AMMOUNT_ATTACKS_PER_IP=4
START_PORT=1
END_PORT=1000
PORT_RANGE=1000
#End_Port=65535
IP_DST_VICTIM="9.8.7.6"
#time between each attack!
NO_Attack_Timer=30

#get general info
capinfos $PCAP_PATH_ORG | grep "First packet time:"
tshark -r $PCAP_PATH_ORG -T fields -e frame.time_epoch >tmp.csv
echo "Measured Start of PCAP FILE:"
head -1 tmp.csv
rm tmp.csv

echo "---LOG: Start Time used: $ATTACK_START_TIMESTAMP"

IP_SRC_ATTACK_list=('3.255.255.255' '11.255.255.255' '19.255.255.255' '27.255.255.255' '35.255.255.255' '43.255.255.255' '51.255.255.255' '59.255.255.255' '67.255.255.255' '75.255.255.255' '83.255.255.255' '91.255.255.255' '99.255.255.255' '107.255.255.255' '115.255.255.255' '123.255.255.255' '131.255.255.255' '139.255.255.255' '147.255.255.255' '155.255.255.255' '163.255.255.255' '171.255.255.255' '179.255.255.255' '187.255.255.255' '195.255.255.255' '203.255.255.255' '211.255.255.255' '219.255.255.255' '227.255.255.255' '235.255.255.255' '243.255.255.255' '251.255.255.255')

OUTPATH="${FOLDER_PATH}tmp/injected_attack.pcap"
OUT_CSV="${FOLDER_PATH}tmp/injected_attack.csv"
LABELD_OUT_CSV="${FOLDER_PATH}tmp/injected_attack_labeled.csv"
OUT_PATH_MAPs="${FOLDER_PATH}maps/"

#needed to generate folder structure
if [ ! -d $OUTPUT_FOLDER_PATH ]; then
    echo "CREATING data temp and result folder at $OUTPUT_FOLDER_PATH"
    mkdir -p $OUTPUT_FOLDER_PATH
    mkdir "$OUTPUT_FOLDER_PATH/tmp"
fi

PCAP_PATH=$PCAP_PATH_ORG

for ((j = 0; j < $AMMOUNT_ATTACKS_PER_IP; j++)); do

    echo "------------------------------------------------------------------------------INJECTING attack $j ---------------------------------------------------"

    CURRENT_PORTs="$START_PORT-$END_PORT"

    IP_SRC_ATTACK="${IP_SRC_ATTACK_list[$i]}"

    echo "$IDT_LOC -i $PCAP_PATH -a PortscanAttack ip.src=$IP_SRC_ATTACK ip.dst=$IP_DST_VICTIM port.dst="$CURRENT_PORTs" inject.at-timestamp=$ATTACK_START_TIMESTAMP -o $OUTPATH"

    $IDT_LOC -i $PCAP_PATH -a PortscanAttack ip.src=$IP_SRC_ATTACK ip.dst=$IP_DST_VICTIM port.dst="$CURRENT_PORTs" inject.at-timestamp=$ATTACK_START_TIMESTAMP -o $OUTPATH

    PCAP_PATH=$OUTPATH

    START_PORT=$(($END_PORT + 1))
    END_PORT=$(($END_PORT + PORT_RANGE + 1))

    for ((i = 0; i < $AMMOUNT_ATTACKS; i++)); do
        echo "------------------------------------------------------------------------------INJECTING Attacker $i ---------------------------------------------------"

        IP_SRC_ATTACK="${IP_SRC_ATTACK_list[$i]}"
        ATTACK_START_TIMESTAMP=$(($ATTACK_START_TIMESTAMP + $NO_Attack_Timer))
        echo "---LOG: Injected Attack in $PCAP_PATH from $IP_SRC_ATTACK to $IP_DST_VICTIM with ports $CURRENT_PORTs at timestamp: $ATTACK_START_TIMESTAMP written to: $OUTPATH"

    done

done

if [ $AMMOUNT_ATTACKS == 0 ]; then
    echo "------------------------------------------------------------------------------Copying Traffic without attacks ---------------------------------------------------"
    cp $PCAP_PATH_ORG $OUTPATH
    IP_SRC_ATTACK=-1
    IP_DST_VICTIM=-1
fi

echo CONVERTING TO CSV
tshark -r $OUTPATH -t ud -T fields -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -e ip.proto -e _ws.col.Time -e frame.time_epoch -e frame.protocols -E separator=, -E quote=d, -E header=y >$OUT_CSV

echo "OUT_CSV Name from tshark: $OUT_CSV"
python3 ../Label_Generator/ONE_TARGET_LABEL.py $IP_DST_VICTIM $OUT_CSV $LABELD_OUT_CSV
echo "LOG: labeled all packets in $OUT_CSV that got destination $IP_DST_VICTIM are labeled 1 (port scan), written to $LABELD_OUT_CSV"

#save the configuration
cp injectRange1000.sh "$FOLDER_PATH/"
