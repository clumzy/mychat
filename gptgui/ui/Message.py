import customtkinter
from platform import platform

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Chat import Chat

class Message(customtkinter.CTkTextbox):
    def __init__(self, master:"Chat", text:str, *args,):
        super().__init__(
            master=master,
            wrap="word",
            padx = 0,
            pady = 0,
            *args)
        self.insert("0.0",text=text)
        self.configure(state="disabled")
        self.bind("<Configure>", self._resize)
        
    def _resize(self, event):
        self._lines:int = self._textbox.count("1.0", "end", "displaylines")[0]
        if platform() == "Windows":
            line_height = 15
        else:
            line_height = 16
        self.configure(height = 15 + self._lines*line_height)

class AssistantMessage(Message):
    def __init__(self, master:"Chat", text:str,*args,):
        super().__init__(master=master, text=text, *args)
        self.configure(
            fg_color="#eeeeee",
            text_color="#111111",)
            
class UserMessage(Message):
    def __init__(self, master:"Chat", text:str,*args,):
        super().__init__(master=master, text=text, * args)
        self.configure(
            fg_color="#eeeebb",
            text_color="#111111")
        
class SystemMessage(Message):
    def __init__(self, master:"Chat", text:str,*args,):
        super().__init__(master=master, text=text, * args)
        self.configure(
            fg_color="#bbbbee",
            text_color="#fafafaf")
