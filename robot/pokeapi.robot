*** Settings ***
Library    Collections
Library    RequestsLibrary
Library    CustomLibrary.py


Suite Setup    Create Session    pokeapi    https://pokeapi.com/api/v2/


*** Variables ***
&{igglybuff}    name=igglybuff    types=normal, fairy    abilities=3    hidden=1
${n_water_pokemons}     186
${water_pokemon_n_68}    milotic


*** Test Cases ***
Get Igglybuff info
    ${resp}=    GET On Session    pokeapi    /pokemon/igglybuff    expected_status=200
    Status Should Be    200  ${resp}
    Dictionary Should Contain Value    ${resp.json()}    igglybuff    ignore_case=True
    ${types_in_response}=    Get List Of Values By Key    ${resp.json()} [types]    name
    ${expected_types}=    Get From Dictionary     &{igglybuff}     types
    Lists Should Be Equal    ${types_in_response}     ${expected_types}
    ${abilities_in_response}=    Count Abilities    ${resp.json()}[abilities]
    ${n_abilities_in_response}=     ${abilities_in_response}[0]
    ${hidden_abilities_in_response}=    ${abilities_in_response}[1]
    ${expected_n_abilities}=     Get From Dictionary     &{igglybuff}     abilities
    ${expected_hidden_abilities}=     Get From Dictionary     &{igglybuff}     hidden
    Should Be Equal    ${n_abilities_in_response}    ${expected_n_abilities}
    Should Be Equal    ${hidden_abilities_in_response}    ${expected_hidden_abilities}


Get water type pokemons
    ${resp}=    GET On Session    pokeapi    /pokemon/type/water    expected_status=200
    Status Should Be    200  ${resp}
    ${n_pokemons_in_response}=    Get Count     ${resp}     pokemon
    Should Be Equal    ${n_pokemons_in_response}     ${n_water_pokemons}
    ${pokemon_n_68_in_response}=    ${resp}[pokemon][68][pokemon][name]
    Should Be Equal    ${pokemon_n_68_in_response}    {water_pokemon_n_68}











