import pyupbit
import pandas as pd
import numpy as np
tickers = pyupbit.get_tickers()
#print(tickers)
df = pyupbit.get_ohlcv("KRW-BTC", interval="minute1", count=10)

# df_list = str(df["open"]).split(' ')
# ds = df_list[5].split('\n')
# df_list.append(ds[0])
# for i in range(0, len(df_list)) :
#     print(df_list[i],"    ", i)
# a = df_list[0] + "\t" + df_list[1] + "\t" + df_list[9]
# apd = []
# apd.append(df_list[0])
# apd.append(df_list[1])
# apd.append(df_list[9])


# df_str = str(df.index)
# df1 = df.transpose()
# df2 = df1.rename(columns=df1.iloc[0])
# df3 = df2.drop(df2.index[0])
# df4 = df3.transpose()
# print(df4)
# print('*'*50)
# a = df.keys()
# df.transpose()
# print(df.info())


#
# print(df_str[16:26])
# print(df_str[27:35])
# Index(['open', 'high', 'low', 'close', 'volume', 'value'], dtype='object')
df.to_csv('C:/Users/Admin/Desktop/minute.csv', mode='a', index=False, header = False)

#df.to_csv('../flume/working/batch-log/upbit.minute.csv', mode='a', index = False)

