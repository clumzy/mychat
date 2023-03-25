import customtkinter
from .Chatbot import Chatbot
from .Conversation import Conversation
from .PromptBox import PromptBox
from .ChatInterface import ChatInterface

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("300x500")
        self.title("Custom GPT")
        self.minsize(300, 500)
        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0), weight=1)
        self.chatbot:Chatbot = Chatbot()
        self.conversation_ui:Conversation = Conversation(master=self)
        self.chat_ui:PromptBox = PromptBox(master=self)
        self.chat_interface:ChatInterface = ChatInterface(self.conversation_ui, self.chatbot)
