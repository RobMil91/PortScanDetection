
import matplotlib.gridspec as gridspec
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
        print(compl_path)
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


def plot_control_line(range, color):

    ctrl_line = np.ones((22,))

    x_axis = range

    plt.plot(x_axis, ctrl_line, color=color, label="1.0", linestyle='--')

    return plt


def plot_on_plt(plt, numpy_array, metric_name, range, color):

    max1 = np.array(numpy_array.max(axis=0))

    x_axis = range

    plt.plot(x_axis, max1, color=color, label=metric_name)

    return plt


def plot_one_subplot():

    return 0

# --------------------------------------------running code----------------


PATH_TO_HISTORIES = str(sys.argv[1])


# OUT_PATH = str(sys.argv[2])


gs = gridspec.GridSpec(4, 4)


np_shape_of_histories = connect_histories(PATH_TO_HISTORIES, "val_accuracy")


range1 = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9']

range2 = ['1', '5', '10', '15', '20', '25',
          '30', '35', '40', '45', '50', '55', '60']


compl_range = range1 + range2

# plt.subplots(1)


fig = plt.figure(figsize=(30, 40))


widthEach = 45
xytickFontsize = 40
labelsize = 40
legendsize = 40
padInch = 0.1

np_shape_of_histories_acc = connect_histories(
    PATH_TO_HISTORIES, "val_accuracy")
np_shape_of_histories_prec = connect_histories(
    PATH_TO_HISTORIES, "val_precision")
np_shape_of_histories_recall = connect_histories(
    PATH_TO_HISTORIES, "val_recall")


# ----------------------------------------------------------------------------------------------------

max1 = np.array(np_shape_of_histories_acc.max(axis=0))


x = compl_range
y = max1


plt.subplot(gs[:2, :2])
fig.set_figwidth(widthEach)

plt.ylim([0.85, 1.01])

plt.xticks(fontsize=xytickFontsize,  rotation=45)
plt.yticks(fontsize=xytickFontsize)

plt.ylabel("Accuracy", fontsize=labelsize)
#  fontsize=14)
plt.xlabel("Exposure Times in Seconds", fontsize=labelsize)
# plt.title("Different Exposure Times")

ctrl_line = np.ones((22,))

x_axis = compl_range

plt.plot(x_axis, ctrl_line, color="black", label="1.0", linestyle='--')


plt.plot(x, y, label="Accuracy Maximum", color="red")
plt.legend(loc="lower right",  prop={'size': legendsize})


# ----------------------------------------------------------------------------------------------------

plt.subplot(gs[:2, 2:])
fig.set_figwidth(widthEach)
max2 = np.array(np_shape_of_histories_prec.max(axis=0))


x = compl_range
y = max2


plt.ylim([0.85, 1.01])

plt.xticks(fontsize=xytickFontsize, rotation=45)
plt.yticks(fontsize=xytickFontsize)

plt.ylabel("Precision", fontsize=labelsize)
#  fontsize=14)
plt.xlabel("Exposure Times in Seconds", fontsize=labelsize)
# plt.title("Different Exposure Times")

ctrl_line = np.ones((22,))

x_axis = compl_range

plt.plot(x_axis, ctrl_line, color="black", label="1.0", linestyle='--')


plt.plot(x, y, label="Precision Maximum", color="Green")

plt.legend(loc="lower right",  prop={'size': legendsize})

# ----------------------------------------------------------------------------------------------------


plt.subplot(gs[2:4, 1:3])
fig.set_figwidth(widthEach)
max3 = np.array(np_shape_of_histories_recall.max(axis=0))


x = compl_range
y = max3


plt.ylim([0.85, 1.01])

plt.xticks(fontsize=xytickFontsize,  rotation=45)
plt.yticks(fontsize=xytickFontsize)

plt.ylabel("Recall", fontsize=labelsize)
#  fontsize=14)
plt.xlabel("Exposure Times in Seconds", fontsize=labelsize)
# plt.title("Different Exposure Times")

ctrl_line = np.ones((22,))

x_axis = compl_range

plt.plot(x_axis, ctrl_line, color="black", label="1.0", linestyle='--')

plt.plot(x, y, label="Recall Maximum", color="Blue")
plt.legend(loc="lower right",  prop={'size': legendsize})


fig.subplots_adjust(hspace=0.5)
fig.subplots_adjust(wspace=0.5)


plt.savefig(str(PATH_TO_HISTORIES) + "exp_time_plots.png",
            bbox_inches="tight", pad_inches=padInch, dpi=100)
plt.show()
