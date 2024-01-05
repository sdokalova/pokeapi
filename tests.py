import requests
import pytest

base_url = "https://pokeapi.co/api/v2/"
session = requests.Session()
water_type_endpoint = base_url + "type/water"
pokemon_endpoint = base_url + "pokemon/"
species_endpoint = base_url + "pokemon-species/"
evolution_chain_endpoint = base_url + "evolution-chain/"
ability_endpoint = base_url + "ability/"
generation_endpoint = base_url + "generation/"


def test_water_type():
    response = session.get(water_type_endpoint)
    assert response.status_code == 200
    assert len(response.json()["pokemon"]) == 186
    assert response.json()["pokemon"][68]["pokemon"]["name"] == "milotic"


def get_pokemon_id(index: int) -> str:
    pokemon_id = session.get(water_type_endpoint).json()["pokemon"][index]["pokemon"]["url"].split("/")[-2]
    return pokemon_id


def count_abilities(list_of_entities: list) -> tuple:
    number_of_abilities = 0
    hidden_abilities = 0
    for element in list_of_entities:
        number_of_abilities += 1
        if element["is_hidden"]:
            hidden_abilities += 1
    return number_of_abilities, hidden_abilities


@pytest.mark.parametrize("pokemon_id, name, types, n_abilities, n_hidden",
                          [
                              ("igglybuff", "igglybuff", ["normal", "fairy"], 3, 1),
                              (get_pokemon_id(68), "milotic", ["water"], 3, 1),
                          ],
                         ids=["igglybuff", "id=68"])
def test_get_pokemon(pokemon_id, name, types, n_abilities, n_hidden):
    response = session.get(pokemon_endpoint + pokemon_id)
    assert response.status_code == 200
    assert response.json()["forms"][0]["name"] == name
    for element in response.json()["types"]:
        assert element["type"]["name"] in types
    number_of_abilities, hidden_abilities = count_abilities(response.json()["abilities"])
    assert number_of_abilities == n_abilities
    assert hidden_abilities == n_hidden


def get_evolution_chain_id(pokemon_name: str) -> str:
    response = session.get(species_endpoint + pokemon_name)
    evolution_chain_id = response.json()["evolution_chain"]["url"].split("/")[-2]
    return evolution_chain_id


@pytest.mark.parametrize("pokemon, n_evolutions, expected_evolutions",
                         [
                             ("eevee", 8, ["vaporeon", "jolteon", "flareon"])
                         ],
                         ids=["eevee"])
def test_evolution(pokemon, n_evolutions, expected_evolutions):
    evolution_chain_id = get_evolution_chain_id(pokemon)
    response = session.get(evolution_chain_endpoint + evolution_chain_id)
    assert response.status_code == 200
    list_of_evolutions = response.json()["chain"]["evolves_to"]
    assert len(list_of_evolutions) == n_evolutions
    evolutions_in_response = [element["species"]["name"] for element in list_of_evolutions]
    assert set(expected_evolutions).issubset(set(evolutions_in_response))


@pytest.mark.parametrize("ability, expected_pokemons",
                         [("cute-charm", ["milotic", "jigglypuff", "wigglytuff"])],
                         ids=["cute-charm"])
def test_ability(ability, expected_pokemons):
    response = session.get(ability_endpoint + ability)
    assert response.status_code == 200
    list_of_pokemons = [element["pokemon"]["name"] for element in response.json()["pokemon"]]
    assert set(expected_pokemons).issubset(set(list_of_pokemons))


def test_generation():
    response = session.get(generation_endpoint + "1")
    assert len(response.json()["pokemon_species"]) == 151
    assert response.json()["pokemon_species"][0]["name"] == "bulbasaur"
    assert response.json()["pokemon_species"][-1]["name"] == "mew"


def test_invalid_pokemon_name():
    response = session.get(pokemon_endpoint + "not_a_pokemon")
    assert response.status_code == 404
