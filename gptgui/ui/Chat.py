import customtkinter

import threading

from .Message import AssistantMessage, UserMessage
from ..ai.Pipe import WitPipe

class Chat(customtkinter.CTkScrollableFrame):
    def __init__(
            self, 
            master:customtkinter.CTkFrame,
            pipe:WitPipe,
            button_callback: customtkinter.CTkButton, 
            *args,):
        super().__init__(master=master,*args)
        self._master = master
        self.grid(row=0, column=0, sticky="nsew")
        self._master.grid_columnconfigure((0), weight=1)
        self._master.grid_rowconfigure((0), weight=1)
        self._message_boxes = []
        self.pipe:WitPipe = pipe
        self._button_callback = button_callback
        #CALLBACK POUR CHANGER L'AFFICHAGE DES TOKENS AU CHANGMENT D'ONGLET
        self.bind("<Visibility>", self._update_token_use)

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
        self.pipe.add_user_prompt(prompt=message)

    def pull_response(self):
        answer_thread = threading.Thread(target=self._thread_pull_response, args=())
        answer_thread.start()

    def _thread_pull_response(self, ):
        response = self.pipe.return_answer()
        self.draw_assistant_message(response)
        self.update()
        self._parent_canvas.yview_moveto(1.0)
        self._update_token_use()

    # CALLBACK POUR LE CHANGEMENT D'ONGLET
    def _update_token_use(self, event = None):
        self._button_callback.configure(text=f"Send\n{self.pipe.token_use}")