import argparse
import locale
import math
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns

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

# Ensure proper language formatting, e.g. months' names
locale.setlocale(locale.LC_ALL, 'en_US')

# Set up command-line argument parser
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

# Parse the command-line arguments
args = parser.parse_args()

# Variables to handle conditional logic based on command-line arguments
fig_suffix, fig_suffix2 = '', ''

# Logic to determine nanoparticles concentration
if args.nano:
    data_file = 'nano.csv'
    column_name = 'total nano'
    fig_suffix = '-nano'
else:
    data_file = 'total.csv'
    column_name = 'total counts'

# Logic to determine mass concentration
if args.mass:
    df = pd.read_csv(os.path.join(path, 'merged-data', data_file), index_col=0)
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
    df = pd.read_csv(os.path.join(path, 'merged-data', data_file), index_col=0)
    ylabel = 'Number concentration [particles/$\mathregular{cm^3}$]'
    coeff = 5e3 if df[column_name].max() < 4e4 else 1e4


# Dates from MINI-WRAS needs conversion to datetime format
df.index = pd.to_datetime(df.index, dayfirst=True)

# Default setting for data grouping on box charts (by month)
grouped_by = [df.index.year, df.index.month]

# Logic to plot box charts per day or month
if args.days:
    # Group data by days
    grouped_by.append(df.index.day)
    xlabels = df.index.strftime('%d/%m').unique()
    figsize = (240 * mm, 150 * mm)
    name_suffix = '-days'
else:
    xlabels = df.index.strftime('%B').unique()
    figsize = (150 * mm, 90 * mm)
    name_suffix = '-months'

boxplot_data = [group[column_name] for _, group in df.groupby(grouped_by)]

# Create a boxplot
plt.figure(figsize=figsize, dpi=300, layout='constrained')
sns.boxplot(data=boxplot_data, linewidth=0.7, flierprops={'marker': 'x'})

# X-axis
plt.xticks(range(len(xlabels)), xlabels, **tick_font)

# Y-axis
ylocator = ticker.LinearLocator(math.ceil(df[column_name].max() / coeff) + 1)
plt.gca().yaxis.set_major_locator(ylocator)
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(y_formatter_function))
plt.ylabel(ylabel, **label_font)

# Calculate y-axis limits
yupper = math.ceil(df[column_name].max() / coeff) * coeff
plt.ylim(0, yupper)

plt.title('2023', **title_font)

# Save figure if requested
fig_name = f'boxplots{name_suffix}{fig_suffix}{fig_suffix2}'
fig_path = os.path.join(path, 'merged-data', f'{fig_name}.png')
save_figure(fig_name, fig_path)
