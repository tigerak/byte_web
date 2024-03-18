from main import bp, socketio
from models import Article
from utils import GPT, Vertex, text_trans, scraping
from utils.mining.crawl import url_scrap

from time import time, sleep
from flask import render_template, request, redirect, url_for, jsonify
from sqlalchemy import desc, and_
# pip install flask-socketio
from flask_socketio import emit, send
import threading


message = 'Prompt Version : 23.12.09. '

@bp.route('/', methods=['GET', 'POST'])
def index():
    

    content = render_template('summary.html', message=message)

    return render_template('index.html', content=content)

    
    
@bp.route('/load_content/summary', methods=['GET', 'POST'])
def load_summary():
    
    if request.method == 'POST':
        start_time = time()
        render = request.form
        
        if render['sub_button'] == 'URL 기사 검색':
            input_url = render['api_url']
            title, article, article_date = scraping(input_url)
            return render_template('summary.html', 
                                   url=input_url,
                                   t=title, 
                                   a=article,
                                   d=article_date,
                                   message=message)
        
        elif render['sub_button'] == '추출':
            title = render['title_text']
            article = render['article_text']
            
            qa = GPT(model_name='gpt_4', 
                     summary_name='topic',
                     proof_name = 'no')
            loop = 0
            count = 0
            while (count <= 140) and (loop < 2):
                loop += 1
                print(loop)
                (count,
                result, 
                proofreading,
                total_cost) = qa.summary_chat(title_chr=title, 
                                            article_chr=article)
            print(result)
            # Split Result 
            result_1 = result.split('한국어 선생님 수정 요약문:')
            topic = result_1[0]
            result_2 = result_1[1].split('요약문 제목:')
            summary = result_2[0]
            try:
                problem = result_2[1]
            except:
                problem = '수정 사항이 없습니다.'
            # Processing Time Calcul
            end_time = time()
            processing_time = str(end_time - start_time).split(".")[0]
            # Cost Calcul
            total_cost = round(total_cost, 6)
            return render_template('summary.html',
                                   t=title,
                                   a=article,
                                   topic=topic,
                                   summary=summary,
                                   problem=problem,
                                   count=count,
                                   processing_time=processing_time,
                                   total_cost=total_cost,
                                   message=message)
          
        elif render['sub_button'] == ('요약' or '교정'):
            input_url = render['api_url']
            title = render['api_title']
            article = render['api_article']
            model_name = render['model']
            summary_name = render['summary_way']
            proof_name = render['proof']
            summary = render['api_summary']
            
        else:
            return '무슨 짓을 한거죠?'
        
        
        # 모델 선택
        if model_name != 'bard':
            qa = GPT(model_name=model_name, 
                     summary_name=summary_name, 
                     proof_name=proof_name)
            
            if render['sub_button'] == '요약':
                (count, 
                summary, 
                proofreading,
                total_cost) = qa.summary_chat(title_chr=title, 
                                              article_chr=article)
                # Rendering Name
                model_name = text_trans(model_name)
                summary_name = text_trans(summary_name)
                # Processing Time Calcul
                end_time = time()
                processing_time = str(end_time - start_time).split(".")[0]
                # Cost Calcul
                total_cost = round(total_cost, 6)
                return render_template('summary.html', 
                                        url=input_url,
                                        m=model_name, 
                                        n=summary_name, 
                                        c=count, 
                                        t=title, 
                                        a=article, 
                                        s=summary, 
                                        p=proofreading,
                                        time=processing_time,
                                        total_cost=total_cost,
                                        message=message)
                
            elif render['sub_button'] == '교정':
                proofreading, total_cost = qa.proof_chat(article=article, 
                                    summary=summary)
                
                model_name = text_trans(model_name)
                # Processing Time Calcul
                end_time = time()
                processing_time = str(end_time - start_time).split(".")[0]
                # Cost Calcul
                total_cost = round(total_cost, 6)
                return render_template('summary.html', 
                                        url=input_url,
                                        m=model_name, 
                                        t=title, 
                                        a=article, 
                                        s=summary, 
                                        p=proofreading,
                                        time=processing_time,
                                        total_cost=total_cost,
                                        message=message)
                
            else:
                return 'GPT는 모든 것을 다했다.'
                
                
        elif model_name == 'bard':
            gg = Vertex(summary_name=summary_name, 
                        proof_name=proof_name)
            if render['sub_button'] == '요약':
                (summary, 
                 proofreading,
                 count,
                 total_cost) = gg.summary(title=title,
                                          article=article)
                # Rendering Name
                model_name = text_trans(model_name)
                summary_name = text_trans(summary_name)
                # Processing Time Calcul
                end_time = time()
                processing_time = str(end_time - start_time).split(".")[0]
                # Cost Calcul
                total_cost = round(total_cost, 6)
                
                return render_template('summary.html', 
                                        url=input_url,
                                        m=model_name, 
                                        n=summary_name, 
                                        c=count, 
                                        t=title, 
                                        a=article, 
                                        s=summary, 
                                        p=proofreading,
                                        time=processing_time,
                                        total_cost=total_cost,
                                        message=message)
            
            elif render['sub_button'] == '교정':
                proofreading, total_cost = gg.proofreader(summary=summary,
                                                          article=article)
                # Rendering Name
                model_name = text_trans(model_name)
                # Processing Time Calcul
                end_time = time()
                processing_time = str(end_time - start_time).split(".")[0]
                # Cost Calcul
                total_cost = round(total_cost, 6)
                
                return render_template('summary.html', 
                                        url=input_url,
                                        m=model_name, 
                                        t=title, 
                                        a=article, 
                                        s=summary, 
                                        p=proofreading,
                                        time=processing_time,
                                        total_cost=total_cost,
                                        message=message)
                
        else:
            return '모델을 선택했나요?'

    return render_template('summary.html', message=message)


@bp.route('/load_content/multi_sum', methods=['GET', 'POST'])
def load_multi_sum():
    
    if request.method == 'POST':
        start_time = time()
        render = request.form
        
        if render['sub_button'] == 'URL 기사 검색':
            main_url = render['main_url']
            sub_url = render['sub_url']
            main_title, main_article, main_date = scraping(main_url)
            sub_title, sub_article, sub_date = scraping(sub_url)
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
        
        if render['sub_button'] == '추출 요약':
            main_title = render['main_title']
            sub_title = render['sub_title']
            main_article = render['main_article']
            sub_article = render['sub_article']
            
            qa = GPT(model_name='gpt_4', 
                     summary_name='topic',
                     proof_name = 'no')
            (result,
             count,
             total_cost) = qa.multi_summary(main_title=main_title,
                                        main_article=main_article,
                                        sub_title=sub_title,
                                        sub_article=sub_article)
            print(result)
            # Split Result 
            result_1 = result.split('편집장 수정 요약문:')
            topic = result_1[0]
            result_2 = result_1[1].split('수정 사항:')
            summary = result_2[0]
            try:
                problem = result_2[1]
            except:
                problem = '수정 사항이 없습니다.'
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
                                   summary=summary,
                                   count=count,
                                   processing_time=processing_time,
                                   total_cost=total_cost,
                                   problem=problem,
                                   topic=topic,
                                   message=message)
    return render_template('multi_sum.html',
                           message=message)


@bp.route('/load_content/chat', methods=['GET', 'POST'])
def chating():
    return render_template('chat.html')

@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    # 메시지와 사용자 이름을 함께 방송합니다.
    socketio.emit('message', {'username': username, 'message': message})
    

@bp.route('/load_content/crawl', methods=['GET', 'POST'])
def crawling():
    return render_template('crawl.html')

def scrape_loop():
    next_page = 1
    while next_page != -1:
        np, time_list, title_list, url_list = url_scrap(next_page)
        socketio.emit('scraped_data', {'np': np, 'data': list(zip(time_list, title_list, url_list))})
        next_page = np
        if np == -1:
            socketio.emit('scraping_finished', {'message': '수집이 완료되었습니다'})
            break
        sleep(1)

@socketio.on('start_scraping')
def handle_start_scraping():
    threading.Thread(target=scrape_loop, daemon=True).start()

   
@bp.route('/test', methods=['GET', 'POST'])
def test_index():
    return render_template('test_index.html')

@socketio.on('connect', namespace='/test')
def test_connect(auth):
    # send(auth, namespace='/test')
    print(auth)
    # emit('test_message', {'name':'알림', 'text':auth}, namespace='/test')

@socketio.on('test_message', namespace='/test')
def test_message(data):
    print(f'\n{data}\n')
    name = data['name']
    text = data['text']
    emit('output_message', {'name':name, 'text':text}, namespace='/test')
    # send(message=data, namespace='/test')
    # emit('some_event', '아니시에이트!!')