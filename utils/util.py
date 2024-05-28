import re

def remove_newlines(serie):
    serie = serie.replace('<span class="highlighted">', '')
    serie = serie.replace('</span>', '')
    serie = serie.replace('<br>', ' ')
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


def remove_mac_specialsymbol(summary):
    symbol_pattern = re.compile(r"[\u001f\b]|&nbsp;")
    summary = symbol_pattern.sub(r" ", summary)
    return summary


def count_summary_char(summary):
    cleaned_summary = re.sub(r'<br>|[-\[\]].*?\]|-', '', summary)
    cleaned_summary = cleaned_summary.strip()
    return cleaned_summary
    
    
def cost_calculation(prompt_complet):
    '''
Returns the number of tokens in a text string.
Encodings specify how text is converted into tokens. Different models use different encodings.
cl100k_base : gpt-4, gpt-3.5-turbo, text-embedding-ada-002
p50k_base : Codex models, text-davinci-002, text-davinci-003
r50k_base(or gpt2) : GPT-3 models like davinci
    '''
    import tiktoken
    
    encoding = tiktoken.get_encoding('cl100k_base')
    num_tokens = len(encoding.encode(prompt_complet))
    
    return num_tokens


def completed_prompt(prompt_form, input_format):
    p = re.compile('(?<=\{)(.*?)(?=\})')
    tag_list = p.findall(prompt_form)
    
    prompt = prompt_form
    for key in input_format:
        if key in tag_list:
            tag = '{'+key+'}'
            prompt = prompt.replace(tag, input_format[key])
            
    return prompt


def importent_sentence(article, topic_article):
    p = re.compile('(?<=\<)(.*?)(?=\>)')
    tag_list = p.findall(topic_article)
    
    importent_article = article
    for tag in tag_list:
        importent_article = importent_article.replace('. ', '.<br/>')
        importent_article = importent_article.replace(tag, f'<span class="highlighted">{tag}</span>')
    
    return importent_article
# if __name__=='__main__':
#     p_c = '''
# ㅎ자ㅓㅓㅏ로ㅜ나ㅓㅇㄹ홎;홎;ㅐ호저홎;ㅐ허ㅗㅠㅍㅈ;ㅐㄱ호ㅠㅓㅈ'
# 해ㅓㅈ거ㅏㅗㅠㅎㅈ개ㅠㅈㄷ걓ㄷ게ㅑ혿개ㅔㅗㅎ
#     '''
#     cost_calculation(p_c)