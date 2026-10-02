import pandas as pd

def data_reading(input_file):
    df = pd.read_csv(input_file, skiprows=2, skipfooter=5, engine='python')

    df["is_rainy"] = ~df["數值/Value"].isin(["0.0", 0.0])

    df["數值/Value"] = df["數值/Value"].replace("Trace", 0)
    df["數值/Value"] = pd.to_numeric(df["數值/Value"], errors="coerce").fillna(0)

    return df