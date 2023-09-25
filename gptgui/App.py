import customtkinter
from tkinterdnd2 import TkinterDnD

from .ui import Tabs
from .ui import PromptBox
from .ai import Memory

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
        self.memory = Memory(location="/Users/george.pied/Code/clumzy/mychat/memories")
        self.prompt_ui:PromptBox = PromptBox(master=self)
        self.tabs_ui:Tabs = Tabs(master=self,)
