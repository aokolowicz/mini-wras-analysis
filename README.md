# MINI-WRAS Analysis

This repository contains a Python script named `number_concentration_filewise.py`, which is designed to analyze and visualize number concentration data obtained from GRIMM MINI-WRAS 1.371 (Wide-Range Aerosol Spectrometer). The script processes data from the `sample-data` folder, specifically the `one_day_sample-C.dat` file, to compute and visualize number concentration trends.\
**Feel free to use and customize it to analyze your own data!**

## Prerequisites

Ensure you have Python installed on your machine. Additionally, install the required libraries by running:

```bash
pip install pandas matplotlib seaborn
```

## Usage

1. Clone this repository to your local machine:

```bash
git clone https://github.com/aokolowicz/mini-wras-analysis.git
```

2. Navigate to the repository folder:

```bash
cd mini-wras-analysis
```

3. Run the script choosing the right keyword and file extension in `list_files()` function, e.g.:

```bash
files = list_files(dir_tree, "location", ".dat")
```

or change the `path` variable in `helpers.py`.

```bash
python number_concentration_filewise.py
```

4. You will be prompted regarding saving the generated figures.

## File Structure

- `boxplot-months.py`: Python script for analyzing and visualizing number concentration data on boxplots per months.
- `helpers.py`: Python script with useful functions and constants.
- `merge-mini-wras-data.py`: Python script for MINI-WRAS data merging.
- `number_concentration_filewise.py`: Python script for analyzing and visualizing number concentration data. Saving to the folders with data filewise.
- `sample-data/`: Directory containing data files used by the repository.

## How to contribute?

Feel free to contribute by opening an issue or submitting a pull request.

## License

This project is licensed under the [MIT License](LICENSE).