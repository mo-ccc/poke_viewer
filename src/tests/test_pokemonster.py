from pokemonster import Pokemonster
import unittest
import copy


class TestApi(unittest.TestCase):
    # instance of Pokemonster bulbasaur
    bulbasaur: Pokemonster = Pokemonster("bulbasaur")

    # test to see if bulbasaur instance has the correct types
    def test_api_types(self):
        self.assertEqual(self.bulbasaur.types, ['grass', 'poison'])

    def test_api_abilities(self):
        self.assertEqual([ab.name for ab in self.bulbasaur.abilities],
                         ['overgrow', 'chlorophyll'])

    sprite_dict: dict = {"default": "https://raw.githubusercontent.com/"
                         "PokeAPI/sprites/master/sprites/pokemon/1.png",
                         "shiny": "https://raw.githubusercontent.com/"
                         "PokeAPI/sprites/master/sprites/pokemon/"
                         "shiny/1.png"}

    def test_api_sprite(self):
        self.assertEqual(self.bulbasaur.sprites, self.sprite_dict)

    # tests the add_pokemon class method with the pokemon sandile
    def test_pokedex_append(self):
        dex: list = Pokemonster.pokedex
        copy_dex: list = copy.deepcopy(dex)
        Pokemonster.add_pokemon("sandile")
        copy_dex.append("sandile")
        self.assertEqual(copy_dex, dex)
