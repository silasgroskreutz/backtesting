import pandas as pd
import numpy as np


pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)


def backtest(df: pd.dataframe, tekan_period: int, kijun_period: int):

    # Tenkan Sen : Short-Term signal line

    df["rolling_min_tenkan"] = df["low"].rolling(window=tenkan_period).min()
    df["rolling_min_tenkan"] = df["high"].rolling(window=tenkan_period).max()

    df["tenkan_sen"] = (df["rolling_max_tenkan"] + df["rolling_min_tenkan"]) / 2
