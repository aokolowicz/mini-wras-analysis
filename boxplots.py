import argparse
import locale
import math
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
import sys

from matplotlib import ticker
from helpers import (
    num_to_mass,
    save_figure,
    y_formatter_function,
    mm,
    path,
    ro,
    corr_fact,
    title_font,
    label_font,
    tick_font,
)


def main():
    # Ensure proper language formatting, e.g. months' names
    locale.setlocale(locale.LC_ALL, 'en_US')

    # Parse the command-line arguments
    args = parse_arguments()

    # Variables to properly name chart files
    fig_suffix, fig_suffix2 = '', ''

    # Determine the usage of total.csv or nano.csv
    data_file, column_name, fig_suffix = determine_data_file(args)

    # Load data
    df = pd.read_csv(os.path.join(path, 'merged-data', data_file), index_col=0)

    # Conversion of MINI-WRAS dates to datetime format
    df.index = pd.to_datetime(df.index, dayfirst=True)

    # Logic for determining mass concentration
    if args.mass:
        df = num_to_mass(df, ro, corr_fact)
        column_name = 'total mass'
        fig_suffix2 = '-mass'
        ylabel = 'Mass concentration [$\mathregular{mg/m^3}$]'

        # Determine coefficient to calculate ylim based on the maximum
        # value in the column
        if df[column_name].max() < 0.2:
            coeff = 0.01
        elif df[column_name].max() < 2:
            coeff = 0.1
        else:
            coeff = 1

    else:
        ylabel = 'Number concentration [particles/$\mathregular{cm^3}$]'
        coeff = 5e3 if df[column_name].max() < 4e4 else 1e4

    # Logic for plotting box charts by day or month
    if args.days:
        # Ensure proper using of flags
        if args.days and args.separately:
            sys.exit('Only one flag can be used: -d or -s.')

        title = f'{df.first_valid_index():%Y}'
        xticks_labels = df.index.strftime('%d/%m').unique()
        figsize = (240 * mm, 150 * mm)
        name_suffix = '-days'

        # Plot data grouped by days
        plot_box_chart(
            df,
            column_name,
            [df.index.year, df.index.month, df.index.day],
            figsize,
            title,
            xticks_labels,
            ylabel,
            args.mass,
            coeff,
        )

    # Logic to plot box charts by day and save figures separately for each month
    elif args.separately:
        figsize = (150 * mm, 90 * mm)

        for _, group in df.groupby([df.index.year, df.index.month]):
            title = f'{group.first_valid_index():%B} {group.first_valid_index():%Y}'
            xticks_labels = group.index.strftime('%a, %d').unique()
            name_suffix = '-' + title.replace(' ', '-')

            # Plot data grouped by days for each month
            plot_box_chart(
                group,
                column_name,
                [group.index.year, group.index.month, group.index.day],
                figsize,
                title,
                xticks_labels,
                ylabel,
                args.mass,
                coeff,
            )

            # Save figure if requested
            fig_name = f'boxplots{name_suffix}{fig_suffix}{fig_suffix2}'
            fig_path = os.path.join(path, 'merged-data', f'{fig_name}.png')
            save_figure(fig_name, fig_path)

        # Exit to avoid saving the plots again
        sys.exit()

    # Logic for plotting box charts by month
    else:
        title = f'{df.first_valid_index():%Y}'
        xticks_labels = df.index.strftime('%B').unique()
        figsize = (150 * mm, 90 * mm)
        name_suffix = '-months'

        # Plot data grouped by month
        plot_box_chart(
            df,
            column_name,
            [df.index.year, df.index.month],
            figsize,
            title,
            xticks_labels,
            ylabel,
            args.mass,
            coeff,
        )

    # Save figure when there is the only one
    fig_name = f'boxplots{name_suffix}{fig_suffix}{fig_suffix2}'
    fig_path = os.path.join(path, 'merged-data', f'{fig_name}.png')
    save_figure(fig_name, fig_path)


def determine_data_file(args):
    """
    Logic for determining particles or nanoparticles concentration
    """
    if args.nano:
        return 'nano.csv', 'total nano', '-nano'
    else:
        return 'total.csv', 'total counts', ''


def parse_arguments():
    """
    Set up command-line argument parser
    """
    parser = argparse.ArgumentParser(
        description='Create boxplots for data grouped by month'
    )
    # Define optional command-line arguments
    parser.add_argument(
        '-d', '--days', action='store_true', help='Plot boxplots per day'
    )
    parser.add_argument(
        '-m', '--mass', action='store_true', help='Process mass data'
    )
    parser.add_argument(
        '-n', '--nano', action='store_true', help='Process nanoparticle data'
    )
    parser.add_argument(
        '-s',
        '--separately',
        action='store_true',
        help='Save separate boxplot charts for each month',
    )
    return parser.parse_args()


def plot_box_chart(
    dataframe,
    column,
    grouped_by,
    figsize,
    title,
    xticks_labels,
    ylabel,
    mass=False,
    coeff=1,
):
    """
    Plots a boxplot from the provided dataframe based on given parameters.
    """
    # Group data by grouped_by variable
    boxplot_data = [
        group[column] for _, group in dataframe.groupby(grouped_by)
    ]

    # Create a boxplot
    plt.figure(figsize=figsize, dpi=300, layout='constrained')
    sns.boxplot(data=boxplot_data, linewidth=0.7, flierprops={'marker': 'x'})

    # X-axis
    plt.xticks(range(len(xticks_labels)), xticks_labels, **tick_font)

    # Y-axis
    if mass:
        ylocator = ticker.LinearLocator(
            math.ceil(dataframe[column].max() / coeff) + 1
        )
        plt.gca().yaxis.set_major_locator(ylocator)
    
    plt.ylabel(ylabel, **label_font)
    plt.gca().yaxis.set_major_formatter(
        ticker.FuncFormatter(y_formatter_function)
    )

    # Calculate y-axis limits
    yupper = math.ceil(dataframe[column].max() / coeff) * coeff
    plt.ylim(0, yupper)

    plt.title(title, **title_font)


if __name__ == '__main__':
    main()
