from populate_data import create_connection, refresh_all_instrument_data
import config, sys
from datetime import datetime
import pandas as pd

from scanner_rules import get_convergence

conn = create_connection(config.DB_FILE)

# Populate the instrument
#refresh_all_instrument_data(conn, 'ETH', 'D1')


# get the candle convergence
# sql = "select ut, date, open, low from instrument_data inner join instrument on instrument_data.imnt_id = instrument.imnt_id where instrument.symbol = 'BNBETH'"
# df = pd.read_sql_query(sql, con=conn)
# df["date"] = pd.to_datetime(df["date"])
# #df.sort_values('date', inplace=True, ascending=False)
# df.sort_values(by=["ut", "date"], inplace=True, ascending=[False, False])
#
# print(df)
#
# g = df.groupby("ut").head(1)
#
# print(g)

g = get_convergence(conn, 'BNBETH')

print(g)


# df1 = df.groupby(["ut"])
# df2 = df1.apply(lambda x: x.sort_values(["date"]))

# g = df.groupby(["ut"]).apply(lambda x: x.sort_values(["date"], ascending=True)).reset_index(drop=True)
# g.groupby("ut").head(1)
#
# print(g)
#
# e = df.set_index('symbol').groupby("ut")['date'].nlargest(1).reset_index()
#
# print(e)

# from datetime import datetime, timedelta, date
# from binance.client import Client
# import config
# import pandas as pd
# import sqlite3
# from populate_data import create_connection, get_old_and_new_candle_time
#
# client = Client(config.API_KEY, config.API_SECRET)
#
# conn = create_connection(config.DB_FILE)
#
# sql = "select instrument.imnt_id, symbol, ut, date, open, high, low, close, volume from instrument_data inner join instrument on instrument_data.imnt_id = instrument.imnt_id where instrument.symbol = 'BNBETH' and instrument_data.ut ='D1'"
# df = pd.read_sql_query(sql, con=conn)
# df.sort_values(by='date')
#
# print(" Close : d% ", df.iloc[-1]['close'])
# print(" Open : d% ", df.iloc[-1]['open'])




# get the last candle
# candles = client.get_klines(symbol='ETHUSDT', interval='1d')
# date = pd.to_datetime(client.get_klines(symbol='ETHUSDT', interval='1d')[-1][0], unit='ms')
#
# candle2 = client.get_historical_klines('ETHUSDT','1d','04 Mar 2021 01:00:00')
#
# data = pd.DataFrame(candle2,  columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av',
#                                  'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
#
# data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
#
# print(data)



# old, new = get_old_and_new_candle_time(conn, 'BNBETH', 'M30')
#
# print(old)
# print(new)

# today = datetime.now()
#
# previous = today - timedelta(minutes=100)
#
# timedelta()
#
# print(today)
#
# print(previous)







# print(previous)
#
# print("{:'%d %b %Y'}".format(previous))
#
# today = "{:'%d %b %Y'}".format(date.today())
#
# print(today)
#
# back_date = date.today() - timedelta(days=100)
#
# init_date = "{:'%d %b %Y'}".format(back_date)
#
# print(init_date)

#new = pd.to_datetime(Client.get_klines(symbol='BTCUSDT', interval = "5m")[-1][0], units='ms')

# print(candles)
#
# print(candles[-1])
#
# print(date)
#
# print(datetime.strptime('1 Jan 2017', '%d %b %Y'))
#
# print(candle2)

#if source == "binance": new = pd.to_datetime(binance_client.get_klines(symbol=symbol, interval=kline_size)[-1][0], unit='ms')