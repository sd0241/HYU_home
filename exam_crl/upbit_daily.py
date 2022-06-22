import pyupbit
print(pyupbit.Upbit)

tickers = pyupbit.get_tickers()
#print(tickers)

df = pyupbit.get_ohlcv("KRW-BTC", count = 100)
print(df)
# df.to_csv('./upbit.day.csv', mode='a')
# df.to_csv('../flume/working/batch-log/upbit.day.csv', mode='a')