
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

    counter = 0
 

    for root, directories, file in os.walk(path):


        for file in file:

            if(file.endswith(".pkl")):
                # print(os.path.join(root,file))
                path = os.path.join(root,file)
                #order does not matter.
                counter = counter + 1

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

    # print("Found : " + str(counter) + " histories")


    return np_current


#function is needed to calculate mean min and max of each epoch 

#input a sequence of histories where the shape of inputs is each column one history
#input 1: format is a numpy shape with epochs as each row
#input 2: epochs
def write_graph_validation_acc_over_epochs(numpy_array, epochs, out_path, metric_name):

  median = np.array(np.median(numpy_array, axis=1))
  min1 = np.array(numpy_array.min(axis=1))
  max1 = np.array(numpy_array.max(axis=1))

  x_axis = np.arange(0,epochs)


  fig, ax = plt.subplots(1)

  if(not(("FP" in metric_name) or ("FN" in metric_name))):
    ax.set_ylim([0, 1])

  ax.plot(x_axis, median, lw=2, label=metric_name + "_median", color='blue')
  ax.fill_between(x_axis, min1, max1, facecolor='blue', alpha=0.4)

  ax.set_title('Median of ' + metric_name.upper() + " over " + str(epochs) + " epochs")
  ax.legend(loc='lower right')
  ax.set_xlabel('epochs')
  ax.set_ylabel(metric_name.replace("val_", ""))

  out_path_name = out_path + "median_over_epochs_" + metric_name + ".jpg"

  plt.savefig(out_path_name)
  plt.show() 



#--------------------------------------------config:----------------
fig = plt.figure(figsize=(30, 40))
#for 2 plots
widthEach = 45
xytickFontsize=40
labelsize=40 
legendsize=40
pad_inches=0.1



#--------------------------------------------running code----------------

PATH_TO_HISTORIES = str(sys.argv[1])

plt.subplot(1, 3, 1)
fig.set_figwidth(widthEach)


np_shape_of_histories = connect_histories(PATH_TO_HISTORIES, "loss")

median = np.array(np.median(np_shape_of_histories, axis=1))
min1 = np.array(np_shape_of_histories.min(axis=1))
max1 = np.array(np_shape_of_histories.max(axis=1))

x_axis = np.arange(0,100)


# fig, ax = plt.subplots(1)

# if(not(("FP" in metric_name) or ("FN" in metric_name))):
#   ax.set_ylim([0, 1])

plt.ylim([0, 1.01])
plt.xticks(fontsize=xytickFontsize)
plt.yticks(fontsize=xytickFontsize)

plt.plot(x_axis, median, lw=2, label="Training Loss", color='orange')
# plt.fill_between(x_axis, min1, max1, facecolor='red', label="Min/Max Accuracy Shading", alpha=0.4)

ctrl_line = np.ones((100,))
plt.plot(x_axis, ctrl_line, color="black", label="1.0", linestyle='--')

# ax.set_title('Median of ' + metric_name.upper() + " over " + str(epochs) + " epochs")
plt.legend(loc='upper right', prop={'size': legendsize})
plt.xlabel('Epochs', fontsize=labelsize)
plt.ylabel("Loss", fontsize=labelsize)

#----------------------------------------------------------------------------------------------------



plt.subplot(1, 3, 2)
fig.set_figwidth(widthEach)


np_shape_of_histories = connect_histories(PATH_TO_HISTORIES, "accuracy")

median = np.array(np.median(np_shape_of_histories, axis=1))
min1 = np.array(np_shape_of_histories.min(axis=1))
max1 = np.array(np_shape_of_histories.max(axis=1))

x_axis = np.arange(0,100)

plt.ylim([0, 1.01])
plt.xticks(fontsize=xytickFontsize)
plt.yticks(fontsize=xytickFontsize)

plt.plot(x_axis, median, lw=2, label="Training Accuracy", color='red')
# plt.fill_between(x_axis, min1, max1, facecolor='green', label="Min/Max Precision Shading", alpha=0.4)

ctrl_line = np.ones((100,))
plt.plot(x_axis, ctrl_line, color="black", label="1.0", linestyle='--')

# ax.set_title('Median of ' + metric_name.upper() + " over " + str(epochs) + " epochs")
plt.legend(loc='lower right',  prop={'size': legendsize})
plt.xlabel('Epochs', fontsize=labelsize)
plt.ylabel("Accuracy", fontsize=labelsize)

#----------------------------------------------------------------------------------------------------


# plt.subplot(1, 3, 3)


# np_shape_of_histories = connect_histories(PATH_TO_HISTORIES, "val_recall")

# median = np.array(np.median(np_shape_of_histories, axis=1))
# min1 = np.array(np_shape_of_histories.min(axis=1))
# max1 = np.array(np_shape_of_histories.max(axis=1))

# x_axis = np.arange(0,100)

# plt.ylim([0, 1.01])
# plt.xticks(fontsize=15)
# plt.yticks(fontsize=15)

# plt.plot(x_axis, median, lw=2, label="Validation Recall Median", color='blue')
# # plt.fill_between(x_axis, min1, max1, facecolor='blue', label="Min/Max Recall Shading", alpha=0.4)

# ctrl_line = np.ones((100,))
# plt.plot(x_axis, ctrl_line, color="black", label="1.0", linestyle='--')

# # ax.set_title('Median of ' + metric_name.upper() + " over " + str(epochs) + " epochs")
# plt.legend(loc='lower right',  prop={'size': 15})
# plt.xlabel('Epochs', fontsize=30)
# plt.ylabel("Recall", fontsize=30)

#----------------------------------------------------------------------------------------------------

plt.savefig(str(PATH_TO_HISTORIES) + "metric_plot.png",pad_inches=pad_inches, bbox_inches="tight", dpi=100)

plt.show() 