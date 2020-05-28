#!/bin/bash

import pandas as pd
from datetime import datetime, timedelta
from binance.client import Client
import sys

binance_client = Client()

end_date = int(datetime(year=2020, month=5, day=28).timestamp() * 1000)
start_date = int(datetime(year=2020, month=4, day=1).timestamp() * 1000)


argvs = sys.argv[1:]

for pair in argvs:
    print(pair)
    df_ohlc = None
    klines_h1 = binance_client.get_historical_klines(pair, Client.KLINE_INTERVAL_1HOUR, start_date, end_date)

    ohlc_data = []
    for kline in klines_h1:
        if kline[0]:
            ohlc_data.append(
                [kline[0], float(kline[1]), float(kline[2]), float(kline[3]), float(kline[4]), float(kline[5])])

    df_ohlc = pd.DataFrame(ohlc_data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df_ohlc['Date'] = df_ohlc['Date'].apply(lambda x: pd.to_datetime(x, unit='ms'))
    df_ohlc = df_ohlc.set_index('Date')

    df_ohlc.to_csv("{}-h1.csv".format(pair))
