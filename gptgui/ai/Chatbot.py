import os
import openai

class Chatbot():
    def __init__(
            self,
            sys_prompt:str,
            openai_key=None,
            *args,):
        #CLES API
        if openai_key is None:
            openai.api_key = os.environ.get("OPENAI_API_KEY")
        else: openai.api_key = openai_key
        #ELEMENTS DE CONTEXTE DE LA DISCUSSION
        if os.path.exists(sys_prompt):
            with open(sys_prompt, 'r') as f:
                system_prompt = f.read()
        else:
            system_prompt = ""
        #LE TABLEAU QUI CONTIENDRA LES MESSAGES DE LA DISCUSSION    
        self._messages = []
        #CONFIGURATION DU SYS PROMPT
        self.set_system_prompt(system_prompt)
        #TOKEN_USE
        self.token_use = 0

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
        if len(self._messages) > 0: self._messages[0]["content"] = prompt
        else: self._messages.append(
            {"role":"system", "content":f"{prompt}"})
    def add_user_prompt(self, prompt:str)->None:
        self._messages.append(
            {"role":"user", "content":f"{prompt}"})
    def _add_assistant_answer(self, answer:str)->None:
        self._messages.append(
            {"role":"assistant", "content":f"{answer}"})
    #FONCTIONS HELPER
    def __str__(self) -> str:
        return "\n".join([str(x["role"])+" : "+str(x["content"]) for x in self._messages[1:]])
        
    #FONCTION QUI RECUPERE LA COMPLETION CHATGPT
    def return_answer(self, messages=None)->str:
        if not messages: messages = self._messages
        #CHAT
        chat = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            temperature=0.7,
            messages = self._messages)
        content = chat.choices[0].message.content #type:ignore
        self._add_assistant_answer(content)
        self.token_use = chat.usage.total_tokens #type:ignore
        return content
    
    def num_tokens_from_messages(self, messages=None)->int:
        """Returns the number of tokens used by a list of messages."""
        return 0
    

