from Aggregation_Map import *
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import scipy.stats as stats


import sys


#debuggin tool, to check a single aggregation map for its properties
if(str(sys.argv[1]) == "--help"):
    print("argv1 == PATH_LABELD_TRACE, needs to be csv")



PATH_TO_MAP = str(sys.argv[1])

map = pd.read_csv(PATH_TO_MAP, index_col=[0])

map = np.array(map)


label = map[-1]

map = map[:len(map)-1]

print(map)
print(map.shape)



print(map.reshape(1024,))

original_map_vector = map.reshape(1024,)


print("label: " + str(label))

print("Max value:" + str(original_map_vector.max()))

print("Mean value vector:" + str(original_map_vector.mean()))
print("STD value vecotr:" + str(original_map_vector.std()))

z_score_vector = stats.zscore(original_map_vector)

if (np.nan in z_score_vector): print("WARNING there is a NAN value in the list!")



print("reshaping: ")

orig_map = original_map_vector.reshape(32,32)
z_score_map = z_score_vector.reshape(32,32)




print( "------------------------------------------------------------------------------Original MAP---------------------------------------------------")
print(orig_map,flush=True)

list = []

list.append(orig_map)

#debug print function 
def print_save_aggregation_map_list(aggregation_map_list, path=None, bool_show=False, grid_rows=5, grid_colums=5, MAP_DIMENSION_X=32, MAP_DIMENSION_Y=32):

    if ((grid_rows * grid_colums) <= (len(aggregation_map_list)-1)): 
        print( "More aggregation Maps given, than fitting the subplot GRID to draw cutting down " )
        max = (len(aggregation_map_list)-1) - (grid_rows * grid_colums) 
        aggregation_map_list = aggregation_map_list[: (len(aggregation_map_list)-1) - max]

    
    for index in range(len(aggregation_map_list)):

        aggr_map = aggregation_map_list[index]
        img_array = aggr_map
        plt.subplot(int(grid_rows), int(grid_colums), index + 1)
        plt.xlabel("Source IP Address Buckets", fontsize=30)
        plt.ylabel("Destination Port Buckets", fontsize=30)
        plt.xticks(range(0,33), fontsize=15)
        plt.yticks(range(0,33), fontsize=15)
        plt.imshow(img_array, cmap='gray', vmin=0, vmax=255,  extent=[0,MAP_DIMENSION_X - 1 ,0,MAP_DIMENSION_Y - 1])

    figure = plt.gcf()
    figure.set_size_inches((20,20), forward=False)
    if(path is not None):
        figure.savefig(path, format='png')
    
    if(bool_show):
        plt.show()


print_save_aggregation_map_list(list, (PATH_TO_MAP + ".png"), True, 1,1)





