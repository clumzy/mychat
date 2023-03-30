import customtkinter

from .Chat import Chat
from .Chatbot import Chatbot

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .App import App

class Tabs(customtkinter.CTkTabview):
    def __init__(self, master:"App", **kwargs):
        super().__init__(master, **kwargs)
        self._tabs = {}
        self.grid(row=0, column=0, columnspan=1, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.create_chat()

    @property
    def current_tab(self):
        return self._tabs[self.get()]

    @property
    def num_tabs(self):
        return len(self._tabs)

    def create_chat(self, goto=True):
        tab_name = str(self.num_tabs + 1)
        print(tab_name)
        self.add(tab_name)
        chat = Chat(
            master=self.tab(tab_name),
            chatbot=Chatbot())
        self._tabs[tab_name] = chat
        if goto: self.set(tab_name)
        