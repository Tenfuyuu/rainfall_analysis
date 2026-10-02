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
    annual_maximum_rainfall["日期/Date"] = (
        annual_maximum_rainfall["日/Day"].astype(str)
        + "/"
        + annual_maximum_rainfall["月/Month"].astype(str)
    )
    annual_maximum_rainfall["最大日雨量/Max Daily Rainfall"] = annual_maximum_rainfall["數值/Value"].round(1)
    annual_maximum_rainfall = annual_maximum_rainfall[["年/Year", "最大日雨量/Max Daily Rainfall", "日期/Date"]]
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