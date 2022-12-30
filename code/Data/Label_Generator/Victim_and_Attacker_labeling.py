import pandas as pandas
from label_utils import *
import ipaddress as ipaddress

import sys


#this modul is given to calculate with exactly one target, all traffic that goes to the target is expected to be port scan.
#this only works with an arbitrary IP address for a victim that is only used in the context of the attack.
if(str(sys.argv[1]) == "--help"):
    print("argv1 == victim ip e.g. 192.168.111.115")
    print("argv2 == UNLABELED TRACE DATA PATH")
    print("argv3 == OUTPUT PATH FOR GENERATED Labeled TRACE")

#program arguments
victim = str(sys.argv[1])
attacker = str(sys.argv[2])
unlabeled_trace_dataframe = pandas.read_csv(str(sys.argv[3]))
#path to put the labeled data
generated_csv_path = str(sys.argv[4])

print("---LOG: Input head: ")
print(unlabeled_trace_dataframe.head())

generate_labels_src_to_dst(unlabeled_trace_dataframe, "ip.src", "ip.dst", attacker, victim)

#drop lines with no dst_port && no src ip
unlabeled_trace_dataframe = unlabeled_trace_dataframe.dropna(subset=["ip.src"])

unlabeled_trace_dataframe.dropna(subset=["tcp.dstport"])
unlabeled_trace_dataframe.dropna(subset=["tcp.dstport"])
indexes = unlabeled_trace_dataframe[ (unlabeled_trace_dataframe['tcp.dstport'].isnull())].index
unlabeled_trace_dataframe.drop(indexes, inplace = True)

index_names = unlabeled_trace_dataframe[ (unlabeled_trace_dataframe["ip.src"].str.contains(","))].index
unlabeled_trace_dataframe.drop(index_names, inplace = True)


#needed to convert ip source to decimal
unlabeled_trace_dataframe['ip.src'] = unlabeled_trace_dataframe['ip.src'].apply(lambda row_value : int(ipaddress.IPv4Address(row_value)))
#used to convert port float to int.
unlabeled_trace_dataframe['tcp.dstport'] = unlabeled_trace_dataframe['tcp.dstport'].apply(lambda row_value : (convert_port_to_int(row_value)))

print("---LOG: General Infos about output dataframe")
print_general_info(unlabeled_trace_dataframe)
unlabeled_trace_dataframe.to_csv(generated_csv_path)

print("---LOG: successful written labeled csv to path: " + str(generated_csv_path))