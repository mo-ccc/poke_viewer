from poke_viewer.pokemonster import Pokemonster
import unittest

class TestApi(unittest.TestCase):
    def test_bulbasaur(self):
        bulbasaur = Pokemonster("bulbasaur")
        self.assertEqual(bulbasaur.types, ['grass', 'poison'])
    