import pyupbit
import pandas as pd
import numpy as np
print(pyupbit.Upbit)

tickers = pyupbit.get_tickers()
df_hour = pyupbit.get_ohlcv("KRW-BTC", interval="minute1", count=3600)
df_list = str(df_hour["open"]).split(' ')
list_a = []
list_result = []
ds1 = 0;
for i in range(0, len(df_list)):
    if (i+1)%6 == 1:
        list_a.append(df_list[i])
    elif (i+1)%6 == 2 :
        list_a.append(df_list[i])
    elif (i+1)%6 == 0:
        ds = df_list[i].split('\n')
        print("ds0 = ",ds[0], i)
        #print(ds[1])
        # list_a.append(ds[i][0])
        # ds1 = ds[i][1]
    else : continue
    if i/6 < 1 :
        list_result.append(list_a)
        list_a = []
    else :
        list_result.append(ds1)
        list_result.append(list_a)
        list_a = []
#print(df_list)
#print(list_result)


# df_list.append(ds[0])
# for j in range(0, len(df_list)) :
#     print(df_list[j],"    ", j)


# df_hour.to_csv('./upbit.hour.csv', mode='a')
# df.to_csv('../flume/working/batch-log/upbit.hour.csv', mode='a')