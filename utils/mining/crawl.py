# pip install selenium
# from selenium import webdriver
from bs4 import BeautifulSoup as bs
import urllib3
from urllib3.util.ssl_ import create_urllib3_context
from datetime import datetime, timedelta


def url_scrap(next_page):
    
    base_url = 'https://www.yna.co.kr/economy/all/'
    target_url = base_url + str(next_page)
    
    ctx = create_urllib3_context()
    ctx.load_default_certs()
    ctx.options |= 0x4 # ssl.OP_LEGACY_SERVER_CONNECT
    
    with urllib3.PoolManager(ssl_context=ctx) as http:
        req = http.request("GET", target_url)
    
    soup = bs(req.data, 'html.parser')

    time_list = soup.select('#container > div > div > div.section01 > section > div.list-type038 > ul > li > div > div.info-box01 > span.txt-time')
    title_list = soup.select('#container > div > div > div.section01 > section > div.list-type038 > ul > li > div > div.news-con > a > strong')
    url_list = soup.select('#container > div > div > div.section01 > section > div.list-type038 > ul > li > div > div.news-con > a')

    today = str(datetime.today().strftime('%m-%d'))
    yesterday = datetime.today() - timedelta(1)
    today_time_list = []
    today_title_list = []
    today_url_list = []
    
    complete_switch = 1
    for idx, t in enumerate(time_list):
        article_time = t.get_text()
        
        if article_time.split(' ')[0] == today:
            today_time_list.append(article_time)
            today_url_list.append('https:' + url_list[idx].get('href'))
            today_title_list.append(title_list[idx].get_text())
        elif article_time != today:
            complete_switch = 0
            break
    if complete_switch == 1:
        next_page = next_page + 1
        print(next_page)
    elif complete_switch == 0:
        next_page = -1
    return next_page, today_time_list, today_title_list, today_url_list

