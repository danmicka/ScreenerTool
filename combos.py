import os, pandas as pd
import plotly.graph_objects as go

desired_width = 500
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 10)

# symbols = ['ENJUSDT']

pairs = {}
dataframes = {}

for filename in os.listdir('./data/D1'):
    #print(filename)
    symbol = filename.split("_")[0]
    ut = filename.split("_")[1].split(".")[0]
    # print("symbol : " + symbol + " UT : " + ut)
    df = pd.read_csv('./data/D1/{}'.format(filename))
    df.sort_values(by='Open_time')
    # Indicators
    # Moving average
    df['20sma'] = df['Close'].rolling(window=20).mean()
    df['50sma'] = df['Close'].rolling(window=50).mean()
    df['100sma'] = df['Close'].rolling(window=100).mean()
    # Bollinger Bands
    df['stddev'] = df['Close'].rolling(window=20).std()
    df['lower_band'] = df['20sma'] - (2.5 * df['stddev'])
    df['upper_band'] = df['20sma'] + (2.5 * df['stddev'])
    df['band_width'] = df['upper_band'] - df['lower_band']
    # ATR
    df['TR'] = abs(df['High'] - df['Low'])
    df['ATR'] = df['TR'].rolling(window=20).mean()


    def slope(ha, hb, dist):
        if hb >= ha:
            p = 100*abs(ha - hb) / ha
        else:
            p = 100*abs(hb - ha) / hb
        return p

    def is_combo_up(df):
        # Price between MAs
        condition0 = (df.iloc[-1]['Close'] > df.iloc[-1]['50sma']) and (df.iloc[-1]['Close'] < df.iloc[-1]['20sma'])
        # Trend check
        condition1 = (df.iloc[-1]['20sma'] > df.iloc[-1]['50sma']) and (df.iloc[-1]['50sma'] > df.iloc[-1]['100sma'])
        # Slope
        #pente = slope(df.iloc[-7]['50sma'], df.iloc[-1]['50sma'], 7)
        #condition2 = pente > 20
        # Bollinger Bands
        condition3 = df.iloc[-1]['Close'] > df.iloc[-1]['lower_band']
        condition4 = (df.iloc[-6]['band_width'] > df.iloc[-5]['band_width']) and (
                df.iloc[-4]['band_width'] > df.iloc[-3]['band_width']) and (
                             df.iloc[-3]['band_width'] > df.iloc[-2]['band_width']) and (
                             df.iloc[-2]['band_width'] > df.iloc[-1]['band_width'])

        return condition0 and condition1 and condition3 and condition4

    iscombo = is_combo_up(df)

    pairs[symbol + '_' + ut] = {'IsCombo': iscombo, 'Slope': slope(df.iloc[-1]['50sma'], df.iloc[-7]['50sma'], 7)}

    # save all dataframes to a dictionary
    # we can chart individual names below by calling the chart() function
    dataframes[symbol + '_' + ut] = df


# print(dataframes)

def chart(df):
    candlestick = go.Candlestick(x=df['Open_time'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])
    upper_band = go.Scatter(x=df['Open_time'], y=df['upper_band'], name='Upper Bollinger Band', line={'color': 'red'})
    lower_band = go.Scatter(x=df['Open_time'], y=df['lower_band'], name='Lower Bollinger Band', line={'color': 'red'})

    sma_20 = go.Scatter(x=df['Open_time'], y=df['20sma'], name='sma 20',
                        line={'color': 'blue'})
    sma_50 = go.Scatter(x=df['Open_time'], y=df['50sma'], name='sma 50',
                        line={'color': 'green'})

    fig = go.Figure(data=[candlestick, upper_band, lower_band, sma_20, sma_50])
    fig.layout.xaxis.type = 'category'
    fig.layout.xaxis.rangeslider.visible = False
    fig.show()

    # if symbol in symbols:
    print(df)


print(pairs)

for key, value in pairs.items():
    if value['IsCombo']:
        print(key)

df = dataframes['DATAUSDT_D1']
chart(df)
