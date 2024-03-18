# MINI-WRAS Analysis
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This repository contains Python scripts designed to analyze and visualize **particles (or nanoparticles) number and mass concentration** data obtained from GRIMM MINI-WRAS 1.371 (Wide-Range Aerosol Spectrometer). Scripts process data from the `sample-data` folder. The directory and file information are stored and managed efficiently using a recursive tree structure implemented through the `directory_tree()` function, enabling quick access and exploration of the directory hierarchy.\
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

3. Run the script by selecting the appropriate keyword and file extension within the `list_files()` function. For example, use `list_files(dir_tree, 'day', 'C.dat')` to specify the directory tree `dir_tree`, filter files by the keyword `'day'`, and limit results to files with the `'C.dat'` extension.

```bash
python number_concentration_filewise.py
```

4. Before using other scripts that require merged data, update the `path` variable in `helpers.py` and use the specified script first.

```bash
python merge-mini-wras-data.py [-p]
```

5. After that, scripts that require merged data can be used.

```bash
python boxplots.py [-d -m -n -s]
```

6. You will be prompted regarding saving the generated figures.

## File Structure

- `helpers.py`: Useful functions and constants.
- `sample-data/`: Directory containing data files used by the repository.
- `number_concentration_filewise.py`: Particle and nanoparticle number concentration data visualization. Saving to the folders with data filewise.
- `merge-mini-wras-data.py`: MINI-WRAS data merging - `C.dat` (particle number concentration) and `M.dat` (particulate matter mass concentration)
- `boxplots.py`: Particle (or nanoparticle) number or mass concentration data on boxplots per months or days.

## How to contribute?

Feel free to contribute by opening an issue or submitting a pull request.

## License

This project is licensed under the [MIT License](LICENSE).