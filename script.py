import json
import csv
import pandas as pd


filename = 'output/part-r-00000'
#filename = 'data.txt'
field_names = ['key', 'links']


dict1 = {}


with open(filename) as fh:

    for line in fh:
        array = []

        command, description = line.strip().split(None, 1)
        dict1[command] = description.strip().split()

a_file = open("index.csv", "w")
writer = csv.writer(a_file)
for key, value in dict1.items():
    writer.writerow([key, value])

a_file.close()
df = pd.read_csv("index.csv", header=None)
df.to_csv("index.csv", header=["key", "Links"], index=False)

