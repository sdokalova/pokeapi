from typing import Any

def get_list_of_values_by_key(dictionary: dict, key: Any) -> list:
    """Makes a list of values from given dictionary by key"""
    lst = []
    if key in dictionary: lst.append(dictionary[key])
    for k, v in dictionary.items():
        if isinstance(v, dict):
            item = get_list_of_values_by_key(v, key)
            if item is not None:
                lst.append(item)
    return lst


def count_abilities(list_of_entities: list) -> tuple:
    """Counts number of pokemon's abilities in response"""
    number_of_abilities = 0
    hidden_abilities = 0
    for element in list_of_entities:
        number_of_abilities += 1
        if element["is_hidden"]:
            hidden_abilities += 1
    return number_of_abilities, hidden_abilities