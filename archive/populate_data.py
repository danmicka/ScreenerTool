from datetime import datetime
from binance.client import Client
import config
import sqlite3

client = Client(config.API_KEY, config.API_SECRET)

connection = sqlite3.connect(config.DB_FILE)

cursor = connection.cursor()

UT = {"M1": "1m", "M3": "3m", "M5": "5m", "M15": "15m", "M30": "30m", "H1": "1h", "H2": "2h", "H4": "4h", "H6": "6h",
      "H8": "8h", "H12": "12h", "D1": "1d", "D3": "3d", "W1": "1w", "M": "1M"}


def populateinstrumentinfo(instrument, ut, timeframe):
    for key, value in UT.items():
        if key == ut:
            tf = value
    records = client.get_historical_klines(instrument[1], tf, timeframe)

    for record in records:
        try:
            record[0] = (datetime.fromtimestamp(record[0] / 1000)).strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                "INSERT INTO instrument_data(imnt_id,ut,date,open,high,low,close,volume) VALUES (?,?,?,?,?,?,?,?)",
                (instrument[0], ut, record[0], record[1], record[2], record[3], record[4], record[5]))
        except Exception as e:
            print(imnt['symbol'])
            print(e)
    connection.commit()

instruments = client.get_all_tickers()

# Get the existing synmbol loaded in the db
cursor.execute("""
    SELECT symbol FROM instrument
""")
rows = cursor.fetchall()
symbols = [row[0] for row in rows]

# Insert new symbols
for imnt in instruments:
    try:
        if imnt['symbol'] not in symbols:
            cursor.execute("INSERT INTO instrument(symbol) VALUES (?)", (imnt['symbol'],))
    except Exception as e:
        print(imnt['symbol'])
        print(e)

connection.commit()

# Get the list of symbol you want data from
cursor.execute("""
    select * from instrument where (symbol like '%ETH' or symbol like '%BTC' or symbol like '%USDT' or symbol like '%BNB') LIMIT 1
""")
rows = cursor.fetchall()
symbols = [row[1] for row in rows]
print(rows)

# populate the instrument info
for row in rows:
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
    populateinstrumentinfo(row, 'D1', "200 day ago CET")

    # sleep after every 3rd call to be kind to the API
    # i += 1
    # if i % 3 == 0:
    #     time.sleep(1)
