import customtkinter

class Message(customtkinter.CTkLabel):
    def __init__(self, master:customtkinter.CTkScrollableFrame, text:str, *args,):
        super().__init__(
            master=master,
            text = text,
            corner_radius = 10,
            justify = "left",
            anchor="w",
            *args)
        self.bind(
            '<Configure>', 
            lambda e: self.configure(
                wraplength=self.winfo_width()-15))
        
class AssistantMessage(Message):
    def __init__(self, master:customtkinter.CTkScrollableFrame, text:str,*args,):
        super().__init__(master=master, text=text, *args)
        self.configure(
            fg_color="#eeeeee",
            text_color="#111111",)
            
class UserMessage(Message):
    def __init__(self, master:customtkinter.CTkScrollableFrame, text:str,*args,):
        super().__init__(master=master, text=text, * args)
        self.configure(
            fg_color="#eeeebb",
            text_color="#111111")

class Conversation(customtkinter.CTkScrollableFrame):
    def __init__(self, master:customtkinter.CTk, *args,):
        super().__init__(master=master,*args)
        self.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure((0), weight=1)
        self._message_boxes = []

    def add_assistant_message(self, message):
        ass_message = AssistantMessage(self, message)
        self._message_boxes.append(ass_message)
        ass_message.grid(
            row=len(self._message_boxes), 
            column=0, 
            sticky="ew",
            padx = 5,
            pady = 5)

    def add_user_message(self, message):
        user_message = UserMessage(self, message)
        self._message_boxes.append(user_message)
        user_message.grid(
            row=len(self._message_boxes), 
            column=0, 
            sticky="ew",
            padx = 5,
            pady = 5,)