import customtkinter

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .App import App

class PromptBox(customtkinter.CTkFrame):
    def __init__(self, master:"App", *args):
        self.master:"App" = master
        super().__init__(master=self.master,*args)
        self.grid(row=1, column=0, sticky="nsew")
        self.grid_rowconfigure((0,1),weight=1) # type: ignore
        self.grid_columnconfigure((0), weight=1)
        self.grid_columnconfigure((1), weight=0)
        #ENVOYER
        self.button = customtkinter.CTkButton(
            master=self, 
            height=80, 
            width=70, 
            command=self.callback_send, # type: ignore
            text="Envoyer")
        self.button.grid(
            row=0, 
            column=1,
            sticky = "ne",
            padx = (5,5))
        #COMMAND
        self.button1 = customtkinter.CTkButton(
            master=self, 
            width=70, 
            command=self.editor_callback, 
            text="Editeur",)
        self.button1.grid(
            row=1, 
            column=1,
            sticky = "ne",
            padx = (5,5),
            pady = (0,5))
        #PROMPTBOX
        self.prompt = customtkinter.CTkTextbox(
            master=self, 
            corner_radius=10,
            wrap = "word")
        self.prompt.grid(
            row=0, 
            column=0, 
            rowspan = 2, 
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
            self.master.conversation_ui.add_user_message(msg)
            self.master.conversation_ui.update()
            self.master.conversation_ui._parent_canvas.yview_moveto(1.0)
            self.master.chatbot.converse(msg, self)
        return 'break' #POUR EVITER QUE LE BOUTTON ENTREE SAUTE LA LIGNE

    def editor_callback(self):
        pass
    