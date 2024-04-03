import math
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import os
import pandas as pd

from matplotlib import ticker
from helpers import (
    directory_tree,
    get_path,
    list_files,
    save_figure,
    tell_parent,
    y_formatter_function,
    print_directory_tree,
    mm,
    label_font,
    tick_font,
    path,
)


def main():
    # File handling, indexes in col=0, conversion needed in process_file()
    dir_tree = directory_tree(path)
    files = list_files(dir_tree, 'location', 'C.dat')  # C.dat for number concentration
    for file in files:
        df, nano = process_file(dir_tree, file)

        # Calculate average values
        avg_conc = df['total counts'].mean()
        avg_nano_conc = nano['total nano'].mean()

        plot_data(df, nano, avg_conc, avg_nano_conc)
        _, xupper, _, _ = set_axes(df)
        annotate_averages(avg_conc, avg_nano_conc, xupper)

        parent = tell_parent(get_path(dir_tree, file, path))
        # print_directory_tree(dir_tree)
        print(f"{parent}: ", get_path(dir_tree, parent, path), "\n\n")

        # Save figure if requested
        fig_name = generate_fig_name(file)
        fig_path = os.path.join(
            get_path(
                dir_tree, tell_parent(get_path(dir_tree, file, path)), path
            ),
            f'{fig_name}.png',
        )
        save_figure(fig_name, fig_path)


def process_file(tree, file):
    """Read data to the pandas.DataFrame and prepare for analysis."""

    df = pd.read_table(get_path(tree, file, path), skiprows=10, index_col=0)

    # Nanoparticles are in the first 8 columns (from 10 to 100 nm),
    # without column 0 where the total counts for all particles are
    nano = df.iloc[:, 1:9]
    nano.insert(
        loc=0,
        column='total nano',
        value=nano.sum(axis=1),
    )

    # Convert index to datetime
    df.index = pd.to_datetime(df.index, dayfirst=True)

    return df, nano


def plot_data(df, nano, avg_conc, avg_nano_conc):
    """Generate plot."""

    plt.figure(figsize=(160 * mm, 120 * mm), dpi=300)

    # Plot total particles concentration and average
    plt.plot(
        df.index,
        df['total counts'],
        'k.:',
        linewidth=1,
        label='Total particles',
    )
    plt.plot(
        [df.index[0], df.index[-1]],
        [avg_conc, avg_conc],
        'k-',
        linewidth=0.5,
        label='Total particles (mean)',
    )

    # Plot nanoparticles concentration and average
    plt.plot(
        df.index, nano['total nano'], 'r.:', linewidth=1, label='Nanoparticles'
    )
    plt.plot(
        [df.index[0], df.index[-1]],
        [avg_nano_conc, avg_nano_conc],
        'r-',
        linewidth=0.5,
        label='Nanoparticles (mean)',
    )

    plt.legend(loc='best', fontsize=6)


def set_axes(df):
    """Set properties of the axes."""

    # X-axis
    xformatter = mdates.DateFormatter('%H:%M')
    xlower = df.index[0].floor('H')
    xupper = df.index[-1].ceil('H')
    plt.gca().xaxis.set_major_formatter(xformatter)
    plt.xticks(**tick_font)
    plt.xlabel('Time [hh:mm]', **label_font)
    plt.xlim(xlower, xupper)

    # Y-axis
    yformatter = ticker.FuncFormatter(y_formatter_function)
    ylocator = (
        ticker.LogLocator(base=10)
        if df['total counts'].max() > 4e4
        else ticker.LinearLocator()
    )
    plt.yscale('log') if df['total counts'].max() > 4e4 else plt.yscale(
        'linear'
    )
    plt.gca().yaxis.set_major_formatter(yformatter)
    plt.gca().yaxis.set_major_locator(ylocator)
    plt.ylabel(
        'Number concentration [particles/$\mathregular{cm^3}$]', **label_font
    )
    plt.yticks(**tick_font)

    # Calculate y-axis limits
    ylower = 100 if df['total counts'].max() > 4e4 else 0
    coeff = 1000 if df['total counts'].max() < 4e4 else 1e5
    yupper = math.ceil(df['total counts'].max() / coeff) * coeff
    plt.ylim(ylower, yupper)

    return xlower, xupper, ylower, yupper


def annotate_averages(avg_conc, avg_nano_conc, xupper):
    """Show average values on graph."""

    for avg, color in zip([avg_conc, avg_nano_conc], ['k', 'r']):
        plt.annotate(
            f'{avg:,.0f}'.replace(',', ' '),
            xy=(xupper, avg),
            xytext=(-6 * len(str(round(avg))), 4),
            fontsize=6,
            textcoords='offset points',
            bbox=dict(boxstyle='round', fc='w', ec=color, alpha=0.8),
        )


def generate_fig_name(file):
    return f"Total Number and Nano ({file[:file.rfind('-')]})"


if __name__ == '__main__':
    main()
