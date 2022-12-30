



import os
import sys
import pandas as pd
import numpy as np
import scipy.stats as stats


#function is needed to delte csv files that hinder 50/50 balanced dataset
def remove_benign(folder_path, count):
    counter = count

    # print("reached")
    # print(folder_path)
    for root, directories, file in os.walk(folder_path):
        for file in file:
            #needed to ignore possible meta data
            if(file.endswith(".csv")):
                folder_path = os.path.join(root,file)
                PATH_TO_MAP = folder_path
                # print(PATH_TO_MAP)
                map = pd.read_csv(PATH_TO_MAP, index_col=[0])

                # print(map)
                #need to make numpy array
                map = np.array(map)
                label = map[-1]
                # print("reached")

                if(label == 0):

                    if(counter > 0):
                        os.remove(PATH_TO_MAP)
                        counter = counter - 1


#function is needed to delte csv files that hinder 50/50 balanced dataset
def remove_portscan(folder_path, count):
    counter = count

    for root, directories, file in os.walk(folder_path):
        for file in file:
            #needed to ignore possible meta data
            if(file.endswith(".csv")):
                folder_path = os.path.join(root,file)
                PATH_TO_MAP = folder_path
                # print(PATH_TO_MAP)
                map = pd.read_csv(PATH_TO_MAP, index_col=[0])

                # print(map)
                #need to make numpy array
                map = np.array(map)
                label = map[-1]
                # print("reached")

                if(label == 1):

                    if(counter > 0):
                        os.remove(PATH_TO_MAP)
                        counter = counter - 1






if(str(sys.argv[1]) == "--help"):
    print("argv1 == PATH_FOLDER_AGGREGATION_MAPS")


path = str(sys.argv[1])

dir_path = path



count = 0
total_labels = 0

    #needed to not flood the stdout with warning messages
warn_message_threshold = 3
warnings = 0



for root, directories, file in os.walk(path):
    for file in file:
        if(file.endswith(".csv")):
            # print(os.path.join(root,file))
            path = os.path.join(root,file)
            # print(path)
            PATH_TO_MAP = path

            map = pd.read_csv(PATH_TO_MAP, index_col=[0])



            map = np.array(map)

            zscore_vector = stats.zscore(map)
            for v in range(len(zscore_vector)):
                
                if (np.isnan(zscore_vector[v]) and warnings < warn_message_threshold): 
                    print("WARNING there is a NAN value in the list!")
                    warnings = warnings + 1


            label = map[-1]

            if(label == 1):
                total_labels= total_labels + 1


            map = map[:len(map)-1]

            count = count + 1

print("The total count of maps in the folder is: ")
print(count)
print("The total amount of labeled maps in the folder is: ")
print(total_labels)


benigin = count - total_labels

# if(total_labels > 0):
#     print("More than one label found!")


if( not (total_labels == benigin)):

# if ((count / total_labels) != 2):
    print("Need to reduce benign or label")


    if(benigin > total_labels):

        print("reducing benign")

        #this is needed to reduce the amount of benigin maps
        amount_to_reduce = benigin - total_labels

        # print(dir_path)
        remove_benign(dir_path, amount_to_reduce)

    if(benigin < total_labels):

        print("reducing portscan")

        amount_to_reduce = total_labels - benigin
        remove_portscan(dir_path, amount_to_reduce)
else:
    print("nothing to do dataset is balanced or not existing")

