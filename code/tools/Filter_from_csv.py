import pandas as pd

#example usage
# python3 Clean_attack_cic.py /datasets/pcaps/100k_chunks_friday/portscan_from_18-40_CET.csv  "172.16.0.1" "192.168.10.50"   /datasets/csv_lab/cic_start_1840_cleaned.csv

#modul needed to clean csv traffic from specific attacks that got injected

import sys

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

PATH_TO_CSV = str(sys.argv[1])

IP_SRC = str(sys.argv[2])

IP_DST = str(sys.argv[3])

OUT_PATH = str(sys.argv[4])

df = pd.read_csv(PATH_TO_CSV)
df = df.drop(df[((df["ip.src"] == IP_SRC) & (df["ip.dst"] == IP_DST))].index)

df.to_csv(sys.argv[4])