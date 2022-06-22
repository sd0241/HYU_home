import plotly
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
import plotly.express as px
import lxml

stock_code = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
stock_code.head()

stock_code.sort_values(['상장일'], ascending=True)
stock_code = stock_code[['회사명', '종목코드']]
stock_code = stock_code.rename(columns={'회사명': 'company', '종목코드': 'code'})
stock_code.code = stock_code.code.map('{:06d}'.format)


#
# # LG화학의 일별 시세 url 가져오기
company='삼성전자'
code = stock_code[stock_code.company==company].code.values[0].strip() ## strip() : 공백제거
# page = 1
#
# url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
# url = '{url}&page={page}'.format(url=url, page=page)
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
# res = requests.get(url,headers=header)
# df = pd.read_html(res.text, header=0)[0]
# df.head()
# # print(df.keys())
# code = stock_code[stock_code.company==company].code.values[0].strip()

df = pd.DataFrame()

for page in range(1,101):
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    url = '{url}&page={page}'.format(url=url, page=page)
    res = requests.get(url, headers=header)
    df = df.append(pd.read_html(res.text, header=0)[0])
    df.head()
    #df = df.append(pd.read_html(url, header = 0)[0], ignore_index=True)
#
    # df.dropna()를 이용해 결측값 있는 행 제거
    df = df.dropna()
#     # 한글로 된 컬럼명을 영어로 바꿔줌
    df1 = df.rename(
        columns={'날짜': 'date', '종가': 'close', '전일비': 'diff', '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})

    # 데이터의 타입을 int형으로 바꿔줌
    df1[['close', 'diff', 'open', 'high', 'low', 'volume']] = df1[
        ['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)
#
#     # 컬럼명 'date'의 타입을 date로 바꿔줌
    df1['date'] = pd.to_datetime(df1['date'])

    # 일자(date)를 기준으로 오름차순 정렬
    df1 = df1.sort_values(by=['date'], ascending=True)

    # 상위 5개 데이터 확인
    df1.head()

plt.figure(figsize=(10,4))
plt.plot(df1['date'], df1['close'])
plt.xlabel('')
plt.ylabel('close')
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off
plt.savefig(company + ".png")
#plt.show()

fig = px.line(df1, x='date', y='close', title='{}의 종가(close) Time Series'.format(company))

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=3, label="3m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(step="all")
        ])
    )
)
fig.show()
df1.to_csv('C:/Users/Admin/samsung.csv',  mode='a')
fig.write_html("file.html")