import argparse
import os
import pandas as pd

from helpers import (
    directory_tree,
    get_path,
    list_files,
    print_directory_tree,
    path,
)


def merge_data(files, output_files):
    """
    Merges data from input files and saves it into output files.
    """
    for file in files:
        df = pd.read_table(
            get_path(t, file, prefix=path), skiprows=10, index_col=0
        )
        if 'nano' in output_files:
            # Nanoparticles are in the first 8 columns (from 10 to 100 nm),
            # without column 0 where the total counts for all particles are
            nano = df.iloc[:, 1:9]
            nano.insert(
                loc=0,
                column='total nano',
                value=[nano.iloc[i].sum() for i in range(nano.shape[0])],
            )

        for output_file in output_files:
            data_to_save = df if 'total' in output_file else nano

            # Ensure that the file is overwritten if it's the first file being saved
            if files.index(file) == 0:
                data_to_save.to_csv(
                    os.path.join(path, 'merged-data', output_file) + '.csv',
                    mode='w',
                )
            else:
                data_to_save.to_csv(
                    os.path.join(path, 'merged-data', output_file) + '.csv',
                    mode='a',
                    header=False,
                )


# Set up command-line argument parser
parser = argparse.ArgumentParser(description='Merge data according to its type')

# Define optional command-line arguments
parser.add_argument(
    '-p',
    '--particulate',
    action='store_true',
    help='Merge particulate matter (PM) data',
)

# Parse the command-line arguments
args = parser.parse_args()

# Get directory tree and files
t = directory_tree(path)
# print_directory_tree(t)

if args.particulate:
    files = list_files(t, 'location', 'M.dat')
    # Merge particulate matter data
    merge_data(files, ['PMs'])

else:
    files = list_files(t, 'location', 'C.dat')
    # Merge total and nano data
    merge_data(files, ['total', 'nano'])
