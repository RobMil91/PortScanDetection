workflow

1. take normal pcap file

2. use IDT2 to inject attack packets
./id2t -i ~/workspace/MA_Thesis/datasets/pcap_lab/clean/test_pcap_14cet_cic.pcap -a PortscanAttack ip.src=192.168.111.111 inject.at-timestamp=1499428783 port.dst="1-65535" ip.dst=192.168.111.112 -o ~/workspace/MA_Thesis/datasets/pcap_lab/clean


3. Label with packet sequence

3.1 csv from pcap 
 tshark -r injected_attack.pcap -t ud -T fields -e ip.src -e ip.dst -e tcp.srcport  -e tcp.dstport  -e udp.srcport  -e udp.dstport -e ip.proto -e frame.time -e _ws.col.Time -e frame.time_epoch -e frame.protocols -E separator=, -E quote=d, -E header=y > labeled_trace.csv

3.2 label the csv 

python3 Packet_Sequence_Label_Data_Generator.py 192.168.111.111 192.168.111.112 /home/robin/workspace/MA_Thesis/datasets/pcap_lab/clean/labeled_trace.csv /home/robin/workspace/MA_Thesis/datasets/pcap_lab/clean/labeled_trace_traffic.csv

4. create maps and print
python3 Workflow.py /home/robin/workspace/MA_Thesis/datasets/pcap_lab/clean/labeled_trace_traffic.csv /home/robin/workspace/MA_Thesis/datasets/pcap_lab/clean/image1.png 10 10

