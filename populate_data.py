import math
from datetime import datetime, date, timedelta, timezone
import time
from binance.client import Client
import config
import sqlite3
import pandas as pd
from sqlite3 import Error
from scanner_rules import prepare_data, is_combo, is_combo_ivt, is_pinbar_on_trend, candle_side

# engine = create_engine('sqlite:///dir_graph.sqlite', connect_args={'check_same_thread': False}, echo=True)
### CONSTANTS
client = Client(config.API_KEY, config.API_SECRET)
UT = {"M1": "1m", "M3": "3m", "M5": "5m", "M15": "15m", "M30": "30m", "H1": "1h", "H2": "2h", "H4": "4h", "H6": "6h",
      "H8": "8h", "H12": "12h", "D1": "1d", "D3": "3d", "W1": "1w", "M": "1M"}
bin_sizes = {"1m": 1, "3m": 3, "5m": 5, "15m": 15, "30m": 30, "1h": 60, "2h": 120, "4h": 240, "6h": 360, "8h": 480,
             "12h": 720, "1d": 1440, "3d": 4320, "1W": 10080}
batch_size = 750
nb_histo_candle = 200


### FUNCTIONS
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False, timeout=40)
    except Error as e:
        print(e)

    return conn


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def get_old_and_new_candle_time(conn, symbol, ut):
    cur = conn.cursor()
    for key, value in UT.items():
        if key == ut:
            tf = value
            break
    try:
        cur.execute(
            "select max(date) from instrument_data inner join instrument on instrument_data.imnt_id = instrument.imnt_id where instrument.symbol = ? and instrument_data.ut = ?",
            (symbol, ut))
        rec = cur.fetchone()
    except Exception as e:
        print(e)

    today = datetime.now()
    nb_min = nb_histo_candle * bin_sizes[tf]
    init_date = today - timedelta(minutes=nb_min)

    if rec[0] is None:
        old = init_date
        purge = None
    else:
        old = datetime.strptime(rec[0], '%Y-%m-%d %H:%M:%S')
        purge = init_date

    new = pd.to_datetime(client.get_klines(symbol=symbol, interval=tf)[-1][0], unit='ms')

    return old, new, purge


def get_instrument_id(conn, symbol):
    cur = conn.cursor()
    try:
        cur.execute("select imnt_id from instrument where symbol = ?", (symbol,))
        rec = cur.fetchone()
    except Exception as e:
        print(e)
    cur.close()
    return rec[0]


def delete_instrument_data(conn, date, ut, imnt_id):
    cur = conn.cursor()
    try:
        query = "delete from instrument_data where date = ? and ut = ? and imnt_id = ?"
        cur.execute(query, (date, ut, imnt_id))
    except Exception as e:
        print(e)
    conn.commit()
    print('Delete existing candles to refresh : %d ' % (cur.rowcount,))
    cur.close()
    return 1


def purge_instrument_data(conn, date, ut, imnt_id):
    cur = conn.cursor()
    try:
        query = "delete from instrument_data where date < ? and ut = ? and imnt_id = ?"
        cur.execute(query, (date, ut, imnt_id))
    except Exception as e:
        print(e)
    conn.commit()
    print('Delete old candles : %d ' % (cur.rowcount,))
    cur.close()
    return 1


def populate_instrument_data(conn, symbol, ut, save=False):
    # Check if data exists
    # sql = "select date, open, high, low, close, volume from instrument_data inner join instrument on instrument_data.imnt_id = instrument.imnt_id where instrument.symbol = '{0}' and instrument_data.ut ='{1}'".format(symbol, ut)
    # data_df = pd.read_sql_query (sql, con=conn)
    # if len(data_df) == 0:
    #   data_df = pd.DataFrame()
    # Check if it is the first load or not
    cur = conn.cursor()
    try:
        cur.execute(
            "select count(1) from instrument_data inner join instrument on instrument_data.imnt_id = instrument.imnt_id where instrument.symbol = ? and instrument_data.ut = ?",
            (symbol, ut))
        rec = cur.fetchone()
    except Exception as e:
        print(e)

    is_first_load = False

    if rec[0] == 0:
        is_first_load = True

    # Get the last candle in the db otherwise the initiale datetime from which we want to load data
    oldest_point, newest_point, purge_point = get_old_and_new_candle_time(conn, symbol, ut)

    delta_min = (newest_point - oldest_point).total_seconds() / 60

    for key, value in UT.items():
        if key == ut:
            tf = value
            break

    available_data = math.ceil(delta_min / bin_sizes[tf])

    if is_first_load:
        print('Downloading all available %s data for %s. Be patient..!' % (tf, symbol))
    else:
        print('Downloading %d minutes of new data available for %s, i.e. %d instances of %s data.' % (
            delta_min, symbol, available_data, tf))

    klines = client.get_historical_klines(symbol, tf, oldest_point.strftime("%d %b %Y %H:%M:%S"))

    if len(klines) == 0:
        return -1

    raw = pd.DataFrame(klines,
                       columns=['date', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av',
                                'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])

    raw['date'] = pd.to_datetime(raw['date'], unit='ms')
    # raw['date'] = raw['date'].apply(utc_to_local, axis=1)

    # Get the imnt_id and Add it to the dataframe / Add the UT
    imnt_id = get_instrument_id(conn, symbol)
    raw['imnt_id'] = imnt_id
    raw['ut'] = ut

    # Filter the columns to match the ones in db
    cols = [col for col in raw.columns if col in ['imnt_id', 'ut', 'date', 'open', 'high', 'low', 'close', 'volume']]
    data = raw[cols]

    data.set_index('date', inplace=True)

    # Clear the existing candle(s) from db if it is not the first load
    # Look @executemany()
    if is_first_load is False:
        for index, row in data.iterrows():
            # delete_instrument_info(conn,row['imnt_id'],ut,index.strftime("%d %b %Y %H:%M:%S"))
            delete_instrument_data(conn, index.strftime('%Y-%m-%d %H:%M:%S'), ut, imnt_id)

    # Purge old records in order to keep the only number of candles required
    purge_instrument_data(conn, purge_point, ut, imnt_id)

    # Insert the new records in the db
    data.to_sql('instrument_data', conn, if_exists='append')
    # print('Populate Instrument Data : %d new symbol inserted' % (data[0].count(),))
    cur.close()

    return data


def populate_instrument_data_old(conn, symbol, ut, timeframe):
    cur = conn.cursor()

    for key, value in UT.items():
        if key == ut:
            tf = value
            break

    records = client.get_historical_klines(symbol[1], tf, timeframe)

    for record in records:
        try:
            record[0] = (datetime.fromtimestamp(record[0] / 1000)).strftime('%Y-%m-%d %H:%M:%S')
            cur.execute(
                "INSERT INTO instrument_data(imnt_id,ut,date,open,high,low,close,volume) VALUES (?,?,?,?,?,?,?,?)",
                (symbol[0], ut, record[0], record[1], record[2], record[3], record[4], record[5]))
        except Exception as e:
            # print(f'instrument: {symbol[0]} , UT: {ut}')
            print(e)
    print('Populate Instrument Info : %d new symbol info inserted' % (cur.rowcount,))
    conn.commit()
    cur.close()


def populate_instrument(conn):
    cur = conn.cursor()

    instruments = client.get_all_tickers()

    # Get the existing symbol loaded in the db
    try:
        cur.execute("""
            SELECT symbol FROM instrument
        """)
        rows = cur.fetchall()
        symbols = [row[0] for row in rows]
    except Exception as e:
        print(e)

    # Insert new symbols
    ct = 1
    for imnt in instruments:
        try:
            if imnt['symbol'] not in symbols:
                cur.execute("INSERT INTO instrument(symbol) VALUES (?)", (imnt['symbol'],))
                ct += 1
        except Exception as e:
            print('Symbol: ' + imnt['symbol'])
            print(e)
    print('Populate Instrument : %d new symbol inserted' % (ct,))
    conn.commit()
    cur.close()


def get_all_symbols(conn):
    cur = conn.cursor()
    # Get the list of symbol you want data from
    try:
        cur.execute("""
            select * from instrument where (symbol like '%ETH' or symbol like '%BTC' or symbol like '%USDT' or symbol like '%BNB') LIMIT 5
        """)
        rows = cur.fetchall()
        symbols = [row[1] for row in rows]
    except Exception as e:
        print(e)

    cur.close()
    return symbols


def get_symbols(conn, pair, limit=None):
    cur = conn.cursor()
    # Get the list of symbol you want data from
    try:
        if limit is None:
            cur.execute("""select * from instrument where symbol like '%{}' and symbol not like '%BEAR%'  and symbol 
            not like '%BULL%' and symbol not like '%DOWN%' and symbol not like '%UP%'""".format(pair))
        else:
            cur.execute("""select * from instrument where symbol like '%{}'  and symbol not like '%BEAR%'  and symbol 
            not like '%BULL%' and symbol not like '%DOWN%' and symbol not like '%UP%' LIMIT {}""".format(pair, limit))
        rows = cur.fetchall()
        symbols = [row[1] for row in rows]
    except Exception as e:
        print(e)

    cur.close()
    return symbols


def delete_signal(conn, ut, imnt_id):
    cur = conn.cursor()
    try:
        query = "delete from signal where ut = ? and imnt_id = ?"
        cur.execute(query, (ut, imnt_id))
    except Exception as e:
        print('Delete Signal : %d / %s ' % (imnt_id, ut))
        print(e)
    conn.commit()
    print('Delete existing signals to refresh : %d ' % (cur.rowcount,))
    cur.close()
    return 1


def populate_signals(conn, symbol, ut):
    cur = conn.cursor()

    df = prepare_data(conn, symbol, ut)

    if df.empty or df.shape[0] < 100:
        return -1

    combo_signal = is_combo(df)
    combo_ivt_signal = is_combo_ivt(df)
    pinbar = is_pinbar_on_trend(df)
    side = candle_side(df)

    # Grab the imnt and ut
    df_imnt = int(df['imnt_id'].head(1).get(0))
    df_ut = df['ut'].head(1).get(0)
    try:
        delete_signal(conn, df_ut, df_imnt)
        # if combo_signal != 0 or combo_ivt_signal != 0 or pinbar != 0:
        cur.execute("INSERT INTO signal(imnt_id, ut, is_combo, is_combo_ivt, is_pinbar, candle_side) VALUES (?,?,?,?,?,?)",
                        (df_imnt, df_ut, combo_signal, combo_ivt_signal, pinbar,side))
    except Exception as e:
        print('Error Insert Signal : %d / %s ' % (df_imnt, df_ut))
        print(e)

    print('Insert Signal : %d / %s ' % (df_imnt, df_ut))
    conn.commit()
    cur.close()


def refresh_all_instrument_data(conn, pair, ut):
    symbols = get_symbols(conn, pair)
    i = 0
    
    for symbol in symbols:
        data = populate_instrument_data(conn, symbol, ut)

        if ut in ["M5", "M15", "M30", "H1", "H2", "H4", "H6", "H8", "H12", "D1", "D3"]:
            populate_signals(conn, symbol, ut)

        # sleep after every 3rd call to be kind to the API
        i += 1
        if i % 3 == 0:
            time.sleep(1)

# populate the instrument info
# for row in rows:
# gettokendata(token['symbol'], 'M5', "1000 minute ago CET")
# gettokendata(token['symbol'], 'M15', "3000 minute ago CET")
# gettokendata(token['symbol'], 'M30', "6000 minute ago CET")
# gettokendata(token['symbol'], 'H1', "200 hour ago CET")
# gettokendata(token['symbol'], 'H2', "400 hour ago CET")
# gettokendata(token['symbol'], 'H4', "800 hour ago CET")
# gettokendata(token['symbol'], 'H6', "1200 hour ago CET")
# gettokendata(token['symbol'], 'H12', "2400 hour ago CET")
# gettokendata(token['symbol'], 'D1', "200 day ago CET")
# gettokendata(token['symbol'], 'D3', "600 day ago CET")
# gettokendata(token['symbol'], 'W1', "200 week ago CET")
# populateinstrumentinfo(conn, row, 'D1', "200 day ago CET")
