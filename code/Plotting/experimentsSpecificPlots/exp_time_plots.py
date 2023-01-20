
import numpy as np
import pandas as pd
from pickle import *
import sys
import os

from matplotlib import pyplot as plt

# function to plot alongside different exposure times (specific thesis graph)


def load_pkl(target_path):
    df = pd.read_pickle(target_path)
    return df


def sort(lst):

    lst.sort(key=float)
    return lst


# function needed to prepare plot from multiple histories:
# it returns a numpy shape of format:
def connect_histories(path, metric_name_in_df):

    np_current = None

    flag_first = 1

    counter = 0

    list_of_paths = os.listdir(path)

    new_list = [item for item in list_of_paths if (".pkl" in item)]

    sorted_files = sorted(new_list, key=lambda x: int(os.path.splitext(x)[0]))

    print(sorted_files)

    for file in sorted_files:

        compl_path = path + file
        # print(compl_path)
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
            # print((np_current.shape))

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

# --------------------------------------------running code----------------


PATH_TO_HISTORIES = str(sys.argv[1])


OUT_PATH = str(sys.argv[2])


np_shape_of_histories = connect_histories(PATH_TO_HISTORIES, "val_accuracy")


range1 = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9']

range2 = ['1', '5', '10', '15', '20', '25',
          '30', '35', '40', '45', '50', '55', '60']


compl_range = range1 + range2


plt.figure(facecolor='white')

plt.ylim([0.8, 1.1])

plt.xticks(size=7)

plt.ylabel("Metric Value")
plt.xlabel("Exposure Times in Seconds")
plt.title("Different Exposure Times")


np_shape_of_histories_acc = connect_histories(
    PATH_TO_HISTORIES, "val_accuracy")
np_shape_of_histories_prec = connect_histories(
    PATH_TO_HISTORIES, "val_precision")
np_shape_of_histories_recall = connect_histories(
    PATH_TO_HISTORIES, "val_recall")


plt = plot_on_plt(plt, np_shape_of_histories_recall,
                  "Validation Recall", compl_range, "green")
plt = plot_on_plt(plt, np_shape_of_histories_prec,
                  "Validation Precision", compl_range, "blue")
plt = plot_on_plt(plt, np_shape_of_histories_acc,
                  "Validation Accuracy", compl_range, "yellow")


plot_control_line(compl_range, "red")

plt.legend(loc="lower right")

plt.savefig(str(OUT_PATH) + "validation_compare")
plt.show()
