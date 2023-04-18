import os
import openai

from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.tools import BaseTool
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage)
from langchain.utilities import WikipediaAPIWrapper

class Chatbot():
    def __init__(self, *args,):
        #CLES API
        self._openai_key = "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"
        self._azure_speech_key = "b736e203fe004d99b5d92d2f2e68c5da"
        self._region = "francecentral"
        #LANGCHAIN CHAT
        self._chat = ChatOpenAI(
            temperature=0.7,
            openai_api_key=self._openai_key,) #type:ignore
        #ELEMENTS DE CONTEXTE DE LA DISCUSSION
        self._system_prompt_loc = os.path.join("prompting/")
        if os.path.exists(os.path.join(self._system_prompt_loc, "sysprompt.txt")):
            with open(os.path.join(self._system_prompt_loc, "sysprompt.txt"), 'r') as f:
                system_prompt = f.read()
        else:
            system_prompt = ""
        #LE TABLEAU QUI CONTIENDRA LES MESSAGES DE LA DISCUSSION    
        self._messages = []
        #CONFIGURATION DU SYS PROMPT
        self.set_system_prompt(system_prompt)

    #FONCTIONS ATTRIBUS
    @property
    def user_messages(self):
        return [x.content for x in self._messages if type(x) == "human"]

    @property
    def assistant_messages(self):
        return [x.content for x in self._messages if type(x) == "ai"]

    @property
    def all_messages(self):
        return [x.content for x in self._messages if type(x) != "system"]

    #FONCTIONS GETSETADD
    def set_system_prompt(self, prompt:str)->None:
        if len(self._messages) > 0: self._messages[0] = prompt
        else: self._messages.append(
            SystemMessage(content = prompt))
    def add_user_prompt(self, prompt:str)->None:
        self._messages.append(
            HumanMessage(content=prompt))
    def _add_assistant_answer(self, answer:AIMessage)->None:
        self._messages.append(
            answer)
    #FONCTIONS HELPER
    def __str__(self) -> str:
        return "\n".join([str(x["role"])+" : "+str(x["content"]) for x in self._messages[1:]])

    #FONCTION POUR RECUPERER UN RESUME DU TEXTE
    def return_recap(self)->str:
        """prompt = "Résume moi en 3 phrases synthétiques et précises le contenu de cet échange, du point de vue de George qui résume à Jeannette.\n"
        package = [{
            "role":"user", 
            "content": prompt+str(self)}]
        return self.return_answer(package)"""
        return "420"
        
    #FONCTION QUI RECUPERE LA COMPLETION CHATGPT
    def return_answer(self, messages=None)->str:
        if not messages: messages = self._messages
        answer = self._chat(messages)
        self._add_assistant_answer(AIMessage(content=answer.content)) #type:ignore
        return answer.content
    
    def num_tokens_from_messages(self, messages=None)->int:
        """Returns the number of tokens used by a list of messages."""
        return 0
    

