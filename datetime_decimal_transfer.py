import pandas as pd

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