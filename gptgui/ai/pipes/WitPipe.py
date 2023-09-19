from wit import Wit
from json import dumps

import os

from ..Chatbot import Chatbot
from ..services import WeatherService, BLIPService, MemoryService
from ...ui.Message import SystemMessage

class WitPipe():
    def __init__(self, prompt_path:str):
        self._mind_bot= Chatbot(
            sys_prompt=os.path.join(prompt_path,"sysprompt.txt"))
        self._wit = Wit("7ZDABHS6FCZTN5LL753LOCGTI7HAOBZW")
        self.last_sys_message:None|SystemMessage = None
    
    @property
    def token_use(self):
        return (str(round(self._mind_bot.token_use/4097.0, 2)))
    
    def _flow(self, outcome:dict):
        package = ""
        if outcome["intents"] == []:
            return None
        elif outcome["intents"][0]["name"] == "get_meteo":
            print("meteo")
            meteo = WeatherService(outcome=outcome,)
            return meteo.get_package()
        elif outcome["intents"][0]["name"] == "get_image_description":
            if self.last_sys_message != None:
                blip = BLIPService(
                    outcome=outcome,
                    img_path=self.last_sys_message.get(0.0,4096.4096).split("\n")[0],
                    )
                return blip.get_package()
        elif outcome["intents"][0]["name"] == "get_image_answer":
            if self.last_sys_message != None:
                blip = BLIPService(
                    outcome=outcome,
                    img_path=self.last_sys_message.get(0.0,4096.4096).split("\n")[0],
                    query=self._mind_bot.user_messages[-1]
                    )
                return blip.get_package()
        elif outcome["intents"][0]["name"] == "store_memory":
            memory = MemoryService(location="/Users/george.pied/Code/clumzy/mychat/memories")
            memory.save_memory(outcome["entities"]["wit$reminder:reminder"][0]["value"])
            return None
        
    def _thought_upload(self, memory_package:str):
        upload = (
            "[UPLOAD EN COURS]\n"
            +memory_package
            +"\n[UPLOAD TERMINE]")
        print(upload)
        self._mind_bot.add_assistant_answer(upload)
    
    def add_user_prompt(self, prompt:str):
        self._mind_bot.add_user_prompt(prompt)

    def return_answer(self):
        memories = MemoryService("/Users/george.pied/Code/clumzy/mychat/memories")
        self._thought_upload(memories.load_memory(self._mind_bot.user_messages[-1]))
        #CONDITION SI LE MESSAGE FAIT MOINS DE 280
        if len(self._mind_bot.user_messages[-1])<280:
            outcome = self._wit.message(self._mind_bot.user_messages[-1], verbose=True)
            print(dumps(outcome, indent=2))
            knowledge_package = self._flow(outcome)
            if knowledge_package:
                self._thought_upload(knowledge_package)
        else: print("Message is too long. Go below 280 characters.")
        return self._mind_bot.return_answer()