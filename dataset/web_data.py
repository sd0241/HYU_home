import pandas_read_xml as pdx
from sqlalchemy import create_engine
import pandas as pd
import datetime
#### =============================DB Connection=================================
connection_url = 'mysql+pymysql://root:sd0241@localhost/apart'
# MariaDB (MySQL) root계정에 비밀번호 root로 로그인하여 estate_db를 사용.
connection = create_engine(connection_url)
# DB에 쿼리를 보내기 위한 connection 생성
conn = connection.connect()
# connection에 대한 객체(conn) 를 생성

#### ===============================WEB API======================================
max_size = 3
# 사용하고자 하는 실시간 API Page는 총 1000 Page지만,
# 이전 데이터는 csv파일로 받아 처리를 했기 때문에 앞에 5Page만 실시간으로 가져올 계획.

column_list = ['BJDONG_NM', 'DEAL_YMD', 'BLDG_AREA', 'FLR_INFO',
               'BLDG_MUSE_NM', 'OBJ_AMT', 'BLDG_NM', 'BUILD_YEAR']
# API가 포함하고있는 Coloum명
column_name = ['법정동명', '거래날짜', '전용면적', '층정보',
               '건물주용도', '거래금액', '건물명', '건축년도']

####    전처리 후 변경할 컬럼명
result = []
data = []
default_date = 0
old_date = 0
new_date = 0
for page_index in range(1, max_size) :
    try :
        df = pdx.read_xml("http://openapi.seoul.go.kr:8088/634472564a68726c313232547272786f/xml/landActualPriceInfo/"+str(page_index) + '/' + str(max_size), ['landActualPriceInfo', 'row'])
        for i in range(0, df.size) :
            for j in column_list :
                data.append(df[i][0][j])        # RangeIndex
            result.append(data)
            data = []
    except KeyError :
        pass
print(result)
#
# ####    for문을 돌면서 각 페이지마다 Request를 요청하여 xml파일을 read함.
# ####    요청된 데이터는 df변수에 저장되며, df를 돌면서 Web page의 정보를 빈 list에 담아 row별로 저장.
df_result = pd.DataFrame(result, columns=column_name)
####    컬럼명을 미리 작성한 컬럼명으로 변경.
# df_result.to_sql(name='aprtzz', con=connection, if_exists='append', index= False)
####    쿼리를 통해 estate_db의 estate_price table로 df_result의 정보를 보냄.

df_mindistance = pd.read_csv('./minDistance.csv')

for i in range(0, len(df_result['건물주용도'])) :
    if df_result['건물주용도'][i] != '아파트' :
        df_result['건물주용도'][i] = None
#
# #### ================================신축구축=================================
df_result['건축년도'] = pd.to_numeric(df_result['건축년도'])
df_result['거래금액'] = pd.to_numeric(df_result['거래금액'])
df_result['전용면적'] = pd.to_numeric(df_result['전용면적'])

date = []
df_result = df_result.astype({'거래날짜' : 'str'})
for i in range(0, len(df_result['거래날짜'])) :
    date.append(df_result['거래날짜'][i][:4] + '-' + df_result['거래날짜'][i][4:6] + '-' + df_result['거래날짜'][i][6:8])
hms = ' 00:00:00'
df_result['거래날짜'] = date
df_result['거래날짜'] = df_result['거래날짜']+hms


min_dist = []
sub_name = []
check = list(df_mindistance['건물명'])
for i in range(0, len(df_result['법정동명'])) :
    for j in range(0, len(df_mindistance['법정동명'])) :
        if (df_result['법정동명'][i] == df_mindistance['법정동명'][j]) :
            if (df_result['건물명'][i] == df_mindistance['건물명'][j]):
                min_dist.append(df_mindistance['최소거리'][j])
                sub_name.append(df_mindistance['역명'][j])
                break
            elif df_result['건물명'][i] not in check :
                df_result['법정동명'][i] = None
                df_result['건물명'][i] = None
                break
        else : pass

df_result = df_result.dropna(subset = ['건물명'], axis = 0)
# # =============================================================================
df_result['최소거리'] = min_dist
df_result['역명'] = sub_name


nowDate = int(datetime.datetime.now().strftime('%Y'))
for i, row in df_result.iterrows() :
    if nowDate - (df_result.at[i, '건축년도']) > 10 :
        df_result.at[i, '신축구분'] = '구축'
    else : df_result.at[i,'신축구분'] = '신축'

df_result['거래금액'] = df_result['거래금액'] * 10000
df_result['평당금액'] = (df_result['거래금액']) / (df_result['전용면적']/3.3)

#### ================================위도경도==================================
df_road = pd.read_csv('./seoul_axis.csv', encoding='cp949')
df_apt = pd.read_csv('./total_apt.csv', encoding='utf-8-sig')



result_b = []
result_dong = []

df_result.to_csv('./web_total_apt_temp.csv', encoding='utf-8-sig', index=False)
df_result = pd.read_csv('./web_total_apt_temp.csv')

# print(df_result['건물명'],df_result['법정동명'])
for i in range(0, len(df_result['건물명'])) :
    result_b.append(df_result['건물명'][i])
    result_dong.append(df_result['법정동명'][i])

apt_b = []
apt_dong = []
lat = []
log = []
result_lat = []
result_log = []

for i in range(0, len(df_apt['건물명'])) :
    apt_b.append(df_apt['건물명'][i])
    apt_dong.append(df_apt['법정동명'][i])
    lat.append(df_apt['위도'][i])
    log.append(df_apt['경도'][i])

for i in range(0, len(result_b)) :
    for j in range(0, len(apt_b)) :
        if result_b[i] == apt_b[j] :
            if result_dong[i] == apt_dong[j] :
                result_lat.append(lat[j])
                result_log.append(log[j])
                break
            if j == len(apt_b)-1 :
                result_lat.append(None)
                result_log.append(None)

df_result['위도'] = result_lat
df_result['경도'] = result_log

for i, row in df_result.iterrows() :
    if df_result.at[i, '최소거리'] > 0.5 :
        df_result.at[i, '역세권여부'] = 0
    else : df_result.at[i,'역세권여부'] = 1



df_result = df_result.dropna(subset = ['건물주용도'], how = 'any', axis=0)
df_result.to_csv('/home/tdata/flume/working/batch-log/web_total_apt.csv', encoding='utf-8-sig', index=False)
