import requests
from webapi import app


def validate_steamid(url):
    try:
        vanity_url = url[30:]
        if vanity_url[-1] == '/':
            vanity_url = vanity_url[0:-1]
        steam_id = url[36:]
        if steam_id[-1] == '/':
            steam_id = steam_id[0:-1]
    except:
        vanity_url = url
        steam_id = url
    steam_response = requests.get('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=' +
                                  app.config['STEAM_API_KEY'] + '&vanityurl=' + vanity_url)
    steam_json = steam_response.json()
    if steam_json['response']['success'] == 1:
        steam_id_final = steam_json['response']['steamid']
    else:
        steam_response = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' +
                                      app.config['STEAM_API_KEY'] + '&steamids=' + steam_id)
        steam_json = steam_response.json()
        if steam_json['response']['players']:
            steam_id_final = steam_json['response']['players'][0]['steamid']
        else:
            steam_id_final = False
    return steam_id_final
