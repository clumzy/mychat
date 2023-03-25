import os
import threading
import openai

from .Conversation import Conversation
from .Chatbot import Chatbot

class ChatInterface():
    def __init__(self, 
                 conversation:Conversation, 
                 chatbot:Chatbot):
        self._conversation:Conversation = conversation
        self._chatbot:Chatbot = chatbot
    
    def push_message(self, message: str,) -> None:
        self._conversation.draw_user_message(message)
        self._conversation.update()
        self._conversation._parent_canvas.yview_moveto(1.0)
        self._chatbot.add_user_prompt(prompt=message)

    def pull_response(self):
        print("Getting response...")
        answer_thread = threading.Thread(target=self.thread_pull_response, args=())
        answer_thread.start()

    def thread_pull_response(self, ):
        response = self._chatbot.return_answer()
        print("Response got !")
        self._chatbot.add_assistant_answer(response)
        self._conversation.draw_assistant_message(response)
        self._conversation.update()
        self._conversation._parent_canvas.yview_moveto(1.0)