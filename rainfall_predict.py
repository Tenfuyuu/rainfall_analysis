import numpy as np
import pandas as pd

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