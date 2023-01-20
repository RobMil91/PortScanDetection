import pandas as pandas
from utils_aggregation import *
import os
import sys
# this module aggregates the previous pcap file that got converted to csv with only the relevant columns into aggregation maps,
# they are written to csv file


if (str(sys.argv[1]) == "--help"):
    print("argv1 == PATH_LABELD_TRACE, needs to be csv")
    print("argv2 == PATH_PRINT_LOCATION, the image")
    print("argv3 == IMMAGE_AMMOUNT")
    print("argv4 == THRESHOLD_PORTSCAN")
    print("argv5 == MAP_DIMENSION_X")
    print("argv6 == MAP_DIMENSION_Y")
    print("argv7 == MAX_PORTS_Y")
    print("argv8 == FIXED EXPOSURE TIME")


PATH_LABELD_TRACE = str(sys.argv[1])
OUTPUT_FOLDER = str(sys.argv[2])
unlabeled_trace_dataframe = pandas.read_csv(PATH_LABELD_TRACE)
# total amount of maps created!
IMAGE_AMMOUNT = int(str(sys.argv[3]))
THRESHOLD_PORTSCAN = int(str(sys.argv[4]))
MAP_DIMENSION_X = int(str(sys.argv[5]))
MAP_DIMENSION_Y = int(str(sys.argv[6]))
MAX_LIMIT_PORTS = int(str(sys.argv[7]))

if (len(sys.argv) > 8):
    time_window = int(str(sys.argv[8]))
    print("The exposure time of each map is: " + str(time_window) + " seconds")
else:
    time_window = calc_time_window(unlabeled_trace_dataframe, IMAGE_AMMOUNT)
    print("The exposure time of each map is: " + str(time_window) + " seconds")

path = str(sys.argv[2])

with open(path + 'metadata.txt', 'a') as f1:

    f1.write("time_window: " + str(time_window) + os.linesep)
    f1.write("MAP_DIMENSION_X: " + str(sys.argv[5]) + os.linesep)
    f1.write("MAP_DIMENSION_Y: " + str(sys.argv[6]) + os.linesep)
    f1.write("MAX_LIMIT_PORTS: " + str(sys.argv[7]) + os.linesep)


# get time window for packet sequence
list_aggregation_maps = aggregation(IMAGE_AMMOUNT, unlabeled_trace_dataframe,
                                    time_window, THRESHOLD_PORTSCAN, MAP_DIMENSION_X, MAP_DIMENSION_Y, MAX_LIMIT_PORTS)

vec_label_list = write_list_to_path(list_aggregation_maps, str(OUTPUT_FOLDER))

print("---LOG: saved maps to " + str(OUTPUT_FOLDER) +
      ":------------------------------------------------------------------------------------")


debug_maps(list_aggregation_maps, path)

print(vec_label_list.shape)
