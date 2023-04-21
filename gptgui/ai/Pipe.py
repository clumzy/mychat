from numpy import append
import wikipedia
wikipedia.set_lang("fr")

import os

from json import loads

from .Chatbot import Chatbot

class WikiPipe():
    def __init__(self,):
        prompt_path = "D:\\George\\Documents\\Envs\\mychat\\prompting"

        self._wiki_bot=Chatbot(
            sys_prompt=os.path.join(prompt_path,"wikiprompt.txt"))
        self._mind_bot= Chatbot(
            sys_prompt=os.path.join(prompt_path,"sysprompt.txt"))
        self._last_user_message = ""
    
    @property
    def token_use(self):
        return (
            str(round(self._wiki_bot.token_use/4097.0, 2))
            +"/"
            +str(round(self._mind_bot.token_use/4097.0, 2)))
    
    def add_user_prompt(self, prompt:str):
        self._wiki_bot.add_user_prompt(prompt)
        self._mind_bot.add_user_prompt(prompt)

    def return_answer(self):
        wiki_bot_result = loads(self._wiki_bot.return_answer())
        print(wiki_bot_result)
        return self._mind_bot.return_answer()
