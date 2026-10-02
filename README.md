# Rainfall Analysis and Visualization Project

## Introduction
This project reads and processes daily rainfall data of Hong Kong Observatory, generates a series of analysed data with functions, predicts the data of future years and visualizes the analysed data for better interpret.

## Dependencies
To run the project, the Python libraries are required as follow:
- pandas
- numpy
- matplotlib

Running it in a virtual environment is recommended:
```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux / MacOS
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Directory
```text
rain_project/
├── main.py
├── config.py
├── data_read.py
├── data_process.py
├── data_integrate.py
├── csv_write.py
├── linear_fitting.py
├── datetime_decimal_transfer.py
├── rainfall_predict.py
├── visualize.py
├── requirements.txt
├── README.md
├── daily_HKO_RF_ALL.csv
└── output/
    ├── Annual_HKO_RF_Analysis_ALL.csv
    ├── Monthly_HKO_RF_Analysis_ALL.csv
    ├── Predicted_RF_Analysis.csv
    └── figures/
        ├── Annual_HK_Extreme_Rainy_Day(s)_Analysis_ALL.png
        ├── Annual_HK_Max_Wet_Days_Analysis_ALL.png
        ├── Annual_HK_Standard_Deviation_Analysis_ALL.png
        ├── Annual_HK_Max_Daily_Rainfall_Analysis_ALL.png
        ├── Annual_HK_Median_Analysis_ALL.png
        ├── Annual_HK_Max_Dry_Days_Analysis_ALL.png
        └── Annual_HK_Rainfall_Analysis_ALL.png
```

## Running Procedure
1. Activate the virtual environment
2. Run the following command in the terminal:
```bash
python3 main.py --input daily_HKO_RF_ALL.csv --out ./output
```

## License
This project is for learning and data analysis purposes only. No commercial use is intended.