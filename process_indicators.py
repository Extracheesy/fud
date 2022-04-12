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

from indicators import moving_averages, oscillators, pivots


def get_df_analysis(df_in, indicators_key, screener, symbol, exchange, interval):
    df = pd.DataFrame(columns=indicators_key)
    df['open'] = df_in['Open']
    df['high'] = df_in['High']
    df['low'] = df_in['Low']
    df['volume'] = df_in['Volume']
    df['close'] = df_in['Close']

    #df = pd.concat([df, df2], axis=1)

    # OSCILLATORS
    oscillators.add_OSCILLATORS_RSI(df)
    oscillators.add_OSCILLATORS_STOCH(df)
    oscillators.add_OSCILLATORS_CCI(df)
    oscillators.add_OSCILLATORS_ADX(df)
    oscillators.add_OSCILLATORS_AO(df)
    oscillators.add_OSCILLATORS_MOM(df)
    oscillators.add_OSCILLATORS_MACD(df)
    oscillators.add_OSCILLATORS_STOCH_RSI(df)
    oscillators.add_OSCILLATORS_WILLIAMS_PERCENT_RANGE(df)
    oscillators.add_OSCILLATORS_EBBP(df)
    oscillators.add_OSCILLATORS_UO(df)

    # MOVING AVERAGES
    moving_averages.add_MOVING_AVERAGES_EMA(df)
    moving_averages.add_MOVING_AVERAGES_SMA(df)
    moving_averages.add_MOVING_AVERAGES_ICHIMOKU8BLINE(df)
    moving_averages.add_MOVING_AVERAGES_VWMA(df)
    moving_averages.add_MOVING_AVERAGES_HMA(df)
    moving_averages.add_BBANDS(df)
    moving_averages.add_PSAR(df)

    # PIVOTS
    pivots.add_PIVOTS_CLASSIC(df)
    pivots.add_PIVOTS_FIBONACCI(df)
    pivots.add_PIVOTS_CAMARILLA(df)
    pivots.add_PIVOTS_WOODIE(df)
    pivots.add_PIVOTS_DM(df)

    df.reset_index(inplace=True, drop=True)
    lst_columns = df.columns.tolist()

    last_raw = df.loc[len(df) -1,:].values.tolist()
    indicators = {lst_columns[i]: last_raw[i] for i in range(len(lst_columns))}

    return indicators

