import customtkinter
from tkextrafont import Font

from .Tabs import Tabs
from .PromptBox import PromptBox

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # WINDOWS GEOMETRY
        self.geometry("300x500")
        self.title("Custom GPT")
        self.minsize(300, 500)
        # WIDGETS
        self.grid_rowconfigure((0), weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.prompt_ui:PromptBox = PromptBox(master=self)
        self.tabs_ui:Tabs = Tabs(master=self,)
