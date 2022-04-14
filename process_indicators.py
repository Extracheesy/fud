# https://www.tradingview.com/support/solutions/43000614331-technical-ratings/
# https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html
# https://www.tradingview.com/support/solutions/43000614331-technical-ratings/
# https://www.tradingview.com/support/solutions/43000521824-pivot-points-standard/

import pandas as pd

# INDICATORS = ["Recommend.Other","Recommend.All","Recommend.MA","RSI","RSI[1]","Stoch.K","Stoch.D","Stoch.K[1]","Stoch.D[1]","CCI20","CCI20[1]","ADX","ADX+DI","ADX-DI","ADX+DI[1]","ADX-DI[1]","AO","AO[1]",
# "Mom","Mom[1]","MACD.macd","MACD.signal","Rec.Stoch.RSI","Stoch.RSI.K","Rec.WR","W.R","Rec.BBPower","BBPower","Rec.UO","UO","close",
# "EMA5","SMA5","EMA10","SMA10","EMA20","SMA20","EMA30","SMA30","EMA50","SMA50","EMA100","SMA100","EMA200","SMA200","Rec.Ichimoku","Ichimoku.BLine","Rec.VWMA","VWMA","Rec.HullMA9","HullMA9",
# "Pivot.M.Classic.S3","Pivot.M.Classic.S2","Pivot.M.Classic.S1","Pivot.M.Classic.Middle","Pivot.M.Classic.R1","Pivot.M.Classic.R2","Pivot.M.Classic.R3","Pivot.M.Fibonacci.S3","Pivot.M.Fibonacci.S2","Pivot.M.Fibonacci.S1","Pivot.M.Fibonacci.Middle","Pivot.M.Fibonacci.R1","Pivot.M.Fibonacci.R2","Pivot.M.Fibonacci.R3","Pivot.M.Camarilla.S3","Pivot.M.Camarilla.S2","Pivot.M.Camarilla.S1","Pivot.M.Camarilla.Middle","Pivot.M.Camarilla.R1","Pivot.M.Camarilla.R2","Pivot.M.Camarilla.R3","Pivot.M.Woodie.S3","Pivot.M.Woodie.S2","Pivot.M.Woodie.S1","Pivot.M.Woodie.Middle","Pivot.M.Woodie.R1","Pivot.M.Woodie.R2","Pivot.M.Woodie.R3","Pivot.M.Demark.S1","Pivot.M.Demark.Middle","Pivot.M.Demark.R1",
# "open", "P.SAR", "BB.lower", "BB.upper", "AO[2]", "volume", "change", "low", "high"]

from indicators import moving_averages, oscillators, pivots, additional_indicators

def get_df_additional_analysis(df_in):
    df = pd.DataFrame()
    df['open'] = df_in['Open']
    df['high'] = df_in['High']
    df['low'] = df_in['Low']
    df['volume'] = df_in['Volume']
    df['close'] = df_in['Close']

    # ADDITIONAL INDICATORS
    df_additional_indicators = pd.DataFrame()
    df_additional_indicators = additional_indicators.add_MOMENTUM_TRIX(df, df_additional_indicators)
    df_additional_indicators = additional_indicators.add_VOLUME_OBV(df, df_additional_indicators)
    df_additional_indicators = additional_indicators.add_VOLATILITY_ATR(df, df_additional_indicators)
    df_additional_indicators = additional_indicators.add_SUPER_TREND(df, df_additional_indicators)
    df_additional_indicators = additional_indicators.add_SENTIMENT_FNG(df, df_additional_indicators)
    df_additional_indicators = additional_indicators.add_MOMENTUM_CHOP(df, df_additional_indicators)
    df_additional_indicators = additional_indicators.add_MOMENTUM_STC(df, df_additional_indicators)

    return df_additional_indicators


def get_df_analysis(df_in, indicators_key, screener, symbol, exchange, interval):
    df = pd.DataFrame(columns=indicators_key)
    df['open'] = df_in['Open']
    df['high'] = df_in['High']
    df['low'] = df_in['Low']
    df['volume'] = df_in['Volume']
    df['close'] = df_in['Close']

    # OSCILLATORS
    df = oscillators.add_OSCILLATORS_RSI(df)
    df = oscillators.add_OSCILLATORS_STOCH(df)
    df = oscillators.add_OSCILLATORS_CCI(df)
    df = oscillators.add_OSCILLATORS_ADX(df)
    df = oscillators.add_OSCILLATORS_AO(df)
    df = oscillators.add_OSCILLATORS_MOM(df)
    df = oscillators.add_OSCILLATORS_MACD(df)
    df = oscillators.add_OSCILLATORS_STOCH_RSI(df)
    df = oscillators.add_OSCILLATORS_WILLIAMS_PERCENT_RANGE(df)
    df = oscillators.add_OSCILLATORS_EBBP(df)
    df = oscillators.add_OSCILLATORS_UO(df)

    # MOVING AVERAGES
    df = moving_averages.add_MOVING_AVERAGES_EMA(df)
    df = moving_averages.add_MOVING_AVERAGES_SMA(df)
    df = moving_averages.add_MOVING_AVERAGES_ICHIMOKU8BLINE(df)
    df = moving_averages.add_MOVING_AVERAGES_VWMA(df)
    df = moving_averages.add_MOVING_AVERAGES_HMA(df)
    df = moving_averages.add_BBANDS(df)
    df = moving_averages.add_PSAR(df)
    df = moving_averages.add_PCTCHANGE(df)

    # PIVOTS
    df = pivots.add_PIVOTS_CLASSIC(df)
    df = pivots.add_PIVOTS_FIBONACCI(df)
    df = pivots.add_PIVOTS_CAMARILLA(df)
    df = pivots.add_PIVOTS_WOODIE(df)
    df = pivots.add_PIVOTS_DM(df)

    df.reset_index(inplace=True, drop=True)
    lst_columns = df.columns.tolist()

    last_raw = df.loc[len(df) -1,:].values.tolist()
    indicators = {lst_columns[i]: last_raw[i] for i in range(len(lst_columns))}

    return indicators

