# https://www.tradingview.com/support/solutions/43000614331-technical-ratings/
# https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html
# https://www.tradingview.com/support/solutions/43000614331-technical-ratings/
# https://www.tradingview.com/support/solutions/43000521824-pivot-points-standard/
import talib
from ta.momentum import awesome_oscillator

import pandas as pd
import numpy as np


def add_OSCILLATORS_RSI(df):
    df['RSI'] = talib.RSI(df['close'], 14)
    df['RSI[1]'] = df['RSI'].shift(1)
    return df

def add_OSCILLATORS_STOCH(df):
    df['Stoch.K'], df['Stoch.D'] = talib.STOCH(df['high'], df['low'], df['close'], fastk_period=14, slowk_period=3, slowd_period=3)
    df['Stoch.K[1]'] = df['Stoch.K'].shift(1)
    df['Stoch.D[1]'] = df['Stoch.D'].shift(1)
    return df

def add_OSCILLATORS_CCI(df):
    df['CCI20'] = talib.CCI(df['high'], df['low'], df['close'], timeperiod=20)
    df['CCI20[1]'] = df['CCI20'].shift(1)
    return df

def add_OSCILLATORS_ADX(df):
    df['ADX'] = talib.ADX(df['high'], df['low'], df['close'], timeperiod=14)
    df['ADX+DI'] = talib.PLUS_DI(df['high'], df['low'], df['close'], timeperiod=14)
    df['ADX-DI'] = talib.MINUS_DI(df['high'], df['low'], df['close'], timeperiod=14)
    df['ADX+DI[1]'] = df['ADX+DI'].shift(1)
    df['ADX-DI[1]'] = df['ADX-DI'].shift(1)
    return df

def add_OSCILLATORS_AO(df, period1=5, period2=34):
    METHODE_TA = True
    if METHODE_TA == True:
        # ao = AwesomeOscillatorIndicator(df['High'], df['Low'])
        # df['AO'] = ao.awesome_oscillator()
        df['AO'] = awesome_oscillator(df['high'], df['low'])
        df['AO'] = df['AO'].astype('float64')
    else:
        price = df['close']
        median = price.rolling(2).median()
        short = talib.SMA(median, period1)
        long = talib.SMA(median, period2)
        df['AO'] = short - long

    df['AO[1]'] = df['AO'].shift(1)
    df['AO[2]'] = df['AO[1]'].shift(1)
    return df

def add_OSCILLATORS_MOM(df, period=10):
    df['Mom'] = talib.MOM(df['close'], timeperiod=period)
    df['Mom[1]'] = df['Mom'].shift(1)
    return df

def add_OSCILLATORS_MACD(df):
    df['MACD.macd'], df['MACD.signal'], hist = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    return df

def add_OSCILLATORS_STOCH_RSI(df):
    df['Stoch.RSI.K'], df['Rec.Stoch.RSI'] = talib.STOCHRSI(df['close'], timeperiod=14, fastk_period=14, fastd_period=3, fastd_matype=3)
    return df

def add_OSCILLATORS_WILLIAMS_PERCENT_RANGE(df):
    '''
    Williams Percent Range
        Buy — indicator < lower band and rising
        Sell — indicator > upper band and falling
        Neutral — neither Buy nor Sell
    '''
    df['W.R'] = talib.WILLR(df['high'], df['low'], df['close'], timeperiod=14)

    df_wr = pd.DataFrame()
    df_wr['W.R'] = df['W.R']
    df_wr['W.R[1]'] = df_wr['W.R'].shift(1)

    df_wr['-80'] = -80
    df_wr['-20'] = -20

    df_wr['buy_condition1'] = (df_wr['W.R[1]'] > df_wr['-80']) & (df_wr['W.R'] < df_wr['-80'])
    df_wr['sell_condition1'] = (df_wr['W.R[1]'] < df_wr['-20']) & (df_wr['W.R'] > df_wr['-20'])

    df_wr['buy_condition2'] = (df_wr['W.R'] > df_wr['W.R[1]']) & (df_wr['W.R'] < df_wr['-80'])
    df_wr['sell_condition2'] = (df_wr['W.R'] < df_wr['W.R[1]']) & (df_wr['W.R'] > df_wr['-20'])

    df_wr['signals'] = 0
    df_wr['signals'] = np.where(df_wr['buy_condition1'] | df_wr['buy_condition2'], 1, df_wr['signals'])
    df_wr['signals'] = np.where(df_wr['sell_condition1'] | df_wr['sell_condition2'], -1, df_wr['signals'])

    df['Rec.WR'] = df_wr['signals']
    return df

def add_OSCILLATORS_EBBP(df):
    # Bull power and bear power by Dr. Alexander Elder show where today’s high and low lie relative to the a 13-day EMA
    '''
        In order to go long (BUY):
        1. The market is in a bull trend, as indicated by the 13-period EMA
        2. Bear Power is in negative territory, but increasing
        Buy — uptrend and BearPower < zero and BearPower is rising

        In order to go short:
        1. The market is in a bear trend, as indicated by the 13-period EMA
        2. Bull Power is in positive territory, but falling
        Sell — downtrend and BullPower > zero and BullPower is falling
    '''

    bull_power = pd.Series(df['high'] - talib.EMA(df['close'], 13), name="Bull.")
    bear_power = pd.Series(df['low'] - talib.EMA(df['close'], 13), name="Bear.")

    df_BBP =  pd.concat([bull_power, bear_power], axis=1)
    df_BBP["EMA13"] = talib.EMA(df['close'], timeperiod=13)
    df_BBP["EMA13_shit_3"] = df_BBP["EMA13"].shift(3)
    df_BBP["EMA13_slope"] = (df_BBP["EMA13"] - df_BBP["EMA13_shit_3"]) / 3
    df_BBP["EMA13_slope"] = np.where( df_BBP["EMA13_slope"] < 0, -1, df_BBP["EMA13_slope"])
    df_BBP["EMA13_slope"] = np.where(df_BBP["EMA13_slope"] > 0, 1, df_BBP["EMA13_slope"])
    df_BBP["EMA13_slope"] = np.where(df_BBP["EMA13_slope"] == 0, 0, df_BBP["EMA13_slope"])

    df_BBP['Bull.-1'] = df_BBP['Bull.'].shift(1)
    df_BBP['Bear.-1'] = df_BBP['Bear.'].shift(1)
    df_BBP['Bull.-2'] = df_BBP['Bull.'].shift(2)
    df_BBP['Bear.-2'] = df_BBP['Bear.'].shift(2)

    df_BBP['0'] = 0
    buy_condition = ((df_BBP["EMA13_slope"] > df_BBP['0']) & (df_BBP['Bear.'] < df_BBP['0']) &
                (df_BBP['Bear.'] > df_BBP['Bear.-1']) & (df_BBP['Bear.'] > df_BBP['Bear.-2']))
    sell_condition = ((df_BBP["EMA13_slope"] < df_BBP['0']) & (df_BBP['Bull.'] > df_BBP['0']) & (
                df_BBP['Bull.'] < df_BBP['Bull.-1']) & (df_BBP['Bull.'] < df_BBP['Bull.-2']))

    df_BBP['signals'] = 0
    df_BBP['signals'] = np.where(buy_condition, 1, df_BBP['signals'])
    df_BBP['signals'] = np.where(sell_condition, -1, df_BBP['signals'])

    df['BBPower'] = bull_power + bear_power
    df['Rec.BBPower'] = df_BBP['signals']
    return df

def add_OSCILLATORS_UO(df):
    '''
     Ultimate Oscillator
        Buy — UO > 70
        Sell — UO < 30
        Neutral — neither Buy nor Sell
    '''
    df['UO'] = talib.ULTOSC(df['high'], df['low'], df['close'], timeperiod1=7, timeperiod2=14, timeperiod3=28)

    df['Rec.UO'] = 0
    df['Rec.UO'] = np.where(df['UO'] > 70, 1, df['Rec.UO'])
    df['Rec.UO'] = np.where(df['UO'] < 30, -1, df['Rec.UO'])
    return df