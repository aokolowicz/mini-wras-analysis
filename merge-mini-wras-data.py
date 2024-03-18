import argparse
import os
import pandas as pd

from helpers import (
    directory_tree,
    get_path,
    list_files,
    parse_arguments,
    print_directory_tree,
    path,
)


def merge_data(files, output_files, prefix):
    """
    Merges data from input files and saves it into output files.
    """
    for file in files:
        df = pd.read_table(
            get_path(t, file, prefix=prefix), skiprows=10, index_col=0
        )
        if 'nano' in output_files:
            # Nanoparticles are in the first 8 columns (from 10 to
            # 100 nm), without column 0 where the total counts for
            # all particles are
            nano = df.iloc[:, 1:9]
            nano.insert(
                loc=0,
                column='total nano',
                value=[nano.iloc[i].sum() for i in range(nano.shape[0])],
            )

        for output_file in output_files:
            data_to_save = nano if 'nano' in output_file else df
            # Ensure that the file is overwritten if it's the first
            # file being saved
            try:
                if files.index(file) == 0:
                    data_to_save.to_csv(
                        os.path.join(prefix, 'merged-data', output_file) + '.csv',
                        mode='w',
                    )
                else:
                    data_to_save.to_csv(
                        os.path.join(prefix, 'merged-data', output_file) + '.csv',
                        mode='a',
                        header=False,
                    )
            except OSError:
                os.mkdir(os.path.join(prefix, 'merged-data'))


# Set up command-line argument parser and parse arguments
args = parse_arguments(particulate=True)

# Get directory tree and files
t = directory_tree(path)
# print_directory_tree(t)

if args.particulate:
    files = list_files(t, 'location', 'M.dat')
    # Merge particulate matter data
    merge_data(files, ['PMs'], path)

else:
    files = list_files(t, 'location', 'C.dat')
    # Merge total and nano data
    merge_data(files, ['total', 'nano'], path)
