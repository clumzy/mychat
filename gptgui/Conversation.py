import customtkinter

from .Message import AssistantMessage, UserMessage

class Chat(customtkinter.CTkScrollableFrame):
    def __init__(self, master:customtkinter.CTk, *args,):
        super().__init__(master=master,*args)
        self.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure((0), weight=1)
        self._message_boxes = []

    def _draw_message(self, text:str, assistant=False):
        if assistant: message = AssistantMessage(self, text)
        else: message = UserMessage(self, text)
        self._message_boxes.append(message)
        message.grid(
            row=len(self._message_boxes), 
            column=0, 
            sticky="ew",
            padx = 5,
            pady = 5)
        #print(message.winfo_height())

    def draw_assistant_message(self, message:str):
        self._draw_message(message, assistant=True)

    def draw_user_message(self, message:str):
        self._draw_message(message, assistant=False)