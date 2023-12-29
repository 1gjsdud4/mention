from flask import Flask, render_template, request, redirect, url_for
from voice import speech
from gpt_Chatbot_function import Chatbot
import random
import time
import csv
from jinja2 import Environment
env = Environment()
env.globals.update(zip=zip)

app = Flask(__name__)

chatgpt = Chatbot()
vo = speech()

talk_count = 0
today_ach = 1
now_level = 4
a = 0
b=0

messages_me = []
gpt_say = []

# 학생 정보 입력
student_id = {'이름': '이현우', '성격': '호기심이 많음, 유머를 좋아함, 질문을 많이 함', '학년': '초등학교 4학년', '성취도': '중위권'}
chatgpt.role('너는 공부를 도와주는 친근한 선생님이야')
chatgpt.learn('나의 정보' + str(student_id))

# 성취기준 호출
f = open('교과목 성취기준 및 평가기준 파일.CSV', 'r')
reader = csv.reader(f)
curri = list(reader)

# 오늘 배운 교과코드
study_today = curri[random.randrange(1, 3)][9]

arr_lo = [0, 9]
for n in range(len(curri)):
    if curri[n][9] == study_today:
        arr_lo[0] = n

# 해당 교과 코드 행 정보 추출
study_now = curri[arr_lo[0]]
print(study_now)

next_study = study_now[12]
last_study = study_now[11]
related_study = study_now[13]

# 교과 정보 및 세부 내용 전달
pedback_rubric = "교과: " + study_now[0] + '\n단원: ' + study_now[3] + '\n성취 기준 학년:' + study_now[2] + '\n성취 기준: ' + study_now[
    5] + '\n성취기준 해설:' + study_now[6] + '\n성취기준 적용시 고려사항: ' + study_now[7] + '\n해당 내용 키워드: ' + study_now[
                    8] + '평가기준:' + study_now[15]
print(pedback_rubric)
chatgpt.learn('오늘 배운 내용:' + study_now[10])
chatgpt.learn('오늘 배운 내용에 대한 세부 정보\n' + pedback_rubric + '을 기준으로 질문과 답을 해')

print('전달완료')
# 첫 대화 시작
respose = chatgpt.ask('나에게 오늘 배운 내용을 확인할 수 있는 질문을 하나 해줘. 되도록 ?로 끝나게 질문해줘. 질문은 하나씩만')
print(respose)
question = respose

gpt_say.append(respose)

@app.route('/')
def logo():
    return render_template("main.html")


@app.route('/1')
def main():
    stu_speech = request.args.get('stu_speech', '녹음버튼을 누르고 말하세요')
    
    return render_template("chatview1.html",  messages_me=messages_me, gpt_say=gpt_say, stu_speech=stu_speech, zip = zip)


@app.route('/2', methods=['POST'])
def start_listening():
    stu_speech = vo.hear()
    return redirect(url_for('main', stu_speech=stu_speech))


@app.route('/3', methods=['POST'])
def gpt_generated():

    global talk_count
    global gpt_say
    global messages_me
    global question
    global now_level
    global next_study 
    global last_study 
    global related_study
    global a
    global b
    message = request.form.get('stu_speech')  # stu_speech 값을 가져옵니다.
    talk_count += 1
    if talk_count < 3:
        if message is not None:


            print('나:', message)
            messages_me.append(message)  # 사용자의 답변을 messages_me 리스트에 추가합니다.
            chatgpt.learn(message)
            time.sleep(10)

            if '궁금' in message or '뭐야' in message:
                response = chatgpt.ask('오늘 배운 내용과 별개로 ' + message)
                talk_count -= 1
                print(response)
                gpt_say.append(response)

            elif '모르' in message or '몰라' in message:
                if talk_count == 3:
                    response = '오늘 배운 내용을 다시 학습해볼까요? [학습자료]'
                else:
                    response = chatgpt.ask('오늘 배운 내용을 잘 모르겠어. 오늘 배운 내용을 다시 설명해줘. 그리고 다시 질문해줘')
                print(response)
                gpt_say.append(response)

            else:
                response = chatgpt.ask('내 답변을 이해할 수 없다면 no라고 말해줘. no로만')
                if 'no' in response or 'No' in response:
                    response = '답변을 이해하지 못했어요. 다시 말해주세요. \n다시 질문할게요 ' + question
                    print(response)
                    gpt_say.append(response)

                    talk_count -= 1
                else:
                    response = chatgpt.ask(
                        message + '가 질문에 대한 답으로 상, 중, 하 중에 어디에 해당한다고 생각해? 평가기준을 기준으로 답해줘. 상, 중, 하 하나로만 답해줘.')
                    print(response)
                    if response is not None:
                        if '상' in response:
                            talk_count = 3
                            response = chatgpt.ask('그러면 답변에 대해 긍정적인 피드백을 줘')
                            now_level = 1
                        elif '중' in response:
                            talk_count += 1
                            response = chatgpt.ask('짧은 피드백과 함께, 오늘 배운 내용을 다시 확인할 수 있는 질문을 해줘')
                            now_level = 2
                        else:
                            if talk_count == 1:
                                response = chatgpt.ask('답변에 대한 짧은 피드백과 함께, 내가 더 답변하기 쉽도록 질문을 다시 해줘')
                                today_ach -= 0.1
                            elif talk_count == 2:
                                response = chatgpt.ask('오늘 배운 내용을 간략하게 설명해주고, 다시 질문해줘')
                                today_ach -= 0.2
                            elif talk_count == 3:
                                response = '오늘 배운 내용을 다시 복습해볼까요?'
                                today_ach = -1
                    print(response)
                    gpt_say.append(response)

        else:
            response = '다시 말해주세요'
            talk_count -= 1
        vo.speak(response)

    return redirect(url_for('main', messages_me=messages_me, gpt_say=gpt_say))


@app.route('/add_message', methods=['POST'])
def add_message():
    stu_speech = request.form.get('stu_speech')  # stu_speech 값을 가져옵니다.
    messages_me.append(stu_speech)
    return redirect(url_for('main', messages_me = messages_me, stu_speech="녹음버튼을 누르고 말하세요"))


if __name__ == '__main__':
    app.run(debug=True)
