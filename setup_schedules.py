from crontab import CronTab

cron = CronTab(user=True)

for job in cron:
    cron.remove(job)

# Populate Instruments list
taskInst = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3  /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_db.py >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument.log 2>&1')
taskInst.hours.during(9,23).every(4)

# Populate Instrument Data
# UT D3
# task1 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  ETH D3 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_ETH_D3.log 2>&1')
# task1.minute.every(30)

taskD3_2 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BTC D3 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BTC_D3.log 2>&1')
taskD3_2.minute.every(5)
taskD3_2.hour.during(9,23).every(2)

taskD3_3 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  USDT D3 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_USDT_D3.log 2>&1')
taskD3_3.minute.every(5)
taskD3_3.hour.during(9,23).every(2)

# task4 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BNB D3 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BNB_D3.log 2>&1')
# task4.minute.every(5)
#
# # UT  D1
# taskD1_1 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  ETH D1 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_ETH_D1.log 2>&1')
# taskD1_1.minute.every(5)
# taskD1_1.minute.during(0,59).every(15)
# taskD1_1.hour.during(9,23)
#
taskD1_2 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BTC D1 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BTC_D1.log 2>&1')
taskD1_2.hour.during(9,23).every(2)
#
taskD1_3 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  USDT D1 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_USDT_D1.log 2>&1')
taskD1_3.hour.during(9,23).every(2)
#
# task4 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BNB D1 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BNB_D1.log 2>&1')
# task4.minute.every(5)
#
# # UT  H12
# task1 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  ETH H12 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_ETH_H12.log 2>&1')
#
taskH12_2 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BTC H12 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BTC_H12.log 2>&1')
taskH12_2.hour.during(9,23).every(2)
#
taskH12_3 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  USDT H12 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_USDT_H12.log 2>&1')
taskH12_3.hour.during(9,23).every(2)
#
# task4 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BNB H12 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BNB_H12.log 2>&1')
# task4.minute.every(5)
#
# # UT  H8
# task1 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  ETH H8 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_ETH_H8.log 2>&1')
# task1.minute.every(5)
#
taskH8_2 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BTC H8 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BTC_H8.log 2>&1')
taskH8_2.hour.during(9,23).every(2)
#
taskH8_3 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  USDT H8 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_USDT_H8.log 2>&1')
taskH8_3.hour.during(9,23).every(2)
#
# task4 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BNB H8 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BNB_H8.log 2>&1')
# task4.minute.every(5)
#
# # UT  H6
# task1 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  ETH H6 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_ETH_H6.log 2>&1')
# task1.minute.every(5)
#
taskH6_2 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BTC H6 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BTC_H6.log 2>&1')
taskH6_2.hour.during(9,23).every(1)
#
taskH6_3 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  USDT H6 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_USDT_H6.log 2>&1')
taskH6_3.hour.during(9,23).every(1)
#
# task4 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BNB H6 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BNB_H6.log 2>&1')
# task4.minute.every(5)
#
# # UT  H4
# task1 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  ETH H4 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_ETH_H4.log 2>&1')
# task1.minute.every(5)
#
taskH4_2 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BTC H4 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BTC_H4.log 2>&1')
taskH4_2.minute.during(0,59).every(30)
taskH4_2.hour.during(9,23)
#
taskH4_3 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  USDT H4 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_USDT_H4.log 2>&1')
taskH4_3.minute.during(1,59).every(30)
taskH4_3.hour.during(9,23)
#
# task4 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BNB H4 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BNB_H4.log 2>&1')
# task4.minute.every(5)
#
# # UT  H2
# task1 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  ETH H2 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_ETH_H2.log 2>&1')
# task1.minute.every(5)
#
taskH2_2 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BTC H2 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BTC_H2.log 2>&1')
taskH2_2.minute.during(0,59).every(15)
taskH2_2.hour.during(9,23)
#
taskH2_3 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  USDT H2 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_USDT_H2.log 2>&1')
taskH2_3.minute.during(1,59).every(15)
taskH2_3.hour.during(9,23)
#
# task4 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BNB H2 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BNB_H2.log 2>&1')
# task4.minute.every(5)
#
# # UT  H1
# task1 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  ETH H1 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_ETH_H1.log 2>&1')
# task1.minute.every(5)
#
taskH1_2 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BTC H1 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BTC_H1.log 2>&1')
taskH1_2.minute.during(0,59).every(10)
taskH1_2.hour.during(9,23)
#
taskH1_3 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  USDT H1 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_USDT_H1.log 2>&1')
taskH1_3.minute.during(1,59).every(10)
taskH1_3.hour.during(9,23)
#
# task4 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BNB H1 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BNB_H1.log 2>&1')
# task4.minute.every(5)
#
# # UT  M30
# task1 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  ETH M30 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_ETH_M30.log 2>&1')
# task1.minute.every(5)
#
taskM30_2 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BTC M30 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BTC_M30.log 2>&1')
taskM30_2.minute.during(0,59).every(5)
taskM30_2.hour.during(9,23)
#
taskM30_3 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  USDT M30 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_USDT_M30.log 2>&1')
taskM30_3.minute.during(1,59).every(5)
taskM30_3.hour.during(9,23)
#
# task4 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BNB M30 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BNB_M30.log 2>&1')
# task4.minute.every(5)
#
# # UT  M15
# task1 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  ETH M15 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_ETH_M15.log 2>&1')
# task1.minute.every(5)
#
taskM15_2 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BTC M15 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BTC_M15.log 2>&1')
taskM15_2.minute.during(0,59).every(5)
taskM15_2.hour.during(9,23)
#
taskM15_3 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  USDT M15 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_USDT_M15.log 2>&1')
taskM15_3.minute.during(1,59).every(5)
taskM15_3.hour.during(9,23)
#
# task4 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BNB M15 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BNB_M15.log 2>&1')
# task4.minute.every(5)
#
# # UT  M5
# taskM5_1 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  ETH M5 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_ETH_M5.log 2>&1')
# taskM5_1.minute.during(0,59).every(5)
# taskM5_1.hour.during(9,23)

# taskM5_2 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BTC M5 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BTC_M5.log 2>&1')
# taskM5_2.minute.during(0,59).every(5)
# taskM5_2.hour.during(9,23)
# #
# taskM5_3 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  USDT M5 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_USDT_M5.log 2>&1')
# taskM5_3.minute.during(0,59).every(5)
# taskM5_3.hour.during(9,23)

# taskM5_4 = cron.new(command='/Users/mickaeldancin/Documents/Python_project/ScreenerTools/venv/bin/python3 /Users/mickaeldancin/Documents/Python_project/ScreenerTools/update_instrument_data_db.py  BNB M5 >> /Users/mickaeldancin/Documents/Python_project/ScreenerTools/logs/populate_instrument_data_BNB_M5.log 2>&1')
# taskM5_4.minute.during(0,59).every(5)
# taskM5_4.hour.during(9,23)

cron.write()






