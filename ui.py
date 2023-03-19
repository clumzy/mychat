import customtkinter

import chatbot

from time import sleep

class PromptBox(customtkinter.CTkFrame):
    def __init__(self, master:customtkinter.CTk, *args):
        super().__init__(master=master,*args)
        self.grid(row=1, column=0, sticky="nsew")
        self.grid_rowconfigure((0,1),weight=1)
        self.grid_columnconfigure((0), weight=1)
        self.grid_columnconfigure((1), weight=0)
        #ENVOYER
        self.button = customtkinter.CTkButton(
            master=self, 
            height=80, 
            width=70, 
            command=self.callback_send, 
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
            self.master.conversation_ui._parent_canvas.yview_moveto('1.0')
            self.master.chatbot.converse(msg, self)
        return 'break' #POUR EVITER QUE LE BOUTTON ENTREE SAUTE LA LIGNE

    def editor_callback(self):
        pass

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

class Conversation(customtkinter.CTkScrollableFrame):
    def __init__(self, master:customtkinter.CTk, *args,):
        super().__init__(master=master,*args)
        self.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure((0), weight=1)
        self._message_boxes = []

    def add_assistant_message(self, message):
        ass_message = AssistantMessage(self, message)
        self._message_boxes.append(ass_message)
        ass_message.grid(
            row=len(self._message_boxes), 
            column=0, 
            sticky="ew",
            padx = 5,
            pady = 5)

    def add_user_message(self, message):
        user_message = UserMessage(self, message)
        self._message_boxes.append(user_message)
        user_message.grid(
            row=len(self._message_boxes), 
            column=0, 
            sticky="ew",
            padx = 5,
            pady = 5,)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("300x500")
        self.title("Custom GPT")
        self.minsize(300, 500)
        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0), weight=1)
        self.chatbot = chatbot.Chatbot()
        self.conversation_ui = Conversation(master=self)
        self.chat_ui = PromptBox(master=self)

if __name__ == "__main__":
    app = App()
    app.mainloop()