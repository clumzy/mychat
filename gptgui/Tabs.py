import customtkinter

from .Chat import Chat
from.Chatbot import Chatbot

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .App import App

class Tabs(customtkinter.CTkTabview):
    def __init__(self, master:"App", **kwargs):
        super().__init__(master, **kwargs)
        self.master:"App" = master
        self._tabs:dict[str,Chat] = {}
        self.grid(row=0, column=0, columnspan=1, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self._token_button = self.master.prompt_ui.token_button
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
        self._tabs[tab_name] = Chat(
            master=self.tab(tab_name),
            chatbot=Chatbot(),
            button_callback = self._token_button)
        if goto: self.set(tab_name)

    def delete_chat(self):
        old_tab = self._tabs.pop(self.get())
        self.delete(self.get())
        old_tab.destroy()