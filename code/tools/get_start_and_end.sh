# input: pcap file_
#output: timestamp prints with CET, UTC and UTC seconds

echo "Location of file:"
echo "$1"

tshark -r "$1" -T fields -e frame.time_epoch -E separator=, -E quote=d, -E header=y > tmp.csv

# echo "time values"
# head -2 tmp.csv

python3 get_end_time_pcap.py tmp.csv

rm tmp.csv