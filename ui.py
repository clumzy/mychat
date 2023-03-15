import customtkinter

import chatbot

class PromptBox(customtkinter.CTkFrame):
    def __init__(self, master, chatbot_instance, *args):
        super().__init__(master, *args)
        super().__init__(master=master,*args)
        self.grid(row=1, column=0, columnspan=1, sticky="nsew")
        self.grid_rowconfigure((0,1),weight=1)
        self.grid_columnconfigure((0,1), weight=1)
        self._chatbot = chatbot_instance
        self.prompt = customtkinter.CTkTextbox(master=self, corner_radius=10,)
        self.prompt.grid(row=0, column=0, rowspan = 2)

        self.button = customtkinter.CTkButton(master=self, height=80, width=70, command=self.send_callback, text="Envoyer")
        self.button.grid(row=0, column=1)
        self.button1 = customtkinter.CTkButton(master=self, height=80, width=70, command=self.editor_callback, text="Editeur")
        self.button1.grid(row=1, column=1)

    def send_callback():
        pass

    def editor_callback():
        pass
        

class Message(customtkinter.CTkTextbox):
    def __init__(self, master, message, *args,):
        super().__init__(
            master=master,
            *args)
        self.insert("0.0", message)
        self.configure(state="disabled")
        
class AssistantMessage(Message):
    def __init__(self, master, message,*args,):
        super().__init__(master=master, message=message, *args)
        self.configure(
            fg_color="#eeeeee",
            text_color="#111111")

class UserMessage(Message):
    def __init__(self, master, message,*args,):
        super().__init__(master=master, message=message, * args)
        self.configure(
            fg_color="#eeeebb",
            text_color="#111111")

class Conversation(customtkinter.CTkScrollableFrame):
    def __init__(self, master, chatbot_instance,*args,):
        super().__init__(master=master,*args)
        self.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure((0), weight=1)
        self._chatbot = chatbot_instance
        self._message_boxes = []

    def add_assistant_message(self, message):
        ass_message = AssistantMessage(self, message)
        self._message_boxes.append(ass_message)
        ass_message.grid(row=len(self._message_boxes), column=0, sticky="ew")

    def add_user_message(self, message):
        user_message = UserMessage(self, message)
        self._message_boxes.append(user_message)
        user_message.grid(row=len(self._message_boxes), column=0, sticky="ew")



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("300x500")
        self.title("small example app")
        self.minsize(300, 500)

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0), weight=1)

        self.chatbot = chatbot.Chatbot()

        self.conversation_ui = Conversation(master=self, chatbot_instance=self.chatbot)
        self.chat_ui = PromptBox(master=self, chatbot_instance=self.chatbot)

if __name__ == "__main__":
    app = App()
    app.mainloop()