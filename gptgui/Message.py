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
