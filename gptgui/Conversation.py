import customtkinter

from .Message import AssistantMessage, UserMessage

class Conversation(customtkinter.CTkScrollableFrame):
    def __init__(self, master:customtkinter.CTk, *args,):
        super().__init__(master=master,*args)
        self.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure((0), weight=1)
        self._message_boxes = []

    def draw_assistant_message(self, message:str):
        ass_message = AssistantMessage(self, message)
        self._message_boxes.append(ass_message)
        ass_message.grid(
            row=len(self._message_boxes), 
            column=0, 
            sticky="ew",
            padx = 5,
            pady = 5)

    def draw_user_message(self, message:str):
        user_message = UserMessage(self, message)
        self._message_boxes.append(user_message)
        user_message.grid(
            row=len(self._message_boxes), 
            column=0, 
            sticky="ew",
            padx = 5,
            pady = 5,)