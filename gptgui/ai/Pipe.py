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
        self._last_user_message = prompt
        self._wiki_bot.add_user_prompt(prompt)
        self._mind_bot.add_user_prompt(prompt)

    def return_answer(self):
        wiki_bot_result = loads(self._wiki_bot.return_answer())
        print(wiki_bot_result)
        mind_package = {"role":"assistant", "content":""}
        if wiki_bot_result["RECHERCHE"] == "OUI":
            print(wiki_bot_result["QUERY"])
            wiki_article_summary = wikipedia.page(wiki_bot_result["QUERY"]).summary
            mind_package["content"] = (
                "[CONTENU EN COURS DE RECEPTION]"
                +"\n[MEMOIRE CHARGEE]"
                +"\n[AFFICHAGE DES INFORMATIONS EN COURS]"
                +wiki_article_summary
                +"\n[REPRISE DU CHAT]")
            return self._mind_bot.return_answer(
                self._mind_bot.get_messages().append(mind_package))
        else:
            return self._mind_bot.return_answer()
