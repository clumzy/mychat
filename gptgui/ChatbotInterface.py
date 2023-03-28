import threading

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Chat import Chat
    from .Chatbot import Chatbot

class ChatbotInterface():
    def __init__(self, 
                 chat:"Chat", 
                 chatbot:"Chatbot"):
        self._chat:"Chat" = chat
        self._chatbot:"Chatbot" = chatbot
    
    def push_message(self, message: str,) -> None:
        self._chat.draw_user_message(message)
        self._chat.update()
        self._chat._parent_canvas.yview_moveto(1.0)
        self._chatbot.add_user_prompt(prompt=message)

    def pull_response(self):
        print("Getting response...")
        answer_thread = threading.Thread(target=self.thread_pull_response, args=())
        answer_thread.start()

    def thread_pull_response(self, ):
        response = self._chatbot.return_answer()
        print("Response got !")
        self._chatbot.add_assistant_answer(response)
        self._chat.draw_assistant_message(response)
        self._chat.update()
        self._chat._parent_canvas.yview_moveto(1.0)