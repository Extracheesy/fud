import sys
sys.path.append('live_tools/utilities')

import pandas as pd

import config

# from TV_indicators import TA_Handler, Interval, get_multiple_analysis
from tradingview_ta import TA_Handler, Interval
import process_recom
import process_indicators
# import TV_analysis
import tools
import fletch_data


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':


    dt = ['20210407', '20220407'] # OK
    dt_y = ['2021-04-07', '2022-04-07']
    # dt = ['20200407', '20220407']

    #df = fletch_data.ohlcv(dt, 'ETH/BTC', '1h')
    #df = fletch_data.ohlcv(dt, 'ETH/BTC', '1d')

    pair = 'BTC-USD'
    if True:
        df = fletch_data.yf_ohlcv(dt_y, pair, '1d')
    else:
        df = fletch_data.ohlcv(dt, 'BTC/USDT', '1d')

    handler = TA_Handler(
        symbol="AAPL",
        interval=Interval.INTERVAL_1_DAY,
        screener="america",
        exchange="NASDAQ",
        # proxies=proxies
    )

    # indicator = handler.get_analysis()

    indicators_keys = config.INDICATORS.copy()

    df_summary_level_0 = pd.DataFrame()
    df_summary_level_1 = pd.DataFrame()
    df_indicators_discret = pd.DataFrame()
    df_indicators_brut = pd.DataFrame()

    df_additional_indicators = process_indicators.get_df_additional_analysis(df)

    len_df = len(df) - 200
    for i in range(len_df):
        current_date = df.index.tolist()[-1]
        indicators = process_indicators.get_df_analysis(df, indicators_keys, "crypto", 'BTC/USDT', "binance", '1d')
        indicator_analysis = process_recom.calculate(indicators, indicators_keys, "crypto", 'BTC/USDT', "binance", '1d')
        df_summary_level_0_new, df_summary_level_1_new, df_indicators_discret_new, df_indicators_brut_new = tools.anlysis_to_df(indicator_analysis, current_date)
        df_summary_level_0 = pd.concat([df_summary_level_0_new, df_summary_level_0])
        df_summary_level_1 = pd.concat([df_summary_level_1_new, df_summary_level_1])
        df_indicators_discret = pd.concat([df_indicators_discret_new, df_indicators_discret])
        df_indicators_brut = pd.concat([df_indicators_brut_new, df_indicators_brut])

        df = df.drop(labels=current_date, axis=0)
        if (i % 50 == 0):
            print("remaining: ",len_df - i, "len df: ",len(df))

    df_additional_indicators.to_csv('OUTPUT/' + pair + '_df_additional_indicators' + '.csv')
    df_indicators_brut.to_csv('OUTPUT/' + pair + '_df_indicators_brut' + '.csv')
    df_indicators_discret.to_csv('OUTPUT/' + pair + '_df_indicators_discret' + '.csv')
    df_summary_level_1.to_csv('OUTPUT/' + pair + '_df_summary_level_1' + '.csv')
    df_summary_level_0.to_csv('OUTPUT/' + pair + '_df_summary_level_0' + '.csv')

    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
