import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


response = requests.get('https://www.op.gg/ranking/ladder/')
print(response)
soup = BeautifulSoup(response.content, 'html.parser')
data = []
data2 = []
div = soup.find('table',{'class':'ranking-table'})
for trs in div.find_all('tr'):
    tds = list(trs.find_all('td'))

    for td in tds:
        if td.find('a'):
            ID = td.find('a').find('span').text
            data.append([ID])
            GRADE = td[3]
            data2.append([GRADE])

print(data)
print(data2)