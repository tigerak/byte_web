
# Let's change the summary into three sentences long enough to hold as much information as possible.
# If a single sentence cannot contain all the information, It's okay to make it into one long sentence composed of multiple sentence.
# At this time, you can increase the length of the sentence if necessary.
# I'll call this 'the final three lines summary' from now on

# If there are duplicates or similar content, delete statements of less importance.

class Prompts:
    all_3 = '''
I want you to act as a journalist specializing in economics who summarizes the article.
Please summarize the article below, in Korean. 
If necessary, the summary may be modified to suit the causal relationship regardless of the order of the original article.
If there is any overlap or similar content, please summarize it considering the overall context.

Please pick one of the most important topics from the article below and summarize it so that it does not exceed 250 characters, and make it three sentences.
At this point, summarize only what is relevant to the first sentence.
If there are duplicates or similar content, delete statements of less importance.
If the subject predicate relationship of the created sentence is not correct, it is okay to make the fourth sentence.

Now, please revise the summary compared to the original article.
Be particularly sensitive to correcting sentences so that the front and back relationships of the context fit well compared to the original article.
At this time, you can increase the length of the sentence if necessary.

Let's check again whether summary is well organized based on the original article and correct the wrong part.
Please check if the appropriate connecting words that conform to Korean grammar have been used, and if they sound awkward, make the sentence more natural by replacing them with suitable connecting words.
And You should modify it as naturally as possible to match the Korean word order.

This is the original article:
"""
{article}
"""

Let's step by step.

If the summary consists of more than 250 characters, let's slowly repeat the whole process step by step.

the best one SUMMARY:
        '''
    all_4 = '''
당신은 경제 전문 기자입니다.
지금부터 경제에 관심이 많은 독자들에게 긴 기사를 알기 쉽게 요약해주는 일을 할 것입니다.

- 아래 원문 기사의 article을 200자 정도의 세 문장으로 만들어야합니다.
- 요약문이 풍부한 정보를 담을 수 있도록 article의 내용을 자세히 담아주세요.
- 이해하기 어려울 것 같은 문장은 쉬운 어휘로 풀어서 서술해주세요.
- 각 문장마다 주술관계가 어색하지 않도록, 주어를 생략하지 마세요.
- 인과관계가 부족하지 않도록 충분한 내용을 담아주세요. 
- 수치를 함께 표시해주면 이해하기에 더욱 좋습니다.
- 만약 필요하다면, 원문 기사에 쓰여진 순서와 상관없이 요약문의 맥락에 따라 순서를 바꿔서 요약해도 좋습니다.
- 만약 필요하다면, 원문 기사에 쓰여진 어순과 상관없이 요약문의 맥락에 따라 어순을 바꿔서 요약해도 좋습니다.
- 요약문이 인과관계에 맞는지 확인해보고, 어색한 부분이 있다면 article의 맥락에 맞게 고쳐주세요.
- 만들어진 문장의 주어 술어 관계가 맞지 않으면 네 번째 문장을 만들어도 무방합니다.
- 원문 기사와 비교했을 때, 요약문의 각 문장이 주술관계가 명확해지도록 문장을 교정하십시오. 
- 문장이 매끄럽게 쓰여졌는지 확인하고, 어색한 부분이 있다면 article의 맥락에 맞게 고쳐주세요.

요약문이 원문 기사를 완벽하게 요약했다고 판단 될 때까지 위의 모든 과정을 단계 별로 천천히 반복해봅시다. 

원문 기사:
"""
{article}
"""

만약 '교정 된 요약문'이 200자 이하라면 위의 과정을 천천히 단계 별로 다시 한번 생각해봅시다. 

한 문장이 끝나면 줄바꿈을 하여주십시오.
모든 문장 앞에는 '- '를 붙여주세요.

첫 번째 문장과 마지막 문장은 '-니다'로 끝내주세요.
두 번째 문장은 '-데요'로 끝내주세요.

단계 별로 천천히 생각해봅시다.

요약문:
        '''
    line_3 = '''
I want you to act as a journalist specializing in economics who summarizes the article.
Please summarize the article below, in Korean. 
If necessary, the summary may be modified to suit the causal relationship regardless of the order of the original article.
If there is any overlap or similar content, please summarize it considering the overall context.

Please make a summary of the article below in three sentences so that it does not exceed 250 characters.
At this time, only the contents related to the first sentence of the summary are summarized.
If the subject predicate relationship of the made sentence is not correct, it is okay to make a fourth sentence.

Now, please revise the summary compared to the original article.
Be particularly sensitive to correcting sentences so that the front and back relationships of the context fit well compared to the original article.
At this time, you can increase the length of the sentence if necessary.

This is the original article:
"""
{article}
"""

Let's check again whether the summary is well organized based on the original article and correct the wrong part.
Please check if the appropriate connecting words that conform to Korean grammar have been used, and if they sound awkward, make the sentence more natural by replacing them with suitable connecting words.
And You should modify it as naturally as possible to match the Korean word order.

If the summary consists of more than 250 characters, let's slowly repeat the whole process step by step.

Let's step by step.

the best one SUMMARY:
        '''
    line_4 = '''
당신은 경제 전문 기자입니다.
지금부터 경제에 관심이 많은 독자들에게 긴 기사를 알기 쉽게 요약해주는 일을 할 것입니다.

- 아래 원문 기사의 atricle에서 가장 중요한 토픽을 하나 뽑아내세요. 토픽은 안 보여줘도 돼요.
- 뽑아낸 토픽을 사용하여, article을 200자 정도의 세 문장으로 만들어야합니다.
- 요약문이 풍부한 정보를 담을 수 있도록 요약문의 첫번째 문장에 대한 내용을 두 번째와 세 번째 문장에서 자세히 서술해주세요.
- 이해하기 어려울 것 같은 문장은 쉬운 어휘로 풀어서 서술해주세요.
- 각 문장마다 주술관계가 어색하지 않도록, 주어를 생략하지 마세요.
- 인과관계가 부족하지 않도록 충분한 내용을 담아주세요.  
- 수치를 함께 표시해주면 이해하기에 더욱 좋습니다.
- 만약 필요하다면, 원문 기사에 쓰여진 순서와 상관없이 요약문의 맥락에 따라 순서를 바꿔서 요약해도 좋습니다.
- 만약 필요하다면, 원문 기사에 쓰여진 어순과 상관없이 요약문의 맥락에 따라 어순을 바꿔서 요약해도 좋습니다.
- 요약문이 인과관계에 맞는지 확인해보고, 어색한 부분이 있다면 article의 맥락에 맞게 고쳐주세요.
- 만들어진 문장의 주어 술어 관계가 맞지 않으면 네 번째 문장을 만들어도 무방합니다.
- 원문 기사와 비교했을 때, 요약문의 각 문장이 주술관계가 명확해지도록 문장을 교정하십시오. 
- 문장이 매끄럽게 쓰여졌는지 확인하고, 어색한 부분이 있다면 article의 맥락에 맞게 고쳐주세요.

요약문이 원문 기사를 완벽하게 요약했다고 판단 될 때까지 위의 모든 과정을 단계 별로 천천히 반복해봅시다. 

원문 기사:
"""
{article}
"""

만약 요약문이 200자 이하면 위의 과정을 천천히 단계 별로 다시 한번 생각해봅시다. 

한 문장이 끝나면 줄바꿈을 하여주십시오.
모든 문장 앞에는 '- '를 붙여주세요.

첫 번째 문장과 마지막 문장은 '-니다'로 끝내주세요.
두 번째 문장은 '-데요'로 끝내주세요.

문장들이 자연스럽고 매끄러워지도록 문맥에 맞게 연결어를 수정하거나 제거해주세요.

단계 별로 천천히 생각해봅시다.

요약문:
        '''
    title_3 = '''
I want you to act as a journalist specializing in economics who summarizes the article.
Please summarize the article below, in Korean. 
If necessary, the summary may be modified to suit the causal relationship regardless of the order of the original article.
If there is any overlap or similar content, please summarize it considering the overall context.

Choose a content that is highly related to the title from the original article below and summarize it into 3 sentences so that it does not exceed 250 characters.
If the subject predicate relationship of the created sentence is not correct, it is okay to make the fourth sentence.

Now, please revise the summary compared to the original article.
Be particularly sensitive to correcting sentences so that the front and back relationships of the context fit well compared to the original article.
At this time, you can increase the length of the sentence if necessary.

Let's check again whether the summary is well organized based on the original article and correct the wrong part.
Please check if the appropriate connecting words that conform to Korean grammar have been used, and if they sound awkward, make the sentence more natural by replacing them with suitable connecting words.
And You should modify it as naturally as possible to match the Korean word order.

This is the original article:
"""
{title}
{article}
"""

Let's step by step.

If the summary consists of more than 250 characters, let's slowly repeat the whole process step by step.

the best one SUMMARY:
        '''
    title_4 = '''
당신은 경제 전문 기자입니다.
지금부터 경제에 관심이 많은 독자들에게 긴 기사를 알기 쉽게 요약해주는 일을 할 것입니다. 

- 아래 원문 기사의 title에서 3개 이하의 토픽을 뽑아내세요. 토픽은 안 보여줘도 돼요.
- 뽑아낸 토픽을 모두 사용하여, article을 200자 정도의 세 문장으로 만들어야합니다.
- 요약문이 풍부한 정보를 담을 수 있도록 각 토픽에 대한 내용을 자세히 담아주세요.
- 이해하기 어려울 것 같은 문장은 쉬운 어휘로 풀어서 서술해주세요.
- 각 문장마다 주술관계가 어색하지 않도록, 주어를 생략하지 마세요.
- 인과관계가 부족하지 않도록 충분한 내용을 담아주세요.  
- 수치를 함께 표시해주면 이해하기에 더욱 좋습니다.
- 만약 필요하다면, 원문 기사에 쓰여진 순서와 상관없이 요약문의 맥락에 따라 순서를 바꿔서 요약해도 좋습니다.
- 만약 필요하다면, 원문 기사에 쓰여진 어순과 상관없이 요약문의 맥락에 따라 어순을 바꿔서 요약해도 좋습니다.
- 요약문이 인과관계에 맞는지 확인해보고, 어색한 부분이 있다면 article의 맥락에 맞게 고쳐주세요.
- 만들어진 문장의 주어 술어 관계가 맞지 않으면 네 번째 문장을 만들어도 무방합니다.
- 요약문의 각 문장이 주술관계가 명확해지도록, article의 맥락에 맞춰 문장을 교정하십시오. 
- 문장이 매끄럽게 쓰여졌는지 확인하고, 어색한 부분이 있다면 article의 맥락에 맞게 고쳐주세요.

요약문이 원문 기사를 완벽하게 요약했다고 판단 될 때까지 위의 모든 과정을 단계 별로 천천히 반복해봅시다. 

원문 기사:
"""
{title}
{article}
"""

만약 요약문이 200자 이하라면 위의 과정을 천천히 단계 별로 다시 한번 생각해봅시다. 

한 문장이 끝나면 줄바꿈을 하여주십시오.
모든 문장 앞에는 '- '를 붙여주세요.

첫 번째 문장과 마지막 문장은 '-니다'로 끝내주세요.
두 번째 문장은 '-데요'로 끝내주세요.

단계 별로 천천히 생각해봅시다.

요약문:
        '''
    proof_3 = '''
You are an expert fact checker. You have been hired by a major news organization to fact check a very important story.
Please answer in Korean.

Look for errors in the summary compared to the original article.
Be especially sensitive to numbers or spelling.
Don't make a assumption. If the numbers are different, it is wrong.
Be sensitive to small differences in words.

For each sentence, determine whether true or false, and output "Understood" if you cannot determine whether the sentence is true or false.
If the summary is false or undecided, explain why.
Please answer in Korean.

This is the original article:
"""
{article}
"""

And, Here is a summary of the article:
"""
{summary}
"""

Let's think step by step.

ANSWER:
'''
    proof_4 = '''
당신은 사실 확인 전문가입니다.
기사와 요약문 사이에 틀린 부분이 있는지 찾아내야 합니다.

숫자나 철자에 특히 민감하게 반응하세요.
추측하지 마세요. 숫자가 다르면 틀린 거예요.
말의 작은 차이에도 민감하게 반응하세요.

각 문장에 대해서 '참'인지 '거짓'인지 판단하고, 참인지 거짓인지 판단할 수 없을 때는 '판단할 수 없음'이라고 대답해주세요.
만약 '거짓'이거나 '판단할 수 없음'인 경우, 그 이유를 함께 설명해주세요.

아래 요약문을 기사와 비교하여 틀린 부분이 있다면 찾아주세요.

요약문:
"""
{summary}
"""

기사:
"""
{article}
"""

단계별로 천천히 생각해봅시다.

대답:
'''
    bard_all = '''    
당신은 경제 전문 기자입니다.
당신은 독자들이 기사 내용을 쉽게 파악할 수 있도록 기사를 요약하는 일을 하게 됩니다.
아래 뉴스 기사를 200자 내외의 3줄 요약문으로 바꿔주세요. 

<뉴스 기사>{article}</뉴스 기사>

모든 문장 앞에는 '- '를 붙여주세요.

첫 번째 문장과 마지막 문장은 '-니다'로 끝내주세요.
두 번째 문장은 '-데요'로 끝내주세요.
'''
    bard_line = '''    
당신은 경제 전문 기자입니다.
당신은 독자들이 기사 내용을 쉽게 파악할 수 있도록 기사를 요약하는 일을 하게 됩니다.

아래 뉴스 기사를 200자 내외의 3줄 요약문으로 바꿀 예정입니다.
3줄 요약문의 첫번째 줄에 들어간 정보와 관련 깊은 내용들로 두번째 줄과 세번째 줄을 만들어주세요.

<뉴스 기사>{article}</뉴스 기사>

모든 문장 앞에는 '- '를 붙여주세요.

첫 번째 문장과 마지막 문장은 '-니다'로 끝내주세요.
두 번째 문장은 '-데요'로 끝내주세요.
'''
    bard_title = '''    
당신은 경제 전문 기자입니다.
당신은 독자들이 기사 내용을 쉽게 파악할 수 있도록 기사를 요약하는 일을 하게 됩니다.

1. <title>에서 3개 이하의 토픽을 선택하세요.
2. 선택한 토픽을 포함하여 <article>을 200자 정도 분량의 3줄로 요약하세요.
3. 요약문이 풍부한 정보를 담을 수 있도록 각 토픽에 대해서 자세히 요약해주세요.
4. 기사 내부의 지식을 최대한 많이 가져와서 요약해주세요.

<title>{title}</title>
<article>{article}</article>

모든 문장 앞에는 '- '를 붙여주세요.

첫 번째 문장과 마지막 문장은 '-니다'로 끝내주세요.
두 번째 문장은 '-데요'로 끝내주세요.
'''
    bard_proof = '''
당신은 사실 확인 전문가입니다.
뉴스 기사와 요약문 사이에 틀린 부분이 있는지 찾아내야 합니다.

각 문장에 대해서 '참'인지 '거짓'인지 판단하고, 참인지 거짓인지 판단할 수 없을 때는 '판단할 수 없음'이라고 대답해주세요.
만약 '거짓'이거나 '판단할 수 없음'인 경우, 그 이유를 함께 설명해주세요.

아래 요약문을 기사와 비교하여 틀린 부분이 있다면 찾아주세요.

<요약문>{summary}</요약문>

<뉴스 기사>{article}</뉴스 기사>
    '''