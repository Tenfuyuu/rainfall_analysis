import config
from data_read import data_reading
from data_process import (
    annual_total_rainfall,
    annual_maximum_rainfall,
    annual_sm_rainfall,
    extreme_days,
    max_wet_dry,
    monthly_avg_rainfall,
)
from data_integrate import data_integration
from csv_write import csv_generation
from linear_fitting import linear_fitting
from visualize import visualization

input_file = config.args.input
output_dir = config.args.out

def main():
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
    col_abs = [{col: ab} for col, ab in zip(column_list[1:], abs)]
    del col_abs[2]
    for col_ab in col_abs:
        column = col_ab.keys()
        ab = col_ab.values()
        visualization(column, annual_df_analysed, df2, ab, config.figures_dir)

if __name__ == "__main__":
    main()