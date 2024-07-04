from models.prompt import Prompts
from utils.util import (cost_calculation, 
                        remove_newlines, 
                        completed_prompt)

# pip install google-cloud-aiplatform 
# gcloud auth application-default login
from vertexai.language_models import TextGenerationModel
from google.cloud import aiplatform
import google.auth

class Vertex():
    def __init__(self, 
                 summary_name='all', 
                 proof_name='no'):
        credentials, project = google.auth.default()
# localhost에서 실행할 때는 Google Cloud SDK가 자동으로 현재 프로젝트를 인식하지만, nginx를 사용하면 Google Cloud SDK가 현재 프로젝트를 인식하지 못합니다.
# 따라서 aiplatform.init() 함수를 호출할 때 프로젝트 ID를 명시적으로 지정해야 합니다.
        aiplatform.init(
            # your Google Cloud Project ID or number
            # environment default used is not set
            project='hybrid-formula-404304',

            # the Vertex AI region you will use
            # defaults to us-central1
            location='asia-northeast3',

            # # Google Cloud Storage bucket in same region as location
            # # used to stage artifacts
            # staging_bucket='gs://my_staging_bucket',

            # custom google.auth.credentials.Credentials
            # environment default credentials used if not set
            credentials=credentials,

            # # customer managed encryption key resource name
            # # will be applied to all Vertex AI resources if set
            # encryption_spec_key_name=my_encryption_key_name,

            # # the name of the experiment to use to track
            # # logged metrics and parameters
            # experiment='my-experiment',

            # # description of the experiment above
            # experiment_description='my experiment description'
        )
        
        self.summary_name=summary_name
        self.proof_name=proof_name
        
        # Model
        self.model = TextGenerationModel.from_pretrained("text-bison@001")
        
    
    def summary(self, title, article):
        # Data Preprocessing
        title = remove_newlines(title)
        article = remove_newlines(article)
        
        # Prompt
        if self.summary_name == 'title':
            prompt_form = Prompts.bard_title
            input_format = {'article' : article, 'title' : title}
        elif self.summary_name == 'all':
            prompt_form = Prompts.bard_all
            input_format = {'article' : article}
        elif self.summary_name == 'line':
            prompt_form = Prompts.bard_line
            input_format = {'article' : article}
        
        prompt = completed_prompt(prompt_form=prompt_form,
                                  input_format=input_format)
        
        response = self.model.predict(prompt,
                                      max_output_tokens=1024,
                                      temperature=0.3,
                                      top_k=40,
                                      top_p=0.8,
                                      candidate_count=1)
        summary_result = response.text
        
        # Test Print
        # print(f"Response from Model: {response}")
        
        ###################################################
        ### 비용 계산 ###
        input_token = cost_calculation(prompt)
        output_token = cost_calculation(summary_result)
        
        input_cost = input_token * (0.0001 / 1000)
        output_cost = output_token * (0.0001 / 1000)
        total_cost = input_cost + output_cost
        ###################################################
        
        ###################################################
        ### 글자 수 계산 ###
        count = len(summary_result.replace(' ', ''))
        # print(f'글자 수 : {count}')
        ###################################################
        
        if self.proof_name == 'yes':
            proof_result, p_total_cost = self.proofreader(summary_result, article)
            ### 비용 계산 ###
            total_cost = total_cost + p_total_cost
        elif self.proof_name == 'no':
            proof_result = '요약 교정을 선택하지 않았습니다.'
        
        return summary_result, proof_result, count, total_cost
        
    def proofreader(self, summary, article):
        # Data Preprocessing
        summary = remove_newlines(summary)
        article = remove_newlines(article)
        
        # Prompt
        prompt_form = Prompts.bard_proof
        input_format = {'summary' : summary, 'article' : article}
        
        prompt = completed_prompt(prompt_form=prompt_form,
                                  input_format=input_format)
        
        # Predict
        response = self.model.predict(prompt,
                                      max_output_tokens=1024,
                                      temperature=0.0,
                                      top_k=40,
                                      top_p=0.8,
                                      candidate_count=1)
        proof_result = response.text
        
        # Test Print
        # print(f"Response from Model: {response}")
        
        ###################################################
        ### 비용 계산 ###
        input_token = cost_calculation(prompt)
        output_token = cost_calculation(proof_result)
        
        input_cost = input_token * (0.0001 / 1000)
        output_cost = output_token * (0.0001 / 1000)
        total_cost = input_cost + output_cost
        ###################################################
        
        return proof_result, total_cost
        
