# https://www.tradingview.com/support/solutions/43000614331-technical-ratings/
# https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html
# https://www.tradingview.com/support/solutions/43000614331-technical-ratings/
# https://www.tradingview.com/support/solutions/43000521824-pivot-points-standard/
import math
import talib
from ta.volume import volume_weighted_average_price

from indicators import Ichimoku

import pandas as pd
import numpy as np


def add_MOVING_AVERAGES_EMA(df):
    df["EMA5"] = talib.EMA(df['close'], timeperiod=5)
    df["EMA10"] = talib.EMA(df['close'], timeperiod=10)
    df["EMA20"] = talib.EMA(df['close'], timeperiod=20)
    df["EMA30"] = talib.EMA(df['close'], timeperiod=30)
    df["EMA50"] = talib.EMA(df['close'], timeperiod=50)
    df["EMA100"] = talib.EMA(df['close'], timeperiod=100)
    df["EMA200"] = talib.EMA(df['close'], timeperiod=200)


def add_MOVING_AVERAGES_SMA(df):
    df["SMA5"] = talib.SMA(df['close'], timeperiod=5)
    df["SMA10"] = talib.SMA(df['close'], timeperiod=10)
    df["SMA20"] = talib.SMA(df['close'], timeperiod=20)
    df["SMA30"] = talib.SMA(df['close'], timeperiod=30)
    df["SMA50"] = talib.SMA(df['close'], timeperiod=50)
    df["SMA100"] = talib.SMA(df['close'], timeperiod=100)
    df["SMA200"] = talib.SMA(df['close'], timeperiod=200)


def add_MOVING_AVERAGES_ICHIMOKU8BLINE(df):
    Ichimoku.get_ICHIMOKU(df)


def add_MOVING_AVERAGES_VWMA(df):
    # Volume Weighted Moving Average (20)
    """
    All Moving Averages
        Buy — MA value < price
        Sell — MA value > price
        Neutral — MA value = price
    """
    df['VWMA'] = volume_weighted_average_price(df['high'], df['low'], df['close'], df['volume'], window=20)

    df['Rec.VWMA'] = 0
    df['Rec.VWMA'] = np.where(df['VWMA'] < df['close'], 1, df['Rec.VWMA'])
    df['Rec.VWMA'] = np.where(df['VWMA'] > df['close'], -1, df['Rec.VWMA'])


def add_MOVING_AVERAGES_HMA(df):
    # Hull Moving Average
    """
    All Moving Averages
        Buy — MA value < price
        Sell — MA value > price
        Neutral — MA value = price
    """
    wma_1 = 2 * talib.WMA(df['close'], timeperiod=int(9 / 2))
    wma_2 = talib.WMA(df['close'], timeperiod=9)
    wma_3 = wma_1 - wma_2
    df['HullMA9'] = talib.WMA(wma_3, timeperiod=math.sqrt(9))

    df['Rec.HullMA9'] = 0
    df['Rec.HullMA9'] = np.where(df['HullMA9'] < df['close'], 1, df['Rec.HullMA9'])
    df['Rec.HullMA9'] = np.where(df['HullMA9'] > df['close'], -1, df['Rec.HullMA9'])


def add_BBANDS(df):
    df_tmp = pd.DataFrame()
    df['BB.upper'], df_tmp['middle_to_drop'], df['BB.lower'] = talib.BBANDS(df['close'], timeperiod=5, nbdevup=2,
                                                                            nbdevdn=2, matype=0)
    # df = df.drop(['middle_to_drop'], axis=1)


def add_PSAR(df):
    df['P.SAR'] = talib.SAR(df['high'], df['low'], acceleration=0, maximum=0)
