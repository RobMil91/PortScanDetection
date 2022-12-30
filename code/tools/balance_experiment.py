
#this modul is needed to balance an entire folder range with maps

# the struct is:
# /devinded_path/runX/maps/exposure_timeX..

#this modul is given to balance a set of maps within a given /maps/ folder
#example command: python3 balance_experiment .../maps/

import os
import sys
import pandas as pd
import numpy as np
import scipy.stats as stats


def reduce_benign(path_to_dir, ammount_to_reduce):

    counter = ammount_to_reduce

    files = os.listdir(path_to_dir)
    # print(files)

    for file in files:
        if(file.endswith(".csv")):
            current_path = path_to_dir + "/" + file
            # print(current_path)
            map = pd.read_csv(current_path, index_col=[0])
            map_np = np.array(map)
            label = map_np[-1]
                # print("reached")

            if(label == 0):

                if(counter > 0):
                    os.remove(current_path)
                    counter = counter - 1

def reduce_portscan(path_to_dir, ammount_to_reduce):

    counter = ammount_to_reduce

    files = os.listdir(path_to_dir)
    # print(files)

    for file in files:
        if(file.endswith(".csv")):
            current_path = path_to_dir + "/" + file
            # print(current_path)
            map = pd.read_csv(current_path, index_col=[0])
            map_np = np.array(map)
            label = map_np[-1]
                # print("reached")

            if(label == 1):

                if(counter > 0):
                    os.remove(current_path)
                    counter = counter - 1


def reduce_on_path(path_to_dir, count, labels):

    benigin = count - labels

    if( not (labels == benigin)):
        print("Need to reduce benign or label")


        if(benigin > labels):

            print("reducing benign")
            amount_to_reduce = benigin - labels

            # print(dir_path)
            reduce_benign(path_to_dir, amount_to_reduce)

        if(benigin < labels):

            print("reducing portscan")

            amount_to_reduce = labels - benigin
            reduce_portscan(path_to_dir, amount_to_reduce)


    else:
        print("nothing to do dataset is balanced or not existing")

def analyse_on_path(path):

    dirs = os.listdir(path)

    # print(dirs)

    count = 0
    total_labels = 0


    for directory in dirs:
        print(directory)
        print("--------------------------------------------------------------------------------------------------------------------------------------------------------")
        files_at_experiment = os.listdir(path + str(directory))
        # print(files_at_experiment)

        for file in files_at_experiment:
            # print(file)

            
            if(file.endswith(".csv")):
                path_to_file = path + directory + "/" + file
                # print(path_to_file)

                map = pd.read_csv(path_to_file, index_col=[0])

                #numpy shape
                map = np.array(map)

                label = map[-1]

                if(label == 1):
                        total_labels = total_labels + 1

                count = count + 1

        print("The total count of maps in the folder is: ")
        print(count)
        print("The total amount of labeled maps in the folder is: ")
        print(total_labels)

        #reduction needs to happen here
        path_to_dir = path_to_file = path + directory 
        # print(path_to_dir)

        reduce_on_path(path_to_dir, count, total_labels)

        count = 0
        total_labels = 0



if(str(sys.argv[1]) == "--help"):
    print("argv1 == PATH_TO_EXPERIMENT_FOLDER")

# the struct is:
# /devinded_path/runX/maps/exposure_timeX..
# need loop to go over all exposure...




# /devinded_path/runX/maps/
path = str(sys.argv[1])

print(path)

analyse_on_path(path)





