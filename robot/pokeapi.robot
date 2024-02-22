*** Settings ***
Library    RequestsLibrary
Library    CustomLibrary


Suite Setup    Create Session    pokeapi    https://pokeapi.co/api/v2/


*** Variables ***
&{igglybuff}    name=igglybuff    types=normal, fairy    abilities=3    hiden=1


*** Test Cases ***
Get Igglybuff info
    ${resp}=    GET On Session pokeapi    /pokemon/igglybuff    expected_status=200
    Status Should Be    200  ${resp}
    Dictionary Should Contain Value    ${resp.json()}    igglybuff    ignore_case=True
    ${types_in_responce}=    Get List Of Values By Key    ${resp.json()["types"]}     name
    Lists Should Be Equal    &{igglybuff}["types"]     ${types_in_responce}




