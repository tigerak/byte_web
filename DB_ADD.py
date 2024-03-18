### 실수 실행 방지 ###
from utils.mod_db.mod_db_util import requests_post, requests_del
import pandas as pd
import requests
import json
### 실수 실행 방지 ###
data_path = '/home/web/app/data.csv'
df = pd.read_csv(data_path)
print(df.shape[0])
# 형태 변환 key
name_change = {'article_date' : 'articleDate',
               'media' : 'media',
               'url' : 'url',
               'category' : 'category',
               'title' : 'title',
               'article' : 'article',
               'summary_title' : 'summaryTitle', 
               'summary' : 'summary'}
send_save_list = []
for row in range(df.shape[0]):
    unit_dict = {}
    for col in df.columns:
        unit_dict[name_change[col]] = df.loc[row][col]
    unit_dict['companyTag'] = None
    unit_dict['primaryTag'] = None
    unit_dict['secondaryTag'] = None
    send_save_list.append(unit_dict)
### 실수 실행 방지 ###
json_str = json.dumps(send_save_list, ensure_ascii=False, indent=2)
### 실수 실행 방지 ###
api_url = 'https://dev-api.mydailybyte.com/article'
### 실수 실행 방지 ###
print(json_str)
### 실수 실행 방지 ###
# response = requests_post(send_save_list)
# print(response)
### 실수 실행 방지 ###