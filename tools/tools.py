import pandas as pd

def del_column_starting_with(df, str):
    list_column_names = df.columns.tolist()
    for name in list_column_names:
        if name.startswith(str):
            df = df.drop([name], axis=1)
    return df

def add_str_to_column_name(df, str):
    list_column_names = df.columns.tolist()
    new_list_column_names = []
    for name in list_column_names:
        name = str + name
        new_list_column_names.append(name)
    df.columns = new_list_column_names
    return df

def anlysis_to_df(analysis, index_date):
    df_indicators_brut = pd.DataFrame([analysis.indicators])
    del_column_starting_with(df_indicators_brut, 'Rec.')
    del_column_starting_with(df_indicators_brut, 'change')

    df_moving_averages = pd.DataFrame([analysis.moving_averages])
    df_moving_averages.drop(columns=df_moving_averages.columns[-1], axis=1, inplace=True)
    df_moving_averages_compute = pd.DataFrame([analysis.moving_averages['COMPUTE']])

    df_oscillators = pd.DataFrame([analysis.oscillators])
    df_oscillators.drop(columns=df_oscillators.columns[-1], axis=1, inplace=True)
    df_oscillators_compute = pd.DataFrame([analysis.oscillators['COMPUTE']])

    add_str_to_column_name(df_oscillators, "OSCc_")
    add_str_to_column_name(df_moving_averages, "OSC_")

    df_indicators_discret = pd.concat([df_oscillators_compute, df_moving_averages_compute], axis=1)
    df_summary_level_1 = pd.concat([df_oscillators, df_moving_averages], axis=1)
    df_summary_level_0 = pd.DataFrame([analysis.summary])

    df_summary_level_0.index = [index_date]
    df_summary_level_1.index = [index_date]
    df_indicators_discret.index = [index_date]
    df_indicators_brut.index = [index_date]

    return df_summary_level_0, df_summary_level_1, df_indicators_discret, df_indicators_brut