workflow

1. take  pcap file
(can be written with wireshark/tshark or downloaded from benchmark sources -> should include port scan behaviour with known attacker!)

2. use IDT2 to inject attack packets
./id2t -i ~/workspace/MA_Thesis/datasets/pcap_lab/clean/test_pcap_14cet_cic.pcap -a PortscanAttack ip.src=192.168.111.111 inject.at-timestamp=1499428783 port.dst="1-65535" ip.dst=192.168.111.112 -o ~/workspace/MA_Thesis/datasets/pcap_lab/clean

3. Label with packet sequence

    3.1 csv from pcap 
    tshark -r injected_attack.pcap -t ud -T fields -e ip.src -e ip.dst -e tcp.srcport  -e tcp.dstport  -e udp.srcport  -e udp.dstport -e ip.proto -e frame.time -e _ws.col.Time -e frame.time_epoch -e frame.protocols -E separator=, -E quote=d, -E header=y > unlabeled_trace.csv


    3.2 label the csv 
    python3 Data/Label_Generator/ONE_TARGET_LABEL.py 192.168.0.5 unlabeled_trace.csv aggregation_ready_trace.csv


#this includes the process of aggregation, 
#in succsession a folder structure is created, 
#this includes human readable log files for aggregation and detection 
# an example plot is created!

4. run Detection on maps Folder

bash run_detection.sh aggregation_ready_trace.csv

