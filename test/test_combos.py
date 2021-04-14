from populate_data import get_symbols, create_connection
import config
from scanner_rules import prepare_data, is_combo_ivt, is_combo, is_pinbar_on_trend
from charts import chart

pairs = {}
dataframes = {}

conn = create_connection(config.DB_FILE)

symbols = get_symbols(conn, 'USDT')

for symbol in symbols:
    df = prepare_data(conn, symbol, 'M5')
    if df.size > 100 and not df.empty:
        #print(df.dtypes)
        iscombo = is_combo(df)
        if iscombo == 1:
            combo = "ComboUp"
        elif iscombo == -1:
            combo = "ComboDown"
        else:
            combo = None

        iscomboivt = is_combo_ivt(df)
        if iscomboivt == 1:
            comboivt = "ComboIVTup"
        elif iscomboivt == -1:
            comboivt = "ComboIVTdown"
        else:
            comboivt = None

        ispb = is_pinbar_on_trend(df)
        if ispb:
            pbup = 'PinBarUp'
        else:
            pbup = None

        pairs[symbol + '_' + 'D1'] = {'IsCombo': combo, 'IsComboIVT': comboivt, 'isPinBarUp' : pbup}
        # save all dataframes to a dictionary we can chart individual names below by calling the chart() function
        dataframes[symbol + '_' + 'D1'] = df
        # print(df)

print(pairs)

for key, value in pairs.items():
    if value['IsCombo'] == "ComboUp" or value['IsCombo'] == "ComboDown" or value['IsComboIVT'] == "ComboIVTup" or value['IsComboIVT'] == "ComboIVTDown" or value['isPinBarUp'] == "PinBarUp":
        print(key, value)

df = dataframes['YFIDOWNUSDT_D1']
chart('YFIDOWNUSDT_D1', df)


