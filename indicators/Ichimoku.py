import pandas as pd
import numpy as np

def get_ICHIMOKU(df_data):
    """
    Ichimoku Cloud
        Buy — base line < price and conversion line crosses price from below and lead line 1 > price and lead line 1 > lead line 2
        Sell — base line > price and conversion line crosses price from above and lead line 1 < price and lead line 1 < lead line 2
        Neutral — neither Buy nor Sell
    """
    df = pd.DataFrame()

    df['High'] = df_data['high']
    df['Close'] = df_data['close']
    df['Low'] = df_data['low']

    high_prices = df['High']
    close_prices = df['Close']
    low_prices = df['Low']

    # Tenkan-sen (Conversion Line): (9-period high + 9-period low)/2))
    nine_period_high = df['High'].rolling(window=9).max()
    nine_period_low = df['Low'].rolling(window=9).min()
    df['tenkan_sen'] = (nine_period_high + nine_period_low) / 2

    # Kijun-sen (Base Line): (26-period high + 26-period low)/2))
    period26_high = high_prices.rolling(window=26).max()
    period26_low = low_prices.rolling(window=26).min()
    df['kijun_sen'] = (period26_high + period26_low) / 2
    # Store Baseline values in df_data
    df_data['Ichimoku.BLine'] = df['kijun_sen']

    # Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2))
    df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(26)

    # Senkou Span B (Leading Span B): (52-period high + 52-period low)/2))
    period52_high = high_prices.rolling(window=52).max()
    period52_low = low_prices.rolling(window=52).min()
    df['senkou_span_b'] = ((period52_high + period52_low) / 2).shift(26)

    # The most current closing price plotted 22 time periods behind (optional)
    df['chikou_span'] = close_prices.shift(-22)  # 22 according to investopedia

    """
        Kijun-sen (The base line)
        Tenkan-sen (The conversion line)
        Lead 1: Average of Conversion and Base Lines
        Lead 2: Average of (52-period high + 52-period low)
    """

    df['baseline'] = df['kijun_sen']
    df['conversion'] = df['tenkan_sen']
    df['conversion[1]'] = df['conversion'].shift(1)
    df['Lead1'] = df['senkou_span_a']
    df['Lead2'] = df['senkou_span_b']

    df['buy_condition_1'] = df['baseline'] < df['Close']   # base line < price
    df['buy_condition_2'] = (df['conversion[1]'] < df['Close'])   # conversion line crosses price from below
    df['buy_condition_3'] = (df['conversion'] > df['Close'])      # conversion line crosses price from below
    df['buy_condition_4'] = df['Lead1'] > df['Close']   # lead line 1 > price
    df['buy_condition_5'] = df['Lead1'] > df['Lead2']   # lead line 1 > lead line 2
    df['buy_condition'] = df['buy_condition_1'] & df['buy_condition_2'] & df['buy_condition_3'] & df['buy_condition_4'] & df['buy_condition_5']

    df['sell_condition_1'] = df['baseline'] > df['Close']   # base line > price
    df['sell_condition_2'] = df['conversion[1]'] > df['Close']   # conversion line crosses price from above
    df['sell_condition_3'] = df['conversion'] < df['Close']     # conversion line crosses price from above
    df['sell_condition_4'] = df['Lead1'] < df['Close']   # lead line 1 < price
    df['sell_condition_5'] = df['Lead1'] < df['Lead2']   # lead line 1 < lead line 2
    df['sell_condition'] = df['sell_condition_1'] & df['sell_condition_2'] & df['sell_condition_3'] & df['sell_condition_4'] & df['sell_condition_5']

    df['signals'] = 0
    df['signals'] = np.where(df['buy_condition'], 1, df['signals'])
    df['signals'] = np.where(df['sell_condition'], -1, df['signals'])

    df_data['Rec.Ichimoku'] = df['signals']
