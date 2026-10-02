import pandas as pd

def data_integration(df, functions):
    dfs = [func(df) for func in functions]
    df1 = dfs[0]
    dfr = [df.iloc[:, 1:] for df in dfs[1:]]
    dfs = [df1] + dfr
    df_analysed = pd.concat(dfs, axis=1)
    return df_analysed