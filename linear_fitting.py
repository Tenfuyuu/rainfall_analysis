import os
from datetime_decimal_transfer import datetime_to_decimal, decimal_to_datetime
from rainfall_predict import predict_rainfall

def linear_fitting(df):
    output_dir = "output"
    if "日期/Date" in df.columns:
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