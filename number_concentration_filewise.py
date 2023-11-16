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
    mm,
    label_font,
    tick_font,
)

# File handling (indexes in col=0, conversion needed)
dir_tree = directory_tree()
files = list_files(dir_tree, "location", ".dat")
for file in files:
    df = pd.read_table(get_path(dir_tree, file), skiprows=10, index_col=0)

    # Nanoparticles are in the first 8 columns (from 10 to 100 nm),
    # without column 0 where the total counts for all particles are
    nano = df.iloc[:, 1:9]
    nano.insert(
        loc=0,
        column="total nano",
        value=[sum(nano.iloc[i]) for i in range(nano.shape[0])],
    )
    df.index = pd.to_datetime(df.index, dayfirst=True)

    # Calculate average values
    avg_conc = df["total counts"].mean()
    avg_nano_conc = nano["total nano"].mean()

    # Plotting
    plt.figure(figsize=(160 * mm, 120 * mm), dpi=300)

    # Plot total particles concentration and average
    plt.plot(
        df.index,
        df["total counts"],
        "k.:",
        linewidth=1,
        label="Total particles",
    )
    plt.plot(
        [df.index[0], df.index[-1]],
        [avg_conc, avg_conc],
        "k-",
        linewidth=0.5,
        label="Total particles (mean)",
    )

    # Plot nanoparticles concentration and average
    plt.plot(
        df.index, nano["total nano"], "r.:", linewidth=1, label="Nanoparticles"
    )
    plt.plot(
        [df.index[0], df.index[-1]],
        [avg_nano_conc, avg_nano_conc],
        "r-",
        linewidth=0.5,
        label="Nanoparticles (mean)",
    )

    plt.legend(loc="best", fontsize=6)

    # X-axis
    xformatter = mdates.DateFormatter("%H:%M")
    xlower = df.index[0].floor("H")
    xupper = df.index[-1].ceil("H")
    plt.gca().xaxis.set_major_formatter(xformatter)
    plt.xticks(**tick_font)
    plt.xlabel("Time [hh:mm]", **label_font)
    plt.xlim(xlower, xupper)

    # Y-axis
    yformatter = ticker.FuncFormatter(y_formatter_function)
    ylocator = (
        ticker.LogLocator(base=10)
        if df["total counts"].max() > 4e4
        else ticker.LinearLocator()
    )
    plt.yscale('log') if df["total counts"].max() > 4e4 else plt.yscale(
        'linear'
    )
    plt.gca().yaxis.set_major_formatter(yformatter)
    plt.gca().yaxis.set_major_locator(ylocator)
    plt.ylabel(
        "Number concentration [particles/$\mathregular{cm^3}$]", **label_font
    )
    plt.yticks(**tick_font)

    # Calculate y-axis limits
    ylower = 100 if df["total counts"].max() > 4e4 else 0
    coeff = 1000 if df["total counts"].max() < 4e4 else 1e5
    yupper = math.ceil(df["total counts"].max() / coeff) * coeff
    plt.ylim(ylower, yupper)

    # Show average values on graph
    for avg, color in zip([avg_conc, avg_nano_conc], ["k", "r"]):
        plt.annotate(
            f"{avg:,.0f}".replace(",", " "),
            xy=(xupper, avg),
            xytext=(-6 * len(str(round(avg))), 4),
            fontsize=6,
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w", ec=color, alpha=0.8),
        )

    # Save figure if requested
    fig_name = f'Total Number and Nano ({file[:file.rfind("-")]})'
    fig_path = os.path.join(
        get_path(dir_tree, tell_parent(get_path(dir_tree, file))),
        f"{fig_name}.png"
    )
    save_figure(fig_name, fig_path)
