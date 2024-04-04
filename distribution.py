import locale
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

from matplotlib import ticker
from helpers import (
    determine_data_file,
    directory_tree,
    get_path,
    num_to_mass,
    parse_arguments,
    save_figure,
    tell_parent,
    mm,
    path,
    ro,
    corr_fact,
    title_font,
    label_font,
    tick_font,
)


def main():
    # TODO: Add distribution creation from 1 .dat file

    # Ensure proper language formatting, e.g. months' names
    locale.setlocale(locale.LC_ALL, 'en_US')

    # Parse the command-line arguments
    args = parse_arguments(separately=True, mass=True)

    # Variables to properly name chart files
    fig_suffix, fig_suffix2 = '', ''

    # Determine the usage of total.csv or nano.csv
    data_file, _, fig_suffix = determine_data_file(args)

    # Load data
    dir_tree = directory_tree(path)
    df = pd.read_csv(get_path(dir_tree, data_file, path), index_col=0)

    # Conversion of MINI-WRAS dates to datetime format
    df.index = pd.to_datetime(df.index, dayfirst=True)

    # Logic for determining mass concentration
    if args.mass:
        df = num_to_mass(df, ro, corr_fact)
        title_prefix = 'Mass'
        fig_suffix2 = '-mass'
    else:
        title_prefix = 'Number'

    # Logic to plot distribution charts separately for each month
    if args.separately:
        # _ is used to ignore the year-month pairs that are generate by
        # dataframe.groupby(). We're not interested in the year-month pairs,
        # but only in the group which contains the data for each month.
        for _, group in df.groupby([df.index.year, df.index.month]):
            month = f'{group.first_valid_index():%B}'
            year = f'{group.first_valid_index():%Y}'
            title = f'{title_prefix} size distribution {month} {year}'
            name_suffix = f'-{group.first_valid_index():%B}-{year}'
            plot_distribution(group, title)

            # Save figure if requested
            parent = tell_parent(get_path(dir_tree, data_file, path))
            fig_name = f'distribution{name_suffix}{fig_suffix}{fig_suffix2}'
            fig_path = os.path.join(
                get_path(dir_tree, parent, path), f'{fig_name}.png'
            )
            save_figure(fig_name, fig_path)

    # Logic to plot one distribution chart
    else:
        title = f'{title_prefix} size distribution {df.first_valid_index():%Y}'
        name_suffix = ''
        plot_distribution(df, title)

        # Save figure if requested
        parent = tell_parent(get_path(dir_tree, data_file, path))
        fig_name = f'distribution{name_suffix}{fig_suffix}{fig_suffix2}'
        fig_path = os.path.join(
            get_path(dir_tree, parent, path), f'{fig_name}.png'
        )
        save_figure(fig_name, fig_path)


def plot_distribution(data, title):
    """Generate distibution chart."""

    # Prepare data for plotting
    averages, dims = process_data(data)

    plt.figure(figsize=(150 * mm, 90 * mm), dpi=300, layout='constrained')
    plt.bar(
        dims,
        averages.loc['frac'][1:],
        width=np.diff(dims + [(dims[-1] - dims[-2]) * 10]),
        color='gray',
        ec='k',
        align='edge',
    )
    # set_axes(averages.loc['frac'][1:].max())
    set_axes(30)

    # Set the title
    plt.title(title, **title_font)


def process_data(data):
    """Prepare data for the distribution chart."""

    # Calculate the values needed
    means = data.mean().to_frame().transpose()
    fractions = means.divide(means.iloc[:, 1:].sum(axis=1), axis=0) * 100

    # Concatenate the average and fractions DataFrames along the rows
    averages = pd.concat([means, fractions])
    # Update index labels
    averages.set_index(pd.Index(['mean', 'frac']), inplace=True)

    # Set particle diameters from MINI-WRAS
    dims = [int(x) for x in averages.columns[1:]]

    return averages, dims


def set_axes(ymax):
    """Set properties of the axes."""

    # Set X-axis to logaritmic
    plt.xscale('log')

    # X-axis
    xformatter = lambda x, pos: '{:,.0f}'.format(float(x)).replace(',', ' ')
    xlower = 1e0
    xupper = 1e5
    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(xformatter))
    plt.xticks(**tick_font)
    plt.xlabel('Particle size [nm]', **label_font)
    plt.xlim(xlower, xupper)

    # Y-axis
    ylower = 0
    # Round UP to the nearest 5
    coeff = 5
    yupper = math.ceil(ymax / coeff) * coeff
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(5.0))
    plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter())
    plt.yticks(**tick_font)
    plt.ylabel('Fraction [%]', **label_font)
    plt.ylim(ylower, yupper)


if __name__ == '__main__':
    main()
