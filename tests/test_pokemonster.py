from src.pokemonster import Pokemonster
from src.poke_abilities import Ability
import unittest
import copy

class TestApi(unittest.TestCase):
    bulbasaur = Pokemonster("bulbasaur")
    def test_api_types(self):
        self.assertEqual(self.bulbasaur.types, ['grass', 'poison'])
    
    def test_api_abilities(self):
        self.assertEqual([ab.name for ab in self.bulbasaur.abilities],
        ['overgrow', 'chlorophyll'])
    
    def test_api_sprite(self):
        self.assertEqual(self.bulbasaur.sprites, 
        {"default": "https://raw.githubusercontent.com/PokeAPI/sprites/"
         "master/sprites/pokemon/1.png",
         "shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/"
         "master/sprites/pokemon/shiny/1.png"})

    def test_pokedex_append(self):
        dex = Pokemonster.list_pokedex()
        copy_dex = copy.deepcopy(dex)
        Pokemonster.add_pokemon("sandile")
        copy_dex.append("sandile")
        self.assertEqual(copy_dex, dex)