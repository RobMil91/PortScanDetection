## What is it?
This project contains a Detection Approach for Portscans with Machine Learning (ML). The process is:

- Network Traffic (PCAP File)
- format to csv ( & adjust Packet attributes)
- build Maps ( 2-Dimensional Representation of a defined Time Window of Network Traffic)
    - The Maps use Axes like Source IP Adress and Destination Port to display the Network Traffic
- Maps are labeled
- Keras ML CNN trains supervised and predicts based on the trained Model
- The created Histories from the Testing/Training Phase can be plotted (metrics like accuracy, precision, recall are used)

# Workflow

1. genereate  pcap file
(can be written with wireshark/tshark or downloaded from benchmark sources -> should include port scan behaviour with known attacker!)

OPTIONAL: 2. use IDT2 to inject attack packets (necessary if no attacker is within the pcap)
./id2t -i ~/workspace/MA_Thesis/datasets/pcap_lab/clean/test_pcap_14cet_cic.pcap -a PortscanAttack ip.src=192.168.111.111 inject.at-timestamp=1499428783 port.dst="1-65535" ip.dst=192.168.111.112 -o ~/workspace/MA_Thesis/datasets/pcap_lab/clean

3. Label the PCAP File and Format Columns -> csv File

    3.1 csv from pcap 
    tshark -r injected_attack.pcap -t ud -T fields -e ip.src -e ip.dst -e tcp.srcport  -e tcp.dstport  -e udp.srcport  -e udp.dstport -e ip.proto -e    frame.time -e _ws.col.Time -e frame.time_epoch -e frame.protocols -E separator=, -E quote=d, -E header=y > unlabeled_trace.csv


    3.2 label the csv 
    python3 Data/Label_Generator/ONE_TARGET_LABEL.py 192.168.0.5 unlabeled_trace.csv aggregation_ready_trace.csv



4. run Detection on maps Folder

bash run_detection.sh aggregation_ready_trace.csv



--------------------------------------------------------------

##Tool kit example commands:


Example Commands:

#shows the amount of labeled maps
pyhon3 analyzse_aggr_maps_folder.py ~/pip_workflow/experiment2/results/

#balances the aggregation maps
python3 reduce_benign_maps.py ~/pip_workflow/experiment5/maps/expeX/

#plots from multiple histories to show differences in metric over different maps attributes
python3 plot_from_histories.py ~/pip_workflow/experiment1/result_histories/ 100 ~/pip_workflow/experiment1/result_histories/metrics/ 'accuracy'

#display one history
python3 plot_1_history.py ~/pip_workflow/experiment1/results/round1.pkl ~/pip_workflow/experiment1/results/metrics/

python3 check_history_columns.py ~/pip_workflow/experiment1/result_histories/ROUND_10.pkl 

#scan csv file for an attack
python3 FIND_ATTACK.py  "110.110.110.110" "12.12.12.12" 1 1 "~/pip_workflow/experiment8/tmp/injected_attack.csv" 

#figure out time of pcap file
./get_start_and_end.sh ~/data/background_traffic_14-14-30.pcap

#train model on aggregation map folder, parameters are : <folder location> <dimensions of maps> <epochs> <batchsize> <validation split> <outputPath> <name>
# if validation split > 0.0 --> the result folder will contain the model plus the histories created by the model testing phase
python3 train_model.py ~/pip_workflow/9_diff_ip_attacks/maps/ 32 100 128 0.0 ~/pip_workflow/9_diff_ip_attacks/results/ round2

#time measure experiment, (how long the classification of an aggregation map takes)
python3 test_model_prediction_time.py ~/experiment_data/time_pred_experiment/loadable_model/ROUND_1_model/ ~/experiment_data/time_pred_experiment/one_aggr_map/ 32 100 128 0.1 ~/experiment_data/time_pred_experiment/loadable_model time_test


