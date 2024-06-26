import csv
import re
import pandas as pd
import os

# Define the file path
file_path = './data_sample.txt'
print(os.getcwd())
# Check if the file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"No such file or directory: '{file_path}'")

# Read the file using csv module
data = []
with open(file_path, 'r') as file:
    reader = csv.reader(file, delimiter=' ')
    for row in reader:
        # Skip comment lines
        if not row or row[0].startswith('#'):
            continue
        data.append(row)

df = pd.DataFrame(data)

df = df.drop(df.columns[[0,1,3,4,6,7,8,9,10,11,12,13,14,15,16]], axis=1)

new_columns = ['winner', 'turns']
move_count = 0
print(df.shape[1])
for col in range(2,df.shape[1]):
    if col % 2 == 0: # Black's Turn
        new_columns.append('W'+str(col//2))
    else:
        new_columns.append('B'+str(col//2))
    df.iloc[:,col] = df.iloc[:,col].apply(lambda x: re.sub(r'^(W|B)\d+\.', '', str(x)))

df.columns = new_columns
print(df)