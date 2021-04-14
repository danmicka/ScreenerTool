import populate_data
import config

conn = populate_data.create_connection(config.DB_FILE)

# Populate the instrument
#populate_data.populate_instrument(conn)

#populate the instrument data
# symbols = populate_data.get_symbols(conn, 'ETH')
#
# for symbol in symbols:
#     populate_data.populate_instrument_data(conn, symbol, 'D1')

#populate_data.refresh_all_instrument_data(conn, 'ETH', 'D1')

# populate_data.populate_signals(conn, 'RCNBTC','H8')

# populate_data.populate_instrument(conn)

populate_data.refresh_all_instrument_data(conn, 'USDT', 'D3')

# populate_data.refresh_all_instrument_data(conn, 'USDT', 'H3')
#
# populate_data.refresh_all_instrument_data(conn, 'USDT', 'H4')
#

