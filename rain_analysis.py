import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--input",
required=True, help="path to daily_HKO_RF_ALL.csv")
parser.add_argument("--out",
required=True, help="output folder")
args=parser.parse_args()

print("運行成功")
print("Run successfully")
print(f"輸入/Input: {args.input}")
print(f"輸出/Output: {args.out}")

def predict_rainfall(df, yrs_col="年/Year", val_col="數據/Value", future_years_count=5):
    x = np.array(df[yrs_col], dtype=float)
    y = np.array(df[val_col], dtype=float)

    a, b = np.polyfit(x, y, deg=1)

    last_year = int(x.max())
    future_years = np.arange(
        last_year + 1, last_year + 1 + future_years_count
    )

    predicted_values = a * future_years + b

    result_df = pd.DataFrame(
        {
            "年/Year": future_years.astype(int),
            "預測值/Predicted Values": np.round(predicted_values, 1),
        }
    )

    return result_df, a, b

def datetime_to_decimal(dt_series):
    dt_series = pd.to_datetime(dt_series, format="%d/%m/%Y")
    year = dt_series.dt.year
    day_of_year = dt_series.dt.dayofyear
    days_in_year = dt_series.dt.is_leap_year.map(
        lambda x: 366 if x else 365
    )

    return year + (day_of_year - 1) / days_in_year


def decimal_to_datetime(decimal_series):
    years = decimal_series.astype(int)
    remainder = decimal_series - years

    days_in_year = years.map(
        lambda y: 366 if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0) else 365
    )
    days = (remainder * days_in_year).round().astype(int)

    return [
        (pd.Timestamp(year=y, month=1, day=1) + pd.Timedelta(days=d)).strftime("%d/%m")
        for y, d in zip(years, days)
    ]

def data_reading(input_file):
    df = pd.read_csv(input_file, skiprows=2, skipfooter=5, engine='python')

    df["is_rainy"] = ~df["數值/Value"].isin(["0.0", 0.0])

    df["數值/Value"] = df["數值/Value"].replace("Trace", 0)
    df["數值/Value"] = pd.to_numeric(df["數值/Value"], errors="coerce").fillna(0)

    return df

def annual_total_rainfall(df):
    annual_total_rainfall = (
        df.groupby("年/Year", as_index=False)["數值/Value"]
        .sum()
        .round(1)
        .rename(columns={"數值/Value": "縂雨量/Rainfall"})
    )
    return annual_total_rainfall

def annual_maximum_rainfall(df):
    annual_maximum_rainfall_idx = (
        df.groupby("年/Year")["數值/Value"]
        .idxmax()
    )
    annual_maximum_rainfall = (
        df.loc[annual_maximum_rainfall_idx, ["年/Year", "月/Month", "日/Day", "數值/Value"]].copy()
    )
    annual_maximum_rainfall["日期/Date(DD/MM)"] = (
        annual_maximum_rainfall["日/Day"].astype(str)
        + "/"
        + annual_maximum_rainfall["月/Month"].astype(str)
    )
    annual_maximum_rainfall["最大日雨量/Max Daily Rainfall"] = annual_maximum_rainfall["數值/Value"].round(1)
    annual_maximum_rainfall = annual_maximum_rainfall[["年/Year", "最大日雨量/Max Daily Rainfall", "日期/Date(DD/MM)"]]
    annual_maximum_rainfall = annual_maximum_rainfall.reset_index(drop=True)
    return annual_maximum_rainfall

def annual_sm_rainfall(df):
    annual_sm_rainfall = (
        df.groupby("年/Year", as_index=False)["數值/Value"]
        .agg(**{
        "標準差/Standard Deviation": "std",
        "中位數/Median": "median"
    })
        .round(1)
    )
    return annual_sm_rainfall

def extreme_days(df):
    rainy_days = df[df["數值/Value"] >= 0.1]["數值/Value"]
    p95_threshold = rainy_days.quantile(0.95)
    df["is_extreme"] = df["數值/Value"] > p95_threshold

    extreme_days = (
        df.groupby("年/Year", as_index=False)["is_extreme"]
        .sum()
        .rename(columns={"is_extreme": "極端雨日/Extreme Rainy Day(s)"})
    )
    return extreme_days

def max_wet_dry(df):
    df["rain_block"] = (df["is_rainy"] != df["is_rainy"].shift()).cumsum()
    consecutive_counts = df.groupby(["年/Year", "rain_block", "is_rainy"]).size()

    def get_max_consecutive(flag):
        sub = consecutive_counts.xs(flag, level="is_rainy", drop_level=False)
        return sub.groupby("年/Year").max().reset_index(name="Max_Days")

    max_wet = get_max_consecutive(True).rename(
        columns={"Max_Days": "最大連續雨日/Max Wet Days"}
    )
    max_dry = get_max_consecutive(False).rename(
        columns={"Max_Days": "最大連續無雨日/Max Dry Days"}
    )

    max_wet_dry = max_wet.merge(max_dry, on="年/Year")
    return max_wet_dry

def monthly_avg_rainfall(df):
    monthly_total = (
        df.groupby(["年/Year", "月/Month"],as_index=False)["數值/Value"]
        .sum()
    )
    monthly_avg_rainfall = (
        monthly_total.groupby("月/Month", as_index=False)["數值/Value"]
        .mean()
        .round(1)
        .rename(columns={"數值/Value": "月均雨量/Monthly Rainfall"})
    )
    return monthly_avg_rainfall

def data_integration(df, functions):
    dfs = [func(df) for func in functions]
    df1 = dfs[0]
    dfr = [df.iloc[:, 1:] for df in dfs[1:]]
    dfs = [df1] + dfr
    df_analysed = pd.concat(dfs, axis=1)
    return df_analysed

def csv_generation(df_analysed, csv_name, title_text):
    output_dir = "output"
    output_file = os.path.join(output_dir, csv_name)

    with open(output_file, "w", encoding="utf-8-sig") as f:
        f.write(title_text)

    df_analysed.to_csv(output_file, mode="a", index=False, encoding="utf-8-sig")
    print("已完成的文件/Generated File：", output_file)

def linear_fitting(df):
    output_dir = "output"
    if "日期/Date(DD/MM)" in df.columns:
        df = df.reset_index(drop=True)
        df["日期/Date"] = df["日期/Date"].astype(str) + "/" + df["年/Year"].astype(str)
        df["日期/Date"] = datetime_to_decimal(df["日期/Date"])
        date_absent = False

    val_cols = [col for col in df.columns if col != "年/Year"]

    Flag = False
    abs = []

    for col in val_cols:
        sub_df, a, b = predict_rainfall(df, val_col=col)
        abs.append((a, b))
        if Flag == False:
            predicted_output = sub_df.rename(columns={"預測值/Predicted Values": "縂雨量/Rainfall"})
            Flag = True
        else:
            predicted_output[col] = sub_df["預測值/Predicted Values"].values

    if not date_absent:
        predicted_output["日期/Date"] = decimal_to_datetime(predicted_output["日期/Date"])
        predicted_output["日期/Date"] = predicted_output["日期/Date"]

    output_file_predicted = os.path.join(output_dir, "Predicted_RF_Analysis.csv")

    predicted_output.to_csv(output_file_predicted, index=False, encoding="utf-8-sig")
    print("已完成的文件/Generated File：", output_file_predicted)
    return predicted_output, abs

def visualization(column, df, df2, ab, ignore_index=True):
    output_dir = "output"

    column = str(column).split("/")[-1]
    
    plt.figure(figsize=(12, 6), dpi=150)
    plt.plot(
        df["年/Year"],
        df[column],
        color='#1f77b4',
        alpha=0.3,
        linewidth=1,
        label=f'Year-{column}',
    )
    plt.scatter(
        df["年/Year"],
        df[column],
        color='#1f77b4',
        alpha=0.6,
        s=15,
    )

    df['Rolling_10Y'] = df[column].rolling(window=10, min_periods=1).mean()
    plt.plot(
        df["年/Year"],
        df['Rolling_10Y'],
        color='#2ca02c',
        linewidth=2.5,
        label='10-Year Moving Average',
    )

    ab = list(ab)
    a = ab[0][0]
    b = ab[0][1]
    X_hist = df[['年/Year']].values
    y_fit = a * X_hist + b
    plt.plot(
        df['年/Year'],
        y_fit,
        color='#d62728',
        linestyle='--',
        linewidth=2,
        label='Linear Regression Fit',
    )

    df3 = pd.concat([df, df2], ignore_index=True)
    plt.plot(
        df3["年/Year"],
        df3[column],
        color='#ff7f0e',
        linestyle=':',
        linewidth=2,
    )
    plt.scatter(
        df2["年/Year"],
        df2[column],
        color='#ff7f0e',
        marker='^',
        s=80,
        zorder=5,
        label='5-Year Prediction',
    )

    plt.title(
        'Hong Kong Annual Rainfall Historical Trend & 5-Year Forecast',
        fontsize=14,
        fontweight='bold',
        pad=15,
    )
    plt.xlabel('年/Year', fontsize=11)
    plt.ylabel(f'{column}', fontsize=11)

    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9)

    plt.tight_layout()

    column = str(column)
    column = column.replace("/", "_")

    plt.savefig(f'{output_dir}/Annual_HK_{column}_Analysis_ALL.png', dpi=300)

    print(f"已完成的圖表/Generated Figure: Annual_HK_{column}_Analysis_ALL.png")

def main():
    input_file = "daily_HKO_RF_ALL.csv"
    df = data_reading(input_file)
    functions = [
        annual_total_rainfall,
        annual_maximum_rainfall,
        annual_sm_rainfall,
        extreme_days,
        max_wet_dry]
    annual_df_analysed = data_integration(df, functions)
    monthly_df_analysed = data_integration(df, [monthly_avg_rainfall])
    csv_generation(annual_df_analysed, "Annual_HKO_RF_Analysis_ALL.csv", "年雨分析\nAnnual Rainfall Analysis\n")
    csv_generation(monthly_df_analysed, "Monthly_HKO_RF_Analysis_ALL.csv", "月雨分析\nMonthly Rainfall Analysis\n")
    df2, abs = linear_fitting(annual_df_analysed)
    column_list = list(annual_df_analysed[1:])
    col_abs = [{column_list[n + 1]: abs[n]} for n in (0,7)]
    for col_ab in col_abs:
        column = col_ab.keys()
        ab = col_ab.values()
        visualization(column, annual_df_analysed, df2, ab)

if __name__ == "__main__":
    main()
