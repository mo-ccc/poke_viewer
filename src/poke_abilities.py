import requests
import json


class Ability:
    def __init__(self, name: str):
        self.name = name
        self.info = self.get_info(name)

    # uses api to get info on an ability name
    def get_info(self, name):
        link = f"https://pokeapi.co/api/v2/ability/{name}"
        json_raw = json.loads(requests.get(link).text)
        ability_info = json_raw["effect_entries"]
        for element in ability_info:
            # checks api to see if ability info is in english
            if element["language"]["name"] == "en":
                # returns only the first paragraph of the info
                return element["effect"].split("\n")[0]
        # if info for the ability is not found in english:
        return "Info not found"

    # to display name and info property together
    @property
    def info_card(self):
        return f"{self.name}:{self.info}"
