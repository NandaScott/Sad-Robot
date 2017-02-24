import requests
import json


def card_fetch(cardname):
    l = []
    response = requests.get('http://api.scryfall.com/cards/search', params={'q':cardname}).json()
    msg = "**" + response['data'][0]['name'] + "** "
    if response['data'][0]['converted_mana_cost'] != "0.0":
        msg += response['data'][0]['mana_cost']
    msg += " - *" + response['data'][0]['set'].upper()+"*"
    msg += "\n"
    msg += response['data'][0]['type_line'] + " "
    if "Creature" in response['data'][0]['type_line']:
        msg += " "+response['data'][0]['power']+"/"+response['data'][0]['toughness']+"\n"
    msg += response['data'][0]['oracle_text'] + "\n"
    msg += response['data'][0]['image_uri']
    l=[msg]
    return l
