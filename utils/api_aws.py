import re
import requests
# modules
from config import AWS_DB_ADDRESS
    
def requests_get(db_id):
    try:
        response = requests.get(f"{AWS_DB_ADDRESS}/{db_id}")  # URL로부터 데이터를 GET 요청
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
        
        ### 불러올 때 줄바꿈 - HTML Tag로 변형
        article = article.replace('다.', '다.<br>')
        
        summary = summary.replace('\n', '<br>')
        summary = summary.replace('\r\n', '<br>')
        
        modified_summary = modified_summary.replace('\n', '<br>')
        modified_summary = modified_summary.replace('\r\n', '<br>')
        
        modified_reason = modified_reason.replace('\n', '<br>')
        modified_reason = modified_reason.replace('\r\n', '<br>')
        
        if modified == True:
            modified = '수정 완료'
        else:
            modified = '----'
        
        tag_list = []
        for tag in company_tag_list:
            filtered_item = {k: v for k, v in tag.items() if v is not None}
            tag_list.append(filtered_item)
        company_tag_list = tag_list

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
    # print(id, prev_id, next_id, article_date, media, url, category,
    #     title, article, summary_title, summary, modified_reason, 
    #     modified_summary_title, modified_summary, modified, modified_date,
    #     company_tag_list, primary_tag, secondary_tag_list)
    return (id, prev_id, next_id, article_date, media, url, category,
            title, article, summary_title, summary, modified_reason, 
            modified_summary_title, modified_summary, modified, modified_date,
            company_tag_list, primary_tag, secondary_tag_list)
    
def match_to_html(data):
    key_id_pairs = {
        # 원문 기사
        'url': 'urlDiv',
        'title': 'titleDiv',
        'category': 'categoryDiv',
        'media': 'mediaDiv',
        'articleDate': 'dateDiv',
        'id': 'dbIdDiv',
        'article': 'articleDiv',
        # aws
        'prevId': 'prevDiv',
        'nextId': 'nextDiv',
        # 태그
        'companyTag': 'companyTag',
        'primaryTag': 'primaryTag',
        'secondaryTag': 'secondaryTag',
        # 인간 수정 요약
        'modified': 'modifiedStatus',
        'modifiedDate': 'modifiedDate',
        'summaryTextCount': 'summaryTextCount',
        'modifiedSummaryTitle': 'modTitDiv',
        'modifiedSummary': 'modSumDiv',
        'modifiedReason': 'modReaDiv',
        # 자체 모델 요약
        'modelTitle': 'modelTitle',
        'modelSummary': 'modelSummary',
        'modelReason': 'modelReason',
        'modelSummaryCount': 'modelSummaryCount'
    }
    
    matching = {}
    for json_key, html_id in key_id_pairs.items():
        if json_key in data:
            if json_key == 'id': # id가 두 곳으로 가야함.
                matching['inputIdDiv'] = str(data['id']) 
            elif json_key == 'modified':
                data['modified'] = '수정 완료' if data['modified'] == True else ''
            # 자체 모델로부터 받는 경우 글자 수까지 받을 수 있으므로 수정할 것.
            elif json_key == 'modifiedSummary': # modifiedSummary 있으면 summaryTextCount 추가
                matching['summaryTextCount'] = str(len(re.sub(r'\n|- ', '', data['modifiedSummary'])))
            matching[html_id] = str(data[json_key]) if not isinstance(data[json_key], (str, list)) else data[json_key]
    
    return matching
    
def aws_db_get(db_id):
    response = requests.get(f"{AWS_DB_ADDRESS}/{db_id}")  # URL로부터 데이터를 GET 요청
    data = response.json()['result']
    
    matched_response = match_to_html(data)
    
    return matched_response


def aws_db_del(db_id):
    try:
        response = requests.delete(f"{AWS_DB_ADDRESS}/{db_id}")
        
        if str(response) == '<Response [200]>':
            res = '!!! 삭제 성공 !!!'
        else :
            res = '@@@ 삭제 실패 @@@'
    except:
        res = '삭제 중 무엇인가 잘못되었음.'
        print(res)
        
        

def requests_put(db_id, mod_sum_tit, mod_sum, mod_rea,
                 company_tag_list, primary_tag, secondary_tag_list):
    
    mod_sum_json = {"modifiedSummaryTitle" : mod_sum_tit,
                    "modifiedSummary" : mod_sum,
                    "modifiedReason" : mod_rea,
                    "companyTag" : company_tag_list,
                    "primaryTag" : primary_tag,
                    "secondaryTag" : secondary_tag_list
                    }
    # 줄바꿈 HTML Tag -> \n
    for key in ['modifiedSummary', 'modifiedReason']:
        mod_sum_json[key] = mod_sum_json[key].replace('<div>', '')
        mod_sum_json[key] = mod_sum_json[key].replace('</div>', '\n')
        mod_sum_json[key] = mod_sum_json[key].replace('<br>', '\n')
        mod_sum_json[key] = mod_sum_json[key].replace('\n\n', '\n')
        mod_sum_json[key] = mod_sum_json[key].replace('\r\n', '\n')
        mod_sum_json[key] = mod_sum_json[key].replace('\n\n', '\n')
    
    try:
        response = requests.put(f"{AWS_DB_ADDRESS}/{db_id}", json=mod_sum_json)
        
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
        response = requests.delete(f"{AWS_DB_ADDRESS}/{db_id}")
        
        if str(response) == '<Response [200]>':
            res = '!!! 삭제 성공 !!!'
        else :
            res = '@@@ 삭제 실패 @@@'
    except:
        res = '삭제 중 무엇인가 잘못되었음.'
        
    return res


def requests_post(add_data_dict):
    try:
        response = requests.post(f"{AWS_DB_ADDRESS}", json=add_data_dict)
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
        response = requests.get(f"{AWS_DB_ADDRESS}/last-id")
        db_id = response.json()['result']
    except:
        print('마지막 기사 조회 오류')
    return db_id