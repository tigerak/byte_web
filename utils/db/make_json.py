import article

import re
import json
import hashlib

def remove_newlines(serie):
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

def dict2json(list_data):
    read_to_json = []
    for item in list_data:
        title = item['title']
        media = item['media']
        date = item['date']
        tag = item['tag']
        summary=item['summary']
        
        context = remove_newlines(item['context'])
        
        id = hashlib.sha256(context.encode('utf-8')).hexdigest()
                
        sample = {
            "data": [
                {
                    "doc_id": id,
                    "doc_title": title,
                    "doc_source": media,
                    "doc_published": date,
                    "doc_class": {
                        "class": "한국언론진흥재단 빅카인즈 뉴스기사",
                        "code": tag
                    },
                    "created": "20211217144113",
                    "paragraphs": [
                        {
                            "context": context,
                            "summary": summary,
                            "context_id": 579695
                        }
                    ]
                },
            ]
        }
        read_to_json.append(sample)
    return read_to_json


if __name__=='__main__':
    list_data = article.Article.byte_test
    
    read_to_json = dict2json(list_data)
    
    json_data = json.dumps(read_to_json)

    with open(r'D:\langchain\VDB_1\byte_test.json', 'w') as f:
        f.write(json_data)