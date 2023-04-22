from numpy import append
import wikipedia
wikipedia.set_lang("fr")
from wit import Wit
from json import loads, dumps


import os

from json import loads

from .Chatbot import Chatbot

class WikiPipe():
    def __init__(self,):
        prompt_path = "D:\\George\\Documents\\Envs\\mychat\\prompting"
        self._mind_bot= Chatbot(
            sys_prompt=os.path.join(prompt_path,"sysprompt.txt"))
        self._wit = Wit("7ZDABHS6FCZTN5LL753LOCGTI7HAOBZW")
    
    @property
    def token_use(self):
        return (str(round(self._mind_bot.token_use/4097.0, 2)))
    
    def add_user_prompt(self, prompt:str):
        self._mind_bot.add_user_prompt(prompt)

    def return_answer(self):

        outcome = self._wit.message(self._mind_bot.user_messages[-1], verbose=True)
        print(dumps(outcome, indent=2))
        return self._mind_bot.return_answer()