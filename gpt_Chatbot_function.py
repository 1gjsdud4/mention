import openai

openai.api_key = '키'

class Chatbot():
    def __init__(self, model='gpt-3.5-turbo'):
        self.model = model
        self.messages = []

    def ask(self, question):
        self.messages.append(
            {'role' : 'user', 'content': question}
        )
        res = self.__ask__()
        return res
    
    def learn(self, learn):
        self.messages.append(
            {'role' : 'user', 'content': learn}
        )
    
    def __ask__(self):
        completion = openai.ChatCompletion.create(
            model = self.model,
            messages = self.messages
        )
        response = completion.choices[0].message['content']
        self.messages.append(
            {'role' : 'assistant', 'content' : response}
        )
        return response
    
    def show_messages(self):
        return self.messages
    
    def clear(self):
        self.messages.clear()

    def role(self,role):
        self.messages.append(
            {'role' : 'system', 'content': role}
        )

        
