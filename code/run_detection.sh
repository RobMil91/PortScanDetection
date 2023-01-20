#need one input argument! -> a labeled csv file

# If Aggregation and Detection Parameters need to be changed from standart, the sub directory scripts need to be adapted
# format:

# #aggregate the traffic into maps, with 1 second exposure time, 32 resolution and threshold 1
bash Data/Aggregation/scripts/sec_aggregation_gc.sh $1 >~/aggregationLog.txt

echo "------------------------------------------------Aggregation Complete--------------------------------------"

# #eval the aggregation maps and create metric history
bash Detection/scripts/runDetectionMultiple_gc.sh >~/detectionLog.txt

echo "------------------------------------------------Detection Complete----------------------------------------"

#writing example Detection Evaluation Metrics for showing a grafical setup is necessary.
python3 Plotting/plot_from_histories.py ~/sec_Min_Aggregation/results/

echo "------------------------------------------------Example Plot created at ~/sec_Min_Aggregation/results/----------------------------------------"
