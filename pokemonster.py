import requests
import json

class Pokemonster:
    def __init__(self, name):
        self.name = name
        self.link = f"http://pokeapi.co/api/v2/pokemon/{self.name}"
        self.data = json.loads(requests.get(self.link).text)
        self.get_abilities()
        
    
    def get_abilities(self):
        self.abilities =  [ab["ability"]["name"] for ab in self.data["abilities"]]
        
    
    def to_string(self):
        print(self.name, self.abilities)
        
        
        
bulbasaur = Pokemonster("bulbasaur")
bulbasaur.to_string()