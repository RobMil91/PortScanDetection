
import os
from re import L

import pandas as pd
import numpy as np
import scipy.stats as stats
import pickle

from matplotlib import pyplot as plt


# function is needed to collect the aggregation maps from a folder.
def get_vector_maps_labels(path):

    map_label_tupel = []

  # the files are not read in specified order.
    for root, directories, file in os.walk(path):
        for file in file:
            if (file.endswith(".csv")):
                path = os.path.join(root, file)

                map_label_tupel.append(read_np_map(path))

    return map_label_tupel

# this function is needed to extract aggregation map and label from given csv path


def read_np_map(PATH_TO_MAP):

    print("---LOG: reading map at path: " + str(PATH_TO_MAP))
    map = pd.read_csv(PATH_TO_MAP, index_col=[0])
    map = np.array(map)
    map_without_label = map[:len(map)-1]
    label = map[-1]
    return (map_without_label, label)

# function is needed to create input shapes for NN input


def get_NN_train_input(tupel_list, x_axis_length, y_axis_length):

    maps = []
    labels = []

    for index in range(len(tupel_list)):

        vector_map = tupel_list[index][0]
        # check if the map actually contains values!
        if (sum(vector_map) == 0):
            print("---LOG: removed empty map!")
            continue

        print("\nThe 2D-Representation of the Aggregation Map is:")
        for i in vector_map.reshape(x_axis_length, y_axis_length, 1):
            for j in i:
                print(j, end=" ")
            print()

        # apply zscore
        n_vector_map = stats.zscore(vector_map)

        # set nan values to 0
        n_vector_map = np.nan_to_num(n_vector_map)

        # rehshape to 32,32
        n_vector_map_dim = n_vector_map.reshape(
            x_axis_length, y_axis_length, 1)

        print("\nThe 2D-Representation of the z-score Normalizsed Aggregation Map is:")
        for i in n_vector_map_dim:
            for j in i:
                print(j, end=" ")
            print()

        # append map
        maps.append(n_vector_map_dim)

        # append label to list
        labels.append((tupel_list[index][1]))

    # transform lists into NN understandable stacks
    maps = np.stack(maps, axis=0)
    labels = np.stack(labels)

    return (maps, labels)


# needed to read the saved history and replot
def load_pkl(target_path):
    df = pd.read_pickle(target_path)
    return df


# this function is used to save to history to current plot to location
def save_plot_val_accuracy_to_pkl(history, target_path_to_print, out_name):
    df = pd.DataFrame(history.history['val_accuracy'])
    df.plot(figsize=(8, 5))
    # needed to save the plt labels of the data
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['val_accuracy'], loc='upper left')
    # necassary to save the file
    df.to_pickle(target_path_to_print + out_name + "_val_accuracy.pkl")


# function needed to save complete history of one ml learn and test phase
# input history: with accuracy, precision, recall, FP, FN
def save_compl_history(history, target_path_to_print, out_name):

    df = pd.DataFrame(history.history)
    df.to_pickle(target_path_to_print + out_name + ".pkl")


# debug function used to quick check
def load_metric_jpg(target_path, out_path):
    df = pd.read_pickle(target_path)
    df.plot(figsize=(8, 5))
    plt.savefig(out_path + ".jpg")
    return df
