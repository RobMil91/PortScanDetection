import numpy as np
# necessary to save background info on the aggregation data


class Aggregation_Map():
    def __init__(self, id, map, label, start_time=None, end_time=None, packet_ammount=None, packet_ammount_labeled=None):
        self.id = id
        self.map = map
        # LABEL FOR ENTIRE MAP!
        self.label = label
        self.start_time = start_time
        self.end_time = end_time
        self.packet_ammount = packet_ammount
        self.packet_ammount_labeled = packet_ammount_labeled

    def to_string_all(self):
        return str(self.id) + " , " + str(self.map) + " , " + str(self.label)

    def to_string_id_label(self):
        return str(self.id) + " , " + str(self.label)

    def get_vector_representation_with_label(self):

        map_numpy = np.array(self.map)

        vec_length = map_numpy.shape[0] * map_numpy.shape[1]

        return np.append(map_numpy.reshape(vec_length,), self.label)
