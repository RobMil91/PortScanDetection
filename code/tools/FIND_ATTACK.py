
import pandas as pandas

#debug tool to identify an attack within a csv packet trace, it also highlights properties of the attack (or given ip)


import sys

# input -> normal_pcap
#example command:
# tshark -r chunk_00076_20170707201608.pcap -t ud -T fields -e ip.src -e ip.dst -e tcp.srcport  -e tcp.dstport  -e udp.srcport  -e udp.dstport -e ip.proto -e frame.time -e _ws.col.Time -e frame.time_epoch -e frame.protocols -E separator=, -E quote=d, -E header=y > portscan_from_20-15_CET.csv


attacker = str(sys.argv[1])
victim = str(sys.argv[2])

STEPS = int(str(sys.argv[3]))

STEP_SIZE = int(str(sys.argv[4]))

unlabeled_trace_dataframe = pandas.read_csv(str(sys.argv[5]))

print("HEAD:")
print(unlabeled_trace_dataframe.head())

print("Attacker: " +  str(attacker))
print("Victim: " +  str(victim))

df = unlabeled_trace_dataframe

attack_traffic_df = df.loc[(df['ip.src'] == attacker) & (df['ip.dst'] == victim)]


print(attack_traffic_df)


if( attack_traffic_df.empty):
    print("no attack found!")
    quit()

end = attack_traffic_df.iloc[-1]

rows = len(attack_traffic_df.index)



print("------------------------------------------------------------------------------------------------------------")
print("start :")
print(attack_traffic_df.iloc[0])

print("------------------------------------------------------------------------------------------------------------")

for i in range(STEPS):

    print("------------------------------------------------------------------------------------------------------------")

    index = (i + 1) *  STEP_SIZE

    print(attack_traffic_df.iloc[index])
    print("------------------------------------------------------------------------------------------------------------")



print("------------------------------------------------------------------------------------------------------------")

print("end :")

print(attack_traffic_df.iloc[-1])


print("------------------------------------------------------------------------------------------------------------")

print("short start to end UTC: ")
print(attack_traffic_df.iloc[0]["frame.time_epoch"])
print(attack_traffic_df.iloc[-1]["frame.time_epoch"])

print("estimated Port Ranges overall max to min")
print(attack_traffic_df["tcp.dstport"].max())
print(attack_traffic_df["tcp.dstport"].min())


