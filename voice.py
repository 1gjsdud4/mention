import speech_recognition as sr
from gtts import gTTS as gt 
import playsound
import os


class speech():
    def hear(self):
        r = sr.Recognizer()
        with sr.Microphone() as mic:
            print(11111111111111)
            audio = r.listen(mic)
            try:
                
                print(222222222222222)
                text = r.recognize_google(audio, language="ko-KR")
            except sr.UnknownValueError:
                text = None
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

        return text
    
    def speak(self, response):
        speech = gt(response, lang='ko')
        filename = 'gpt_response.mp3'
        os.remove(filename)
        speech.save(filename) 
        playsound.playsound(filename)
