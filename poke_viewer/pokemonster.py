import requests
import json


class Pokemonster:
    def __init__(self, name: str):
        self.name = name
        self.link = f"http://pokeapi.co/api/v2/pokemon/{self.name}"
        self.get_data()
        self.get_abilities()
        self.get_types()
        self.get_default_and_shiny_sprite()

    def get_data(self):
        try:
            data = requests.get(self.link).text
            self.data = json.loads(data)
        except (AttributeError, json.decoder.JSONDecodeError):
            raise Exception("We were unable to find that pokemon")

    def get_abilities(self):
        self.abilities = [ab["ability"]["name"]
                          for ab in
                          self.data["abilities"]]

    def get_sprite_of_type(self, version: str):
        sprites = self.data["sprites"]
        return sprites[version]

    def get_default_and_shiny_sprite(self):
        self.sprites = (self.get_sprite_of_type("front_default"),
                        self.get_sprite_of_type("front_shiny"))

    def get_types(self):
        types = self.data["types"]
        self.types = [type["type"]["name"] for type in types]

    @property
    def to_string(self):
        return (self.name, self.abilities, self.types, self.sprites)


bulbasaur = Pokemonster("bulbasaur")
print(bulbasaur.to_string)
