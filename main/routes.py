import json
import re
from time import time, sleep

import requests

from flask import (render_template, request, 
                   redirect, url_for, jsonify, abort)
# from sqlalchemy import desc, and_
# pip install flask-socketio
from flask_socketio import emit, send
import threading

# module
from main import main_bp, socketio
from config import MODEL_API_ADDRESS, DATA_API_ADDRESS
from models import Article
# from utils import (GPT, Scraping, Vertex,  
from utils import (GPT, Scraping, importent_sentence, remove_mac_specialsymbol, count_summary_char)
from utils.mining.crawl import url_scrap
from utils.api_aws import (requests_get, requests_put, requests_del, 
                           aws_db_get, aws_db_del, get_last_id)

message = 'Prompt Version : 24.01.08. '

@main_bp.route('/', methods=['GET', 'POST'])
def index():

    content = render_template('summary.html', message=message)

    return render_template('index.html', content=content)



@main_bp.route('/load_content/summary', methods=['GET', 'POST'])
def load_summary():

    if request.method == 'POST':
        start_time = time()
        render = request.form

        if render['sub_button'] == 'URL 기사 검색':
            input_url = render['api_url']

            scrape = Scraping()

            media, title, article, article_date = scrape.scraping(input_url)
            return render_template('summary.html',
                                   url=input_url,
                                   title=title,
                                   article=article,
                                   article_date=article_date,
                                   message=message)

        else:
            title = render['api_title']
            article = render['articleHighLight']

            if render['sub_button'] == '기존 요약':
                summary_name = 'topic'
            elif render['sub_button'] == '실험 요약':
                summary_name = 'experiment'
            elif render['sub_button'] == '개인화 요약':
                summary_name = 'personal'

            # GPT Ready 
            qa = GPT(model_name='gpt_4',
                     summary_name=summary_name)

            # Quality Test 
            loop = 0
            count = 0
            while (count <= 140) and (loop < 1):
                loop += 1
                # print(loop)
                (result,
                 count,
                 total_cost) = qa.summary_chat(title=title,
                                               article=article)
            # print(result)

            # Split Result 
            result_1 = result.split('### 경제 기자 요약문')
            topic = result_1[0]
            result_2 = result_1[1].split('### 아나운서용 대본')
            history = result_2[0]
            result_3 = result_2[1].split('### 대본 제목')
            summary = result_3[0]
            summary_title = result_3[1]

            # Cost Calcul
            total_cost = round(total_cost, 6)

            # Mark Topic Sentences
            if render['highlight']== 'yes':
                importent_gpt = GPT(model_name='gpt_4', summary_name='importent')
                topic_article, importent_cost = importent_gpt.importent_chat(topic=topic, article=article)
                article = importent_sentence(article=article, topic_article=topic_article)
                total_cost = round(total_cost, 6) + round(importent_cost, 6)

            # Processing Time Calcul
            end_time = time()
            processing_time = str(end_time - start_time).split(".")[0]
            return render_template('summary.html',
                                   title=title,
                                   article=article,
                                   topic=topic,
                                   history=history,
                                   summary_title=summary_title,
                                   summary=summary,
                                   summary_method=render['sub_button'],
                                   count=count,
                                   processing_time=processing_time,
                                   total_cost=total_cost,
                                   message=message)


    return render_template('summary.html', message=message)


@main_bp.route('/load_content/multi_sum', methods=['GET', 'POST'])
def load_multi_sum():

    if request.method == 'POST':
        start_time = time()
        render = request.form

        if render['sub_button'] == 'URL 기사 검색':
            main_url = render['main_url']
            sub_url = render['sub_url']

            scrape = Scraping()

            main_media, main_title, main_article, main_date = scrape.scraping(main_url)
            sub_media, sub_title, sub_article, sub_date = scrape.scraping(sub_url)
            return render_template('multi_sum.html',
                                   main_url=main_url,
                                   main_title=main_title,
                                   main_article=main_article,
                                   main_date=main_date,
                                   sub_url=sub_url,
                                   sub_title=sub_title,
                                   sub_article=sub_article,
                                   sub_date=sub_date,
                                   message=message)

        if render['sub_button'] == '복수 요약':
            main_title = render['main_title']
            sub_title = render['sub_title']
            main_article = render['main_article']
            sub_article = render['sub_article']

            qa = GPT(model_name='gpt_4',
                     summary_name='topic')
            (result,
             count,
             total_cost) = qa.multi_summary(main_title=main_title,
                                        main_article=main_article,
                                        sub_title=sub_title,
                                        sub_article=sub_article)
            # print(result)
            # Split Result 
            result_1 = result.split('경제 기자 요약문:')
            topic = result_1[0]
            result_2 = result_1[1].split('아나운서용 대본:')
            history = result_2[0]
            result_3 = result_2[1].split('대본 제목:')
            summary = result_3[0]
            summary_title = result_3[1]
            # Processing Time Calcul
            end_time = time()
            processing_time = str(end_time - start_time).split(".")[0]
            # Cost Calcul
            total_cost = round(total_cost, 6)
            return render_template('multi_sum.html',
                                   main_title=main_title,
                                   main_article=main_article,
                                   sub_title=sub_title,
                                   sub_article=sub_article,
                                   summary_title=summary_title,
                                   summary=summary,
                                   count=count,
                                   processing_time=processing_time,
                                   total_cost=total_cost,
                                #    problem=problem,
                                   topic=topic,
                                   history=history,
                                   message=message)
    return render_template('multi_sum.html',
                           message=message)


@main_bp.route('/load_content/mod_db', methods=['GET', 'POST'])
def mod_db():
    if request.method == 'GET':
        num = request.args.get('lastViewNumber')
        res = '이것은 마지막으로 본 기사입니다.'

    elif request.method == 'POST':
        render = request.form
        # print(render)
        res = ''

        if render['sub_button'] == '마지막 저장 기사':
            num = request.form['lastSaveNumber']
            res = '이것은 마지막 저장 기사입니다.'

        elif render['sub_button'] == '마지막 본 기사':
            num = request.form['lastViewNumber']
            res = '이것은 마지막으로 본 기사입니다.'

        elif render['sub_button'] == '마지막 기사 조회':
            num = get_last_id()
            res = '이것은 DB의 마지막 기사입니다.'

        elif render['sub_button'] == '검색':
            try:
                num = str(int(render['api_id']))
            except:
                num = '숫자 아님'

        elif render['sub_button'] == '<< 이전':
            num = render['prev_num'].replace('번', '')

        elif render['sub_button'] == '다음 >>':
            num = render['next_num'].replace('번', '')

        elif render['sub_button'] == '저 장':
            try:
                num = str(int(render['currentNewsNumber']))
            except:
                num = '숫자 아님'

            company_tag_raw = render.getlist('company_tag')
            try:
                # company_tag_raw가 통채로 string임.
                company_tag = [item for item in company_tag_raw if item][0]
                split_pattern = re.compile(r'(?<=})\s*, \s*(?={)')
                company_tag_raw = list(split_pattern.split(company_tag))
                corrected_data = [item.replace("'", '"') for item in company_tag_raw]
                company_tag_list = [json.loads(tag) for tag in corrected_data if tag]
            except:
                company_tag_list = None

            primary_tag_raw = render['primary_tag']
            primary_tag_list = list(primary_tag_raw.split(', '))
            primary_tag = primary_tag_list[0]

            secondary_tag_raw = render['secondary_tag']
            secondary_tag_list = list(secondary_tag_raw.split(', '))

            mod_sum_tit = render['mod_sum_tit']
            mod_sum = render['mod_sum']
            mod_sum = remove_mac_specialsymbol(mod_sum)
            mod_rea = render['mod_rea']
            mod_rea = remove_mac_specialsymbol(mod_rea)

            # print(num, company_tag_list, primary_tag, secondary_tag_list,
            #       mod_sum_tit, mod_sum, mod_rea, save_path)
            res = requests_put(db_id=num,
                            company_tag_list=company_tag_list,
                            primary_tag=primary_tag,
                            secondary_tag_list=secondary_tag_list,
                            mod_sum_tit=mod_sum_tit,
                            mod_sum=mod_sum,
                            mod_rea=mod_rea)

        elif render['sub_button'] == '삭제':
            try:
                num = str(int(render['currentNewsNumber']))
            except:
                num = '숫자 아님'
            res = requests_del(num)
            num = str(int(num) - 1)

    (id, prev_id, next_id, article_date, media, url, category,
     title, article, summary_title, summary, modified_reason,
     modified_summary_title, modified_summary, modified, modified_date,
     company_tag_list, primary_tag, secondary_tag_list) = requests_get(num)
    # print(id, prev_id, next_id, article_date, media, url, category,
    #         title, article, summary_title, summary, modified_reason, 
    #         modified_summary_title, modified_summary, modified, modified_date,
    #         company_tag_list, primary_tag, secondary_tag_list)
    
    # 수정 요약문 총 글자 수 계산
    count_summary = len(count_summary_char(modified_summary))
    
    return render_template('mod_db.html',
                            id=id,
                            prev_id=prev_id,
                            next_id=next_id,
                            article_date = article_date,
                            media = media,
                            url = url,
                            category = category,
                            title = title,
                            article = article,
                            summary_title = summary_title,
                            summary = summary,
                            modified_reason = modified_reason,
                            modified_summary_title = modified_summary_title,
                            modified_summary = modified_summary,
                            count_summary = count_summary,
                            modified = modified,
                            modified_date = modified_date,
                            company_tag_list = company_tag_list,
                            primary_tag = primary_tag,
                            secondary_tag_list = secondary_tag_list,
                            res = res,
                            message=message)



@main_bp.route('/load_content/dpo_data', methods=['GET', 'POST'])
def dpo_data():

    return render_template('dpo_data.html',
                            message=message)

@main_bp.route('/load_content/db_manager', methods=['GET', 'POST'])
def db_manager():

    return render_template('db_manager.html',
                            message=message)

    
@main_bp.route('/util/url_scraping', methods=['POST'])
def url_scraping():
    data = request.form
    
    url = data['urlDiv']
    
    scrape = Scraping()
    media, title, article, article_date = scrape.scraping(url)
    
    response = {
        "urlDiv" : url,
        "mediaDiv" : media,
        "titleDiv" : title,
        "articleDiv" : article,
        "dateDiv" : article_date
    }
    
    return jsonify(response)
    
@main_bp.route('/util/model_api', methods=['POST'])
def model_api():
    data = request.form
    
    response = requests.post(MODEL_API_ADDRESS, data=data)
    response = response.json()
    transfor_html_id = {
        "modelSummaryCount" : response['summary_count'],
        "modelTitle" : response['summary_title'],
        "modelSummary" : response['summary'],
        "modelReason" : response['summary_reason'] + "\n" \
                        + "기업 태그(Company Tag):\n" \
                        + "Main:" + response['main'] + "\n" \
                        + "Sub:" + response['sub'] + "\n" \
                        + "대분류(Major Classification):\n" \
                        + response['major_class'] + "\n" \
                        + "중분류(Medium Classification):\n" \
                        + response['medium_class']
    }
    
    return jsonify(transfor_html_id)

@main_bp.route('/util/aws_db_api', methods=['POST'])
def db_move():
    data = request.form
    
    button_values = ['searchButton', 'prevBut', 'nextBut']
    if data['buttonId'] in button_values:
        db_id = [value for key, value in data.items() 
                 if key not in ['buttonId', 'lastViewNumber']]
        get_dict = aws_db_get(db_id[0])
        return jsonify(get_dict)
    
    elif data['buttonId'] == 'listVisitButton':
        db_id = request.form['lastViewNumber']
        get_dict = aws_db_get(db_id)
        return jsonify(get_dict)
    
    elif data['buttonId'] == 'lastArticleButton':
        db_id = get_last_id()
        get_dict = aws_db_get(db_id)
        return jsonify(get_dict)
    
    elif data['buttonId'] == 'delButton':
        del_db_id = request.form['dbIdDiv']
        aws_db_del(del_db_id)
        return_db_id = request.form['prevDiv'] if request.form['prevDiv'] != 'None' else request.form['nextDiv']
        get_dict = aws_db_get(return_db_id)
        return jsonify(get_dict)
    
    elif data['buttonId'] == 'saveButton':
        return jsonify()

@main_bp.route('/util/data_api', methods=['POST'])
def data_api():
    data = request.form
    
    response = requests.post(DATA_API_ADDRESS, data=data)

    return response.json()

    
@main_bp.route('/load_content/kg_db', methods=['GET', 'POST'])
def kg_db():
    if request.method == 'GET':
        render = '겟'

    if request.method == 'POST':
        start_time = time()
        render = request.form

        if render['sub_button'] == 'URL 기사 검색':
            input_url = render['api_url']

            scrape = Scraping()

            media, title, article, article_date = scrape.scraping(input_url)
            return render_template('kg_db.html',
                                   url=input_url,
                                   title=title,
                                   article=article,
                                   article_date=article_date,
                                   message=message)

    return render_template('kg_db.html',
                           message=render)




# @main_bp.route('/load_content/chat', methods=['GET', 'POST'])
# def chating():
#     return render_template('chat.html')

# @socketio.on('message')
# def handle_message(data):
#     username = data['username']
#     message = data['message']
#     # 메시지와 사용자 이름을 함께 방송합니다.
#     socketio.emit('message', {'username': username, 'message': message})


# @main_bp.route('/load_content/crawl', methods=['GET', 'POST'])
# def crawling():
#     return render_template('crawl.html')

# def scrape_loop():
#     next_page = 1
#     while next_page != -1:
#         np, time_list, title_list, url_list = url_scrap(next_page)
#         socketio.emit('scraped_data', {'np': np, 'data': list(zip(time_list, title_list, url_list))})
#         next_page = np
#         if np == -1:
#             socketio.emit('scraping_finished', {'message': '수집이 완료되었습니다'})
#             break
#         sleep(1)

# @socketio.on('start_scraping')
# def handle_start_scraping():
#     threading.Thread(target=scrape_loop, daemon=True).start()


# @main_bp.route('/test', methods=['GET', 'POST'])
# def test_index():
#     return render_template('test_index.html')

# @socketio.on('connect', namespace='/test')
# def test_connect(auth):
#     # send(auth, namespace='/test')
#     print(auth)
#     # emit('test_message', {'name':'알림', 'text':auth}, namespace='/test')

# @socketio.on('test_message', namespace='/test')
# def test_message(data):
#     print(f'\n{data}\n')
#     name = data['name']
#     text = data['text']
#     emit('output_message', {'name':name, 'text':text}, namespace='/test')
#     # send(message=data, namespace='/test')
#     # emit('some_event', '아니시에이트!!')


# DB 저장 페이지
@main_bp.route('/news_save', methods=['GET'])
def news_save():

    return render_template('news_save.html')

@main_bp.route('/getNews')
def get_news():
    url = request.args.get("url")
    scrape = Scraping()
    media, title, article, article_date = scrape.scraping(url)
    if (media == "알 수 없는 언론사"):
        result = '실패'
    else:
        result = {
            'media' : media,
            'title' : title,
            'article' : article,
            'article_date' : article_date
        }
        jsonify(result)

    return result

@main_bp.route('/save', methods=['POST'])
def save_news():
    payLoad = request.get_json()
    print(payLoad)

    response = requests.post('https://dev-api.mydailybyte.com/article', json=payLoad)
    #response = requests.post('http://localhost:8080/article', json=payLoad)

    if (response.status_code == 201):
        return response.text
    else:
        return abort(400, "error")
