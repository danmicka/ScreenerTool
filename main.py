import json
import sqlite3, config
import pandas as pd

from populate_data import create_connection
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory="templates")

conn = create_connection(config.DB_FILE)
conn.row_factory = sqlite3.Row

def f(row):
    rating = 0
    if row["is_combo"] == -1:
        combo = "[-C]"
        rating += 1
    elif row["is_combo"] == 1:
        combo = "[+C]"
        rating += 1
    else:
        combo = ""

    if row["is_combo_ivt"] == -1:
        combov = "[-C*]"
        rating += 1
    elif row["is_combo_ivt"] == 1:
        combov = "[+C*]"
        rating += 1
    else:
        combov = ""

    if row["is_pinbar"] == -1:
        pinbar = "[-PB]"
        rating += 3
    elif row["is_pinbar"] == 1:
        pinbar = "[+PB]"
        rating += 3
    else:
        pinbar = ""

    if row["candle_side"] == 1:
        side = "[Up]"
    else:
        side = "[Down]"

    if rating != 0:
        val = str(rating) + combo + combov + pinbar + side
    else:
        val = combo + combov + pinbar + side

    return val

# def get_data(conn):
#     sql = "select  symbol, ut, is_combo, is_combo_ivt, is_pinbar  from signal inner join instrument on signal.imnt_id = instrument.imnt_id where is_combo <> 0 or is_combo_ivt <> 0 or is_pinbar <> 0 ORDER BY symbol"
#
#     df = pd.read_sql(sql, conn)
#
#     df["signal"] = df.apply(f, axis=1)
#
#     new = df[['symbol', 'ut', 'signal']]
#
#     pivot = new.pivot("symbol", columns="ut")
#
#     return(pivot)

@app.get("/")
def index(request: Request):
    #print(dir(request))
    # conn = create_connection(config.DB_FILE)
    # conn.row_factory = sqlite3.Row
    # cur = conn.cursor()
    # cur.execute(
    #     "select  symbol, ut, is_combo, is_combo_ivt, is_pinbar  from signal inner join instrument on signal.imnt_id = instrument.imnt_id where is_combo <> 0 or is_combo_ivt <> 0 or is_pinbar <> 0 ORDER BY symbol")
    #
    # rows = cur.fetchall()
    sql = "select  distinct symbol, ut, is_combo, is_combo_ivt, is_pinbar, candle_side  from signal inner join instrument on signal.imnt_id " \
          "= instrument.imnt_id where symbol in (select distinct symbol from signal inner join instrument on signal.imnt_id " \
          "= instrument.imnt_id and (is_combo <> 0 or is_combo_ivt <> 0 or is_pinbar <> 0)) and ut in ('M15','M30','H1','H2','H3','H4','H6','H8','H12','D1','D3') ORDER BY symbol "
    # ,'D1','D3'
    df = pd.read_sql(sql, conn)

    df["signal"] = df.apply(f, axis=1)
    # add the columns for the pivot function
    new = df[['symbol', 'ut', 'signal']]
    # remove duplicates if any and take the last record
    new.drop_duplicates(subset=['symbol', 'ut'], keep='last')
    # pivot the table
    pivot = new.pivot(index="symbol", columns="ut", values='signal').reset_index()
    # clean / remove the columns for later processing
    pivot.columns.name = None

    print(pivot)

    data_top = list(pivot.columns)

    print(data_top)

    pivot_json = pivot.to_json(orient='records', date_format='iso')

    json_dictionary = json.loads(pivot_json)

    # for signal in pivot_json:
    #     print(signal['symbol'][0])

    #pivot_dict = pivot.to_dict()

    print(json_dictionary)

    #rows = get_data(conn)
    content = {
        "columns": data_top,
        "rows":json_dictionary
    }
    return JSONResponse(content=content)
    # return templates.TemplateResponse("index.html", {"request": request, "signals": json_dictionary, "fields": data_top})

    #return {"title": "dashboard", "Signals": rows}



