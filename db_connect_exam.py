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
connection_url = 'mysql+pymysql://root:root@localhost/estate_db'
# MariaDB (MySQL) root계정에 비밀번호 root로 로그인하여 estate_db를 사용.
connection = create_engine(connection_url)
# DB에 쿼리를 보내기 위한 connection 생성
conn = connection.connect()
# connection에 대한 객체(conn) 를 생성
#### ===================================CSV Merge====================================
input_file = r'./' 					# '' 안에 불러올 csv 파일 위치 확인 !!
# 읽고 싶은 파일의 경로 선택.
output_file = r'./apt_total.csv'				# 결합 후 내보낼 파일명 및 위치 확인 !!
# 출력 파일의 경로 및 파일명.확장자 선택.
allFile_list = glob.glob(os.path.join(input_file, '아파트*'))
# input_file 변수 경로에 있는 '아파트'로 시작하는 모든 파일을 호출하여 파일명을 list에 담음.
allData = []					# Dataframe에 적용할 빈 List 생성.
for file in allFile_list:
    df = pd.read_csv(file, encoding='cp949')		# 각 파일을 cp949 encoding방식으로 불러옴.
    allData.append(df) 				# 각 내용을 list에 추가.
df_apt = pd.concat(allData, axis=0, ignore_index=True) 	# concat함수를 통해 리스트 내용을 지속적으로 이어서 작성.
df_apt = df_apt.drop_duplicates()   		# 중복 데이터 제거.
df_apt = df_apt.sort_values('계약년월') 		# '집계일자' 컬럼 기준 데이터 정렬.

df_apt.to_csv(output_file,encoding='utf-8-sig', index=False)    # 완성된 데이터는 utf-8-sig형식으로 인코딩 된 CSV 파일로 반환.

# ==================================READ EXCEL========================================
df_apt = pd.read_csv('./apt_total.csv', encoding='utf-8-sig')
# #위 코드 경로는 자신의 경로에 맞출것!
date = ''
nowDate = int(datetime.datetime.now().strftime('%Y'))   # 현재 날짜의 년도 호출
date_list = []
m2_price = []
df_apt['계약년월'] = df_apt['계약년월']*100+df_apt['계약일']   # 계약년월 컬럼과 계약일 컬럼을 하나의 날짜로 통합
df_apt = df_apt.drop(['계약일'], axis=1)   # 분석에 필요없는 컬럼 제거
df_apt = df_apt.drop(['본번'], axis=1)    # 분석에 필요없는 컬럼 제거
df_apt = df_apt.drop(['부번'], axis=1)    # 분석에 필요없는 컬럼 제거
df_apt = df_apt.drop(['해제사유발생일'], axis=1)   # 분석에 필요없는 컬럼 제거
df_apt.rename(columns = {'계약년월' : '거래날짜'}, inplace = True)  # 컬럼명 변경
df_apt.rename(columns = {'거래금액(만원)' : '거래금액'}, inplace = True) # 컬럼명 변경
dong = []
city = []
for i in df_apt['시군구'] :                # '시군구'컬럼에는 시/구/동의 정보가 담겨있음.
    temp = i.split(' ')                   # 해당 컬럼에서 '시/군'과 '동' 데이터를 따로 취득해야 하기 때문에
    city.append(temp[0] + ' ' + temp[1])  # for 구문을 이용하여 이를 나눠줌.
    dong.append(temp[2])
df_apt['시군구'] = city                    # 나눠진 '시/구' 데이터는 '시군구' 컬럼에 적용.
df_apt['법정동명'] = dong                  # 나머지 '동' 데이터는 '법정동명'에 적용.
df_apt = df_apt[['시군구', '법정동명', '번지', '단지명', '전용면적(㎡)', '거래날짜', '거래금액', '층', '건축년도', '도로명' ]]
# 컬럼명 순서로 데이터 재정렬
df_apt = df_apt.rename(columns = {'전용면적(㎡)' : '전용면적'})  # 컬럼명 변경
df_apt = df_apt.rename(columns = {'층' : '층정보'})             # 컬럼명 변경
df_apt = df_apt.rename(columns = {'단지명' : '건물명'})           # 컬럼명 변경

date = []
df_apt = df_apt.astype({'거래날짜' : 'str'})        # 데이터 타입을 string 형태로 형변환.
for i in range(0, len(df_apt['거래날짜'])) :        # 거래 날짜의 년도/월/일 순으로 나누고, 날짜 형싱 yyyy-mm-dd 형태로 저장.
    date.append(df_apt['거래날짜'][i][:4] + '-' + df_apt['거래날짜'][i][4:6] + '-' + df_apt['거래날짜'][i][6:8])
hms = ' 00:00:00'                   #데이터 베이스 및 logstash의 timestamp에 맞추어 시/분/초 데이터를 추가해주기 위한 hms변수 선언
df_apt['거래날짜'] = date             # 나눠진 데이터 데이터를 '거래날짜' 컬럼에 저장.
df_apt['거래날짜'] = df_apt['거래날짜']+hms # 기존 데이터에 시/분/초 문자열을 더함.

for i, row in df_apt.iterrows() :                   # df_apt의 영역을 탐색함.
    if nowDate - (df_apt.at[i, '건축년도']) > 10 :    # 올해의 년도에서 '건축년도' 컬럼을 뺀 값이 10년 이상이면
        df_apt.at[i, '신축구분'] = '구축'             # 해당 건물은 '구축'으로 판단.
    else : df_apt.at[i,'신축구분'] = '신축'           #그렇지 않으면 '신축'으로 판단.

# df_apt = df_apt.replace(' ', None)
# df_apt = df_apt.dropna(subset = ['도로명'], how = 'any', axis=0)
# df_apt_result = df_apt.dropna(subset = ['도로명'], axis = 0)
# df_apt["거래금액"] = df_apt["거래금액"].str.replace(pat=r'[^\w]', repl=r'', regex=True)
# df_apt['거래금액'] = pd.to_numeric(df_apt['거래금액'])

df_apt['거래금액'] = df_apt['거래금액'] * 10000
df_apt['평당금액'] = (df_apt['거래금액']) / (df_apt['전용면적']/3.3)
#df_apt.to_csv('C:/Users/Admin/Desktop/total_apt.csv', encoding='utf-8-sig', index=False)

####===================================위도/경도============================================
df_road = pd.read_csv('C:/Users/Admin/Desktop/PBL수업내용/__MINI/__Estimate자료/mini_dataset/seoul_axis.csv', encoding='cp949')
df_mindistance = pd.read_csv('C:/Users/Admin/Desktop/minDistance.csv')
new_road = []
for i in range(0, len(df_apt['도로명'])):
    rn = df_apt['도로명'][i].split(' ')[0]
    new_road.append(rn) # '도로명'컬럼을 split하여 0번째 index에 해당하는 값만 Append시킴.

df_apt['수정된 도로명'] = new_road    #위에서 작성한 new_road 리스트를 '수정된 도로명' 컬럼에 대입.
roadInfo = list(df_road['도로명'])   # '도로명'에 대한 데이터를 list로 형변환)
lat = list(df_road['위도'])   # '위도'에 대한 데이터를 list로 형변환)
lon = list(df_road['경도'])   # '경도'에 대한 데이터를 list로 형변환)

latitude_list = []      # 위도 데이터를 저장할 list 생성
longitude_list = []     # 경도 데이터를 저장할 list 생성
for i in range(0, len(df_apt['수정된 도로명'])):  # 수정된 도로명 데이터 탐색
    nr = new_road[i]    # 해당 index에 해당하는 주소를 nr에 대입.
    try:
        indexN = roadInfo.index(nr)             #   nr과 일치하는 값이 있는 index 추출
        latitude_list.append(lat[indexN])       #   위도(lat) 데이터에서 위에서 구한 index에 있는 위도 데이터를 latitude list에 저장.
        longitude_list.append(lon[indexN])      #   경도(lon) 데이터에서 위에서 구한 index에 있는 위도 데이터를 longitude list에 저장.
    except ValueError as e:                     #   만약 위도나 경도 데이터가 탐색결과가 없다면 None처리.
        latitude_list.append(None)
        longitude_list.append(None)


df_apt['최소거리'] = df_mindistance['최소거리']     # 최소거리 컬럼 생성
df_apt['역명'] = df_mindistance['역명']           # 역명 컬럼 생성
df_apt['위도'] = latitude_list                    # 위도 컬럼 생성
df_apt['경도'] = longitude_list                   # 경도 컬럼 생성
df_apt = df_apt.drop(['수정된 도로명'], axis=1)     # 탐색에 사용했던 '수정된 도로' 컬럼 생성
df_apt = df_apt.dropna(subset = ['위도'], how = 'any', axis=0) # 위도가 None인 Row를 제거.

for i, row in df_apt.iterrows() :               # Dataframe의 모든 아이템을 탐색하면서
    if df_apt.at[i, '최소거리'] > 0.5 :          # 최소거리가 500m 이상인 경우
        df_apt.at[i, '역세권여부'] = 0            #역세권이 아님을 0으로 표현.
    else : df_apt.at[i,'역세권여부'] = 1         #역세권일 경우, 1로 표현.

df_apt.to_csv('C:/Users/Admin/Desktop/total_apt.csv', encoding='utf-8-sig', index=False)
# # =====================================================================================
#
