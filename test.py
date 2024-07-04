from utils import GPT
from app.utils.api_palm import Vertex
from models import Article
import time
import pandas as pd
from utils.mining.crawl import url_scrap

if __name__ == '__main__':
    ###
    # summary_select = ['all', 'line', 'title']
    # model_select = ['gpt_3', 'gpt_4']
    
    # k = 0
    
    # from models import Article
    # dicts = Article.byte_test
    # for item in dicts[k:k+1]:
    #     t = item['title']
    #     a = item['context']
    #     s = item['summary']
    #     print(f'HUMAN SUMMARY :\n{s}')
    #     for ss in summary_select:
    #         for ms in model_select:
    #             qa = GPT(model_name=ms, summary_name=ss, proof_name='no')
    #             qa.summary_chat(t, a)

    ### Google BARD
#     import os
#     print(os.cpu_count())
    
#     article = Article.byte_test[0]
        
#     prompt = f'''
# 당신은 경제 전문 기자입니다.
# 당신은 독자들이 기사 내용을 쉽게 파악할 수 있도록 기사를 요약하는 일을 하게 됩니다.
# 아래 뉴스 기사를 200자 내외의 3줄 요약문으로 바꿔주십시오. 

# <뉴스 기사>{article}</뉴스 기사>

# 첫 번째 문장과 마지막 문장은 '-니다'로 끝내주세요.
# 두 번째 문장은 '-데요'로 끝내주세요.

# 단계별로 천천히 생각해보세요.
#     '''
#     gg = Vertex()
#     gg.summary(prompt)

    ### Crawling ###
    next_page = 1

    total_today_time = []
    total_today_title = []
    total_today_url = []
    while next_page != -1:
        n_p, today_time_list, today_title_list, today_url_list = url_scrap(next_page)
        next_page = n_p
        total_today_time.extend(today_time_list)
        total_today_title.extend(today_title_list)
        total_today_url.extend(today_url_list)
        # 대기
        time.sleep(1)
        
    print(total_today_title)
    # df = pd.DataFrame(columns=['date', 'title', 'url'])
    # df['date'] = total_today_time
    # df['title'] = total_today_title
    # df['url'] = total_today_url

    # df.to_csv('test.csv', index=None)
    # print(df)

    