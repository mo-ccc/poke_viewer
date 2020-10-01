import requests
import json


class Ability:
    def __init__(self, name: str):
        self.name = name
        self.info = self.get_info(name)

    # uses api to get info on an ability name
    def get_info(self, name):
        link = f"https://pokeapi.co/api/v2/ability/{name}"
        raw = json.loads(requests.get(link).text)
        ability_info = raw["effect_entries"]
        for element in ability_info:
            if element["language"]["name"] == "en":
                return element["effect"].split("\n")[0]

        return "Info not found"

    @property
    def info_card(self):
        return f"{self.name}:{self.info}"
