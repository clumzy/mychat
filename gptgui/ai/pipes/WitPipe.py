from wit import Wit
from json import dumps

import os

from ..Chatbot import Chatbot
from ..services import WeatherService, BLIPService
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
                    img_path=self.last_sys_message.get(0.0,4096.4096).split("\n")[0])
                return blip.get_package()

    def _thought_upload(self, memory_package:str):
        upload = (
            "[UPLOAD MEMOIRE EN COURS]\n"
            +memory_package
            +"\n[UPLOAD MEMOIRE TERMINE]")
        print(upload)
        self._mind_bot.add_assistant_answer(upload)
    
    def add_user_prompt(self, prompt:str):
        self._mind_bot.add_user_prompt(prompt)

    def return_answer(self):
        outcome = self._wit.message(self._mind_bot.user_messages[-1], verbose=True)
        print(dumps(outcome, indent=2))
        knowledge_package = self._flow(outcome)
        if knowledge_package:
            self._thought_upload(knowledge_package)
        return self._mind_bot.return_answer()