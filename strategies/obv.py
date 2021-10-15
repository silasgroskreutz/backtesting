import pandas as pd
import numpy as np

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)

def backtest(df: pd.dataframe, ma_period: int):

    df["obv"] = (np.sign(df["close"].diff()) * df["volume"]).fillna(0).cumsum()
    df["obv_ma"] = round(data["obv"].rolling(window=ma_period).mean(), 2)

    df["signal"] = np.where(df["obv"] > df["obv_ma"], 1, -1)
    df["pnl"] = df["close"].pct_change() * df["signal"].shift(1)

    # notes on the different functions
    #   rolling() - calculate a moving average
    #   diff() - difference in value between each row
    #   pct_change - percentage difference between each row
    #   np.where() - fill a new column with conditional values
    #   shift() - used here to apply signal to correct row in pandas


    return df["pnl"].sum()
