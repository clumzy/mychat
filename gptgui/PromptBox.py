import customtkinter

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .App import App

class PromptBox(customtkinter.CTkFrame):
    def __init__(self, master:"App", *args):
        self.master:App = master
        super().__init__(
            master=self.master,
            *args)
        self.grid(row=1, column=0, sticky="sew")
        self.grid_rowconfigure((0,1),weight=1) # type: ignore
        self.grid_columnconfigure((0), weight=1)
        self.grid_columnconfigure((1), weight=0)
        #ENVOYER
        self.send_button = customtkinter.CTkButton(
            master=self, 
            height=40, 
            width=80, 
            command=self.callback_send, # type: ignore
            text="Envoyer")
        self.send_button.grid(
            row=0, 
            column=1,
            columnspan = 2,
            sticky = "nwe",
            padx = (5,5))
        #SOUVENIR
        self.memory_button = customtkinter.CTkButton(
            master=self,
            height=20, 
            width=80, 
            command=self.callback_editor, 
            text="Résumé",)
        self.memory_button.grid(
            row=1, 
            column=1,
            columnspan=2,
            sticky = "swe",
            padx = (5,5),
            pady = (0,5))
        #NOUVELLE CONV
        self.add_conv_button = customtkinter.CTkButton(
            master=self,
            height=20, 
            width=35, 
            command=self.callback_newtab, 
            text="+",
            fg_color="#54A75E",
            hover_color="#3A7641")
        self.add_conv_button.grid(
            row=2, 
            column=1,
            sticky = "sw",
            padx = (5,5),
            pady = (0,5))
        #SUPPRIMER CONV
        self.delete_button = customtkinter.CTkButton(
            master=self,
            height=20, 
            width=35, 
            command=self.callback_deltab, 
            text="X",
            fg_color="#B36262",
            hover_color="#874B4B")
        self.delete_button.grid(
            row=2, 
            column=2,
            sticky = "se",
            padx = (5,5),
            pady = (0,5))
        #PROMPTBOX
        self.prompt = customtkinter.CTkTextbox(
            master=self, 
            corner_radius=10,
            wrap = "word",
            height=120)
        self.prompt.grid(
            row=0, 
            column=0, 
            rowspan = 3, 
            sticky = "ew",
            padx = (5,0),
            pady = (0,5))
        self.prompt.bind("<Control-Return>",self.callback_send)

    def callback_send(self, *args):
        msg = self.prompt.get(0.0,4096.4096)
        if msg[-1] == "\n": msg = msg[:-1]
        if msg != "":
            self.prompt.delete(0.0,4096.4096)
            self.update()
            self.master.tabs_ui.current_tab.push_message(msg)
            self.master.tabs_ui.current_tab.pull_response()
        return 'break' #POUR EVITER QUE LE BOUTTON ENTREE SAUTE LA LIGNE

    def callback_editor(self):
        recap = str(self.master.tabs_ui.current_tab._chatbot)
        print(recap)

    def callback_newtab(self):
        self.master.tabs_ui.create_chat()

    def callback_deltab(self,):
        self.master.tabs_ui.delete_chat()
    