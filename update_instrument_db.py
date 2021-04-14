from populate_data import create_connection, populate_instrument
import config
from datetime import datetime

conn = create_connection(config.DB_FILE)

# Populate the instrument
populate_instrument(conn)

print('Last Instrument update : ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

