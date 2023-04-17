import customtkinter

import threading

from .Message import AssistantMessage, UserMessage
from .Chatbot import Chatbot

class Chat(customtkinter.CTkScrollableFrame):
    def __init__(
            self, 
            master:customtkinter.CTkFrame,
            chatbot:Chatbot,
            button_callback: customtkinter.CTkButton, 
            *args,):
        super().__init__(master=master,*args)
        self._master = master
        self.grid(row=0, column=0, sticky="nsew")
        self._master.grid_columnconfigure((0), weight=1)
        self._master.grid_rowconfigure((0), weight=1)
        self._message_boxes = []
        self.chatbot:Chatbot = chatbot
        self._button_callback = button_callback
        self._token_use = 0
        #CALLBACK POUR CHANGER L'AFFICHAGE DES TOKENS AU CHANGMENT D'ONGLET
        self.bind("<Visibility>", self._update_token_use)
        self._update_token_use(update_button=True)

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
        self.grid_columnconfigure(0, weight=1)

    def draw_assistant_message(self, message:str):
        self._draw_message(message, assistant=True)

    def draw_user_message(self, message:str):
        self._draw_message(message, assistant=False)

    def push_message(self, message: str,) -> None:
        self.draw_user_message(message)
        self.update()
        self._parent_canvas.yview_moveto(1.0)
        self.chatbot.add_user_prompt(prompt=message)
        self._update_token_use(update_button=True)

    def pull_response(self):
        print("Getting response...")
        answer_thread = threading.Thread(target=self._thread_pull_response, args=())
        answer_thread.start()

    def _thread_pull_response(self, ):
        response = self.chatbot.return_answer()
        print("Response got !")
        self.draw_assistant_message(response)
        self.update()
        self._parent_canvas.yview_moveto(1.0)
        self._update_token_use(update_button=True)

    def recap_chat(self,):
        print("Getting recap...")
        recap_thread = threading.Thread(target=self._thread_recap_chat, args=())
        recap_thread.start()
    
    def _thread_recap_chat(self, ):
        response = self.chatbot.return_recap()
        print("Recap got !")
        print(response)

    # CALLBACK POUR LE CHANGEMENT D'ONGLET
    def _update_token_use(self, event = None, update_button = True):
        token_thread = threading.Thread(target=self._thread_update_token_use, args=[update_button])
        token_thread.start()

    def _thread_update_token_use(self, update_button:bool):
        self._token_use = self.chatbot.num_tokens_from_messages()
        if update_button and self.winfo_viewable() == 1:
            self._button_callback.configure(
                text = str(4095 - self._token_use))