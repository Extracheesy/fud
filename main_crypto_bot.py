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
import super_reversal
import backtesting

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

    # pair = "LTC/USDT"
    pair = 'BTC-USD'

    #interval = '1d'
    interval = '1h'

    if False:
        df = fletch_data.yf_ohlcv(dt_y, pair, interval)
    if False:
        df = fletch_data.ohlcv(dt, 'BTC/USDT', interval)

    # start = '2021-05-07-00-00'
    # stop = '2022-05-07-00-00'

    start = '2017-08-17-00-00'
    stop = '2022-04-27-00-00'

    dt = [start, stop]

    df = fletch_data.Historical_Crypto_ohlcv(dt, pair, '1d')

    strat = super_reversal.super_reversion_strat(
        df=df.loc[:],
        st_short_atr_window=15,
        st_short_atr_multiplier=5,
        short_ema_window=5,
        long_ema_window=400
    )

    strat.populate_indicators()
    strat.populate_buy_sell(show_log=False)
    bt_result = strat.run_backtest(initial_wallet=1000, return_type="metrics")
    df_trades, df_days = backtesting.basic_single_asset_backtest(trades=bt_result['trades'], days=bt_result['days'])
    backtesting.plot_wallet_vs_asset(df_days=df_days)

    # In[6]:

    backtesting.plot_bar_by_month(df_days=df_days)

    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
