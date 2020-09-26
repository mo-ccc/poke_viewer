from poke_viewer.pokemonster import Pokemonster
import unittest

class TestApi(unittest.TestCase):
    bulbasaur = Pokemonster("bulbasaur")
    def test_api_types(self):
        self.assertEqual(self.bulbasaur.types, ['grass', 'poison'])
    
    def test_api_abilities(self):
        self.assertEqual(self.bulbasaur.abilities, ['overgrow', 'chlorophyll'])
    
    def test_api_sprite(self):
        self.assertEqual(self.bulbasaur.sprites, 
        ["https://raw.githubusercontent.com/PokeAPI/sprites/"
         "master/sprites/pokemon/1.png",
         "https://raw.githubusercontent.com/PokeAPI/sprites/"
         "master/sprites/pokemon/shiny/1.png"])
        