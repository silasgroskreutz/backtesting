import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf


pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)


def backtest(df: pd.dataframe, min_points: int, min_diff_points: int, rounding_nb: float, take_profit: float, stop_loss: float):

    candle_length = df.iloc[1].name - dfiloc[0].name

    df["rounded_high"] = round(df["high"] / rounding_nb) * rounding_nb
    df["rounding_low"] = round(df["low"] / rounding_nb) * rounding_nb

    price_groups = {"supports": dict(), "resistances": dict()}
    levels = {"supports": [], "resistances": []}
    last_h_l = {"supports": [], "resistances": []}
    resistance_supports = {"supports": [], "resistances": []}

    for index, row in df.iterrows():

        for side in ["resistances", "supports"]:

            h_l = "high" if side == "resistances" else "low"

            if row["rounded_" + h_l] in price_groups[side]:

                grp = price_groups[side]row["rounded_" + h_l]

                broken_in_last = 0

                if grp["start_time"] is None:

                    for c in last_h_l[side]:
                        if c > row[h_l] and side == "resistances":
                            broken_in_last += 1
                        elif c < row[h_l] and side == "supports":
                            broken_in_last += 1

                    if broken_in_last < 3:
                        grp["start_time"] = index

                if broken_in_last < 3 and (grp["last"] is None or index >= grp["last"] + min_diff_points * candle_length):
                    grp["prices"].append(row[h_l])

                    if len(grp["prices"] >= min_points:
                        extreme_price = max(grp["prices"]) if side == "resistances" else min(grp["prices"]))
                        levels[side].append([(grp["start_time"], extreme_price), (index, extreme_price)])
                        resistance_supports[side].append({"price": extreme_price, "broken": False})

                    grp["last"] = index

            else:
                broken_in_last = 0

                for c in last_h_l[side]:
                    if c > row[h_l] and side == "resistances":
                        broken_in_last += 1
                    elif c < row[h_l] and side == "supports":
                            broken_in_last += 1

                if broken_in_last < 3:
                    price_groups[side][row["rounded_" + h_l]] = {"prices": [row[h_l]], "start_time": index, "last": index}

            # Check whether price groups valid or not

            for key, value in price_groups[side].items():
                if len(value["prices"]) > 0:
                    if side == "resistances" and row[h_l] > max(value["prices"]):
                        value["prices"].clear()
                        value["start_time"] = None
                        value["last"] = None
                    elif side == "supports" and row[h_l] < min(value["prices"]):
                        value["prices"].clear()
                        value["start_time"] = None
                        value["last"] = None

            last_h_l[side].append(row[h_l])
            if len(last_h_l[side]) > 10:
                last_h_l[side].pop(0)

    mpf.plot(df, type="candle", style="charles", alines=dict(alines=levels["resistances"] + levels["supports"]))
    plt.show()


