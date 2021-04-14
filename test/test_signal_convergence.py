import sqlite3, config
from populate_data import create_connection
import pandas as pd

from scanner_rules import get_convergence

conn = create_connection(config.DB_FILE)
cur = conn.cursor()


# Function
def f(row):
    rating = 0
    if row["is_combo"] == -1:
        combo = "-C"
        rating -= 1
    elif row["is_combo"] == 1:
        combo = "+C"
        rating += 1
    else:
        combo = ""

    if row["is_combo_ivt"] == -1:
        combov = "-C*"
        rating -= 1
    elif row["is_combo_ivt"] == 1:
        combov = "+C*"
        rating += 1
    else:
        combov = ""

    if row["is_pinbar"] == -1:
        pinbar = "-PB"
        rating -= 1
    elif row["is_pinbar"] == 1:
        pinbar = "+PB"
        rating += 1
    else:
        pinbar = ""

    if row["candle_side"] == 1:
        side = "Up"
    else:
        side = "Down"

    val = '[' + str(rating) + ']' + '[' + combo + ']' + '[' + combov + ']' + '[' + pinbar + ']' + '[' + side + ']'

    return val


# Get the list signals for each token having at least one
sql = "select  distinct symbol, ut, is_combo, is_combo_ivt, is_pinbar  from signal inner join instrument on " \
      "signal.imnt_id = instrument.imnt_id where (is_combo <> 0 or is_combo_ivt <> 0 or is_pinbar <> 0) and ut in (" \
      "'M15','M30','H1','H2','H3','H4','H6','H8','H12','D1','D3') ORDER BY symbol "
# and ut in ('M15','M30','H1','H2','H3','H4','H6','H8','H12','D1','D3') ORDER BY symbol "

df = pd.read_sql(sql, conn)

df["signal"] = df.apply(f, axis=1)
# add the columns for the pivot function
new = df[['symbol', 'ut', 'signal']]
# pivot the table

new.drop_duplicates(subset=['symbol', 'ut'], keep='last')

signals = new.pivot(index="symbol", columns="ut", values='signal').reset_index()

# signals = pd.pivot_table(new,index=["symbol"], columns="ut", values='signal')

#signals.reset_index()

# clean / remove the first level of column name for later processing
signals.columns.name = None

print(signals)

# # Get the last candle side for each token having at least one signal
# sql = "select  distinct symbol from signal inner join instrument on signal.imnt_id = instrument.imnt_id where " \
#       "is_combo <> 0 or is_combo_ivt <> 0 or is_pinbar <> 0 ORDER BY symbol "
# cur.execute(sql)
# rows = cur.fetchall()

# rows_list = []
#
# for symbol in rows:
#     res = get_convergence(conn, symbol[0])
#     for elem in res:
#         rows_list.append(elem)

# result = pd.DataFrame(rows_list, columns=['symbol', 'ut', 'side'])
#
# result['side'] = result['side'].astype(int)
#
# convergence = result.pivot(index="symbol", columns="ut", values='side').reset_index()



# signals.columns.name = None
#
# print(signals.columns)
#
# convergence.rename(columns=lambda x: "SIDE_" + x if x != "symbol" else x, inplace=True)
#
# print(convergence)
#
# final = pd.merge(signals, convergence, on="symbol")
#
# print(final)
