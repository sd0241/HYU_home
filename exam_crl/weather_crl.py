# 오늘의 날씨  / 미세먼지 / 헤드라인뉴스 / IT뉴스 / 해커스영어지문
from selenium import webdriver
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")

browser = webdriver.Chrome(options=options)\

url = "https://www.naver.com/"
browser.get(url)

browser.find_element_by_id("query").send_keys("동탄 날씨")
browser.find_element_by_id("search_btn").click()

soup = BeautifulSoup(browser.page_source, "lxml")
weather = soup.find("div", attrs={"class":"api_cs_wrap"})
weather_1 = weather.find("div", attrs={"class":"today_area _mainTabContent"})
weather_2 = weather.find("div", attrs={"class":"table_info weekly _weeklyWeather"})

min_temp = weather_1.find("span",attrs={"class":"min"}).find("span",attrs={"class":"num"}).get_text()+"˚"
max_temp = weather_1.find("span",attrs={"class":"max"}).find("span",attrs={"class":"num"}).get_text()+"˚"

morning_rain_rate = weather_2.find("span",attrs={"class":"point_time morning"}).find("span", attrs={"class":"rain_rate"}).find("span",attrs={"class":"num"}).get_text()+"%"
afternoon_rain_rate = weather_2.find("span",attrs={"class":"point_time afternoon"}).find("span", attrs={"class":"rain_rate"}).find("span",attrs={"class":"num"}).get_text()+"%"

dust_info = weather_1.find("div",attrs={"class":"sub_info"}).find("dl",attrs={"class":"indicator"}).find_all("dd")
pm = dust_info[0].get_text()
spm = dust_info[1].get_text()



print("[오늘의 날씨]")
print(weather_1.find("p",attrs={"class":"cast_txt"}).get_text())
print("현재",weather_1.find("span",attrs={"class":"todaytemp"}).get_text()+"℃",end="")
print(" (최저",min_temp,"/","최고",max_temp+")")
print("오전 강수확률",morning_rain_rate,"/","오후 강수확률",afternoon_rain_rate)
print("\n미세먼지",pm)
print("초미세먼지",spm,"\n")

browser.back()
browser.find_element_by_class_name("link_news").click()
soup = BeautifulSoup(browser.page_source,"lxml")
headLine = soup.find("div",attrs={"class":"hdline_news"}).find("ul",attrs={"class":"hdline_article_list"}).find_all("li")
print("[헤드라인 뉴스]")
for news in range(0,3):
    print(f"{news+1}.",headLine[news].find("div",attrs={"class":"hdline_article_tit"}).find("a").get_text().strip())
    print("   (링크 :","https://news.naver.com"+headLine[news].find("div",attrs={"class":"hdline_article_tit"}).find("a")["href"]+")")

print("\n[IT 뉴스]")
# nclicks(LNB.sci)
browser.find_element_by_xpath("//*[@id='lnb']/ul/li[8]/a").click()
soup = BeautifulSoup(browser.page_source,"lxml")
it_headline = soup.find("div",attrs={"class":"cluster_group _cluster_content"}).find("div",attrs={"class":"cluster_body"}).find("ul",attrs={"class":"cluster_list"}).find_all("li")
# cluster_text -> a
for itnews in range(0,3):
    print(f"{itnews+1}.",it_headline[itnews].find("div",attrs={"class":"cluster_text"}).find("a",attrs={"class":"cluster_text_headline nclicks(cls_sci.clsart)"}).get_text())
    print("   (링크 :",it_headline[itnews].find("div",attrs={"class":"cluster_text"}).find("a",attrs={"class":"cluster_text_headline nclicks(cls_sci.clsart)"})["href"])

url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english"
browser.get(url)
soup = BeautifulSoup(browser.page_source,"lxml")

hackers = soup.find("div",attrs={"class":"conv_container"}).find_all("div",attrs={"class":"conv_txtBox"})
for hacker in range(1,-1,-1):
    if hacker == 1:
        print("\n[영어지문]")
    elif hacker == 0:
        print("\n[한글지문]")
    print(hackers[hacker].find("div", attrs={"class": "conv_txt"}).find("div", attrs={"id": "conv_kor_t2"}).find("span",attrs={"class":"conv_sub"}).get_text())
    print(hackers[hacker].find("div", attrs={"class": "conv_txt"}).find("div", attrs={"id": "conv_kor_t3"}).find("span",attrs={"class":"conv_sub"}).get_text())
    print(hackers[hacker].find("div", attrs={"class": "conv_txt"}).find("div", attrs={"id": "conv_kor_t4"}).find("span",attrs={"class":"conv_sub"}).get_text())
    print(hackers[hacker].find("div", attrs={"class": "conv_txt"}).find("div", attrs={"id": "conv_kor_t5"}).find("span",attrs={"class":"conv_sub"}).get_text())
