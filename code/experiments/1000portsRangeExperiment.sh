

# Configuration:
PCAP_Location=$1
IDT_LOC=~/workspace/MA_Thesis/ID2T/id2t

#get no attack pcap (monday CIC)



#inject attacks from 32 source IP address buckets




PCAP_PATH_ORG=~/workspace/data/control_exp/portscan_2_min.pcap





#------------------------------------------------------------config  aggregation:

Complete_Seconds_in_CSV=900

MAP_THRESHOLD_PORTSCAN=1
#RESOLUTION
MAP_RESOULTION=32

#65536
#Given to decide the range of the y-axis in port totals -> std is all ports, if 1000 ports all above ports are ignored.
MAX_CHECKED_PORTS=65536



#----------------------------------------------------- config CNN classification:

aggr_maps_path=~/PortScanDetectionExperiments/ExposureTimeExperiments/maps/
results_path=~/PortScanDetectionExperiments/ExposureTimeExperiments/results/
# NAME="ROUND_1"
# RESOLUTION=32
# EPOCHS=100
# BATCH_SIZE=128
# VALIDATION_SPLIT=0.2




mkdir ~/PortScanDetectionExperiments/

# echo "--LOG: $Experiment_Folder $IDT_LOC $PCAP_Location $ATTACK_START_TIMESTAMP $Buckets_that_PortScan $AMMOUNT_ATTACKS_PER_Attacker $Start_Port $End_Port "$VICTIM_Node_IP" $NO_Attack_Timer > ~/PortScanDetectionExperiments/attackInjectionLog.txt"

bash parameter_scripts/inject_32_Attacks.sh $Experiment_Folder $IDT_LOC $PCAP_Location $ATTACK_START_TIMESTAMP $Buckets_that_PortScan $AMMOUNT_ATTACKS_PER_Attacker $Start_Port $End_Port "$VICTIM_Node_IP" $NO_Attack_Timer > ~/PortScanDetectionExperiments/attackInjectionLog.txt

# echo "--LOG: $Experiment_Folder $IDT_LOC $PCAP_Location $ATTACK_START_TIMESTAMP $Buckets_that_PortScan $AMMOUNT_ATTACKS_PER_Attacker $Start_Port $End_Port "$VICTIM_Node_IP" $NO_Attack_Timer > ~/PortScanDetectionExperiments/attackInjectionLog.txt"

bash parameter_scripts/aggregateSeconds.sh ~/PortScanDetectionExperiments/ExposureTimeExperiments/tmp/injected_attack_labeled.csv ~/PortScanDetectionExperiments/ExposureTimeExperiments/ $Complete_Seconds_in_CSV $MAP_THRESHOLD_PORTSCAN $MAP_RESOULTION $MAX_CHECKED_PORTS > ~/PortScanDetectionExperiments/aggregationLog.txt

echo "------------------------------------------------Aggregation Complete--------------------------------------"

../tools/balance_experiment.py ~/PortScanDetectionExperiments/ExposureTimeExperiments/maps/


echo "------------------------------------------------Balancing Complete--------------------------------------"


bash parameter_scripts/classify.sh $aggr_maps_path $results_path > ~/PortScanDetectionExperiments/detectionLog.txt


echo "------------------------------------------------Detection Complete--------------------------------------"

python3 ../Plotting/subplots_exp_time.py $aggr_maps_path

echo "------------------------------------------------Plotting Complete--------------------------------------"























#aggregation on exposure times from 0.1 to 0.9 seconds

#aggregation on exposure times from 1 second to 60 seconds


#balance the experiments folders


#classifiy all folders


#plot results of classifying 