import customtkinter

import threading

from .Message import AssistantMessage, UserMessage
from .Chatbot import Chatbot



from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Tabs import Tabs

class Chat(customtkinter.CTkScrollableFrame):
    def __init__(
            self, 
            master:customtkinter.CTkFrame,
            chatbot:Chatbot, 
            *args,):
        super().__init__(master=master,*args)
        self._master = master
        self.grid(row=0, column=0, sticky="nsew")
        self._master.grid_columnconfigure((0), weight=1)
        self._master.grid_rowconfigure((0), weight=1)
        self._message_boxes = []
        self._chatbot:Chatbot = chatbot

    def _draw_message(self, text:str, assistant=False):
        if assistant: message = AssistantMessage(self, text)
        else: message = UserMessage(self, text)
        self._message_boxes.append(message)
        message.grid(
            row=len(self._message_boxes), 
            column=0, 
            sticky="nsew",
            padx = 5,
            pady = 5)
        
        self.grid_columnconfigure(0, weight=2)
        #print(message.winfo_height())

    def draw_assistant_message(self, message:str):
        self._draw_message(message, assistant=True)

    def draw_user_message(self, message:str):
        self._draw_message(message, assistant=False)

    def push_message(self, message: str,) -> None:
        self.draw_user_message(message)
        self.update()
        self._parent_canvas.yview_moveto(1.0)
        self._chatbot.add_user_prompt(prompt=message)

    def pull_response(self):
        print("Getting response...")
        answer_thread = threading.Thread(target=self._thread_pull_response, args=())
        answer_thread.start()

    def _thread_pull_response(self, ):
        response = self._chatbot.return_answer()
        print("Response got !")
        self._chatbot.add_assistant_answer(response)
        self.draw_assistant_message(response)
        self.update()
        self._parent_canvas.yview_moveto(1.0)
        print(self._chatbot.num_tokens_from_messages())