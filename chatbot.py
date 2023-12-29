from gpt_Chatbot_function import Chatbot
import random
import time
from voice import speech
import csv

conversation = []
chatgpt = Chatbot()
vo = speech()


#학생 정보 입력
student_id = { '이름': '이현우', '성격': '호기심이 많음, 유머를 좋아함, 질문을 많이 함' , '학년' : '초등학교 4학년', '성취도' : '중위권'} 
chatgpt.role('너는 공부를 도와주는 친근한 선생님이야')
chatgpt.learn('나의 정보'+ str(student_id))


# 성취기준 호출 
f = open('교과목 성취기준 및 평가기준 파일.CSV','r') 
reader = csv.reader(f)
curri = list(reader)


#오늘 배운 교과코드 
study_today = curri[random.randrange(1,3)][9]

arr_lo = [0,9]
for n in range(len(curri)):
    if curri[n][9] == study_today:
        arr_lo[0]=n

# 해당 교과 코드 행 정보 추출
study_now = curri[arr_lo[0]]
print(study_now)

# 교과 정보 및 세부 내용 전달
pedback_rubric = "교과: " + study_now[0] + '\n단원: ' + study_now[3] + '\n성취 기준 학년:' + study_now[2] + '\n성취 기준: '+ study_now[5] + '\n성취기준 해설:' + study_now[6] + '\n성취기준 적용시 고려사항: ' +study_now[7]+ '\n해당 내용 키워드: ' +study_now[8]+ '평가기준:'+study_now[15]
print(pedback_rubric)
chatgpt.learn('오늘 배운 내용:'+ study_now[10])
chatgpt.learn('오늘 배운 내용에 대한 세부 정보\n'+ pedback_rubric + '을 기준으로 질문과 답을 해')

print('전달완료')
       





#첫 대화 시작
question = chatgpt.ask('나에게 오늘 배운 내용을 확인할 수 있는 질문을 하나 해줘. 되도록 ?로 끝나게 질문해줘. 질문은 하나씩만')
print(question)
vo.speak(question)


talk_count = 0
today_ach = 1
now_level = 4


# 오늘 배운 내용으로 chatbot과 상호작용
while talk_count < 3:
    message = vo.hear()
    talk_count += 1

    if message != None:
        if '그만' in message:
            print('종료합니다')
            break
        print('나:', message)
        chatgpt.learn(message)
        #gpt 답변 횟수 제한으로 시간 조절
        time.sleep(6)

        if '궁금' in message or '뭐야' in message:
            print(0)
            response = chatgpt.ask('오늘 배운 내용과 별개로'+ message)
            talk_count -=1
            print(response)
            vo.speak(response)
        elif'모르' in message or'몰라' in message:
            print(5)
            if talk_count == 3:
                print('오늘 배운 내용을 다시 학습해볼까요 [학습자료]')
            else:
                response = chatgpt.ask('오늘 배운 내용을 잘 모르겠어. 오늘 배운 내용을 다시 설명해줘. 그리고 다시 질문해줘')
            print(response)
            vo.speak(response)
        else:
            response = chatgpt.ask('내 답변을 이해할 수 없다면 no라고 말해줘. no로만')
            if 'no' in response or 'No' in response:
                print(response)
                response = '답변을 이해하지 못했어요. 다시 말해주세요 \n 다시 질문할게요' + question
                print(response)
                vo.speak(response)
                talk_count -=1
            else:            
                response = chatgpt.ask( message + '가 질문에 대한 답으로 상, 중, 하 중에 어디에 해당한다고 생각해? 평가기준을 기준으로 답해줘. 상, 중, 하 하나로만 답해줘. ')
                print(response)
                if response != None:
                    if '상' in response:
                        print(1)
                        talk_count =3
                        response = chatgpt.ask('그러면 답변에 대해 긍정적인 피드백을 줘')
                        now_level = 1
                    elif '중' in response:
                        print(2)
                        talk_count +=1
                        response = chatgpt.ask('짧은 피드백과 함께, 오늘 배운 내용을 다시 확인할 수 있는 질문을 해줘')
                        now_level = 2
                        
                    else:
                        print(3)
                        if talk_count == 1:
                            response = chatgpt.ask('답변에 대한 짧은 피드백과 함께, 내가 더 답변하기 쉽도록 질문을 다시 해줘')
                            today_ach -=0.1
                        elif talk_count ==2:
                            response = chatgpt.ask('오늘 배운 내용을 간략하게 설명해주고, 다시 질문해줘')
                            today_ach -0.2
                        elif talk_count == 3:
                            response = '오늘 배운 내용을 다시 복습해볼까요?'
                            today_ach = -1
                print(response)
                vo.speak(response)

    else:
        print('다시 말해주세요')
        talk_count -=1
    
    print(talk_count)
    print(now_level)            

# 오늘 배운 내용과 관련된 다른 성취기준
next_study = study_now[12]
last_study = study_now[11]
related_study = study_now[13]
print(next_study, last_study, related_study)


# 앞선 대화 성취도에 따른 다음 학습 정보 

if now_level == 4:
    
    arr_lo = [0,4]
    for n in range(len(curri)):
        if curri[n][4] == last_study:
            arr_lo[0]=n

    # 해당 교과 코드 행 정보 추출
    study_next = curri[arr_lo[0]]
    print(study_next)

elif now_level == 3:
    study_next = study_now

elif now_level == 2:
    study_next = study_now
elif now_level == 1:

    arr_lo = [0,4]
    for n in range(len(curri)):
        if curri[n][4] == next_study:
            arr_lo[0]=n

    # 해당 교과 코드 행 정보 추출
    study_next = curri[arr_lo[0]]
    print(study_next)




study_next_detail = "교과: " + study_next[0] + '\n단원: ' + study_next[3] + '\n성취 기준 학년:' + study_next[2] + '\n성취 기준: '+ study_next[5] + '\n성취기준 해설:' + study_next[6] + '\n성취기준 적용시 고려사항: ' +study_next[7]+ '\n해당 내용 키워드: ' +study_next[8]+ '평가기준:'+study_next[15]
print(study_next_detail)
chatgpt.learn('다음 추천 학습 내용:'+ study_next[10])
chatgpt.learn('다음 추천 학습 내용에 대한 세부 정보\n'+ study_next_detail + '을 기준으로 다음 학습을 할 수 있도록 도와줘')

#두번째 대화 시작
question = chatgpt.ask(' 다음 추천 학습 내용을 보고 다음 학습을 할 수 있도록 도와줘')
print(question)
vo.speak(question)
print('학습 콘텐츠 연결 [링크]')

talk_count = 0

while talk_count <3:
    print('두번째 대화루프')
    talk_count +=1
    message = vo.hear()
    talk_count += 1

    if message != None:
        if '그만' in message:
            print('종료합니다')
            break
        print('나:', message)
        chatgpt.learn(message)
        #gpt 답변 횟수 제한으로 시간 조절
        time.sleep(5)

        if '궁금' in message or '뭐야' in message:
            print(0)
            response = chatgpt.ask('오늘 배운 내용과 별개로'+ message)
            talk_count -=1
        else:
            response = chatgpt.ask(message)
        

        print(response)
        vo.speak(response)

    else:
        print('다시 말해주세요')
        talk_count -=1


arr_lo = [0,4]
for n in range(len(curri)):
    if curri[n][4] == related_study:
            arr_lo[0]=n

   
study_next = curri[arr_lo[0]]
print(study_next)

study_next_detail = "교과: " + study_next[0] + '\n단원: ' + study_next[3] + '\n성취 기준 학년:' + study_next[2] + '\n성취 기준: '+ study_next[5] + '\n성취기준 해설:' + study_next[6] + '\n성취기준 적용시 고려사항: ' +study_next[7]+ '\n해당 내용 키워드: ' +study_next[8]+ '평가기준:'+study_next[15]
print(study_next_detail)
chatgpt.learn('다음 추천 다른 교과 학습 내용:'+ study_next[10])
chatgpt.learn('다음 추천 학습 내용에 대한 세부 정보\n'+ study_next_detail + '을 기준으로 다음 학습을 하도록 유도해줘')

#세번째 대화 시작
question = chatgpt.ask('다음 추천 학습 내용을 보고 다음 학습으로 연결해줘')
print(question)
vo.speak(question)
a= '학습 콘텐츠 연결 [링크] 할까요?'


talk_count = 0

print(a)
vo.speak(a)


while talk_count <2:
    talk_count +=1
    message = vo.hear()
    talk_count += 1

    if message != None:
        if '그만' in message:
            print('종료합니다')
            break
        print('나:', message)
        chatgpt.learn(message)
        #gpt 답변 횟수 제한으로 시간 조절
        time.sleep(5)

        if '궁금' in message or '뭐야' in message:
            print(0)
            response = chatgpt.ask('오늘 배운 내용과 별개로'+ message)
            talk_count -=1
       
        else:
            response = chatgpt.ask(message)

        print(response)
        vo.speak(response)

    else:
        print('다시 말해주세요')
        talk_count -=1
