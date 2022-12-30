
import os
import sys
import pandas as pd
import numpy as np
import math
import scipy.stats as stats


class Analyse:

    def __init__(self):
        self.id = None
        self.labels = None
        self.count = None
        







    if(str(sys.argv[1]) == "--help"):
        print("argv1 == PATH_AGGREGATION_MAPS")


    path = str(sys.argv[1])



    #print all


    # for root, directories, file in os.walk(path):
    #     for file in file:
    #         if(file.endswith(".csv")):
    #             # print(os.path.join(root,file))
    #             path = os.path.join(root,file)
    #             print(path)

    #             command_string = 'python3 check_aggr_map.py ' +  str(path)
    #             print(command_string)
    #             os.system(command_string)

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



