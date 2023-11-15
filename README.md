# Mini WRAS Analysis

This repository contains a Python script named `number_concentration_daily.py`, which is designed to analyze and visualize number concentration data obtained from GRIMM MINI-WRAS 1.371 (Wide-Range Aerosol Spectrometer). The script processes data from the `sample-data` folder, specifically the `one_day-C.dat` file, to compute and visualize number concentration trends.

## Prerequisites

Ensure you have Python installed on your machine. Additionally, install the required libraries by running:

```bash
pip install pandas matplotlib
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
python number_concentration_daily.py
```

4. You will be prompted regarding saving the generated figure.

## File Structure

- `number_concentration_daily.py`: Python script for analyzing and visualizing number concentration data.
- `sample-data/`: Directory containing data files used by the repository.

## How to contribute?

Feel free to contribute by opening an issue or submitting a pull request.

## License

This project is licensed under the [MIT License](LICENSE).