import math
import matplotlib.pyplot as plt
import os
import pandas as pd

# Define the path to the data
path = r'C:\Users\Adrian\Desktop\repos\mini-wras-analysis\sample-data'

# Define constants
mm = 1 / 25.4  # Conversion factor from inches to mm
ro = 1680  # kg/m3
corr_fact = 1.48  # Correct the calculated mass concentration

# Define font parameters
title_font = {'fontname': 'Verdana', 'fontsize': 14, 'weight': 'bold'}
label_font = {'fontname': 'Verdana', 'fontsize': 8, 'weight': 'bold'}
tick_font = {'fontname': 'Verdana', 'fontsize': 8}


def directory_tree(path=os.getcwd()):
    """
    Generate a nested dictionary representing the directory
    tree.
    """
    tree = {}
    # Iterate over items (folders and files) in the root directory
    for item in os.listdir(path):
        # Create the full path to the current item
        item_path = os.path.join(path, item)

        # Check if the current item is a directory
        if os.path.isdir(item_path):
            # If it's a directory, recursively generate the tree for
            # the subdirectory
            tree[item] = directory_tree(item_path)
        else:
            # If it's a file, add it to the tree with a value of None
            tree[item] = None

    return tree


def get_path(tree, tree_item, prefix=os.getcwd()):
    """
    Recursively searche for a target file in a nested directory
    tree.
    """
    for item, subtree in tree.items():
        # Construct the full path
        item_path = os.path.join(prefix, item)

        # Check if 'item' matches the target_file (base case)
        if item == tree_item:
            return item_path
        # Check if 'subtree' is a subdirectory (a nested dictionary)
        elif isinstance(subtree, dict):
            # Recursively search the subdirectory
            result = get_path(subtree, tree_item, item_path)
            if result is not None:
                return result

    # If target file is not found in this level of the directory tree
    return None


def list_files(tree, keyword, file_extension):
    """
    Recursively search the nested directory tree for files that
    match a keyword and file extension.
    """
    files = []
    # Iterate through items (keys and values) in the current
    # directory level
    for item, subtree in tree.items():
        # If the item is a file
        if subtree is None:
            # Check if it matches the keyword and file extension
            if item.lower().find(keyword.lower()) > -1 and item.endswith(
                file_extension
            ):
                files.append(item)
        else:
            result = list_files(subtree, keyword, file_extension)
            if len(result) > 0:
                files.extend(result)

    return files


def num_to_mass(dataframe, ro, conv_fact=1):
    """
    Convert number concentrations in 1/cm^3 to mass concentrations in mg/m^3
    using provided density.
    """
    # Create an empty DataFrame with the same index as the input DataFrame
    mass_df = pd.DataFrame(index=dataframe.index)

    # Loop through columns in the input DataFrame
    for col in dataframe:
        # Try to convert column name col (str) to diameter d (int).
        # Omit col='total counts'.
        try:
            d = int(col) * 1e-9  # Convert nanometers to meters
        except ValueError:
            continue

        # Calculate the volume of a particle using the diameter d
        V = 4 / 3 * math.pi * (d / 2) ** 3  # m^3

        # Calculate the total volume of particles of a particular size
        # as pandas.Series and convert to m^3
        V_total = V * dataframe[col] * 1e6  # m^3

        # Calculate the mass of particles using the density ro
        # as pandas.Series and convert to mg
        mass = V_total * ro * 1e6  # mg

        # Add the calculated mass pandas.Series to the mass DataFrame
        mass_df[col] = mass * conv_fact  # Apply conversion factor

    # Calculate the total mass for each row and insert the 'total mass' column
    mass_df.insert(
        loc=0,
        column='total mass',
        value=[mass_df.iloc[i].sum() for i in range(mass_df.shape[0])],
    )

    # Return the DataFrame containing mass concentrations
    return mass_df


def print_directory_tree(tree, indent=0):
    """
    Print a nested dictionary representing the directory tree
    with proper indents.
    """
    for item, subtree in tree.items():
        if subtree is None:
            print('  ' * indent + '- ' + item)
        else:
            print('  ' * indent + '+ ' + item)
            print_directory_tree(subtree, indent + 1)


def save_figure(fig_name, fig_path):
    """
    Prompt user to save the current figure.
    """
    save_figure = input("Save figure? (Y/n)\n")
    if save_figure.lower() != "n":
        plt.savefig(fig_path)
        print(f"Figure saved as {fig_name}.png")
    else:
        print("Figure not saved.")


def tell_parent(item_path):
    """
    Extract the name of the parent folder from the given
    item path.
    """
    # Find the index of the last backslash in the item_path
    end = item_path.rfind('\\')
    # Find the index of the second-to-last backslash, starting
    # from the beginning of the string
    start = item_path.rfind('\\', 0, end) + 1
    # Return parent's folder name if both start and end indices
    # are valid
    if start > 0 and end > 0 and end > start:
        return item_path[start:end]
    else:
        return None


def y_formatter_function(x, pos):
    """
    Custom formatter function for y-axis ticks.
    """
    if x == 0:
        return '{:,}'.format(int(x))
    elif x < 0.01:
        return '{:,.3f}'.format(float(x))
    elif x < 0.1:
        return '{:,.2f}'.format(float(x))
    elif x < 1:
        return '{:,.1f}'.format(float(x))
    else:
        return '{:,}'.format(int(x))


if __name__ == '__main__':
    # One level up from the current working directory
    tree = directory_tree(os.getcwd()[: os.getcwd().rfind('\\')])
    print_directory_tree(tree)
