import pandas as pd
import pandas_read_xml as pdx

df = pdx.read_xml("http://openapi.seoul.go.kr:8088/634472564a68726c313232547272786f/xml/landActualPriceInfo/1/5/", ['landActualPriceInfo', 'row'])
column_list = ['RTMS_ID', 'LAND_CD', 'SGG_CD','BJDONG10_CD','BJDONG_NM', 'ACC_YEAR', 'JOB_GBN', 'JOB_GBN_NM', 'DEAL_YMD', 'OBJ_SEQNO', 'TOT_AREA', 'BLDG_AREA', 'RIGHT_GBN', 'FLR_INFO', 'BLDG_MUSE_CD', 'BLDG_MUSE_NM', 'OBJ_AMT', 'BLDG_NM', 'BUILD_YEAR']

data = []
result = []
for i in range(0, df.size) :
    for j in column_list :
        data.append(df[i][0][j])
    result.append(data)
    data = []

df_result = pd.DataFrame(result, columns=column_list)
df_result.fillna('-')
# df_result.to_csv('C:/Users/Admin/estate.csv', encoding='utf-8-sig')