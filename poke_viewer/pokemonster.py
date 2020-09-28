import requests
import json


class Pokemonster:
    def __init__(self, name: str):
        self.name: str = name
        link = f"http://pokeapi.co/api/v2/pokemon/{self.name}"
        self.data: dict = self.get_data(link)
        self.abilities: list = self.get_abilities()
        self.types: list = self.get_types()
        self.sprites: dict = self.get_default_and_shiny_sprite()

    def get_data(self, link: str):
        try:
            data = requests.get(link).text
            return json.loads(data)
        except (AttributeError, json.decoder.JSONDecodeError):
            raise Exception("We were unable to find that pokemon")

    def get_abilities(self) -> list:
        return [ab["ability"]["name"]
                for ab in
                self.data["abilities"]]

    def get_sprite_of_type(self, version: str) -> str:
        # gets the dictionary of sprites from the api data
        sprites: dict = self.data["sprites"]
        # returns the link of a sprite of requested version
        return sprites[version]

    '''
    uses the get_sprite_of_type function twice to get
    the default and shiny sprite links and return them
    in a dict object.
    '''
    def get_default_and_shiny_sprite(self) -> dict:
        return {"default": self.get_sprite_of_type("front_default"),
                "shiny": self.get_sprite_of_type("front_shiny")}

    def get_types(self) -> list:
        types: dict = self.data["types"]
        return [type["type"]["name"] for type in types]

    @property
    def to_string(self) -> tuple:
        return (self.name, self.abilities, self.types, self.sprites)

    pokedex = ['bulbasaur', 'ivysaur', 'venusaur', 'charmander',
               'charmeleon', 'charizard', 'squirtle', 'wartortle',
               'blastoise', 'caterpie', 'metapod', 'butterfree',
               'weedle', 'kakuna', 'beedrill', 'pidgey',
               'pidgeotto', 'pidgeot', 'rattata', 'raticate',
               'spearow', 'fearow', 'ekans', 'arbok', 'pikachu',
               'raichu', 'sandshrew', 'sandslash', 'nidoran-f',
               'nidorina', 'nidoqueen', 'nidoran-m', 'nidorino',
               'nidoking', 'clefairy', 'clefable', 'vulpix',
               'ninetales', 'jigglypuff', 'wigglytuff', 'zubat',
               'golbat', 'oddish', 'gloom', 'vileplume', 'paras',
               'parasect', 'venonat', 'venomoth', 'diglett',
               'dugtrio', 'meowth', 'persian', 'psyduck', 'golduck',
               'mankey', 'primeape', 'growlithe', 'arcanine',
               'poliwag', 'poliwhirl', 'poliwrath', 'abra',
               'kadabra', 'alakazam', 'machop', 'machoke',
               'machamp', 'bellsprout', 'weepinbell', 'victreebel',
               'tentacool', 'tentacruel', 'geodude', 'graveler',
               'golem', 'ponyta', 'rapidash', 'slowpoke', 'slowbro',
               'magnemite', 'magneton', 'farfetchd', 'doduo',
               'dodrio', 'seel', 'dewgong', 'grimer', 'muk',
               'shellder', 'cloyster', 'gastly', 'haunter',
               'gengar', 'onix', 'drowzee', 'hypno', 'krabby',
               'kingler', 'voltorb', 'electrode', 'exeggcute',
               'exeggutor', 'cubone', 'marowak', 'hitmonlee',
               'hitmonchan', 'lickitung', 'koffing', 'weezing',
               'rhyhorn', 'rhydon', 'chansey', 'tangela',
               'kangaskhan', 'horsea', 'seadra', 'goldeen',
               'seaking', 'staryu', 'starmie', 'mr-mime',
               'scyther', 'jynx', 'electabuzz', 'magmar', 'pinsir',
               'tauros', 'magikarp', 'gyarados', 'lapras', 'ditto',
               'eevee', 'vaporeon', 'jolteon', 'flareon', 'porygon',
               'omanyte', 'omastar', 'kabuto', 'kabutops',
               'aerodactyl', 'snorlax', 'articuno', 'zapdos',
               'moltres', 'dratini', 'dragonair', 'dragonite',
               'mewtwo', 'mew']

    @classmethod
    def list_pokedex(cls):
        return cls.pokedex

    @classmethod
    def add_pokemon(cls, name):
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
        if response.status_code == 200:
            if name in cls.pokedex:
                print("Pokemon already in pokedex")
            else:
                cls.pokedex.append(name)
        else:
            print("Pokemon not found")

    @classmethod
    def remove_pokemon(cls, name):
        for pokemon in cls.pokedex:
            if name == pokemon.name:
                cls.pokedex.remove(name)
                return
        print("Could not find that pokemon in the pokedex")
