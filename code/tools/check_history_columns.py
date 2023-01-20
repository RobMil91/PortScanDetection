import pandas as pd
import sys

# debug tool, to command line allow for readin a pickle file, and print to console


def load_columns(target_path):

    history = pd.read_pickle(target_path)

    for column in history.columns:

        print(column)


TARGET_PATH_TO_HISTORY = str(sys.argv[1])


load_columns(TARGET_PATH_TO_HISTORY)
