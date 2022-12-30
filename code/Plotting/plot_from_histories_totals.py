
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
                #order does not matter?!
                # in every no matter which order red pkl it gets order from the epoch
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

    print("Found : " + str(counter) + " histories")


    return np_current


def calc_fnr_on_epochs(np_shape_fn, np_shape_tp, epochs):


  column_list = []

  # fn_val_in_epoch_i = np_shape_fn[0]
  # tp_val_in_epoch_i = np_shape_tp[0]

  # # print(np_shape_fn[0])
  # # print(np_shape_tp[0])

  # rate = fn_val_in_epoch_i / (fn_val_in_epoch_i + tp_val_in_epoch_i)
  # # print("rate")
  # # print(rate)

  for i in range(epochs):

    fn_val_in_epoch_i = np_shape_fn[i]
    tp_val_in_epoch_i = np_shape_tp[i]

    column_list.append(fn_val_in_epoch_i / (fn_val_in_epoch_i + tp_val_in_epoch_i))

  return np.array(column_list)

# function needed to calculate array (vecot wise) the false positives rates
#input shapes need to be identical
def calc_fpr_on_epochs(np_shape_fp, np_shape_tn, epochs):

  list = []

  for i in range(epochs):

    fp_val_in_epoch_i = np_shape_fp[i]
    tp_val_in_epoch_i = np_shape_tn[i]

    list.append(fp_val_in_epoch_i / (fp_val_in_epoch_i + tp_val_in_epoch_i))

  return np.array(list)
#--------------------------------------------running code----------------


# config: 

all_ylim=[0.0,30]


PATH_TO_HISTORIES = str(sys.argv[1])


plt.subplot(1, 3, 1)




np_shape_of_histories_FN = connect_histories(PATH_TO_HISTORIES, "val_FN")

print(np_shape_of_histories_FN.shape)


median = np.array(np.median(np_shape_of_histories_FN, axis=1))
min1 = np.array(np_shape_of_histories_FN.min(axis=1))
max1 = np.array(np_shape_of_histories_FN.max(axis=1))

x_axis = np.arange(0,100)


plt.ylim(all_ylim)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

plt.plot(x_axis, median, lw=2, label="False Negative Rate Median", color='orange')
plt.fill_between(x_axis, min1, max1, facecolor='orange', label="Min/Max Shading", alpha=0.4)

# ctrl_line = np.ones((100,))
# plt.plot(x_axis, ctrl_line, color="black", label="1.0", linestyle='--')

# ax.set_title('Median of ' + metric_name.upper() + " over " + str(epochs) + " epochs")
plt.legend(loc='upper right', prop={'size': 20})
plt.xlabel('Epochs', fontsize=30)
plt.ylabel("False Negative Rate", fontsize=30)

#----------------------------------------------------------------------------------------------------

plt.subplot(1, 3, 2)


np_shape_of_histories_FP = connect_histories(PATH_TO_HISTORIES, "val_FP")

print(np_shape_of_histories_FN.shape)


median = np.array(np.median(np_shape_of_histories_FP, axis=1))
min1 = np.array(np_shape_of_histories_FP.min(axis=1))
max1 = np.array(np_shape_of_histories_FP.max(axis=1))

x_axis = np.arange(0,100)


plt.ylim(all_ylim)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

plt.plot(x_axis, median, lw=2, label="False Positive Rate Median", color='red')
plt.fill_between(x_axis, min1, max1, facecolor='red', label="Min/Max Shading", alpha=0.4)

# ctrl_line = np.ones((100,))
# plt.plot(x_axis, ctrl_line, color="black", label="1.0", linestyle='--')

# ax.set_title('Median of ' + metric_name.upper() + " over " + str(epochs) + " epochs")
plt.legend(loc='upper right', prop={'size': 20})
plt.xlabel('Epochs', fontsize=30)
plt.ylabel("False Positive Rate", fontsize=30)

#----------------------------------------------------------------------------------------------------


# plt.subplot(1, 3, 3)


# np_shape_of_histories = connect_histories(PATH_TO_HISTORIES, "val_recall")

# median = np.array(np.median(np_shape_of_histories, axis=1))
# min1 = np.array(np_shape_of_histories.min(axis=1))
# max1 = np.array(np_shape_of_histories.max(axis=1))

# x_axis = np.arange(0,100)

# plt.ylim([0.5, 1.01])
# plt.xticks(size=7)

# plt.plot(x_axis, median, lw=2, label="Validation Recall Median", color='blue')
# plt.fill_between(x_axis, min1, max1, facecolor='blue', label="Min/Max Recall Shading", alpha=0.4)

# ctrl_line = np.ones((100,))
# plt.plot(x_axis, ctrl_line, color="black", label="1.0", linestyle='--')

# # ax.set_title('Median of ' + metric_name.upper() + " over " + str(epochs) + " epochs")
# plt.legend(loc='lower right')
# plt.xlabel('Epochs')
# plt.ylabel("Precision Value")

# #----------------------------------------------------------------------------------------------------


plt.tight_layout(pad=5.0)

plt.show() 