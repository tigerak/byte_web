from models import Prompts
from config import Openai_api
from utils.util import (cost_calculation, 
                        remove_newlines,
                        completed_prompt)

import re

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


class GPT():
    def __init__(self, 
                 openai_api_key=Openai_api.API_KEY, 
                 model_name = 'gpt_4',
                 summary_name = 'topic'):
        
        self.openai_api_key = openai_api_key
        self.model_name = model_name
        self.summary_name = summary_name
        if model_name == 'gpt_4':
            model_name = Openai_api.CHAT_MODEL_4
    
        self.chat_model = ChatOpenAI(openai_api_key=self.openai_api_key,
                                     model=model_name,
                                     temperature=0.0)
        
    def prompt(self):
        select = {'topic_4':Prompts.topic_4,
                  'experiment_4':Prompts.experiment_4,
                  'importent_4':Prompts.importent_4,
                  'personal_4':Prompts.personal_4}
        
        choice_name = ''.join([self.summary_name, self.model_name[-2:]])
        prompt_select = select[choice_name]
        return prompt_select
    
    def select_chat(self, title, article):
        summary_prompt = PromptTemplate(input_variables=['title', 'article'],
                                        template=self.prompt())
        input_format = {'title' : title, 'article' : article}
        
        summary_chain = LLMChain(llm=self.chat_model,
                                 prompt=summary_prompt)
        
        ######
        c_t = article + self.prompt()
        ######
        return summary_chain, input_format, c_t
         
    def summary_chat(self, title, article):
        # Data Preprocessing
        title = remove_newlines(title)
        article = remove_newlines(article)
        
        summary_chain, input_format, c_t = self.select_chat(title, article)

        summary_result = summary_chain.run(input_format)
        
        # Test Print
        # print(f'{self.summary_name} RESULT -! :\nTITLE : {title_chr}\nAI SUMMARY :\n{summary_result}')
        
        ###################################################
        ### 비용 계산 ###
        input_token = cost_calculation(c_t)
        output_token = cost_calculation(summary_result)
        if self.model_name == 'gpt_3':
            input_cost = input_token * (0.0015 / 1000)
            output_cost = output_token * (0.002 / 1000)
            total_cost = input_cost + output_cost
        elif self.model_name == 'gpt_4':
            input_cost = input_token * (0.03 / 1000)
            output_cost = output_token * (0.06 / 1000)
            total_cost = input_cost + output_cost
        ###################################################
        
        ###################################################
        ### 글자 수 계산 ###
        try:
            count = summary_result.split('아나운서용 대본:')[1]
            count = count.split('대본 제목:')[0]
            count = remove_newlines(count)
            count = count.replace(' ', '')
        except:
            count = remove_newlines(summary_result)
            count = count.replace(' ', '')
            count = '4444' # 임시
        ###################################################
        
        return  summary_result, len(count), total_cost
            
        
    def multi_summary(self, main_title, main_article, sub_title, sub_article):
        main_title = remove_newlines(main_title)
        main_article = remove_newlines(main_article)
        sub_title = remove_newlines(sub_title)
        sub_article = remove_newlines(sub_article)
        
        input_format = {'main_title' : main_title, 'main_article' : main_article, 
                        'sub_title' : sub_title, 'sub_article' : sub_article}
        
        multi_prompt = PromptTemplate(input_variables=['main_title', 'main_article',
                                                       'sub_title', 'sub_article'],
                                      template=Prompts.topic_multi)
        
        multi_chain = LLMChain(llm=self.chat_model,
                               prompt=multi_prompt)
        
        multi_result = multi_chain.run(input_format)
        
        ###################################################
        ### 비용 계산 ###
        c_t = main_title + main_article + sub_title + sub_article + Prompts.topic_multi
        input_token = cost_calculation(c_t)
        output_token = cost_calculation(multi_result)
        input_cost = input_token * (0.03 / 1000)
        output_cost = output_token * (0.06 / 1000)
        total_cost = input_cost + output_cost
        ###################################################
        
        ###################################################
        ### 글자 수 계산 ###
        try:
            count = multi_result.split('한국어 선생님 수정 요약문:')[1]
            count = count.split('수정 사항:')[0]
            count = remove_newlines(count)
            count = count.replace(' ', '')
        except:
            count = remove_newlines(multi_result)
            count = count.replace(' ', '')
        # print(f'글자 수 : {len(count)}')
        ###################################################
        
        return multi_result, len(count), total_cost
    
    
    def importent_chat(self, topic, article):
        # Data Preprocessing
        article = remove_newlines(article)
        
        importent_prompt = PromptTemplate(input_variables=['topic', 'article'],
                                          template=self.prompt())
        input_format = {'topic' : topic, 'article' : article}
        
        importent_chain = LLMChain(llm=self.chat_model,
                                   prompt=importent_prompt)
        
        importent_result = importent_chain.run(input_format)
        
        # Test Print
        # print(f'{self.summary_name} RESULT -! :\nTITLE : {title_chr}\nAI SUMMARY :\n{summary_result}')
        
        ###################################################
        ### 비용 계산 ###
        input_token = cost_calculation(article + self.prompt())
        output_token = cost_calculation(importent_result)
        if self.model_name == 'gpt_3':
            input_cost = input_token * (0.0015 / 1000)
            output_cost = output_token * (0.002 / 1000)
        elif self.model_name == 'gpt_4':
            input_cost = input_token * (0.03 / 1000)
            output_cost = output_token * (0.06 / 1000)
        total_cost = input_cost + output_cost
        ###################################################
        
        return  importent_result, total_cost