*** Settings ***
Documentation     Test suite for validating various PokéAPI endpoints.
Library           RequestsLibrary
Library           Collections
Suite Setup       Set Base URL

*** Variables ***
${BASE_URL}       https://pokeapi.co/api/v2

*** Keywords ***
Set Base URL
    Set Global Variable    ${BASE_URL}    https://pokeapi.co/api/v2

*** Test Cases ***
Get Igglybuff Information
    [Documentation]    Validates fetching of Igglybuff data from PokéAPI.
    # Establish a session with the base URL for the PokéAPI
    Create Session    pokeapi    ${BASE_URL}
    # Perform a GET request to retrieve data for Igglybuff
    ${response}=    GET On Session    pokeapi    /pokemon/igglybuff
    # Assert that the response status code is 200 (OK)
    Should Be Equal As Strings    ${response.status_code}    200
    # Convert the JSON response into a dictionary for easy data manipulation
    ${body}=    Convert To Dictionary    ${response.json()}
    # Ensure the response contains the 'name' key and log the name
    Dictionary Should Contain Key    ${body}    name
    Log    Igglybuff name in response: ${body['name']}
    # Extract the types of Igglybuff and verify they include 'normal' and 'fairy'
    ${type1}=    Set Variable    ${body['types'][0]['type']['name']}
    ${type2}=    Set Variable    ${body['types'][1]['type']['name']}
    Log    Igglybuff types: ${type1}, ${type2}
    Should Be True    '${type1}' == 'normal' or '${type2}' == 'normal'
    Should Be True    '${type1}' == 'fairy' or '${type2}' == 'fairy'
    # Count the total and hidden abilities of Igglybuff
    ${abilities}=    Set Variable    ${body['abilities']}
    Log    Abilities: ${abilities}
    ${hidden_abilities_count}=    Evaluate    len([ability for ability in ${abilities} if ability['is_hidden'] == True])
    Log    Number of hidden abilities: ${hidden_abilities_count}
    # Assert that Igglybuff has exactly 3 abilities, one of which is hidden
    Should Be True    len(${abilities}) == 3 and ${hidden_abilities_count} == 1
    Log    Ability checks passed: 3 abilities with 1 hidden.

List Water Type Pokémon
    [Documentation]    Validates fetching of water type Pokémon and asserts specific conditions.
    # Establish a session with the base URL for the PokéAPI
    Create Session    pokeapi    ${BASE_URL}
    # Perform a GET request to retrieve water type Pokémon list
    ${response}=    GET On Session    pokeapi    /type/water
    # Assert that the response status code is 200 (OK)
    Should Be Equal As Strings    ${response.status_code}    200
    # Convert the JSON response into a dictionary
    ${body}=    Set Variable    ${response.json()}
    # Log the list of water type Pokémon
    Log    ${body}
    # Assert the list contains the expected number of water type Pokémon
    ${pokemon_count}=    Get Length    ${body['pokemon']}
    Should Be Equal As Numbers    ${pokemon_count}    186
    # Find Milotic in the list and validate its presence
    ${milotic}=    Evaluate    [pokemon for pokemon in ${body['pokemon']} if pokemon['pokemon']['name'] == 'milotic'][0]
    Should Not Be Empty    ${milotic}
    # Extract and log Milotic's ID for use in subsequent tests
    Set Suite Variable    ${milotic_id}    ${milotic['pokemon']['url'].split('/')[-2]}
    Log    Milotic ID is ${milotic_id}

Get Milotic Information Using ID
    [Documentation]    Validates fetching of Milotic data using previously saved ID.
    # Establish a session with the base URL for the PokéAPI
    Create Session    pokeapi    ${BASE_URL}
    # Perform a GET request to retrieve data for Milotic using its ID
    ${response}=    GET On Session    pokeapi    /pokemon/${milotic_id}
    # Assert that the response status code is 200 (OK)
    Should Be Equal As Strings    ${response.status_code}    200
    # Convert the JSON response into a dictionary
    ${body}=    Set Variable    ${response.json()}
    # Log Milotic's data
    Log    ${body}
    # Ensure the response contains the 'name' key and validate it's Milotic
    Dictionary Should Contain Key    ${body}    name
    Should Be Equal    ${body['name']}    milotic
    # Check Milotic's type is 'water'
    ${type}=    Set Variable    ${body['types'][0]['type']['name']}
    Should Be Equal    ${type}    water
    # Count the total and hidden abilities of Milotic
    ${abilities}=    Set Variable    ${body['abilities']}
    ${hidden_abilities}=    Evaluate    len([ability for ability in ${abilities} if ability['is_hidden']])
    # Assert that Milotic has exactly 3 abilities, one of which is hidden
    Should Be True    len(${abilities}) == 3 and ${hidden_abilities} == 1

Get Eevee Evolution Chain
    [Documentation]    Fetches Eevee's evolution chain ID and validates it contains specific evolutions.
    # Establish a session with the base URL for the PokéAPI
    Create Session    pokeapi    ${BASE_URL}
    # Perform a GET request to retrieve data for Eevee's species
    ${response}=    GET On Session    pokeapi    /pokemon-species/eevee
    # Assert that the response status code is 200 (OK)
    Should Be Equal As Strings    ${response.status_code}    200
    # Convert the JSON response into a dictionary
    ${body}=    Set Variable    ${response.json()}
    # Extract the URL for Eevee's evolution chain
    ${evolution_chain_url}=    Set Variable    ${body['evolution_chain']['url']}
    # Log the evolution chain URL
    Log    Evolution chain URL is ${evolution_chain_url}
    # Extract the evolution chain ID from the URL
    ${evolution_chain_id}=    Evaluate    ${evolution_chain_url.split('/')[-2]}
    # Perform a GET request to retrieve Eevee's evolution chain using its ID
    ${evolution_response}=    GET On Session    pokeapi    /evolution-chain/${evolution_chain_id}
    # Assert that the response status code is 200 (OK)
    Should Be Equal As Strings    ${evolution_response.status_code}    200
    # Convert the JSON response into a dictionary
    ${evolution_body}=    Set Variable    ${evolution_response.json()}
    # Log the evolution chain data
    Log    ${evolution_body}
    # Validate the presence of Vaporeon, Jolteon, and Flareon in the evolution chain
    ${evolutions}=    Evaluate    [evo['species']['name'] for evo in ${evolution_body['chain']['evolves_to']}]
    Should Contain    ${evolutions}    vaporeon
    Should Contain    ${evolutions}    jolteon
    Should Contain    ${evolutions}    flareon

Get Pokémon With Cute Charm Ability
    [Documentation]    Fetches Pokémon with the Cute Charm ability and validates specific Pokémon are included.
    # Establish a session with the base URL for the PokéAPI
    Create Session    pokeapi    ${BASE_URL}
    # Perform a GET request to retrieve Pokémon list with the Cute Charm ability
    ${response}=    GET On Session    pokeapi    /ability/cute-charm
    # Assert that the response status code is 200 (OK)
    Should Be Equal As Strings    ${response.status_code}    200
    # Convert the JSON response into a dictionary
    ${body}=    Set Variable    ${response.json()}
    # Log the Pokémon list with Cute Charm ability
    Log    ${body}
    # Extract the names of Pokémon with the Cute Charm ability
    ${pokemon_names}=    Evaluate    [pokemon['pokemon']['name'] for pokemon in ${body['pokemon']}]
    # Validate that Milotic, Jigglypuff, and Wigglytuff are included in the list
    Should Contain    ${pokemon_names}    milotic
    Should Contain    ${pokemon_names}    jigglypuff
    Should Contain    ${pokemon_names}    wigglytuff
