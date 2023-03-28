import os
import threading
import openai

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Conversation import Chat

class Chatbot():
    def __init__(self, *args,):
        #CLES API
        self._openai_key = "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"
        self._azure_speech_key = "b736e203fe004d99b5d92d2f2e68c5da"
        self._region = "francecentral"
        self._has_ended = False
        #ELEMENTS DE CONTEXTE DE LA DISCUSSION
        self._system_prompt_loc = os.path.join("D:\\George\\Documents\\Envs\\mychat\\prompting")
        if os.path.exists(os.path.join(self._system_prompt_loc, "sysprompt.txt")):
            with open(os.path.join(self._system_prompt_loc, "sysprompt.txt"), 'r') as f:
                self._system_prompt = f.read()
        else:
            self._system_prompt = ""
        #LE TABLEAU QUI CONTIENDRA LES MESSAGES DE LA DISCUSSION    
        self._messages = []
        self._messages.append({"role": "system", "content" : self._system_prompt})

        #FENETRE
        self._message_box = None

    #FONCTIONS ATTRIBUS
    @property
    def user_messages(self):
        return [x["content"] for x in self._messages if x["role"] == "user"]

    @property
    def assistant_messages(self):
        return [x["content"] for x in self._messages if x["role"] == "assistant"]

    @property
    def all_messages(self):
        return [x["content"] for x in self._messages if x["role"] != "system"]

    #FONCTIONS GETSETADD
    def set_system_prompt(self, prompt:str)->None:
        self._system_prompt = prompt

    def add_user_prompt(self, prompt:str)->None:
        self._messages.append({"role": "user", "content": prompt})

    def add_assistant_answer(self, answer:str)->None:
        self._messages.append({"role": "assistant", "content": answer})
    #FONCTIONS HELPER

    #FONCTION THREADEE QUI AGIT SUR 
    def return_answer(self)->str:
        completion_package = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self._messages,
                api_key=self._openai_key)
        response = completion_package.choices[0].message.content # type: ignore
        return response
    
    