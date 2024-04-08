import os

from helpers import (
    directory_tree,
    get_path,
    list_files,
    parse_arguments,
    print_directory_tree,
    process_file,
    tell_parent,
    path,
)


def main():
    # Set up command-line argument parser and parse arguments
    args = parse_arguments(particulate=True)

    # Get directory tree and files
    t = directory_tree(path)
    # print_directory_tree(t)

    if args.particulate:
        files = list_files(t, 'location', 'M.dat')
        # Merge particulate matter data
        merge_data(t, files, ['PMs'], path)

    else:
        files = list_files(t, 'location', 'C.dat')
        # Merge total and nano data
        merge_data(t, files, ['total', 'nano'], path)


def merge_data(tree, files, output_files, prefix):
    """Merge data from input `files` and save into `output files`."""

    for file in files:
        # Find higher level directories
        parent1 = tell_parent(get_path(tree, file, prefix=prefix))
        parent2 = tell_parent(get_path(tree, parent1, prefix=prefix))
        px2 = get_path(tree, parent2, prefix=prefix)

        # Load data
        # For PMs, nano DataFrame is unnecessary due to data structure
        df, nano = process_file(tree, file)

        if not os.path.isdir(os.path.join(px2, 'merged-data')):
            os.mkdir(os.path.join(px2, 'merged-data'))

        for output_file in output_files:
            data_to_save = nano if 'nano' in output_file else df
            # Ensure that the file is overwritten if it's the first
            # file being saved
            if files.index(file) == 0:
                data_to_save.to_csv(
                    os.path.join(px2, 'merged-data', output_file) + '.csv',
                    mode='w',
                )
            else:
                data_to_save.to_csv(
                    os.path.join(px2, 'merged-data', output_file) + '.csv',
                    mode='a',
                    header=False,
                )


if __name__ == '__main__':
    main()
