from models import Prompts
from config import Openai_api
from utils.util import (cost_calculation, 
                        remove_newlines,
                        completed_prompt)

import re

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import create_qa_with_sources_chain
# from langchain.chains.combine_documents.stuff import StuffDocumentsChain
# from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings


class GPT():
    def __init__(self, 
                 openai_api_key=Openai_api.API_KEY, 
                 model_name = 'gpt_3',
                 summary_name = 'title',
                 proof_name = 'no',
                 persist_dir=Openai_api.PERSIST_DIR, 
                 embedding_model_name=Openai_api.EMBEDDING_MODEL):
        
        self.openai_api_key = openai_api_key
        self.model_name = model_name
        self.summary_name = summary_name
        self.proof_name = proof_name
        if model_name == 'gpt_3':
            model_name = Openai_api.CHAT_MODEL_3
        elif model_name == 'gpt_4':
            model_name = Openai_api.CHAT_MODEL_4
        # self.embedding_model = OpenAIEmbeddings(openai_api_key=openai_api_key,
        #                                         model=embedding_model_name)
        # self.db = Chroma(persist_directory=persist_dir,
        #                  embedding_function=self.embedding_model)
    
        self.chat_model = ChatOpenAI(openai_api_key=self.openai_api_key,
                                     model=model_name,
                                     temperature=0.0)
        
    def prompt(self):
        select = {'all_3':Prompts.all_3, 
                  'all_4':Prompts.all_4, 
                  'line_3':Prompts.line_3, 
                  'line_4':Prompts.line_4, 
                  'title_3':Prompts.title_3, 
                  'title_4':Prompts.title_4,
                  'topic_4':Prompts.topic_4}
        
        choice_name = ''.join([self.summary_name, self.model_name[-2:]])
        prompt_select = select[choice_name]
        return prompt_select
    
    def select_chat(self, title_chr, article_chr):
        if self.summary_name == 'title' or self.summary_name == 'topic':
            summary_prompt = PromptTemplate(input_variables=['title', 'article'],
                                            template=self.prompt())
            input_format = {'title' : title_chr, 'article' : article_chr}
        else:
            summary_prompt = PromptTemplate(input_variables=['article'],
                                            template=self.prompt())
            input_format = {'article' : article_chr}
        
        summary_chain = LLMChain(llm=self.chat_model,
                                 prompt=summary_prompt)
        
        ######
        c_t = article_chr + self.prompt()
        ######
        return summary_chain, input_format, c_t
    
        
    def select_proof(self):
        
        if self.model_name == 'gpt_3':
            proofreader_templit = Prompts.proof_3
        elif self.model_name == 'gpt_4':
            proofreader_templit = Prompts.proof_4
            
        proofreader_prompt = PromptTemplate(input_variables=['article', 'summary'],
                                            template=proofreader_templit)
        proofreader_chain = LLMChain(llm=self.chat_model,
                                     prompt=proofreader_prompt)

        return proofreader_chain, proofreader_templit
        
            
    def summary_chat(self, title_chr, article_chr):
        # Data Preprocessing
        article_chr = remove_newlines(article_chr)
        title_chr = remove_newlines(title_chr)
        
        summary_chain, input_format, c_t = self.select_chat(title_chr, article_chr)

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
            count = summary_result.split('한국어 선생님 수정 요약문:')[1]
            count = count.split('요약문 제목:')[0]
            count = remove_newlines(count)
            count = count.replace(' ', '')
        except:
            count = remove_newlines(summary_result)
            count = count.replace(' ', '')
        ###################################################
        
        if self.proof_name == 'yes':
            proof_result, p_total_cost = self.proof_chat(article_chr, summary_result)
            ### 비용 계산 ###
            total_cost = total_cost + p_total_cost
        elif self.proof_name == 'no':
            proof_result = '요약 교정을 선택하지 않았습니다.'
            
        return len(count), summary_result, proof_result, total_cost
            
        
    def proof_chat(self, article, summary):
        proofreader_chain, cost_calcul_prom = self.select_proof()
        
        article = remove_newlines(article)
        
        proofreader_result = proofreader_chain.run({'article' : article, 'summary' : summary})
        
        # Test Print
        # print('AI PROOFREADER :\n', proofreader_result)
        
        ###################################################
        ### 비용 계산 ###
        total_text = cost_calcul_prom + article + summary
        input_token = cost_calculation(total_text)
        output_token = cost_calculation(proofreader_result)
        if self.model_name == 'gpt_3':
            input_cost = input_token * (0.0015 / 1000)
            output_cost = output_token * (0.002 / 1000)
            total_cost = input_cost + output_cost
        elif self.model_name == 'gpt_4':
            input_cost = input_token * (0.03 / 1000)
            output_cost = output_token * (0.06 / 1000)
            total_cost = input_cost + output_cost
        ###################################################
        
        return proofreader_result, total_cost
        
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