
import numpy as np
import pandas as pd
from pickle import *
import sys
import os

from matplotlib import pyplot as plt


def load_pkl(target_path):
  df = pd.read_pickle(target_path)

#needed for debuging
  # df.plot(figsize=(8,5))
  # plt.show()
  return df

def connect_histories(path, metric_name_in_df):

    np_current = None

    flag_first = 1
 

    for root, directories, file in os.walk(path):


        for file in file:

            if(file.endswith(".pkl")):
                # print(os.path.join(root,file))
                path = os.path.join(root,file)

                # print("debug loading pkl")
                history = load_pkl(path)

                #a column is imported as a series logic below forces dataframes!
                df = history[metric_name_in_df].to_frame()               

                numpy_array_itr_val = df.to_numpy()

                if(flag_first == 1):
                    flag_first = 0
                    np_current = numpy_array_itr_val

                else:

                    np_current = np.concatenate([np_current, numpy_array_itr_val], axis = 1)
                    # print((np_current.shape))

    # print("finished loop----------------------")

    #     #need epochs,learning_runs
    # print(np_current.shape)


    return np_current


#function is needed to calculate mean min and max of each epoch 

#input a sequence of histories where the shape of inputs is each column one history
#input 1: format is a numpy shape with epochs as each row
#input 2: epochs
def write_graphs_over_range(path, epochs, out_path):



  metric_name = "accuracy"
  numpy_array = connect_histories(path, metric_name)

  median = np.array(np.median(numpy_array, axis=1))
  min1 = np.array(numpy_array.min(axis=1))
  max1 = np.array(numpy_array.max(axis=1))

  x_axis = np.arange(0,epochs)

  
  fig, ax = plt.subplots(1)

  # ax.set_ylim([0, 1])

  ax.plot(x_axis, median, lw=2, label=metric_name + "_median", color='blue')
  ax.fill_between(x_axis, min1, max1, facecolor='yellow', alpha=0.4)

  ax.set_title('Median of ' + metric_name.upper() + " over " + str(epochs) + " epochs")
  ax.legend(loc='lower right')
  ax.set_xlabel('epochs')
  ax.set_ylabel(metric_name.replace("val_", ""))


  metric_name = "precision"
  numpy_array = connect_histories(path, metric_name)

  median = np.array(np.median(numpy_array, axis=1))
  min1 = np.array(numpy_array.min(axis=1))
  max1 = np.array(numpy_array.max(axis=1))

  x_axis = np.arange(0,epochs)
  fig, ax = plt.subplots(2)

  # ax.set_ylim([0, 1])

  ax.plot(x_axis, median, lw=2, label=metric_name + "_median", color='blue')
  ax.fill_between(x_axis, min1, max1, facecolor='yellow', alpha=0.4)

  ax.set_title('Median of ' + metric_name.upper() + " over " + str(epochs) + " epochs")
  ax.legend(loc='lower right')
  ax.set_xlabel('epochs')
  ax.set_ylabel(metric_name.replace("val_", ""))


  metric_name = "recall"
  numpy_array = connect_histories(path, metric_name)

  median = np.array(np.median(numpy_array, axis=1))
  min1 = np.array(numpy_array.min(axis=1))
  max1 = np.array(numpy_array.max(axis=1))

  x_axis = np.arange(0,epochs)
  fig, ax = plt.subplots(3)

  # ax.set_ylim([0, 1])

  ax.plot(x_axis, median, lw=2, label=metric_name + "_median", color='blue')
  ax.fill_between(x_axis, min1, max1, facecolor='yellow', alpha=0.4)

  ax.set_title('Median of ' + metric_name.upper() + " over " + str(epochs) + " epochs")
  ax.legend(loc='lower right')
  ax.set_xlabel('epochs')
  ax.set_ylabel(metric_name.replace("val_", ""))


  metric_name = "FP"
  fig, ax = plt.subplots(4)
  numpy_array = connect_histories(path, metric_name)

  median = np.array(np.median(numpy_array, axis=1))
  min1 = np.array(numpy_array.min(axis=1))
  max1 = np.array(numpy_array.max(axis=1))

  x_axis = np.arange(0,epochs)

  ax.plot(x_axis, median, lw=2, label=metric_name + "_median", color='blue')
  ax.fill_between(x_axis, min1, max1, facecolor='yellow', alpha=0.4)

  ax.set_title('Median of ' + metric_name.upper() + " over " + str(epochs) + " epochs")
  ax.legend(loc='lower right')
  ax.set_xlabel('epochs')
  ax.set_ylabel(metric_name.replace("val_", ""))





  out_path_name = out_path + "median_over_epochs_" + "acc_prec_recal_FP" + ".jpg"

  plt.savefig(out_path_name)
  plt.show()






#   return plt


#possiblity to write y values to given range with histories
# def write_graph_over_range(numpy_array, range, out_path, metric_name, index, plt):

#   median = np.array(np.median(numpy_array, axis=1))
#   min1 = np.array(numpy_array.min(axis=1))
#   max1 = np.array(numpy_array.max(axis=1))

#   #need to be able to adapt to for example exposure time
#   x_axis = np.arange(0, range)

#   fig, ax = plt.subplots(index)

#   if(not(("FP" in metric_name) or ("FN" in metric_name))):
#     ax.set_ylim([0, 1])

#   ax.plot(x_axis, median, lw=2, label=metric_name + "_median", color='blue')
#   ax.fill_between(x_axis, min1, max1, facecolor='blue', alpha=0.4)

#   ax.set_title('Median of ' + metric_name.upper() + " over " + str(range) + " epochs")
#   ax.legend(loc='lower right')
#   ax.set_xlabel('epochs')
#   ax.set_ylabel(metric_name.replace("val_", ""))
  







#   #after all subplots have been added

#   # out_path_name = out_path + "median_over_epochs_" + "acc_prec_recal_FP" + ".jpg"

#   # plt.savefig(out_path_name)
#   # plt.show() 
#   return plt

#   


def load_history(target_path):


  history = pd.read_pickle(target_path)

#--------------------------------------------running code----------------

PATH_TO_HISTORIES = str(sys.argv[1])

EPOCHS = int(str(sys.argv[2]))

OUT_PATH = str(sys.argv[3])



# np_shape_of_histories = connect_histories(PATH_TO_HISTORIES)



write_graphs_over_range(PATH_TO_HISTORIES, EPOCHS, OUT_PATH)

# load_history(PATH_TO_HISTORIES)

# print("Plotting metric median over epochs for: " +  str(METRIC_NAME))

# metrics = ["accuracy", "precision", "recall", "FP"]

# plt_current = plt.figure()

# for i in range(0,4):

#   print(metrics[i])


