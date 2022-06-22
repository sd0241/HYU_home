import math
from time import sleep
import pandas_read_xml as pdx
from geopy import Nominatim
from sqlalchemy import create_engine
import pandas as pd
import glob
import os
import datetime
import googlemaps

#### ==================================DB Connection=================================
# connection_url = 'mysql+pymysql://root:root@localhost/estate_db'
# # MariaDB (MySQL) root계정에 비밀번호 root로 로그인하여 estate_db를 사용.
# connection = create_engine(connection_url)
# # DB에 쿼리를 보내기 위한 connection 생성
# conn = connection.connect()
# # connection에 대한 객체(conn) 를 생성
#### ===================================CSV Merge====================================
input_file = r'./' 					# '' 안에 불러올 csv 파일 위치 확인 !!
# 읽고 싶은 파일의 경로 선택.
output_file = r'./apt_total.csv'				# 결합 후 내보낼 파일명 및 위치 확인 !!
# 출력 파일의 경로 및 파일명.확장자 선택.
allFile_list = glob.glob(os.path.join(input_file, '아파트*'))	# 불러올 공통 파일명 잘 보기
# input_file 경로 내의 불러올 파일 선택
print(allFile_list)

#전체 칼럼 가져오기
allData = []					# 잠시 csv 저장할 리스트 작성
for file in allFile_list:
    df = pd.read_csv(file, encoding='cp949')		# for구문으로 csv파일들을 읽어 들인다 ( cp949 == euc-kr과 같은 encoding )
    allData.append(df) 				# 빈 리스트에 읽어 들인 내용을 추가한다
df_apt = pd.concat(allData, axis=0, ignore_index=True) 	# concat함수를 이용해서 리스트의 내용을 병합
df_apt = df_apt.drop_duplicates()   		# 중복행 제거
df_apt = df_apt.sort_values('계약년월') 		# '집계일자'칼럼 기준 데이터 정렬

df_apt.to_csv(output_file,encoding='utf-8-sig', index=False)	# 완성된 csv 파일 내보내기 utf-8
# print('merge complete')
# ==================================READ EXCEL========================================
# df_apt = pd.read_csv('C:/Users/Admin/Desktop/total_apt.csv', encoding='utf-8-sig')
df_apt = pd.read_csv('./apt_total.csv', encoding='utf-8-sig')
# #위 코드 경로는 자신의 경로에 맞출것!
date = ''
nowDate = int(datetime.datetime.now().strftime('%Y'))
date_list = []
m2_price = []
df_apt['계약년월'] = df_apt['계약년월']*100+df_apt['계약일']
df_apt = df_apt.drop(['계약일'], axis=1)
df_apt = df_apt.drop(['본번'], axis=1)
df_apt = df_apt.drop(['부번'], axis=1)
df_apt = df_apt.drop(['해제사유발생일'], axis=1)
df_apt.rename(columns = {'계약년월' : '거래날짜'}, inplace = True)
df_apt.rename(columns = {'거래금액(만원)' : '거래금액'}, inplace = True)
dong = []
city = []
for i in df_apt['시군구'] :
    temp = i.split(' ')
    city.append(temp[0] + ' ' + temp[1])
    dong.append(temp[2])
df_apt['시군구'] = city
df_apt['법정동명'] = dong
df_apt = df_apt[['시군구', '법정동명', '번지', '단지명', '전용면적(㎡)', '거래날짜', '거래금액', '층', '건축년도', '도로명' ]]
df_apt = df_apt.rename(columns = {'전용면적(㎡)' : '전용면적'})
df_apt = df_apt.rename(columns = {'층' : '층정보'})
df_apt = df_apt.rename(columns = {'단지명' : '건물명'})
date = []
df_apt = df_apt.astype({'거래날짜' : 'str'})
for i in range(0, len(df_apt['거래날짜'])) :
    date.append(df_apt['거래날짜'][i][:4] + '-' + df_apt['거래날짜'][i][4:6] + '-' + df_apt['거래날짜'][i][6:8])
hms = ' 00:00:00'
df_apt['거래날짜'] = date
df_apt['거래날짜'] = df_apt['거래날짜']+hms
for i, row in df_apt.iterrows() :
    if nowDate - (df_apt.at[i, '건축년도']) > 10 :
        df_apt.at[i, '신축구분'] = '구축'
    else : df_apt.at[i,'신축구분'] = '신축'

# df_apt = df_apt.replace(' ', None)
# df_apt = df_apt.dropna(subset = ['도로명'], how = 'any', axis=0)
# df_apt_result = df_apt.dropna(subset = ['도로명'], axis = 0)
# df_apt["거래금액"] = df_apt["거래금액"].str.replace(pat=r'[^\w]', repl=r'', regex=True)
# df_apt['거래금액'] = pd.to_numeric(df_apt['거래금액'])

df_apt['거래금액'] = df_apt['거래금액'] * 10000
df_apt['평당금액'] = (df_apt['거래금액']) / (df_apt['전용면적']/3.3)
#df_apt.to_csv('C:/Users/Admin/Desktop/total_apt.csv', encoding='utf-8-sig', index=False)

####===================================위도/경도============================================
#
# sleep(10)
# df_apt = pd.read_csv('C:/Users/Admin/Desktop/total_apt.csv', encoding='utf-8-sig')
df_road = pd.read_csv('C:/Users/Admin/Desktop/PBL수업내용/__MINI/__Estimate자료/mini_dataset/seoul_axis.csv', encoding='cp949')
df_mindistance = pd.read_csv('C:/Users/Admin/Desktop/minDistance.csv')
new_road = []
for i in range(0, len(df_apt['도로명'])):
    rn = df_apt['도로명'][i].split(' ')[0]
    new_road.append(rn)

df_apt['수정된 도로명'] = new_road
roadInfo = list(df_road['도로명'])
lat = list(df_road['위도'])
lon = list(df_road['경도'])

latitude_list = []
longitude_list = []
for i in range(0, len(df_apt['수정된 도로명'])):
    nr = new_road[i]
    try:
        indexN = roadInfo.index(nr)
        latitude_list.append(lat[indexN])
        longitude_list.append(lon[indexN])
    except ValueError as e:
        latitude_list.append(None)
        longitude_list.append(None)


df_apt['최소거리'] = df_mindistance['최소거리']
df_apt['역명'] = df_mindistance['역명']
df_apt['위도'] = latitude_list
df_apt['경도'] = longitude_list
df_apt = df_apt.drop(['수정된 도로명'], axis=1)
df_apt = df_apt.dropna(subset = ['위도'], how = 'any', axis=0)

for i, row in df_apt.iterrows() :
    if df_apt.at[i, '최소거리'] > 0.5 :
        df_apt.at[i, '역세권여부'] = 0
    else : df_apt.at[i,'역세권여부'] = 1



df_apt.to_csv('C:/Users/Admin/Desktop/total_apt.csv', encoding='utf-8-sig', index=False)
# # =====================================================================================
#
