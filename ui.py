import customtkinter

import main

class Conversation(customtkinter.CTkScrollableFrame):
    def __init__(self, chatbot,*args,):
        super().__init__()
        self.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        self.scrollable_frame.grid_rowconfigure(0,weight=1)
        self.scrollable_frame.grid_columnconfigure((0), weight=1)
        self._chatbot = chatbot
        self._chatbot.register_window(self)
        self._message_boxes = []

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("300x500")
        self.title("small example app")
        self.minsize(300, 500)

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.scrollable_frame = customtkinter.CTkScrollableFrame(master=self, width=200, height=200)
        self.scrollable_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        self.scrollable_frame.grid_rowconfigure(0,weight=1)
        self.scrollable_frame.grid_columnconfigure((0), weight=1)

        self.textbox = customtkinter.CTkTextbox(master=self.scrollable_frame, corner_radius=20,)
        self.textbox.grid(row=0, column=0, sticky="ew")
        st = "Test."
        self.textbox.insert("0.0", st)
        self.textbox.configure(state="disabled")
        
        def handle_click(event):
            print("clicked!")

        def send_callback():
            pass

        def editor_callback():
            pass

        self.textbox.bind("<Control-Return>", handle_click)

        self.prompt = customtkinter.CTkTextbox(master=self, corner_radius=10,)
        self.prompt.grid(row=1, column=0, rowspan = 2, sticky="nsew")

        self.button = customtkinter.CTkButton(master=self, command=send_callback, text="Envoyer")
        self.button.grid(row=1, column=1, sticky="ew")
        self.button1 = customtkinter.CTkButton(master=self, command=editor_callback, text="Editeur")
        self.button1.grid(row=2, column=1, sticky="ew")

if __name__ == "__main__":
    app = App()
    app.mainloop()