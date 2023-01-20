
import numpy as np
import pandas as pd
from pickle import *
import sys
import os

from matplotlib import pyplot as plt


def load_pkl(target_path):
    df = pd.read_pickle(target_path)
    return df


def sort(lst):

    lst.sort(key=str)
    return lst


# function needed to prepare plot from multiple histories:
# it returns a numpy shape of format:

def connect_histories(path, metric_name_in_df):

    np_current = None

    flag_first = 1

    counter = 0

    list_of_paths = os.listdir(path)

    new_list = [item for item in list_of_paths if (".pkl" in item)]

    sorted_files = sorted(new_list, key=lambda x: float(
        x.replace("ROUND_1exposure_time_", "").replace("seconds.pkl", "")))

    for file in sorted_files:

        compl_path = path + file
        counter = counter + 1
        history = load_pkl(compl_path)
        df = history[metric_name_in_df].to_frame()

        numpy_array_itr_val = df.to_numpy()

        if (flag_first == 1):
            flag_first = 0
            np_current = numpy_array_itr_val

        else:
            np_current = np.concatenate(
                [np_current, numpy_array_itr_val], axis=1)

    return np_current


def plot_on_plt(plt, numpy_array, metric_name, range, color):

    max1 = np.array(numpy_array.max(axis=0))

    x_axis = range

    # plt.figure(facecolor='white')
    plt.plot(x_axis, max1, color=color, label=metric_name)

    return plt


def plot_one_subplot():

    return 0

# --------------------------------------------running code----------------


PATH_TO_HISTORIES = str(sys.argv[1])


# OUT_PATH = str(sys.argv[2])


np_shape_of_histories = connect_histories(PATH_TO_HISTORIES, "val_accuracy")


range1 = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9']

range2 = ['1', '5', '10', '15', '20', '25',
          '30', '35', '40', '45', '50', '55', '60']


compl_range = range1 + range2


np_shape_of_histories_tp = connect_histories(PATH_TO_HISTORIES, "val_TP")
np_shape_of_histories_tn = connect_histories(PATH_TO_HISTORIES, "val_TN")
np_shape_of_histories_fp = connect_histories(PATH_TO_HISTORIES, "val_FP")
np_shape_of_histories_fn = connect_histories(PATH_TO_HISTORIES, "val_FN")
# np_shape_of_histories_recall = connect_histories(PATH_TO_HISTORIES, "val_recall")


# # , marker="*"


# ----------------------------------------------------------------------------------------------------

# mean over all epochs
# max1 = np.array(np_shape_of_histories_fn.max(axis=0))

# FNR = FN / FN + TP
def calc_fnr(np_shape_fn, np_shape_tp, xticks, epochs):

    new_array = []

    for j in range(xticks):

        column_list = []

        for i in range(epochs):

            fn_val_in_epoch_i_at_exp_t_j = np_shape_fn[i][j]
            tp_val_in_epoch_i_at_exp_t_j = np_shape_tp[i][j]

            column_list.append(fn_val_in_epoch_i_at_exp_t_j /
                               (fn_val_in_epoch_i_at_exp_t_j + tp_val_in_epoch_i_at_exp_t_j))

        new_array.append(column_list)

    fnr = np.array(np.array(new_array).mean(axis=1))

    return fnr

# FPR = FP / FP + TN


def calc_fpr(np_shape_fp, np_shape_tn, xticks, epochs):

    new_array = []

    for j in range(xticks):

        column_list = []

        for i in range(epochs):

            fp_val_in_epoch_i_at_exp_t_j = np_shape_fp[i][j]
            tn_val_in_epoch_i_at_exp_t_j = np_shape_tn[i][j]

            column_list.append(fp_val_in_epoch_i_at_exp_t_j /
                               (fp_val_in_epoch_i_at_exp_t_j + tn_val_in_epoch_i_at_exp_t_j))

        new_array.append(column_list)

    fpr = np.array(np.array(new_array).mean(axis=1))

    return fpr


fig = plt.figure(figsize=(20, 13))

# for 2 plots
widthEach = 60
xytickFontsize = 23
labelsize = 35
legendsize = 40
pad_inches = 0.1

x = compl_range
y = calc_fnr(np_shape_of_histories_fn, np_shape_of_histories_tp, 22, 100)


plt.subplot(1, 3, 1)

fig.set_figwidth(widthEach)


plt.ylim([0, 0.3])

plt.xticks(fontsize=23, rotation=45)
plt.yticks(fontsize=23)

plt.ylabel("False Negative Rate", fontsize=labelsize)
#  fontsize=14)
plt.xlabel("Exposure Times in Seconds", fontsize=labelsize)
# plt.title("Different Exposure Times")

# ctrl_line = np.ones((22,))

# x_axis = compl_range

# plt.plot(x_axis, ctrl_line, color="black", label="1.0", linestyle='--')


plt.plot(x, y, label="False Negative Rate", color="orange")

plt.legend(loc="upper right", prop={'size': legendsize})


# ----------------------------------------------------------------------------------------------------


plt.subplot(1, 3, 2)

fig.set_figwidth(widthEach)

x = compl_range
y = calc_fpr(np_shape_of_histories_fp, np_shape_of_histories_tn, 22, 100)


plt.ylim([0, 0.3])

plt.xticks(fontsize=23, rotation=45)
plt.yticks(fontsize=23)

plt.ylabel("False Positive Rate", fontsize=labelsize)
#  fontsize=14)
plt.xlabel("Exposure Times in Seconds", fontsize=labelsize)


plt.plot(x, y, label="False Positive Rate", color="red")

plt.legend(loc="upper right", prop={'size': legendsize})


# ----------------------------------------------------------------------------------------------------


plt.savefig(str(PATH_TO_HISTORIES) + "exp_time_plotsRATES.png",
            pad_inches=pad_inches, bbox_inches="tight", dpi=100)
# plt.savefig(str(OUT_PATH))

plt.show()
