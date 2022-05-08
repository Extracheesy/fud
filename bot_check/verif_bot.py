import sys
sys.path.append('live_tools/utilities')

import numpy as np
import pandas as pd
import requests
from datetime import datetime

import config

# from TV_indicators import TA_Handler, Interval, get_multiple_analysis
from tradingview_ta import TA_Handler, Interval
import process_recom
import process_indicators
# import TV_analysis
import tools
import fletch_data


def get_price(symbol):
    endpoint_url = 'https://ftx.com/api/markets'

    request_url = f'{endpoint_url}/{symbol}'
    df = pd.DataFrame(requests.get(request_url).json())

    return df['result']['price']

def get_price_historical(str_time, symbol):
    endpoint_url = 'https://ftx.com/api/markets'

    request_url = f'{endpoint_url}/{symbol}'
    # window length in seconds. options: 15, 60, 300, 900, 3600, 14400, 86400, or any multiple of 86400 up to 30*86400
    second_min = 15
    toto = datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S.%f')
    start_date = datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S.%f').timestamp()

    print(toto, "   ", start_date)

    # start_date = 1651235835000.0

    historical = requests.get(f'{request_url}/candles?resolution={second_min}&start_time={start_date}').json()
    df = pd.DataFrame(historical['result'])

    print(df['startTime'][0], "   ", df['time'][0])

    return df['close'][0]

def verif_bot():

    df_bot_data = pd.read_csv('./bot_check/broker_history.csv')

    df_BUY = df_bot_data.drop(df_bot_data[df_bot_data['type'] != 'BUY'].index)
    df_SELL = df_bot_data.drop(df_bot_data[df_bot_data['type'] != 'SELL'].index)

    df_BUY['actual_price'] = ""
    df_BUY['historical_price'] = ""
    for i in df_BUY.index.tolist():
        df_BUY['actual_price'][i] = get_price(df_BUY['symbol'][i])
        df_BUY['historical_price'][i] = get_price_historical(df_BUY['time'][i], df_BUY['symbol'][i])

    df_BUY['delta'] = np.where(df_BUY['actual_price'] - df_BUY['symbol_price'] >= 0, 'POSITIVE', 'NEGATIVE')
    df_BUY['delta_percent'] = 100 * (df_BUY['actual_price'] - df_BUY['symbol_price']) / df_BUY['symbol_price']

    df_BUY['diff'] = np.where(df_BUY['historical_price'] == df_BUY['symbol_price'], True, False)
    df_BUY['diff_val'] = np.where(df_BUY['diff'], True, df_BUY['historical_price'] - df_BUY['symbol_price'])


    df_SELL['historical_buying_price'] = ""
    df_SELL['historical_selling_price'] = ""
    for i in df_SELL.index.tolist():
        df_SELL['historical_selling_price'][i] = get_price_historical(df_SELL['time'][i], df_SELL['symbol'][i])
        df_SELL['historical_buying_price'][i] = get_price_historical(df_SELL['buying_time'][i], df_SELL['symbol'][i])

    df_SELL['diff_selling_price'] = np.where(df_SELL['historical_selling_price'] == df_SELL['symbol_price'], True, False)
    df_SELL['diff_selling_price_val'] = np.where(df_SELL['diff_selling_price'], True, df_SELL['historical_selling_price'] - df_SELL['symbol_price'])
    df_SELL['delta_selling_percent'] = 100 * (df_SELL['historical_selling_price'] - df_SELL['symbol_price']) / df_SELL['symbol_price']

    df_SELL['diff_buying_price'] = np.where(df_SELL['historical_buying_price'] == df_SELL['symbol_buying_price'], True, False)
    df_SELL['diff_buying_price_val'] = np.where(df_SELL['diff_buying_price'], True, df_SELL['historical_buying_price'] - df_SELL['symbol_buying_price'])
    df_SELL['delta_buying_percent'] = 100 * (df_SELL['historical_buying_price'] - df_SELL['symbol_buying_price']) / df_SELL['symbol_buying_price']

    df_BUY.to_csv('./bot_check/buying_history.csv')
    df_SELL.to_csv('./bot_check/selling_history.csv')

    return df_BUY, df_SELL
