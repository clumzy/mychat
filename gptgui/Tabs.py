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
        if self.num_tabs == 0:
            tab_name = "Default"
        else:
            tab_name = None
            while tab_name == None or tab_name == '':
                name_dialog = customtkinter.CTkInputDialog(
                    text = "Nom du nouveau chat :",
                    title = "Nouveau chat")
                tab_name = name_dialog.get_input()
                if tab_name in self._tabs.keys(): tab_name = None
        self.add(tab_name)
        chat = Chat(
            master=self.tab(tab_name),
            chatbot=Chatbot())
        self._tabs[tab_name] = chat
        if goto: self.set(tab_name)

    def delete_chat(self):
        self._tabs.pop(self.get())
        self.delete(self.get())