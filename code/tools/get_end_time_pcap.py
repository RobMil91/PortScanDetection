import sys
import pandas as pd

#debug tool, to identify start and end time of a given pcap file (packet trace file)
#caution this might be time and ram consuming depending on the pcap file size

CSV_PATH =  str(sys.argv[1])

df = pd.read_csv(CSV_PATH)



start_time_epoch = df['frame.time_epoch'].iloc[0]

end_time_epoch = df['frame.time_epoch'].iloc[-1]

time = end_time_epoch - start_time_epoch

time_seconds = time

time_minutes = time_seconds / 60

time_hours = time_minutes / 60

print("start_time_epoch: " + str(start_time_epoch))
print("end_time_epoch: " + str(end_time_epoch))
print("PCAP TRACE DURATION in seconds: " +  str(time_seconds))
print("PCAP TRACE DURATION in minutes: " +  str(time_minutes))
print("PCAP TRACE DURATION in hours: " +  str(time_hours))