import requests
import json
from poke_abilities import Ability


class Pokemonster:
    def __init__(self, name: str):
        self.name: str = name
        # link is created with name
        link: str = f"http://pokeapi.co/api/v2/pokemon/{self.name}"
        # link is passed to function below
        self.data: dict = self.get_data(link)
        self.abilities: list = self.get_abilities()
        self.types: list = self.get_types()
        self.sprites: dict = self.get_default_and_shiny_sprite()

    # makes a request with a link to return json
    def get_data(self, link: str) -> dict:
        try:
            data: str = requests.get(link).text
            return json.loads(data)
        except (AttributeError, json.decoder.JSONDecodeError):
            raise Exception("We were unable to find that pokemon")

    # pulls abilities from json self.data
    # instantiates an Ability object from the poke_abilities module
    # uses list comprehension to cover every ability
    def get_abilities(self) -> list:
        return [Ability(ab["ability"]["name"])
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

    # parses json to retrieve types
    def get_types(self) -> list:
        types: dict = self.data["types"]
        # list comprehension to fill list with every type
        return [type["type"]["name"] for type in types]

    @property
    def to_string(self) -> tuple:
        return (self.name, self.ability_full,
                self.types, self.sprites)

    @property
    def ability_names(self) -> list:
        return [ab.name for ab in self.abilities]

    @property
    def ability_full(self) -> list:
        return [ab.info_card for ab in self.abilities]

    pokedex: list = ['bulbasaur', 'ivysaur', 'venusaur', 'charmander',
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

    # adds a pokemon to the pokedex list if the pokemon exists on the api
    # returns an int value that is used to determine the outcome
    @classmethod
    def add_pokemon(cls, name: str) -> int:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
        if response.status_code == 200:
            if name in cls.pokedex:
                print("Pokemon already in pokedex")
                return 1
            else:
                cls.pokedex.append(name)
                return 0
        else:
            print("Pokemon not found")
            return 2

    # removes a pokemon from the pokedex if it is there
    @classmethod
    def remove_pokemon(cls, name: str):
        for pokemon in cls.pokedex:
            if name == pokemon.name:
                cls.pokedex.remove(name)
                return
        print("Could not find that pokemon in the pokedex")
