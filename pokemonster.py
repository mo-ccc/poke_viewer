import requests
import json

class Pokemonster:
    def __init__(self, name):
        self.name = name
        self.link = f"http://pokeapi.co/api/v2/pokemon/{self.name}"
        self.data = json.loads(requests.get(self.link).text)
        self.get_abilities()
        self.get_types()
        
    def get_abilities(self):
        self.abilities =  [ab["ability"]["name"] for ab in self.data["abilities"]]
    
        
    def get_sprite(self, version):
        sprites = self.data["sprites"]
        self.sprite = sprites[version]
        
    def get_types(self):
        types = self.data["types"]
        self.types = [type["type"]["name"] for type in types]
    
    @property
    def to_string(self):
        return (self.name, self.abilities, self.types)
        
        
        
bulbasaur = Pokemonster("bulbasaur")
print(bulbasaur.to_string)