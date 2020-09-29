import requests
import json


class Ability:
    def __init__(self, name: str):
        self.name = name
        self.info = self.get_info(name)
    
    def __str__(self):
        return f"{self.name}:{self.info}"
    
    def get_info(self, name):
        link = f"https://pokeapi.co/api/v2/ability/{name}"
        raw = json.loads(requests.get(link).text)
        ability_info = raw["effect_entries"]
        for element in ability_info:
            if element["language"]["name"] == "en":
                return element["effect"]

        return "Info not found"