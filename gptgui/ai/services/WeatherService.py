from meteofrance_api import MeteoFranceClient
from datetime import datetime

class WeatherService():
    def __init__(self, outcome:dict, default_city:str = "Paris") -> None:
        self._outcome = outcome
        self._today = datetime.now()
        self._client = MeteoFranceClient()
        self._default_city = default_city
        try:
            wit_date_string = self._outcome["entities"]["wit$datetime:datetime"][0]["value"]
        except KeyError: wit_date_string = "None"
        if wit_date_string != "None":
            self._date = datetime.strptime(wit_date_string[:10]+"-23-59", "%Y-%m-%d-%H-%M")
        else: self._date = datetime.now()
        try:
            self._location = self._outcome["entities"]["wit$location:location"][0]["value"]
        except KeyError: self._location = "Paris"
        pass

    def get_package(self,):
        list_places = self._client.search_places(self._location)
        my_place = list_places[0]
        my_place_weather_forecast = self._client.get_forecast_for_place(my_place)
        diff = self._date-self._today
        my_place_daily_forecast = my_place_weather_forecast.daily_forecast
        if diff.days < 15:
            package = my_place_daily_forecast[diff.days]
            package["dt"] = self._date.strftime("%A %d/%m/%Y")
            package["sun"]["rise"] = datetime.fromtimestamp(
                package["sun"]["rise"]).strftime("%H:%M")
            package["sun"]["set"] = datetime.fromtimestamp(
                package["sun"]["set"]).strftime("%H:%M")
        else:
            package = "Impossible de donner une prédiction météo au delà de 15 jours. Veuillez-en informer l'utilisateur."
        return str(package)
    
    