from Aggregation_Map import Aggregation_Map
import numpy as np
import ipaddress
import scipy.stats as stats
import pandas as pd
import os

def ip_to_int(str_ip):

    return int(ipaddress.IPv4Address(str_ip))

def calc_time_window(df, image_ammount):
    end_time_epoch = df['frame.time_epoch'].iloc[-1]
    print("end_time_epoch: " +  str(end_time_epoch))
    start_time_epoch = df['frame.time_epoch'][1]
    print("start_time_epoch: " +  str(start_time_epoch))

    print("duration: " + str(end_time_epoch - start_time_epoch))

    return (end_time_epoch - start_time_epoch) / image_ammount


# x achsis buckets -> dataset get lowest and highest source IP calculate / 32 
#this function returns the exact ARRAY value [0,31] for the ip source address
def get_X_bucket(int_value_ip, buckets = 32.0):

    #buckets -1 are used, because there are 32 buckets but 0 is one of them so technically the max bucket is 31 (expl with 32x32)
    bucket_size = (ip_to_int("255.255.255.255") / (buckets - 1))

    # calculate ip / bucket size -> get index
    index = int_value_ip / (bucket_size)

    return round(index) 


#this function is needed because we invert the y axis for human readablitity in the greyscale graph
#the objective is to let 0/0 be port bucket from 0 to first bucket and ip from first bucket 
#this function returns the exact ARRAY value [0,31] for the port
def get_Y_bucket(int_value_port, max_ports = 65536, bucket_ammount = 32):

  port_buckets_size = int(max_ports / (bucket_ammount - 1))

#the problem is the row is correct at 0 but since an array is shaped with array 0 being on top
#we need to put it on row 31 -> calculation is done with real_bucket - buckets in absolut
# e.g. 0 needs to be 31 -> 0 -31 in abs = 31

  bucket = round(int_value_port / port_buckets_size)

  position_in_array = abs(bucket - (bucket_ammount - 1)) 

  return position_in_array


#needed to create an empty 2 dimensional array
def get_Repr_Array(x_array = 32, y_array = 32):

  #init array with integer value 0's
  grid = [[0 for y in range(x_array) ] for x in range(y_array)]

  return grid


#this function will cut down the resolution if specified
def packets_to_map(df, source_column, destination_column, MAP_DIMENSION_X, MAP_DIMENSION_Y, MAX_LIMIT_PORTS):

        repr_array = get_Repr_Array(MAP_DIMENSION_X, MAP_DIMENSION_Y)

        for row in df.iterrows():

            packet_source_IP_address_decimal = row[1][source_column]
            x_index_for_repr_array = get_X_bucket(packet_source_IP_address_decimal, MAP_DIMENSION_X)

            packet_destination_port = row[1][destination_column]
            y_index_for_repr_array = get_Y_bucket(packet_destination_port, MAX_LIMIT_PORTS, MAP_DIMENSION_Y)

            if(packet_destination_port < MAX_LIMIT_PORTS):
                repr_array[y_index_for_repr_array][x_index_for_repr_array] += 1

        return repr_array


#timewindow inclusiv start, exclusiv end
#needed to cut pcap that is converted to csv into the exposure time windows
def aggregation(image_ammount, df, time_window, threshold_classify_portscan, MAP_DIMENSION_X, MAP_DIMENSION_Y, MAX_LIMIT_PORTS):

    aggr_map_list = []
    #only observed defined destination ports
    df = df[df["tcp.dstport"] <= MAX_LIMIT_PORTS]

    start_time_epoch = df['frame.time_epoch'][0]
    current_timestamp = start_time_epoch


    for index in range(image_ammount):
        #cut dataframe from complete dataframe according to exposure time
        iteration_df = df.loc[(df['frame.time_epoch'] >= current_timestamp)  &  (df['frame.time_epoch'] < current_timestamp + time_window)]

        print("---LOG: Trace: " + str(index)+ "; packets: ")
        # ,ip.src,ip.dst,tcp.dstport,frame.time_epoch,Assigned_Label
        print(iteration_df[["ip.src","ip.dst", "tcp.dstport", "Assigned_Label"]])

        print("time window:")
        
        print(iteration_df[['frame.time_epoch']].astype(int))

        #calculate the array represenation
        aggregation_map_array = packets_to_map(iteration_df, "ip.src", "tcp.dstport", MAP_DIMENSION_X, MAP_DIMENSION_Y, MAX_LIMIT_PORTS)

        print("---LOG: Trace: " + str(index)+ "; Aggregation Array: ")

        print("\nThe 2D-Array Aggregation is:")
        for i in aggregation_map_array:
            for j in i:
                print(j, end=" ")
            print()

        #check for label
        if(iteration_df[iteration_df['Assigned_Label'] == 1]['Assigned_Label'].count() >= threshold_classify_portscan):
            aggr_map = Aggregation_Map(index, np.array(aggregation_map_array), 1, current_timestamp, 
            current_timestamp + time_window, iteration_df['Assigned_Label'].count(),
             iteration_df[iteration_df['Assigned_Label'] == 1]['Assigned_Label'].count())
        else:
            aggr_map = Aggregation_Map(index, np.array(aggregation_map_array), 0, current_timestamp, 
            current_timestamp + time_window, iteration_df['Assigned_Label'].count(),
             iteration_df[iteration_df['Assigned_Label'] == 1]['Assigned_Label'].count())

        aggr_map_list.append(aggr_map)

        current_timestamp = current_timestamp + time_window

    return aggr_map_list


def write_list_to_path(list_aggregation_maps, path):

    result_list = []

    for index in range(len(list_aggregation_maps)):

        aggr_map = list_aggregation_maps[index]

        vec_and_label = aggr_map.get_vector_representation_with_label()

        dataframe = pd.DataFrame(vec_and_label)

    #only for resolutrion
        map_numpy = np.array(aggr_map.map)

        dataframe.to_csv(path + str(index) + "vector-map" + "-resolution-" + str(map_numpy.shape[0]) + "-" + str(map_numpy.shape[1]) + ".csv")

        result_list.append(vec_and_label)

    return np.array(result_list)


def debug_maps(list_aggregation_maps, path):

    with open(path + 'map_metadata.txt', 'a') as f2:


        for index in range(len(list_aggregation_maps)):

            aggr_map = list_aggregation_maps[index]

            f2.write("Map ID: " + str(aggr_map.id) + "; start: " + str(aggr_map.start_time)  
            + "; end: " + str(aggr_map.end_time) + "; packet_ammount_total: " + 
            str(aggr_map.packet_ammount) + "; port scan packets: " 
            + str(aggr_map.packet_ammount_labeled) + 
            "; LABEL: " + str(aggr_map.label) +
            os.linesep)