import config as config

import pandas as pd
import re
import json
from tqdm import tqdm

import tiktoken
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings

class Make_DB():
    def __init__(self, data_url, chunk_size, 
                 embedding_model_name, persist_dir,
                 openai_api_key, batch_size):
        self.data_url = data_url
        self.chunk_size = chunk_size
        self.embedding_model_name = embedding_model_name
        self.persist_dir = persist_dir
        self.openai_api_key = openai_api_key
        self.batch_size = batch_size
        
        self.make_db()
        
    def make_df(self):
        with open(self.data_url, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        print('Read JSON Complete - Happy:]')
        
        df = pd.DataFrame(columns=['id', 'title', 'date', 'media', 'tag', 'summary', 'content'])
        
        for i, item in tqdm(enumerate(json_data), total=len(json_data)):
            item = item['data'][0]
            
            c = self.remove_newlines(item['paragraphs'][0]['context'])
            
            df.loc[i]=[
                item['doc_id'],
                item['doc_title'],
                item['doc_published'],
                item['doc_source'],
                item['doc_class']['code'],
                item['paragraphs'][0]['summary'],
                c
            ]
        print(df)
        return df
                
    def make_chunk(self):
        with open(self.data_url, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        print('Read JSON Complete - Happy:]')
        
        all_chunks = []
        text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=0
            )
        print(f'기사 개수 : {len(json_data)}')
        
        for i, item in tqdm(enumerate(json_data), 
                            total=len(json_data)):
            item = item['data'][0]
            content = self.remove_newlines(item['paragraphs'][0]['context'])
            chunks = text_splitter.split_text(content)
            for j, c in enumerate(chunks):
                doc = Document(
                    
                    page_content=c,
                    metadata={'id' : item['doc_id'],
                              'page' : j+1,
                              'title' : item['doc_title'],
                              'date' : item['doc_published'],
                              'media' : item['doc_source'],
                              'tag' : item['doc_class']['code'],
                              'summary' : item['paragraphs'][0]['summary']}
                )
                all_chunks.append(doc)
        
        print(all_chunks[-1].metadata)
        print(f'청크 개수 : {len(all_chunks)}')
        # self.token_cal(all_chunks)
        return all_chunks
        
    def make_db(self):
        embedding_model = OpenAIEmbeddings(openai_api_key=self.openai_api_key, 
                                           model=self.embedding_model_name)
        
        all_chunk = self.make_chunk()
        div_chunk = [all_chunk[i:i+self.batch_size] for i in range(0, len(all_chunk), self.batch_size)]
        for chunk in tqdm(div_chunk, total=len(div_chunk)):
            self.save_db(chunk, embedding_model)
        
    def save_db(self, chunk, embedding_model):
        db = Chroma.from_documents(
            documents=chunk,
            embedding=embedding_model,
            persist_directory=self.persist_dir,
        )
        db.persist()
                
    def remove_newlines(self, serie):
        emoji_pattern = re.compile("["
                # u"\U0001F600-\U0001F64F"  # emoticons
                # u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                # u"\U0001F680-\U0001F6FF"  # transport & map symbols
                # u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                u"\U00010000-\U0010FFFF"  #BMP characters 이외
                                "]+", flags=re.UNICODE)
        serie = emoji_pattern.sub(r'', serie) # no emoji
        serie = serie.replace('\n', ' ')
        serie = serie.replace('    ', ' ')
        serie = serie.replace('   ', ' ')
        serie = serie.replace('  ', ' ')
        return serie
    
    def num_tokens_from_string(self, string: str, encoding_name: str):
        '''
        Returns the number of tokens in a text string.
        Encodings specify how text is converted into tokens. Different models use different encodings.
        cl100k_base : gpt-4, gpt-3.5-turbo, text-embedding-ada-002
        p50k_base : Codex models, text-davinci-002, text-davinci-003
        r50k_base(or gpt2) : GPT-3 models like davinci
        '''
        encoding = tiktoken.get_encoding(encoding_name)
        tokens = encoding.encode(string)
        num_tokens = len(tokens)
        return num_tokens
    
    def token_cal(self, df_chunks):
        max = 0
        acc = 0
        count = 0
        for i in df_chunks:
            s = self.num_tokens_from_string(i.page_content, "cl100k_base")
            if s > max:
                max = s
            acc += s
            count += 1
        r = acc/count
        print('min token :', r ,'max token :', max)
    

if __name__=='__main__':
    data_url = config.Openai_api.DATA_URL
    chunk_size = config.Openai_api.CHUNK_SIZE
    embedding_model_name = config.Openai_api.EMBEDDING_MODEL
    persist_dir = config.Openai_api.PERSIST_DIR
    openai_api_key = config.Openai_api.API_KEY
    batch_size = config.Openai_api.BATCH_SIZE
    
    Make_DB(data_url, chunk_size, embedding_model_name, 
                  persist_dir, openai_api_key, batch_size)
    