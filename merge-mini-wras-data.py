import os
import pandas as pd

from helpers import directory_tree, get_path, list_files, print_directory_tree, path

# Get directory tree and files
t = directory_tree(path)
# print_directory_tree(t)
files = list_files(t, 'location', 'C.dat')

# Loop through the files and process data
for file in files:
    df = pd.read_table(get_path(t, file, prefix=path), skiprows=10, index_col=0)
    # Nanoparticles are in the first 8 columns (from 10 to 100 nm),
    # without column 0 where the total counts for all particles are
    nano = df.iloc[:, 1:9]
    nano.insert(
        loc=0,
        column='total nano',
        value=[nano.iloc[i].sum() for i in range(nano.shape[0])],
    )

    # Ensure that the file is overwritten
    if files.index(file) == 0:
        df.to_csv(os.path.join(path, 'merged-data', 'total.csv'), mode='w')
        nano.to_csv(os.path.join(path, 'merged-data', 'nano.csv'), mode='w')
    else:
        df.to_csv(
            os.path.join(path, 'merged-data', 'total.csv'), mode='a', header=False
        )
        nano.to_csv(os.path.join(path, 'merged-data', 'nano.csv'), header=False)
