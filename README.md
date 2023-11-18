# MINI-WRAS Analysis

This repository contains Python scripts designed to analyze and visualize particles (or nanoparticles) number and mass concentration data obtained from GRIMM MINI-WRAS 1.371 (Wide-Range Aerosol Spectrometer). Scripts processes data from the `sample-data` folder to compute and visualize particles (or nanoparticles) number or mass concentration trends.\
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

3. Run the script:

```bash
python number_concentration_filewise.py
```

choosing the right keyword and file extension in `list_files()` function or change the `path` variable in the `helpers.py` file.

```bash
files = list_files(dir_tree, 'location', '.dat')
```

4. Other scripts require merged data. Make sure to use the following script beforehand.

```bash
python merge-mini-wras-data.py 
```

5. You will be prompted regarding saving the generated figures.

## File Structure

- `boxplots.py`: Particle (or nanoparticle) number or mass concentration data on boxplots per months or days.
- `helpers.py`: Useful functions and constants.
- `merge-mini-wras-data.py`: MINI-WRAS data merging - `C.dat` (particle number concentration) and `M.dat` (particulate matter mass concentration)
- `number_concentration_filewise.py`: Particle and nanoparticle number concentration data visualization. Saving to the folders with data filewise.
- `sample-data/`: Directory containing data files used by the repository.

## How to contribute?

Feel free to contribute by opening an issue or submitting a pull request.

## License

This project is licensed under the [MIT License](LICENSE).