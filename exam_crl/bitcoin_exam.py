import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import pybithumb
import time

tickers = pybithumb.get_tickers()
price = pybithumb.get_current_price("BTC")


result = []
price = []
for i in range(0, 5) :
     price.append("BTC")
     price.append(pybithumb.get_current_price("BTC"))
     price.append("ETH")
     price.append(pybithumb.get_current_price("ETH"))
     time.sleep(10)
     print(i)


