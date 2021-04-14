from populate_data import create_connection, refresh_all_instrument_data
import config, sys
from datetime import datetime

if len(sys.argv) == 1:
    sys.exit("Argument Missing")

pair = sys.argv[1]
ut = sys.argv[2]

conn = create_connection(config.DB_FILE)

print('########################################## ' + datetime.now().strftime(
    '%Y-%m-%d %H:%M:%S') + ' Instruments data update : ' + ' Pair : ' + pair + 'UT: ' + ut + '#####################################################')

# Populate the instrument
refresh_all_instrument_data(conn, pair, ut)
