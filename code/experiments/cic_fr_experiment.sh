
# Configuration:
PCAP_Location=$1
IDT_LOC=~/workspace/MA_Thesis/ID2T/id2t


#------------------------------------------------------------config  Labeling:

victim="192.168.10.50"
attacker="172.16.0.1"

#------------------------------------------------------------config  aggregation:

Complete_Seconds_in_CSV=2400

MAP_THRESHOLD_PORTSCAN=1
#RESOLUTION
MAP_RESOULTION=32

#65536
#Given to decide the range of the y-axis in port totals -> std is all ports, if 1000 ports all above ports are ignored.
MAX_CHECKED_PORTS=65536

#----------------------------------------------------- config CNN classification:

aggr_maps_path=~/PortScanDetectionExperiments/CICExperiments/maps/
results_path=~/PortScanDetectionExperiments/CICExperiments/results/

Rounds=2

mkdir ~/PortScanDetectionExperiments/
mkdir ~/PortScanDetectionExperiments/CICExperiments/


#convert to CSV

# echo CONVERTING TO CSV 
tshark -r $PCAP_Location -t ud -T fields -e ip.src -e ip.dst -e tcp.dstport -e frame.time_epoch -E separator=, -E quote=d, -E header=y > ~/PortScanDetectionExperiments/CICExperiments/tmp_cic.csv

#label victim to target
python3 ../Data/Label_Generator/Victim_and_Attacker_labeling.py $victim $attacker ~/PortScanDetectionExperiments/CICExperiments/tmp_cic.csv ~/PortScanDetectionExperiments/CICExperiments/v_a_labeled_cic.csv > ~/PortScanDetectionExperiments/labelLog.txt


# echo "------------------------------------------------Labeling Complete--------------------------------------"


bash parameter_scripts/aggregateSTD.sh ~/PortScanDetectionExperiments/CICExperiments/v_a_labeled_cic.csv ~/PortScanDetectionExperiments/CICExperiments/ $Complete_Seconds_in_CSV $MAP_THRESHOLD_PORTSCAN $MAP_RESOULTION $MAX_CHECKED_PORTS > ~/PortScanDetectionExperiments/aggregationLog.txt

# echo "------------------------------------------------Aggregation Complete--------------------------------------"


#backup unbalance

cp -r ~/PortScanDetectionExperiments/CICExperiments/maps/ ~/PortScanDetectionExperiments/CICExperiments/unbal_maps/


echo "------------------------------------------------Backup Unbalanced Maps Complete--------------------------------------"


python3 ../tools/balance_experiment.py ~/PortScanDetectionExperiments/CICExperiments/maps/


echo "------------------------------------------------Balancing Complete--------------------------------------"


bash parameter_scripts/runDetectionMultiple.sh ~/PortScanDetectionExperiments/CICExperiments/maps/exposure_time_1seconds/ $results_path $Rounds > ~/PortScanDetectionExperiments/detectionLog.txt


echo "------------------------------------------Folder with histories for each run is in: $results_path--------------"

