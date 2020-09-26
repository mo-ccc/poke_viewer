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
        self.sprites = [self.get_sprite_of_type("front_default"),
                        self.get_sprite_of_type("front_shiny")]

    def get_types(self):
        types = self.data["types"]
        self.types = [type["type"]["name"] for type in types]

    @property
    def to_string(self):
        return (self.name, self.abilities, self.types, self.sprites)

    pokemon_152 = ['bulbasaur', 'ivysaur', 'venusaur', 'charmander',
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
    def list_152(cls):
        return cls.pokemon_152

    @classmethod
    def add_pokemon(cls, name):
        x = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
        if x.status_code == 200:
            cls.pokemon_152.append(name)
        else:
            print("Pokemon not found")
