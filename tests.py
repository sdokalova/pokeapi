import requests
import pytest

session = requests.Session()

base_url = "https://pokeapi.co/api/v2/"
water_type_endpoint = base_url + "type/water"
pokemon_endpoint = base_url + "pokemon/"
species_endpoint = base_url + "pokemon-species/"
evolution_chain_endpoint = base_url + "evolution-chain/"
ability_endpoint = base_url + "ability/"
generation_endpoint = base_url + "generation/"


def test_water_type():
    """Tests if https://pokeapi.co/api/v2/type/ endpoint returns data for pokemons of expected type
    and that the list of returned pokemons contain expected pokemon example"""
    response = session.get(water_type_endpoint)
    assert response.status_code == 200
    assert len(response.json()["pokemon"]) == 186
    assert response.json()["pokemon"][68]["pokemon"]["name"] == "milotic"


def get_pokemon_id(index: int) -> str:
    """Returns pokemon id of given index from water-type pokemoms"""
    pokemon_id = session.get(water_type_endpoint).json()["pokemon"][index]["pokemon"]["url"].split("/")[-2]
    return pokemon_id


def count_abilities(list_of_entities: list) -> tuple:
    """Counts number of pokemon's abilities in response"""
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
    """Tests if https://pokeapi.co/api/v2/pokemon/ endpoint returns expected data by
    pokemon name or id"""
    response = session.get(pokemon_endpoint + pokemon_id)
    assert response.status_code == 200
    assert response.json()["forms"][0]["name"] == name
    for element in response.json()["types"]:
        assert element["type"]["name"] in types
    number_of_abilities, hidden_abilities = count_abilities(response.json()["abilities"])
    assert number_of_abilities == n_abilities
    assert hidden_abilities == n_hidden


def get_evolution_chain_id(pokemon_name: str) -> str:
    """Returns evolution chain id by pokemon's name"""
    response = session.get(species_endpoint + pokemon_name)
    evolution_chain_id = response.json()["evolution_chain"]["url"].split("/")[-2]
    return evolution_chain_id


@pytest.mark.parametrize("pokemon, n_evolutions, expected_evolutions",
                         [
                             ("eevee", 8, ["vaporeon", "jolteon", "flareon"])
                         ],
                         ids=["eevee"])
def test_evolution(pokemon, n_evolutions, expected_evolutions):
    """Tests if https://pokeapi.co/api/v2/evolution-chain/ endpoint returns expected data by pokemon name"""
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
    """Tests if https://pokeapi.co/api/v2/ability/ endpoint returns expected data by ability name"""
    response = session.get(ability_endpoint + ability)
    assert response.status_code == 200
    list_of_pokemons = [element["pokemon"]["name"] for element in response.json()["pokemon"]]
    assert set(expected_pokemons).issubset(set(list_of_pokemons))


def test_generation():
    """Tests if https://pokeapi.co/api/v2/generation/ endpoint returns expected data
    for pokemons of first generation"""
    response = session.get(generation_endpoint + "1")
    assert len(response.json()["pokemon_species"]) == 151
    assert response.json()["pokemon_species"][0]["name"] == "bulbasaur"
    assert response.json()["pokemon_species"][-1]["name"] == "mew"


def test_invalid_pokemon_name():
    """Tests if https://pokeapi.co/api/v2/pokemon/ endpoint returns 404 Status
    for attempt to get data by invalid pokemon name"""
    response = session.get(pokemon_endpoint + "not_a_pokemon")
    assert response.status_code == 404
