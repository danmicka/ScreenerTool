import os, time, re, shutil
import config, csv
from binance.client import Client
from datetime import datetime, timedelta

client = Client(config.API_KEY, config.API_SECRET)

UT = {"M1": "1m", "M3": "3m", "M5": "5m", "M15": "15m", "M30": "30m", "H1": "1h", "H2": "2h", "H4": "4h", "H6": "6h",
      "H8": "8h", "H12": "12h", "D1": "1d", "D3": "3d", "W1": "1w", "M": "1M"}


def gettokendata(token, ut, timeframe):

    filename = 'data/' + ut + '/' + token + '_' + ut + '.csv'

    for key, value in UT.items():
        if key == ut:
            tf = value

    tokens = client.get_historical_klines(token, tf, timeframe)

    if len(tokens) == 0 or len(tokens) < 50:
        return

    csvfile = open(filename, 'w', newline='')
    csvfile_writer = csv.writer(csvfile, delimiter=',')

    csvfile_writer.writerow(['Open_time','Open','High','Low','Close','Volume','Close_time'])

    for token in tokens:
        token[0] = (datetime.fromtimestamp(token[0] / 1000)).strftime('%Y-%m-%d %H:%M:%S')
        token[6] = (datetime.fromtimestamp(token[6] / 1000)).strftime('%Y-%m-%d %H:%M:%S')
        csvfile_writer.writerow([token[0], token[1], token[2], token[3], token[4], token[6], token[6]])

    print(filename)
    csvfile.close()


def getalltokeninfo():
    tokenscsv = open('../data/tokens.csv', 'w', newline='')
    token_writer = csv.writer(tokenscsv)
    _tokens = client.get_all_tickers()

    for _token in _tokens:
        token_writer.writerow([_token['symbol'], _token['price']])

    tokenscsv.close()


# getalltokeninfo()

# gettokendata('BTCUSDT', 'M15', "1 week ago CET")

def generateallcsvfiles():

    for ut in UT:
        if not os.path.exists('data/' + ut + '/'):
            os.makedirs('data/' + ut + '/')
        for f in os.listdir('data/' + ut + '/'):
            os.remove(os.path.join('data/' + ut + '/', f))

    # Get the list of available tokens
    tokens = client.get_all_tickers()
    #i = 1
    for token in tokens:
        if token['symbol'][-4:] == 'USDT' and 'UP' not in token['symbol'] and 'DOWN' not in token['symbol']:# and token['symbol'][:3] == 'ADA':
            # gettokendata(token['symbol'], 'M5', "1000 minute ago CET")
            # gettokendata(token['symbol'], 'M15', "3000 minute ago CET")
            # gettokendata(token['symbol'], 'M30', "6000 minute ago CET")
            # gettokendata(token['symbol'], 'H1', "200 hour ago CET")
            # gettokendata(token['symbol'], 'H2', "400 hour ago CET")
            # gettokendata(token['symbol'], 'H4', "800 hour ago CET")
            # gettokendata(token['symbol'], 'H6', "1200 hour ago CET")
            # gettokendata(token['symbol'], 'H12', "2400 hour ago CET")
            gettokendata(token['symbol'], 'D1', "200 day ago CET")
            # gettokendata(token['symbol'], 'D3', "600 day ago CET")
            # gettokendata(token['symbol'], 'W1', "200 week ago CET")

            # sleep after every 3rd call to be kind to the API
            #i += 1
            # if i % 3 == 0:
            #     time.sleep(1)

generateallcsvfiles()



