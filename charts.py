import plotly.graph_objects as go



def chart(key, df):
    candlestick = go.Candlestick(x=df['date'], open=df['open'], high=df['high'], low=df['low'], close=df['close'])
    upper_band = go.Scatter(x=df['date'], y=df['upper_band'], name='Upper Bollinger Band', line={'color': 'red'})
    lower_band = go.Scatter(x=df['date'], y=df['lower_band'], name='Lower Bollinger Band', line={'color': 'red'})

    sma_20 = go.Scatter(x=df['date'], y=df['20sma'], name='sma 20',
                        line={'color': 'blue'})
    sma_50 = go.Scatter(x=df['date'], y=df['50sma'], name='sma 50',
                        line={'color': 'green'})

    fig = go.Figure(data=[candlestick, upper_band, lower_band, sma_20, sma_50])
    fig.layout.xaxis.type = 'category'
    fig.layout.xaxis.rangeslider.visible = False
    symbol = key.split("_")[0]
    ut = key.split("_")[1].split(".")[0]
    fig.update_layout(
        title = symbol + ' ' + ut
    )
    fig.show()
