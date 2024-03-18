from mining.scrap import scraping
import json
import time
from tqdm import tqdm

i = 0
switch = 0
data = {}
remove_talk = ['사진', '친구 초대', '퀴즈', '콘텐츠', '토론방', 
               '모의고사', '삭제된', '광고', '스타벅스']
    
with open('/home/web/app/models/kakao_group.txt', 'r') as f:
    for line in f:
        if (line.startswith('[Agent ')) :
            remove_switch = 0
            for r in remove_talk:
                if r in line:
                    remove_switch = 1
            if remove_switch == 0:
                switch = 1
                data[i] = {'summary':'', 'url':''}
            
        elif (switch == 1) and (line.startswith('-')):
            data[i]['summary'] = data[i]['summary'] + line
            
        elif (switch == 1) and ((line.startswith('https://')) or (line.startswith('bit.ly/'))):
            data[i]['url'] = line.strip()
            switch = 0
            i += 1
            
        # if i > 5:
        #     break
f.close()

import urllib3
from urllib3.util.ssl_ import create_urllib3_context

ctx = create_urllib3_context()
ctx.load_default_certs()
ctx.options |= 0x4 # ssl.OP_LEGACY_SERVER_CONNECT
    
remove_count = 0
for i in tqdm(data):
    media, title, article, article_date = scraping(ctx, data[i]['url'])
    if media == '알 수 없는 언론사':
        print(f'{i}번 요약문 :\n {title} ==> {article}')
        remove_count += 1
        # data[i]['title'] = ''
        # data[i]['article'] = ''
        # continue
    data[i]['media'] = media
    data[i]['title'] = title
    data[i]['article'] = article
    time.sleep(0.3)
    
print(f'총 데이터 개수 : {len(data.keys())}\n\
        삭제 개수 : {remove_count}\n\
        사용 가능 데이터 : {len(data.keys()) - remove_count}')

with open('jjj.json', 'w', encoding='utf-8') as f : 
    j = json.dump(data, f, indent=4, ensure_ascii=False)

### {'media':'알 수 없는 언론사'} 삭제하고 사용하시오. ###