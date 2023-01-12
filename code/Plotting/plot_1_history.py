import pandas as pd
from matplotlib import pyplot as plt
import sys
#debug function to identify one history all columns are plotted

def plot_selected(history_column, column_name, out_path):

  print("plotting " + str(column_name))
  df = history_column
  df.plot(figsize=(8,5))
  plt.title(column_name)
  plt.ylabel(column_name)
  plt.xlabel('epoch')
  plt.legend([column_name], loc='lower right')

  save_path = out_path + column_name + ".jpg"
  plt.savefig(save_path)


def load_metric_jpg(target_path, out_path):


  history = pd.read_pickle(target_path)

  for column in history.columns:

    plot_selected(history[column], column, out_path)

  return history




#-----------------------------------actual code------------------------------------------


PATH_TO_HISTORY = str(sys.argv[1])

OUT_PATH = str(sys.argv[2])

load_metric_jpg(PATH_TO_HISTORY, OUT_PATH)