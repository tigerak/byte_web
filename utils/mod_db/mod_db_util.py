import json
from flask import render_template
import requests

api_url = 'https://dev-api.mydailybyte.com/article'
    
def requests_get(db_id):
    try:
        response = requests.get(f"{api_url}/{db_id}")  # URL로부터 데이터를 GET 요청
        data = response.json()  # 응답 데이터를 JSON 형태로 변환
        for col in data['result']:
            if data['result'][col] == None:
                data['result'][col] = ''
                
        id = data['result']['id']
        prev_id = data['result']['prevId']
        next_id = data['result']['nextId']
        article_date = data['result']['articleDate']
        media = data['result']['media']
        url = data['result']['url']
        category = data['result']['category']
        title = data['result']['title']
        article = data['result']['article']
        summary_title = data['result']['summaryTitle']
        summary = data['result']['summary']
        modified_reason = data['result']['modifiedReason']
        modified_summary_title = data['result']['modifiedSummaryTitle']
        modified_summary = data['result']['modifiedSummary']
        modified = data['result']['modified']
        modified_date = data['result']['modifiedDate']
        company_tag_list = data['result']['companyTag']
        primary_tag = data['result']['primaryTag']
        secondary_tag_list = data['result']['secondaryTag']
        
        article = article.replace('. ', '. <br>')
        summary = summary.replace('\n-', '<br>-')
        if modified == True:
            modified = '수정 완료'
        else:
            modified = '----'
        
        tag_list = []
        for tag in company_tag_list:
            tag_json = json.dumps(tag, ensure_ascii=False)
            tag_list.append(tag_json)
        company_tag_list = tag_list
        
        # data = {'last_read_num' : db_id}
        # with open(read_path, 'w', encoding='utf-8') as f :
        #     j = json.dump(data, f, indent=4, ensure_ascii=False)

    except :
        mess = ''
        
        article = is_natural_number(db_id)
        
        id = mess
        prev_id = mess
        next_id = mess
        article_date = mess
        media = mess
        url = mess
        category = mess
        title = mess
        summary_title = mess
        summary = mess
        modified_reason = mess
        modified_summary_title = mess
        modified_summary = mess
        modified = mess
        modified_date = mess
        company_tag_list = [mess]
        primary_tag = mess
        secondary_tag_list = [mess]
        print(id, prev_id, next_id, article_date, media, url, category,
            title, article, summary_title, summary, modified_reason, 
            modified_summary_title, modified_summary, modified, modified_date,
            company_tag_list, primary_tag, secondary_tag_list)
    return (id, prev_id, next_id, article_date, media, url, category,
            title, article, summary_title, summary, modified_reason, 
            modified_summary_title, modified_summary, modified, modified_date,
            company_tag_list, primary_tag, secondary_tag_list)
        

def requests_put(db_id, mod_sum_tit, mod_sum, mod_rea,
                 company_tag_list, primary_tag, secondary_tag_list):
    
    mod_sum_json = {"modifiedSummaryTitle" : mod_sum_tit,
                    "modifiedSummary" : mod_sum,
                    "modifiedReason" : mod_rea,
                    "companyTag" : company_tag_list,
                    "primaryTag" : primary_tag,
                    "secondaryTag" : secondary_tag_list
                    }
    try:
        response = requests.put(f"{api_url}/{db_id}", json=mod_sum_json)
        
        if str(response) == '<Response [200]>':
            res = '!!! 저장 성공 !!!'
            # data = {'last_save_num' : db_id}
            # with open(save_path, 'w', encoding='utf-8') as f :
            #     j = json.dump(data, f, indent=4, ensure_ascii=False)
            
        else :
            res = '@@@ 저장 실패 @@@'
            
    except:
        res = '무엇인가 잘못되었음.'
        
    return res
    

def is_natural_number(db_id):
    try:
        int(db_id)
        if (db_id < 1): # or (db_id > )
            article = 'DB는 1번부터 시작합니다.'
        else:
            article = 'DB의 마지막 번호 이상입니다.'
    except:
        article = 'DB 번호에 숫자만 입력하고 검색버튼을 눌러주세요.'
        
    return article

def requests_del(db_id):
    try:
        response = requests.delete(f"{api_url}/{db_id}")
        print(response)
        
        if str(response) == '<Response [200]>':
            res = '!!! 삭제 성공 !!!'
        else :
            res = '@@@ 삭제 실패 @@@'
    except:
        res = '무엇인가 잘못되었음.'
        
    return res


def requests_post(add_data_dict):
    try:
        response = requests.post(f"{api_url}", json=add_data_dict)
        print(response)
        
        if str(response) == ('<Response [201]>' or '<Response [200]>'):
            res = '!!! 저장 성공 !!!'
        else :
            res = '@@@ 저장 실패 @@@'
    except:
        res = '무엇인가 잘못되었음.'
        
    return res

def get_last_id():
    try:
        response = requests.get(f"{api_url}/last-id")
        res = response.json()['result']
    except:
        res = 'error'
    return res