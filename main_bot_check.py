import sys
sys.path.append('live_tools/utilities')

import pandas as pd
import requests

import config

# from TV_indicators import TA_Handler, Interval, get_multiple_analysis
from tradingview_ta import TA_Handler, Interval
import process_recom
import process_indicators
# import TV_analysis
import tools
import fletch_data

import verif_bot

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    df_buying, df_selling = verif_bot.verif_bot()


    print_hi('PyCharm')


