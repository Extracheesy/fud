import talib
import ta
from ta.momentum import awesome_oscillator
from finta import TA
import pandas as pd
import numpy as np
import super_trend_indicator, custom_indicators

def add_MOMENTUM_TRIX(df, df_trix):
    # when the TRIX crosses above the zero line it gives a buy signal, and when it closes below the zero line, it gives a sell signal.

    # trixLength = 30
    trixLength = 9
    trixSignal = 21

    TALIB = True
    if TALIB == True:
        df_trix['TRIX_PCT'] = talib.TRIX(df['close'], timeperiod=trixLength)
    else:
        df_trix['TRIX'] = ta.trend.ema_indicator(ta.trend.ema_indicator(ta.trend.ema_indicator(close=df['close'],
                                                                                               window=trixLength),
                                                                        window=trixLength),
                                                 window=trixLength)
        df_trix['TRIX_PCT'] = df_trix["TRIX"].pct_change() * 100

    df_trix['TRIX_SIGNAL'] = ta.trend.sma_indicator(df_trix['TRIX_PCT'], trixSignal)
    df_trix['trix_h'] = df_trix['TRIX_PCT'] - df_trix['TRIX_SIGNAL']

    df_trix['STOCH_RSI'] = ta.momentum.stochrsi(close=df['close'], window=14, smooth1=3, smooth2=3)

    df_trix['0.2'] = 0.2
    df_trix['0.82'] = 0.82
    df_trix['0'] = 0

    df_trix['buy_condition'] = (df_trix['trix_h'] > df_trix['0']) & (df_trix['STOCH_RSI'] <= df_trix['0.82'])
    df_trix['sell_condition'] = (df_trix['trix_h'] < df_trix['0']) & (df_trix['STOCH_RSI'] >= df_trix['0.2'])

    df_trix['Rec.trix'] = 0
    df_trix['Rec.trix'] = np.where(df_trix['buy_condition'], 1, df_trix['Rec.trix'])
    df_trix['Rec.trix'] = np.where(df_trix['sell_condition'], -1, df_trix['Rec.trix'])

    df_trix = df_trix.drop(['0.2'], axis=1)
    df_trix = df_trix.drop(['0.82'], axis=1)
    df_trix = df_trix.drop(['0'], axis=1)
    df_trix = df_trix.drop(['buy_condition'], axis=1)
    df_trix = df_trix.drop(['sell_condition'], axis=1)
    df_trix = df_trix.drop(['TRIX_PCT'], axis=1)
    df_trix = df_trix.drop(['TRIX_SIGNAL'], axis=1)
    df_trix = df_trix.drop(['STOCH_RSI'], axis=1)

    return df_trix

# On Balance Volume
def add_VOLUME_OBV(df, df_obv):
    df_obv['obv'] = talib.OBV(df['close'], df['volume'])

    return df_obv

def add_VOLATILITY_ATR(df, df_atr):
    df_atr['atr'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=14)

    return df_atr

def add_SUPER_TREND(df, df_super_trend):
    atr_period = 10
    atr_multiplier = 3.0

    df_s_trend = super_trend_indicator.Supertrend(df, atr_period, atr_multiplier)
    df_super_trend['Supertrend'] = df_s_trend['Supertrend']
    df_super_trend['Final Lowerband'] = df_s_trend['Final Lowerband']
    df_super_trend['Final Upperband'] = df_s_trend['Final Upperband']

    return df_super_trend

def add_SENTIMENT_FNG(df, df_fear):
    df_fear['fear'] = custom_indicators.fear_and_greed(df['close'])

    return df_fear

def add_MOMENTUM_CHOP(df, df_chop):
    # Choppiness indicator
    # When the CHOP values are above 61.8 thresholds, it means consolidated market or sideways movements in the market.
    # When the CHOP values are below 38.2 thresholds, it indicates a continuing trend.
    df_chop['chop'] = custom_indicators.chop(df['high'], df['low'], df['close'], window=14)

    df_chop['61.8'] = 61.8
    df_chop['38.2'] = 38.2

    df_chop['trend_condition'] = (df_chop['chop'] > df_chop['61.8'])
    df_chop['chopy_condition'] = (df_chop['chop'] < df_chop['38.2'])

    df_chop['Rec.chop'] = 0
    df_chop['Rec.chop'] = np.where(df_chop['trend_condition'], 'CHOPPY', df_chop['Rec.chop'])
    df_chop['Rec.chop'] = np.where(df_chop['chopy_condition'], 'TRENDY', df_chop['Rec.chop'])

    df_chop = df_chop.drop(['trend_condition'], axis=1)
    df_chop = df_chop.drop(['chopy_condition'], axis=1)
    df_chop = df_chop.drop(['61.8'], axis=1)
    df_chop = df_chop.drop(['38.2'], axis=1)

    return df_chop

# Schaff Trend Cycle
def add_MOMENTUM_STC(df, df_stc):
    """
    STC indicator generates its buy signal when the signal line turns up from 25 (to indicate a bullish reversal is happening and signaling that it is time to go long),
    or turns down from 75 (to indicate a downside reversal is unfolding and so it's time for a short sale).
    """
    df_stc['stc'] = TA.STC(df).copy()
    df_stc['stc[1]'] = df_stc['stc'].shift(1)

    df_stc['25'] = 25
    df_stc['75'] = 75

    df_stc['buy_condition'] = (df_stc['stc'] > df_stc['stc[1]']) & (df_stc['stc[1]'] < df_stc['25']) & (df_stc['stc'] > df_stc['25'])
    df_stc['sell_condition'] = (df_stc['stc'] < df_stc['stc[1]']) & (df_stc['stc[1]'] > df_stc['75']) & (df_stc['stc'] < df_stc['75'])


    df_stc['Rec.stc'] = 0
    df_stc['Rec.stc'] = np.where(df_stc['buy_condition'], 1, df_stc['Rec.stc'])
    df_stc['Rec.stc'] = np.where(df_stc['sell_condition'], -1, df_stc['Rec.stc'])

    df_stc = df_stc.drop(['buy_condition'], axis=1)
    df_stc = df_stc.drop(['sell_condition'], axis=1)
    df_stc = df_stc.drop(['25'], axis=1)
    df_stc = df_stc.drop(['75'], axis=1)

    return df_stc
