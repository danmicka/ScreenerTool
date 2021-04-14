import pandas as pd


### FUNCTIONS
def prepare_data(conn, symbol, ut):
    sql = "select instrument.imnt_id, symbol, ut, date, open, high, low, close, volume from instrument_data inner join instrument on instrument_data.imnt_id = instrument.imnt_id where instrument.symbol = '{0}' and instrument_data.ut ='{1}'".format(
        symbol, ut)

    df = pd.read_sql_query(sql, con=conn)
    df.sort_values(by='date')
    # to do : check the type in the db
    df['close'] = df['close'].astype(float)
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    # Add the indicator values
    # Moving average
    df['20sma'] = df['close'].rolling(window=20).mean()
    df['50sma'] = df['close'].rolling(window=50).mean()
    df['100sma'] = df['close'].rolling(window=100).mean()
    # Bollinger Bands
    df['stddev'] = df['close'].rolling(window=20).std()
    df['lower_band'] = df['20sma'] - (2.5 * df['stddev'])
    df['upper_band'] = df['20sma'] + (2.5 * df['stddev'])
    df['band_width'] = df['upper_band'] - df['lower_band']
    # ATR
    # df['TR'] = abs(df['high'] - df['low'])
    # df['ATR'] = df['TR'].rolling(window=20).mean()

    return df


# def candle_side(row):
#     # row : ut, date, open, close
#     if row["close"] > row["open"]:
#         return 1
#     else:
#         return -1

def candle_side(df):
    df.sort_values(by='date')
    if df.iloc[-1]['close'] > df.iloc[-1]['open']:
        return 1
    else:
        return -1


def get_convergence(conn, symbol):
    sql = "select ut, date, open, close from instrument_data inner join instrument on instrument_data.imnt_id = instrument.imnt_id where instrument.symbol = '{0}'".format(
        symbol)
    df = pd.read_sql_query(sql, con=conn)
    df.sort_values(by=['ut', 'date'])
    df['date'] = pd.to_datetime(df["date"])
    # Get the last candle data
    df.sort_values(by=['ut', 'date'], inplace=True, ascending=[False, False])
    res = df.groupby("ut").head(1)
    res['side'] = df.apply(candle_side, axis=1)
    res['symbol'] = symbol
    # Filter the columns to match the ones in db
    cols = ['symbol', 'ut', 'side']
    # return e list
    data = res[cols].values.tolist()

    return data


def is_combo(df):
    df.sort_values(by='date')
    # Price between MAs - Combo UP
    condition1 = (df.iloc[-1]['close'] > df.iloc[-1]['50sma']) and (df.iloc[-1]['close'] < df.iloc[-1]['20sma'])
    # Trend check
    condition2 = (df.iloc[-1]['20sma'] > df.iloc[-1]['50sma']) and (df.iloc[-1]['50sma'] > df.iloc[-1]['100sma'])
    # Price between MAs - Combo UDOWN
    condition3 = (df.iloc[-1]['close'] < df.iloc[-1]['50sma']) and (df.iloc[-1]['close'] > df.iloc[-1]['20sma'])
    # Trend check
    condition4 = (df.iloc[-1]['20sma'] < df.iloc[-1]['50sma']) and (df.iloc[-1]['50sma'] < df.iloc[-1]['100sma'])

    # Slope
    # pente = slope(df.iloc[-7]['50sma'], df.iloc[-1]['50sma'], 7)
    # condition2 = pente > 20
    # Bollinger Bands
    condition5 = df.iloc[-1]['close'] > df.iloc[-1]['lower_band']
    condition6 = (df.iloc[-6]['band_width'] > df.iloc[-5]['band_width']) and (
            df.iloc[-4]['band_width'] > df.iloc[-3]['band_width']) and (
                         df.iloc[-3]['band_width'] > df.iloc[-2]['band_width']) and (
                         df.iloc[-2]['band_width'] > df.iloc[-1]['band_width'])
    if condition1 and condition2 and condition5 and condition6:
        return 1
    elif condition3 and condition4 and condition5 and condition6:
        return -1
    else:
        return 0


def is_combo_ivt(df):
    df.sort_values(by='date')

    zone = 20
    Close = df.iloc[-1]['close']
    Open = df.iloc[-1]['open']
    Low = df.iloc[-1]['low']
    High = df.iloc[-1]['high']

    Close1 = df.iloc[-2]['close']
    Open1 = df.iloc[-2]['open']
    Low1 = df.iloc[-2]['low']
    High1 = df.iloc[-2]['high']

    BBB = df.iloc[-1]['lower_band']
    BBH = df.iloc[-1]['upper_band']
    MM50 = df.iloc[-1]['50sma']
    BBB1 = df.iloc[-2]['lower_band']
    BBH1 = df.iloc[-2]['upper_band']
    MM501 = df.iloc[-2]['50sma']

    BBRange = (BBH - BBB) * zone / 100
    RangeHUP = BBH + BBRange
    RangeHDN = BBH - BBRange
    RangeBUP = BBB + BBRange
    RangeBDN = BBB - BBRange
    BBRange1 = (BBH1 - BBB1) * zone / 100
    RangeHUP1 = BBH1 + BBRange1
    RangeHDN1 = BBH1 - BBRange1
    RangeBUP1 = BBB1 + BBRange1
    RangeBDN1 = BBB1 - BBRange1

    c1 = (MM50 > RangeHDN and MM50 < RangeHUP)
    c11 = (MM501 > RangeHDN1 and MM501 < RangeHUP1)
    c2 = ((Close or Open or High) > RangeHDN and (Close or Open or High) < RangeHUP)
    c21 = ((Close1 or Open1 or High1) > RangeHDN1 and (Close1 or Open1 or High1) < RangeHUP1)
    c3 = (MM50 > RangeBDN and MM50 < RangeBUP)
    c31 = (MM501 > RangeBDN1 and MM501 < RangeBUP1)
    c4 = ((Close or Open or Low) > RangeBDN1 and (Close or Open or Low) < RangeBUP)
    c41 = ((Close1 or Open1 or Low1) > RangeBDN1 and (Close1 or Open1 or Low1) < RangeBUP1)

    if (c1 or c11) and (c2 or c21):
        return -1
    elif (c3 or c31) and (c4 or c41):
        return 1
    else:
        return 0


def is_pinbar_on_trend(df):
    df.sort_values(by='date')

    # Current Candle
    open = df.iloc[-1]['open']
    close = df.iloc[-1]['close']
    high = df.iloc[-1]['high']
    low = df.iloc[-1]['low']

    Range = high - low

    sma20 = df.iloc[-1]['20sma']
    sma50 = df.iloc[-1]['50sma']
    sma100 = df.iloc[-1]['100sma']

    bblowerband = df.iloc[-1]['lower_band']
    # BBUpperBand = df.iloc[-1]['upper_band']

    # Previous Candle
    open1 = df.iloc[-2]['open']
    close1 = df.iloc[-2]['close']
    high1 = df.iloc[-2]['high']
    low1 = df.iloc[-2]['low']
    Range1 = high1 - low1

    sma20_1 = df.iloc[-2]['20sma']
    sma50_1 = df.iloc[-2]['50sma']
    sma100_1 = df.iloc[-2]['100sma']

    bblowerband1 = df.iloc[-2]['lower_band']
    # BBUpperBand1 = df.iloc[-2]['upper_band']

    # Candle 7
    sma50_7 = df.iloc[-8]['50sma']
    sma100_7 = df.iloc[-8]['100sma']

    # Trend
    c1 = (sma20 > sma50) and (sma50 > sma100)
    c2 = (sma50 > sma50_7) and (sma100 > sma100_7)

    # Current candle is a pinbar
    # The wick is at least 2 times the body of the candle.
    # The opening and closing are in 1/3 of the lower half of the candle
    c3 = 2 * abs(float(close) - float(open)) < Range
    c4 = (float(close) > float(low) + ((2 * Range) / 3)) and (float(open) > float(low) + ((2 * Range) / 3))
    # Bearish = > close < low + ((range / 3)) and open < low + ((range / 3))

    # Current Pinbar with BB & MMs
    c5 = (low < sma20) and (high > sma20)
    c6 = (low < sma50) and (high > sma50)
    c7 = (low < sma100) and (high > sma100)
    c8 = (low < bblowerband) and (high > bblowerband)
    c9 = (low > bblowerband) and (high < sma50)

    ccurrent = (c3 and c4) and (c5 or c6 or c7 or c8 or c9)

    # Previous candle is a pinbar
    c32 = 2 * abs(float(close1) - float(open1)) < Range1
    c42 = close1 > low1 + ((2 * Range1) / 3) and open1 > low1 + ((2 * Range1) / 3)
    # Bearish = > close < low + ((range / 3)) and open < low + ((range / 3))

    # Previous Pinbar with BB & MMs
    c52 = (low1 < sma20_1) and (high1 > sma20_1)
    c62 = (low1 < sma50_1) and (high1 > sma50_1)
    c72 = (low1 < sma100_1) and (high1 > sma100_1)
    c82 = (low1 < bblowerband1) and (high1 > bblowerband1)
    c92 = (low1 > bblowerband1) and (high1 < sma50_1)

    cprevious = (c32 and c42) and (c52 or c62 or c72 or c82 or c92)

    if c1 and c2 and (ccurrent or cprevious):
        return 1
    else:
        return 0
