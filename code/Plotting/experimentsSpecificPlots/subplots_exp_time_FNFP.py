
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

    # print(sorted_files)

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


range1 = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9']

range2 = ['1', '5', '10', '15', '20', '25',
          '30', '35', '40', '45', '50', '55', '60']


compl_range = range1 + range2


gs = gridspec.GridSpec(4, 4)

fig = plt.figure(figsize=(30, 40))


widthEach = 45
xytickFontsize = 40
labelsize = 40
legendsize = 40
pad_inches = 0.1


np_shape_of_histories_fp = connect_histories(PATH_TO_HISTORIES, "val_FP")
np_shape_of_histories_fn = connect_histories(PATH_TO_HISTORIES, "val_FN")
# np_shape_of_histories_recall = connect_histories(PATH_TO_HISTORIES, "val_recall")


# ----------------------------------------------------------------------------------------------------

max1 = np.array(np_shape_of_histories_fn.mean(axis=0))


x = compl_range
y = max1


plt.subplot(gs[:2, :2])


fig.set_figwidth(widthEach)

plt.ylim([0, 35])

plt.xticks(fontsize=xytickFontsize, rotation=45)
plt.yticks(fontsize=xytickFontsize)

plt.ylabel("Total Amount", fontsize=labelsize)
#  fontsize=14)
plt.xlabel("Exposure Times in Seconds", fontsize=labelsize)
# plt.title("Different Exposure Times")

# ctrl_line = np.ones((22,))

# x_axis = compl_range

# plt.plot(x_axis, ctrl_line, color="black", label="1.0", linestyle='--')


plt.plot(x, y, label="False Negative", color="orange")
plt.legend(loc="upper right", prop={'size': legendsize})


# ----------------------------------------------------------------------------------------------------

plt.subplot(gs[:2, 2:])

fig.set_figwidth(widthEach)

max2 = np.array(np_shape_of_histories_fp.mean(axis=0))


x = compl_range
y = max2


plt.ylim([0, 35])

plt.xticks(fontsize=xytickFontsize, rotation=45)
plt.yticks(fontsize=xytickFontsize)

plt.ylabel("Total Amount", fontsize=labelsize)
#  fontsize=14)
plt.xlabel("Exposure Times in Seconds", fontsize=labelsize)


plt.plot(x, y, label="False Positive", color="red")

plt.legend(loc="upper right", prop={'size': legendsize})

# ----------------------------------------------------------------------------------------------------


plt.subplot(gs[2:4, 1:3])

# max2 = np.array(np_shape_of_histories_fp.mean(axis=0))

# splitseconds input data
# [275574, 137890, 92002, 69054, 55284, 46102, 39550, 34636, 30810]

# size = 9 + 13?

split_seconds_sizes = [275574, 137890, 92002,
                       69054, 55284, 46102, 39550, 34636, 30810]
sec_to_min_sizes = [27748, 5736, 2862, 1818,
                    1324, 1010, 814, 684, 568, 470, 420, 364, 320]

y_range = split_seconds_sizes + sec_to_min_sizes

max2 = y_range


x = compl_range
y = max2


plt.ylim([0, 275574])

plt.xticks(fontsize=xytickFontsize, rotation=45)
plt.yticks(fontsize=xytickFontsize)

plt.ylabel("Total Amount", fontsize=labelsize)
#  fontsize=14)
plt.xlabel("Exposure Times in Seconds", fontsize=labelsize)


# # creating the bar plot
# plt.bar(courses, values, color ='maroon',
#         width = 0.4)

plt.bar(x, y, color="blue", label="Balanced Sample Size", width=0.4)

# plt.plot(x,y, label="FP", color="Red")

plt.legend(loc="upper right", prop={'size': legendsize})

# ----------------------------------------------------------------------------------------------------

fig.subplots_adjust(hspace=0.5)
fig.subplots_adjust(wspace=0.5)


plt.savefig(str(PATH_TO_HISTORIES) + "exp_time_plotsTOTALS.png",
            pad_inches=pad_inches, bbox_inches="tight", dpi=100)
# plt.savefig(str(OUT_PATH),  bbox_inches="tight")

plt.show()
