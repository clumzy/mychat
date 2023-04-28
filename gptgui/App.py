import customtkinter
from tkinterdnd2 import TkinterDnD

from .ui.Tabs import Tabs
from .ui.PromptBox import PromptBox

class App(customtkinter.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        # WINDOWS GEOMETRY
        self.geometry("300x500")
        self.title("Custom GPT")
        self.minsize(300, 500)
        # FONT
        # WIDGETS
        self.grid_rowconfigure((0), weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.prompt_ui:PromptBox = PromptBox(master=self)
        self.tabs_ui:Tabs = Tabs(master=self,)
