import sqlite3, config
from populate_data import create_connection
from flask import Flask, escape, request, render_template

app = Flask(__name__)


@app.route("/")
def index():
    #print(dir(request))
    conn = create_connection(config.DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "select  symbol, ut, is_combo, is_combo_ivt, is_pinbar  from signal inner join instrument on signal.imnt_id = instrument.imnt_id where is_combo <> 0 or is_combo_ivt <> 0 or is_pinbar <> 0")

    rows = cur.fetchall()

    return render_template('index.html', signals=rows)

    #return {"title": "dashboard", "Signals": rows}


