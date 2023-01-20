from numpy import NaN
import math

# for debug info


def print_general_info(trace_dataframe):
    print(trace_dataframe.head())
    print(trace_dataframe.info(verbose=True))
    print("unlabeled_trace_dataframe[Assigned_Label].value_counts()")
    print(trace_dataframe["Assigned_Label"].value_counts())

# this function is needed to label all traffic in direction of victim as 1 (port scan)


def generate_labels_one_target(unlabeled_dataframe, ip_dst_column, victim_ip):

    unlabeled_dataframe["Assigned_Label"] = 0
    unlabeled_dataframe.loc[(
        unlabeled_dataframe[ip_dst_column] == victim_ip), "Assigned_Label"] = 1

# function is needed to remove float from df


def convert_port_to_int(float_value):
    if (math.isnan(float_value)):
        return 0
    else:
        return int(float_value)

# function is needed to label if source is attacker and victim is destination


def generate_labels_src_to_dst(unlabeled_df, ip_src_col, ip_dst_col, attacker, victim):

    unlabeled_df["Assigned_Label"] = 0
    unlabeled_df.loc[(unlabeled_df[ip_src_col] == attacker) & (
        unlabeled_df[ip_dst_col] == victim), "Assigned_Label"] = 1
