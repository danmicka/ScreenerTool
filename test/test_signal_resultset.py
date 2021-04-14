import sqlite3, config
from populate_data import create_connection
import pandas as pd

conn = create_connection(config.DB_FILE)
cur = conn.cursor()
sql = "select  symbol, ut, is_combo, is_combo_ivt, is_pinbar  from signal inner join instrument on signal.imnt_id = instrument.imnt_id where is_combo <> 0 or is_combo_ivt <> 0 or is_pinbar <> 0 ORDER BY symbol"

df = pd.read_sql(sql, conn)

print(df)


def f(row):
    if row["is_combo"] == -1:
        combo = "(-C)"
    elif row["is_combo"] == 1:
        combo = "(+C)"
    else:
        combo = ""

    if row["is_combo_ivt"] == -1:
        combov = "(-C*)"
    elif row["is_combo_ivt"] == 1:
        combov = "(+C*)"
    else:
        combov = ""

    if row["is_pinbar"] == -1:
        pinbar = "(-PB)"
    elif row["is_pinbar"] == 1:
        pinbar = "(+PB)"
    else:
        pinbar = ""

    val = combo + combov + pinbar

    return val


df["signal"] = df.apply(f, axis=1)

# pivot = df.pivot("symbol", columns="ut")
#
print(df)

new = df[['symbol', 'ut', 'signal']]

print(new)

pivot = new.pivot(index="symbol", columns="ut", values='signal').reset_index()
pivot.columns.name = None

print(pivot)

#print(pivot.columns())

# pivot_json = pivot.to_json(orient='records', date_format='iso')
#
# print(pivot_json)

data_top = list(pivot.columns)

print(data_top)
