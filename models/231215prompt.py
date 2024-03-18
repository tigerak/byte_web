# - 요약문이 풍부한 정보를 담을 수 있도록 article의 내용을 자세히 담아주세요.
# - article의 문장들에서 말하고자하는 뉘앙스를 잘 살려서 요약문을 생성하세요.
# - 블필요하거나 지협적인 내용들은 담지 마세요.
# - 본문의 어휘를 그대로 쓸 필요는 없습니다.
# - 요약문에 전문적인 용어가 들어가야 한다면, article에 그 용어에 대한 해설이 있을 경우, 요약문에 그 해설도 포함시켜주세요.
# - 만약 연결어나 조사의 쓰임이 요약문의 전체 맥락과 맞지 않는다면, 알맞은 연결어나 조사로 바꿔주세요.
# - 한 문장 안에 두 개의 구절이 서로 다른 내용일 경우 '-요,'를 통해 적절히 나눠주세요.
# - 문장들을 순서에 따라 매끄럽게 연결해주세요.
# - 수치를 함께 표시해주면 이해하기에 더욱 좋습니다.
# - 약자가 나온다면 원어 다음에 괄호안에 넣어 표현해주세요.
# - 비교할 때는 무엇과 비교하는지도 알려주세요.
# - 앞에서 언급되지 않은 주어나 목적어가 있다면 문장에 함께 표현해주세요.
# - 문장이 매끄럽게 쓰여졌는지 확인하고, 어색한 부분이 있다면 article의 맥락에 맞게 고쳐주세요.

# 아래 원문 기사의 article에서 topic을 뽑아주세요.
# 선택한 topic들을 관련도에 따라서 group으로 구분하세요.
# topic과 group은 1개 일 수도 있고, 여러개 일 수도 있습니다.
# 원문 기사의 title을 중심으로 topic과 group을 참고해서 '더욱 중요한 topic'들을 뽑아주세요.

# 원문 기사의 title을 중심으로 중요한 topic들을 뽑아주세요.

# - article의 사실을 최대한 왜곡 없이 전달해주세요.

# 당신은 지금부터 이 기사에 대해 아무런 배경지식이 없는 독자입니다.
# 경제 기자 요약문을 읽고 이해되지 않는 단어를 수식할 수 있는 말을 article에서 찾아 수정하세요.
# 그리고 무엇을 수정했는지 말해주세요. 

# 독자 수정 요약문이 200자를 넘는다면 위의 과정을 천천히 다시 한번 반복해봅시다.

# 독자 수정 요약문을 읽고 사건의 배경과 원인과 결과가 일관된 줄거리를 갖도록 수정하세요.
# article의 사실을 왜곡하지 마세요. 거짓말 하면 안돼요 !!

# - 만약 문장 전체의 주어, 목적어, 서술어의 관계가 전체 맥락과 맞지 않는다면, 문장에서 주어, 목적어, 서술어의 관계가 알맞게 되도록 수정해주세요.
class Prompts:
    topic_multi = '''
당신은 경제 전문 기자입니다.
지금부터 경제에 관심이 많은 독자들에게 긴 기사를 알기 쉽게 요약해주는 일을 할 것입니다.

아래 원문 기사의 main_article과 sub_article에서 topic을 뽑아주세요.
선택한 topic들을 관련도에 따라서 group으로 구분하세요.
topic과 group은 1개 일 수도 있고, 여러개 일 수도 있습니다.
원문 기사의 main_title과 sub_title을 중심으로 topic과 group을 참고하여 '더 중요한 topic'들을 뽑아주세요.

<Instructions>
- '더 중요한 topic'에 집중하여 200자 이하의 구체적인 3줄 요약문을 생성해야 합니다.
- main_title과 sub_title의 nuance를 잘 살려서 표현해주세요.
- 요약 과정에서 main_article과 sub_article의 nuance가 잘못 전달되지 않도록 천천히 생각하면서 요약하세요.
- 전문적인 용어가 사용되면 main_article과 sub_article에서 그 설명을 찾아 요약문에 추가하세요.
- 인과관계가 부족하지 않도록 충분한 내용을 담아주세요. 
- 수치를 함께 표시해주세요.
- 약자가 나온다면 원어 다음에 괄호안에 넣어 표현해주세요.
- 비교할 때는 무엇과 비교하는지도 알려주세요.
</Instructions>

원문 기사:
"""
main_title : {main_title}
main_article : {main_article}

sub_title : {sub_title}
sub_article : {sub_article}
"""

<style>
3줄 요약문을 만들 때, 한 문장이 끝나면 줄바꿈을 하여주십시오.
모든 문장 앞에는 '- '를 붙여주세요.
첫 번째 문장과 마지막 문장은 '-니다'로 자연스럽게 끝내주세요.
두 번째 문장은 '-데요' 혹은 '-는데요'로 자연스럽게 끝내주세요.
</style>

경제 기자 요약문이 200자를 넘는다면 위의 과정을 천천히 다시 한번 반복해봅시다.


당신은 지금부터 이 기사에 대해 아무런 배경 지식이 없는 독자입니다.
경제 기자 요약문을 읽고 이해되지 않는 부분이 있다면 main_article과 sub_article에서 그 배경을 찾아 내용을 추가하는 일을 할거에요.

구체적인 수치가 있다면 함께 추가하세요.
경제 기자 요약문을 절대 수정하지 마세요!! 배경 내용을 추가하는 일만 하세요.

독자 수정 요약문이 200자를 넘는다면 위의 과정을 반복하며 가장 불필요한 부분만 제거해주세요.
그리고 무엇을 추가했는지 말해주세요.


당신은 지금부터 신문사의 편집장입니다.
독자 수정 요약문을 읽고 사건의 배경과 원인과 결과가 일관된 줄거리를 갖도록 수정하는 일을 할거에요.

article의 핵심적인 내용이 빠지지 않도록 추가해주세요. 관련된 수치가 있다면 함께 추가하세요.
요약문이 풍부한 정보를 갖도록 article을 참조하여 사건의 원인과 결과를 추가하세요.
article을 참조하여 사실관계를 명확하게 파악할 수 있도록 내용을 수정하세요.
article의 맥락을 고려하여 인과관계에 맞게 내용을 수정하세요.
원인과 결과를 확실하게 말하세요.
중복되거나 불필요한 내용은 간략하게 수정하세요.
자연스러운 문장이 되도록 수정하세요.
명칭 바꾸지 마세요.
불필요한 어휘는 삭제하세요. 하지만 article의 맥락 상 필요한 어휘는 지우지 마세요!
요약문의 전체 맥락을 고려하여 접속사, 연결어, 조사를 올바르게 수정하세요.
article의 사실을 왜곡하지 마세요. 추측하지 마세요. 거짓말 하면 안돼요 !!
날짜를 추정하지 마세요.

편집장 수정 요약문이 200자를 넘는다면 가장 불필요한 부분을 제거하고 위의 과정을 반복하세요.
편집장 수정 요약문이 140자 미만이라면 article에서 사건의 원인과 결과를 추가하고 위 과정을 반복하세요.
그리고 무엇을 수정했는지 말해주세요.


당신은 지금부터 한국어 선생님입니다.
편집장 수정 요약문을 읽고 문장의 어색한 부분을 자연스럽게 수정하는 일을 할거에요.

편집장 수정 요약문의 내용을 축약하지 마세요!!! 문장의 배치만 자연스럽게 수정하세요.
이 때, 요약문의 첫 문장은 주어가 제일 처음 나오도록 수정하세요.
한 문장 안에 두 개의 구절이 서로 다른 내용일 경우 적절한 접속사나 연결어를 추가하세요.
article의 사실을 왜곡하지 마세요. 추측하지 마세요. 거짓말 하면 안돼요 !!
편집장 수정 요약문의 전체 문장 관계를 고려하여 조사를 수정하세요.
접속사나 연결어를 이유없이 수정, 삭제하지 마세요.
article의 맥락 상 불필요한 어휘는 지우세요.
문장의 어미를 문맥에 맞게 수정해주세요.
요약문 전체 문장의 관계를 고려하여 문장이 올바른 인과관계를 갖도록 수정하세요.
문장의 주어와 술어가 일치되도록 자연스럽게 수정하세요.
편집장 수정 요약문에 <style>을 무조건 확실하게 적용시키세요!

그리고 무엇을 수정했는지 말해주세요.


단계 별로 천천히 생각해봅시다.


topic & group & 더 중요한 topic & 경제 기자 요약문 & 독자 수정 요약문 & 편집장 수정 요약문 & 한국어 선생님 수정 요약문 & 수정 사항:
    '''
    
# 원인과 결과를 확실하게 말하세요.
# 중복되거나 불필요한 내용은 간략하게 수정하세요.
# 불필요한 어휘는 삭제하세요. 하지만 article의 맥락 상 필요한 어휘는 지우지 마세요!
# article의 맥락을 고려하여 상관관계에 맞게 내용을 수정하세요.

# 경제 기자 요약문을 절대 수정하지 마세요!! 
# 배경 내용을 추가하는 일만 하세요.


# article에서 가장 먼저 나오는 사건이 요약문에서도 제일 앞에 나오도록 수정하세요.

    topic_4 = '''
당신은 한국의 경제 전문 기자입니다.
지금부터 경제에 관심이 많은 한국 독자들에게 긴 기사를 알기 쉽게 요약해주는 일을 할 것입니다.

아래 원문 기사의 article에서 topic을 뽑아주세요.
선택한 topic들을 관련도에 따라서 group으로 구분하세요.
topic과 group은 1개 일 수도 있고, 여러개 일 수도 있습니다.
원문 기사의 title을 중심으로 topic과 group을 참고하여 '더 중요한 topic'들을 뽑아주세요.

'더 중요한 topic'에 집중하여 200자 내외의 구체적인 3줄 요약문을 생성해야 합니다.

<Instructions>
- 문어체 표현을 쉽게 읽을 수 있는 구어체 표현으로 길게 풀어서 설명하세요.
- title의 nuance를 잘 살려서 표현해주세요.
- article의 핵심적인 내용이 빠지지 않도록 추가하세요.
- 사건의 배경과 원인과 결과가 일관된 줄거리를 갖도록 요약하세요.
- article의 맥락을 고려하여 원인과 결과를 잘 파악할 수 있도록 요약하세요.
- article을 참조하여 시간의 변화를 잘 파악할 수 있게 요약하세요.
- 중복되거나 불필요한 내용은 간략하게 수정하세요. 
- 전문적인 용어가 사용되면 article에서 그 설명을 찾아 요약문에 추가하세요.
- 중요한 세부 사항과 종속절을 포함해서 완전한 문맥을 유지해주세요.
- 수치를 함께 표시해주세요.
- 약자가 나온다면 원어 다음에 괄호안에 넣어 표현해주세요.
- 비교할 때는 무엇과 비교하는지도 알려주세요.
- 완성된 요약문을 다시 읽어보고 요약문이 논리적인지 생각하며 위 과정을 천천히 반복하세요.
</Instructions>

원문 기사:
"""
title : {title}
article : {article}
"""

아직 <Style>을 적용하지 않습니다.
완성된 경제 기자 요약을 천천히 읽어보고 논리적으로 미흡한 부분이 있다면 위 과정을 천천히 반복하세요.
경제 기자 요약문이 200자를 넘는다면 위의 과정을 천천히 다시 한번 반복하며 가장 중요하지 않은 내용만 제거하세요.


당신은 지금부터 이 기사에 대해 아무런 배경 지식이 없는 독자입니다.
요약문만으로는 이해하기 힘든 사건이 있다면 사건의 발생 배경을 요약문에 추가하는 일을 할거에요.

경제 기자 요약문을 읽고 사건의 발생 배경이 있다면 article에서 찾아 추가하세요. 
구체적인 수치가 있다면 함께 추가하세요.
경제 기자 요약문에 논리적으로 배경 내용을 추가하는 일만 하세요.

독자 수정 요약문이 200자를 넘는다면 위의 과정을 천천히 반복하며 가장 중요하지 않은 내용만 제거하세요.


당신은 지금부터 경제 전문 신문사의 편집장입니다.
독자 수정 요약문을 읽고 사건의 배경과 원인과 결과가 일관된 줄거리를 갖도록 수정하는 일을 할거에요.

<1단계>
article의 핵심적인 내용이 빠지지 않도록 추가하세요. 관련된 수치가 있다면 함께 추가하세요.
article을 참조하여 사건의 결과와 원인, 배경 순서로 문장의 요소들을 재배치하세요.
article을 참조하여 시간의 변화를 잘 파악할 수 있게 내용을 수정하세요.
요약문만으로는 이해하기 힘든 내용이 있다면 article에서 그에 대한 자세한 원인을 찾아 추가하세요.
중복되거나 불필요한 내용은 간략하게 수정하세요. 
자연스러운 문장이 되도록 구절이나 어절의 위치를 변경하세요.
중요한 세부 사항과 종속절을 포함해서 완전한 문맥을 유지해주세요.
논리적으로 요약되도록 article과 비교하여 문장들을 수정하세요.
어휘를 수정할 때는 그 nuance가 달라지지 않도록 각별히 주의하세요. 이 작업은 무척 신중하게 이루어져야합니다.
article을 참조하여 이전 문장과 결이 다른 내용을 서술하는 문장은 필요하다면 첫머리에 접속사 등의 연결어를 추가하세요.
한 문장 안에 여러 개의 구절이 서로 결이 다른 내용을 서술할 경우, 구절 사이에 '-요,'를 이용하거나 접속사 등의 연결어를 추가하세요.
요약문의 전체 맥락을 고려하여 문장이 줄줄 늘어지지 않도록 접속사 등의 연결어를 추가하세요.
용어나 명칭을 바꾸지 마세요.
날짜를 추정하지 마세요.
수치 정보를 포함시키세요.
문어체 표현을 쉽게 읽을 수 있는 구어체 표현으로 길게 풀어서 수정하세요.
수정한 내용을 다시 읽어보고 요약문이 논리적인지 생각하며 위 과정을 천천히 반복하세요.
</1단계>
<2단계>
편집장 수정 요약문이 article의 사실관계를 명확하게 파악하고 있는지 확인하고 틀린 문장을 수정하세요. 
article의 사실과 다른 내용을 말하고 있다면 <1단계>의 모든 과정을 다시 한번 천천히 반복해봅시다.
<Style>을 적용하세요.
편집장 수정 요약문을 200자 이하의 구체적인 3문장 요약문으로 만들어야합니다.
편집장 수정 요약문이 200자를 넘는다면 200자 이하가 될 때까지 <1단계>의 과정을 천천히 반복하며 가장 중요하지 않은 내용부터 제거하세요.
편집장 수정 요약문이 140자 이하라면 <1단계>의 과정을 천천히 반복하며 사건의 결과와 원인과 배경을 추가하세요.
완성된 편집장 수정 요약문을 읽어보고 논리적으로 미흡한 부분이 있다면 <1단계>의 과정을 천천히 반복하세요.
</2단계>

완성된 편집장 수정 요약문을 읽어보고 논리적으로 미흡한 부분이 있다면 <1단계>의 과정을 천천히 반복하세요.
<Style>을 적용할 때 편집장 수정 요약문의 접속사나 접속 부사구를 절대 삭제하지 마세요.

편집장 수정 요약문을 천천히 읽어보고 25자 이하의 제목을 지어주세요. title과 article을 참고해도 됩니다.


당신은 지금부터 한국어 선생님입니다.
편집장 수정 요약문을 읽고 문장의 어색한 부분을 자연스럽게 수정하는 일을 할거에요.

편집장 수정 요약문의 내용을 제발 축약하지 마세요.
편집장 수정 요약문이 article의 사실관계를 명확하게 파악하고 있는지 확인하고 틀린 문장을 수정하세요.
article의 nuance를 명확하게 전달하십시오.
문장의 맥락을 고려하여 어절의 조사를 추가 및 수정하세요.
편집장 수정 요약문 문장 첫머리에 필요한 접속사나 연결어를 추가하세요.
편집장 수정 요약문의 접속사나 연결어는 꼭 필요할 때만 수정, 삭제하세요.
문장의 주어와 술어가 일치되도록 수정하세요.
문장의 어미를 문맥에 맞게 수정해주세요.
어휘를 수정, 추가할 때는 그 nuance가 달라지지 않도록 각별히 주의하세요.

<Style>
3줄 요약문을 만들 때, 한 문장이 끝나면 줄바꿈을 하여주십시오. 
이 때, 접속어나 접속 부사구를 절대 삭제하지 마세요.
모든 문장 앞에는 '- '를 붙여주세요.
첫 번째 문장과 마지막 문장은 '-니다'로 자연스럽게 끝내주세요.
두 번째 문장은 '-데요' 혹은 '-는데요'로 자연스럽게 끝내주세요.
</Style>

한국어 선생님 수정 요약문에 <Style>을 무조건 확실하게 적용시키세요!
<Style>을 적용할 때 편집장 수정 요약문의 접속사나 접속 부사구를 절대 삭제하지 마세요.
수정한 내용을 다시 읽어보고 논리적인 문장을 완성했는지 천천히 생각해보세요.

단계 별로 천천히 생각해봅시다.


당신은 지금부터 견습 기자입니다.
article에서 '더 중요한 topic'에 해당하는 문장을 모두 찾아 < >표시를 하고 알려주세요. 


더 중요한 topic & 요약문 제목 & 견습 기자가 < >표시를 한 부분 & 한국어 선생님 수정 요약문:
    '''
# & 경제 기자 요약문 & 독자 수정 요약문 & 편집장 수정 요약문 
# 독자 수정 요약문만 출력해주세요: // 무엇을 수정했는지 말하기 지우기
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
- 뽑아낸 토픽을 모두 사용하여, article을 200자 이내의 세 문장으로 만들어야합니다.
- 요약문이 풍부한 정보를 담을 수 있도록 각 토픽에 대한 내용을 자세히 담아주세요.
- 이해하기 어려울 것 같은 문장은 쉬운 어휘로 풀어서 서술해주세요.
- 약자가 나온다면 원어 다음에 괄호안에 넣어 표현해주세요.
- 각 문장마다 주술관계가 어색하지 않도록, 주어를 생략하지 마세요.
- 인과관계가 부족하지 않도록 충분한 내용을 담아주세요.  
- 비교할 때는 무엇과 비교하는지도 알려주세요.
- 수치를 함께 표시해주면 이해하기에 더욱 좋습니다.
- 만약 필요하다면, 원문 기사에 쓰여진 순서와 상관없이 요약문의 맥락에 따라 순서를 바꿔서 요약해도 좋습니다.
- 만약 필요하다면, 원문 기사에 쓰여진 어순과 상관없이 요약문의 맥락에 따라 어순을 바꿔서 요약해도 좋습니다.
- 불필요하게 중복된 내용이 있다면 수정해주세요.
- 필요 없는 연결어도 수정해주세요.
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

요약문이 200자를 넘는다면 위의 모든 과정을 천천히 다시 한번 반복해봅시다.

한 문장이 끝나면 줄바꿈을 하여주십시오.
모든 문장 앞에는 '- '를 붙여주세요.

첫 번째 문장과 마지막 문장은 '-니다'로 끝내주세요.
두 번째 문장은 '-데요'로 끝내주세요.

단계 별로 천천히 생각해봅시다.

3줄 요약문 & 수정된 요약문 & 마지막 수정 요약문:
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