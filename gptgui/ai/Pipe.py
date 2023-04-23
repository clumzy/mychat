from numpy import append
import wikipedia
wikipedia.set_lang("fr")
from wit import Wit
from json import loads, dumps
import pyowm

from meteofrance_api import MeteoFranceClient

from datetime import datetime

import os

from json import loads

from .Chatbot import Chatbot

class WitPipe():
    def __init__(self,):
        prompt_path = "D:\\George\\Documents\\Envs\\mychat\\prompting"
        self._mind_bot= Chatbot(
            sys_prompt=os.path.join(prompt_path,"sysprompt.txt"))
        self._wit = Wit("7ZDABHS6FCZTN5LL753LOCGTI7HAOBZW")
    
    @property
    def token_use(self):
        return (str(round(self._mind_bot.token_use/4097.0, 2)))
    
    def _flow(self, outcome:dict):
        package = ""
        if outcome["intents"] == []:
            return None
        elif outcome["intents"][0]["name"] == "get_meteo":
            print("meteo")
            try:
                date = outcome["entities"]["wit$datetime:datetime"][0]["value"]
            except KeyError: date = "None"
            try:
                location = outcome["entities"]["wit$location:location"][0]["value"]
            except KeyError: location = "Paris"
            print(date)
            client = MeteoFranceClient()
            list_places = client.search_places(location)
            my_place = list_places[0]
            print(my_place)
            my_place_weather_forecast = client.get_forecast_for_place(my_place)
            today = datetime.now()
            if date != "None":
                date = datetime.strptime(date[:10]+"-23-59", "%Y-%m-%d-%H-%M")
            else:
                date = datetime.now()
            diff = date-today
            print(diff.days)
            my_place_daily_forecast = my_place_weather_forecast.daily_forecast
            if diff.days < 15:
                package = my_place_daily_forecast[diff.days]
            else:
                package = "Impossible de donner une prédiction météo au delà de 15 jours. Veuillez-en informer l'utilisateur."
            return str(package)

    
    def _memory_upload(self, memory_package:str):
        upload = (
            "[UPLOAD MEMOIRE EN COURS]\n"
            +memory_package
            +"\n[UPLOAD MEMOIRE TERMINE]"
        )
        print(upload)
        self._mind_bot.add_assistant_answer(upload)
    
    def add_user_prompt(self, prompt:str):
        self._mind_bot.add_user_prompt(prompt)

    def return_answer(self):
        outcome = self._wit.message(self._mind_bot.user_messages[-1], verbose=True)
        print(dumps(outcome, indent=2))
        knowledge_package = self._flow(outcome)
        if knowledge_package:
            self._memory_upload(knowledge_package)
        return self._mind_bot.return_answer()