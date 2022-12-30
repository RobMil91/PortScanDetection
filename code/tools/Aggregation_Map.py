from cProfile import label
import pandas as pd
import numpy as np

class Aggregation_Map():
    def __init__(self, id, map, label, start_time=None, end_time=None, packet_ammount=None, packet_ammount_labeled=None, normalizsed_map=None):
        self.id = id
        self.map = map
        #LABEL FOR ENTIRE MAP!
        self.label = label
        self.start_time = start_time
        self.end_time = end_time
        self.packet_ammount = packet_ammount
        self.packet_ammount_labeled = packet_ammount_labeled
        self.normalizsed_map = normalizsed_map

    def to_string_all(self):
        return str(self.id) + " , " + str(self.map) + " , " + str(self.label)

    def to_string_id_label(self):
        return str(self.id) + " , " + str(self.label)


    def print_map():
        raise("TODo")


    def save_map():
        raise("TODO")


    def set_normalizsed_map(self, normalizsed_map):
        self.normalizsed_map = normalizsed_map


    def save_N_map_to_path_csv(self, path):
        dataframe = pd.DataFrame(self.normalizsed_map)
        dataframe.to_csv(path)
    
    def save_map_to_path_csv(self, path):
        dataframe = pd.DataFrame(self.map)
        dataframe.to_csv(path)

    def get_vector_representation(self):
        
        map_numpy = np.array(self.map)

        vec_length = map_numpy.shape[0] * map_numpy.shape[1]

        return map_numpy.reshape(vec_length,)


    def get_vector_representation_with_label(self):
        
        map_numpy = np.array(self.map)

        vec_length = map_numpy.shape[0] * map_numpy.shape[1]


        return np.append(map_numpy.reshape(vec_length,), self.label)
