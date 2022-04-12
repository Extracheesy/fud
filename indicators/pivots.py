# https://www.tradingview.com/support/solutions/43000614331-technical-ratings/
# https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html
# https://www.tradingview.com/support/solutions/43000614331-technical-ratings/
# https://www.tradingview.com/support/solutions/43000521824-pivot-points-standard/

import pandas as pd
import numpy as np

def get_pecedent_high(lst, period):
    test_df = pd.DataFrame()
    len_def = len(lst)

    new_lst = []
    new_lst_2 = []
    max_lst = []
    min_lst = []
    for i in range(len_def, 0, -1):
        val_min = i - period
        if val_min < 0:
            val_min = 0
        new_lst_2.append(lst[i-1])
        new_lst.append(lst[val_min : i])
        max_lst.append(max(lst[val_min: i]))
        min_lst.append(min(lst[val_min: i]))

    max_lst.reverse()
    min_lst.reverse()

    return max_lst, min_lst

def add_PIVOTS_CLASSIC(df):
    list_index = df.index.tolist()

    fmt = '%Y-%m-%d %H:%M:%S'
    # tstamp1 = datetime.strptime(list_index[0], fmt)
    # tstamp2 = datetime.strptime(list_index[1], fmt)

    tstamp1 = list_index[0]
    tstamp2 = list_index[1]

    if tstamp1 > tstamp2:
        td = tstamp1 - tstamp2
    else:
        td = tstamp2 - tstamp1
    td_mins = int(round(td.total_seconds() / 60))

    # print('The difference is approx. %s minutes' % td_mins)

    PPClassic = pd.DataFrame()
    PPClassic['CLOSEcurr'] = df['close']
    # PPClassic['CLOSEprev'] = df['close'].shift(1)
    PPClassic['CLOSEprev'] = df['close']
    PPClassic['HIGHcurr'] = df['high']
    # PPClassic['HIGHprev'] = df['high'].shift(1)
    PPClassic['LOWcurr'] = df['low']
    # PPClassic['LOWprev'] = df['low'].shift(1)

    PPClassic['HIGHprev'], PPClassic['LOWprev'] = get_pecedent_high(df['close'].tolist(), 30)

    PPClassic['PP'] = (PPClassic['HIGHprev'] + PPClassic['LOWprev'] + PPClassic['CLOSEprev']) / 3
    df['Pivot.M.Classic.R1'] = PPClassic['PP'] * 2 - PPClassic['LOWprev']
    df['Pivot.M.Classic.S1'] = PPClassic['PP'] * 2 - PPClassic['HIGHprev']
    df['Pivot.M.Classic.R2'] = PPClassic['PP'] + (PPClassic['HIGHprev'] - PPClassic['LOWprev'])
    df['Pivot.M.Classic.S2'] = PPClassic['PP'] - (PPClassic['HIGHprev'] - PPClassic['LOWprev'])
    df['Pivot.M.Classic.R3'] = PPClassic['PP'] + 2 * (PPClassic['HIGHprev'] - PPClassic['LOWprev'])
    df['Pivot.M.Classic.S3'] = PPClassic['PP'] - 2 * (PPClassic['HIGHprev'] - PPClassic['LOWprev'])
    df['Pivot.M.Classic.Middle'] = PPClassic['PP']

def add_PIVOTS_FIBONACCI(df):
    list_index = df.index.tolist()

    fmt = '%Y-%m-%d %H:%M:%S'
    # tstamp1 = datetime.strptime(list_index[0], fmt)
    # tstamp2 = datetime.strptime(list_index[1], fmt)

    tstamp1 = list_index[0]
    tstamp2 = list_index[1]

    if tstamp1 > tstamp2:
        td = tstamp1 - tstamp2
    else:
        td = tstamp2 - tstamp1
    td_mins = int(round(td.total_seconds() / 60))

    # print('The difference is approx. %s minutes' % td_mins)

    PPClassic = pd.DataFrame()
    PPClassic['CLOSEcurr'] = df['close']
    # PPClassic['CLOSEprev'] = df['close'].shift(1)
    PPClassic['CLOSEprev'] = df['close']
    PPClassic['HIGHcurr'] = df['high']
    # PPClassic['HIGHprev'] = df['high'].shift(1)
    PPClassic['LOWcurr'] = df['low']
    # PPClassic['LOWprev'] = df['low'].shift(1)

    PPClassic['HIGHprev'], PPClassic['LOWprev'] = get_pecedent_high(df['close'].tolist(), 30)

    # PP = (HIGHprev + LOWprev + CLOSEprev) / 3
    PPClassic['PP'] = (PPClassic['HIGHprev'] + PPClassic['LOWprev'] + PPClassic['CLOSEprev']) / 3
    # R1 = PP + 0.382 * (HIGHprev - LOWprev)
    df['Pivot.M.Fibonacci.R1'] = PPClassic['PP'] + 0.382 * (PPClassic['HIGHprev'] - PPClassic['LOWprev'])
    # S1 = PP - 0.382 * (HIGHprev - LOWprev)
    df['Pivot.M.Fibonacci.S1'] = PPClassic['PP'] - 0.382 * (PPClassic['HIGHprev'] - PPClassic['LOWprev'])
    # R2 = PP + 0.618 * (HIGHprev - LOWprev)
    df['Pivot.M.Fibonacci.R2'] = PPClassic['PP'] + 0.618 * (PPClassic['HIGHprev'] - PPClassic['LOWprev'])
    # S2 = PP - 0.618 * (HIGHprev - LOWprev)
    df['Pivot.M.Fibonacci.S2'] = PPClassic['PP'] - 0.618 * (PPClassic['HIGHprev'] - PPClassic['LOWprev'])
    # R3 = PP + (HIGHprev - LOWprev)
    df['Pivot.M.Fibonacci.R3'] = PPClassic['PP'] + (PPClassic['HIGHprev'] - PPClassic['LOWprev'])
    # S3 = PP - (HIGHprev - LOWprev)
    df['Pivot.M.Fibonacci.S3'] = PPClassic['PP'] - (PPClassic['HIGHprev'] - PPClassic['LOWprev'])
    df['Pivot.M.Fibonacci.Middle'] = PPClassic['PP']


def add_PIVOTS_CAMARILLA(df):
    list_index = df.index.tolist()

    fmt = '%Y-%m-%d %H:%M:%S'
    # tstamp1 = datetime.strptime(list_index[0], fmt)
    # tstamp2 = datetime.strptime(list_index[1], fmt)

    tstamp1 = list_index[0]
    tstamp2 = list_index[1]

    if tstamp1 > tstamp2:
        td = tstamp1 - tstamp2
    else:
        td = tstamp2 - tstamp1
    td_mins = int(round(td.total_seconds() / 60))

    # print('The difference is approx. %s minutes' % td_mins)

    PPClassic = pd.DataFrame()
    PPClassic['CLOSEcurr'] = df['close']
    # PPClassic['CLOSEprev'] = df['close'].shift(1)
    PPClassic['CLOSEprev'] = df['close']
    PPClassic['HIGHcurr'] = df['high']
    # PPClassic['HIGHprev'] = df['high'].shift(1)
    PPClassic['LOWcurr'] = df['low']
    # PPClassic['LOWprev'] = df['low'].shift(1)

    PPClassic['HIGHprev'], PPClassic['LOWprev'] = get_pecedent_high(df['close'].tolist(), 30)

    # PP = (HIGHprev + LOWprev + CLOSEprev) / 3
    PPClassic['PP'] = (PPClassic['HIGHprev'] + PPClassic['LOWprev'] + PPClassic['CLOSEprev']) / 3
    # R1 = CLOSEprev + 1.1 * (HIGHprev - LOWprev) / 12
    df['Pivot.M.Camarilla.R1'] = PPClassic['CLOSEprev'] + 1.1 * (PPClassic['HIGHprev'] - PPClassic['LOWprev']) / 12
    # S1 = CLOSEprev - 1.1 * (HIGHprev - LOWprev) / 12
    df['Pivot.M.Camarilla.S1'] = PPClassic['CLOSEprev'] - 1.1 * (PPClassic['HIGHprev'] - PPClassic['LOWprev']) / 12
    # R2 = CLOSEprev + 1.1 * (HIGHprev - LOWprev) / 6
    df['Pivot.M.Camarilla.R2'] = PPClassic['CLOSEprev'] + 1.1 * (PPClassic['HIGHprev'] - PPClassic['LOWprev']) / 6
    # S2 = CLOSEprev - 1.1 * (HIGHprev - LOWprev) / 6
    df['Pivot.M.Camarilla.S2'] = PPClassic['CLOSEprev'] - 1.1 * (PPClassic['HIGHprev'] - PPClassic['LOWprev']) / 6
    # R3 = CLOSEprev + 1.1 * (HIGHprev - LOWprev) / 4
    df['Pivot.M.Camarilla.R3'] = PPClassic['CLOSEprev'] + 1.1 * (PPClassic['HIGHprev'] - PPClassic['LOWprev']) / 4
    # S3 = CLOSEprev - 1.1 * (HIGHprev - LOWprev) / 4
    df['Pivot.M.Camarilla.S3'] = PPClassic['CLOSEprev'] - 1.1 * (PPClassic['HIGHprev'] - PPClassic['LOWprev']) / 4
    df['Pivot.M.Camarilla.Middle'] = PPClassic['PP']

def add_PIVOTS_WOODIE(df):
    list_index = df.index.tolist()

    fmt = '%Y-%m-%d %H:%M:%S'
    # tstamp1 = datetime.strptime(list_index[0], fmt)
    # tstamp2 = datetime.strptime(list_index[1], fmt)

    tstamp1 = list_index[0]
    tstamp2 = list_index[1]

    if tstamp1 > tstamp2:
        td = tstamp1 - tstamp2
    else:
        td = tstamp2 - tstamp1
    td_mins = int(round(td.total_seconds() / 60))

    # print('The difference is approx. %s minutes' % td_mins)

    PPClassic = pd.DataFrame()
    PPClassic['CLOSEcurr'] = df['close']
    # PPClassic['CLOSEprev'] = df['close'].shift(1)
    PPClassic['CLOSEprev'] = df['close']
    PPClassic['HIGHcurr'] = df['high']
    # PPClassic['HIGHprev'] = df['high'].shift(1)
    PPClassic['LOWcurr'] = df['low']
    # PPClassic['LOWprev'] = df['low'].shift(1)

    PPClassic['HIGHprev'], PPClassic['LOWprev'] = get_pecedent_high(df['close'].tolist(), 30)

    # PP = (HIGHprev + LOWprev + 2 * OPENcurr) / 4
    PPClassic['PP'] = (PPClassic['HIGHprev'] + PPClassic['LOWprev'] + 2 * PPClassic['CLOSEprev']) / 4
    # R1 = 2 * PP - LOWprev
    df['Pivot.M.Woodie.R1'] = 2 * PPClassic['PP'] - PPClassic['LOWprev']
    # S1 = 2 * PP - HIGHprev
    df['Pivot.M.Woodie.S1'] = 2 * PPClassic['PP'] - PPClassic['HIGHprev']
    # R2 = PP + (HIGHprev - LOWprev)
    df['Pivot.M.Woodie.R2'] = PPClassic['PP'] + (PPClassic['HIGHprev'] - PPClassic['LOWprev'])
    # S2 = PP - (HIGHprev - LOWprev)
    df['Pivot.M.Woodie.S2'] = PPClassic['PP'] - (PPClassic['HIGHprev'] - PPClassic['LOWprev'])
    # R3 =  HIGHprev + 2 * (PP -  LOWprev)
    df['Pivot.M.Woodie.R3'] = PPClassic['HIGHprev'] + 2 * (PPClassic['PP'] - PPClassic['LOWprev'])
    # S3 =  LOWprev - 2 * (HIGHprev - PP)
    df['Pivot.M.Woodie.S3'] = PPClassic['LOWprev'] - 2 * (PPClassic['HIGHprev'] - PPClassic['PP'])
    df['Pivot.M.Woodie.Middle'] = PPClassic['PP']

def add_PIVOTS_DM(df):

    list_index = df.index.tolist()

    fmt = '%Y-%m-%d %H:%M:%S'
    # tstamp1 = datetime.strptime(list_index[0], fmt)
    # tstamp2 = datetime.strptime(list_index[1], fmt)

    tstamp1 = list_index[0]
    tstamp2 = list_index[1]

    if tstamp1 > tstamp2:
        td = tstamp1 - tstamp2
    else:
        td = tstamp2 - tstamp1
    td_mins = int(round(td.total_seconds() / 60))

    # print('The difference is approx. %s minutes' % td_mins)

    PPClassic = pd.DataFrame()
    PPClassic['CLOSEcurr'] = df['close']
    # PPClassic['CLOSEprev'] = df['close'].shift(1)
    PPClassic['CLOSEprev'] = df['close']
    PPClassic['OPENprev'] = df['open']
    PPClassic['HIGHcurr'] = df['high']
    # PPClassic['HIGHprev'] = df['high'].shift(1)
    PPClassic['LOWcurr'] = df['low']
    # PPClassic['LOWprev'] = df['low'].shift(1)

    PPClassic['HIGHprev'], PPClassic['LOWprev'] = get_pecedent_high(df['close'].tolist(), 30)

    PPClassic['X'] = 0
    # IF  OPENprev == CLOSEprev
    #     X = HIGHprev + LOWprev + 2 * CLOSEprev
    PPClassic['X'] = np.where(PPClassic['OPENprev'] == PPClassic['CLOSEprev'], PPClassic['HIGHprev'] + PPClassic['LOWprev'] + 2 * PPClassic['CLOSEprev'], PPClassic['X'])
    # ELSE
    #       IF CLOSEprev > OPENprev
    #           X = 2 * HIGHprev + LOWprev + CLOSEprev
    PPClassic['X'] = np.where(PPClassic['OPENprev'] > PPClassic['CLOSEprev'], 2 * PPClassic['HIGHprev'] + PPClassic['LOWprev'] + PPClassic['CLOSEprev'], PPClassic['X'])
    #       ELSE
    #           X = 2 * LOWprev + HIGHprev + CLOSEprev
    PPClassic['X'] = np.where(PPClassic['OPENprev'] < PPClassic['CLOSEprev'], 2 * PPClassic['LOWprev'] + PPClassic['HIGHprev'] + PPClassic['CLOSEprev'], PPClassic['X'])

    # PP = X / 4
    PPClassic['PP'] = PPClassic['X'] / 4
    # R1 = X / 2 - LOWprev
    df['Pivot.M.Demark.R1'] = PPClassic['X'] / 2 - PPClassic['LOWprev']
    # S1 = X / 2 - HIGHprev
    df['Pivot.M.Demark.S1'] = PPClassic['X'] / 2 - PPClassic['HIGHprev']

    df['Pivot.M.Demark.Middle'] = PPClassic['PP']
