import requests

from webapi import app, db
from webapi.models import User


class LoginService:
    @staticmethod
    def fetch_google_id(access_token):
        data_google = requests.get("https://www.googleapis.com/oauth2/v1/userinfo?access_token=" + access_token)
        data_google = data_google.json()
        data_avail = []
        for keys in data_google:
            data_avail.append(keys)
        if "error" in data_avail:
            return False
        google_data = {"name": data_google["name"],
                       "email": data_google["email"],
                       "picture": data_google["picture"]}
        return google_data

    @staticmethod
    def get_user(google_data):
        existing_user = User.query.filter_by(email=google_data["email"]).first()
        if existing_user:
            data = {"ign": existing_user.ign,
                    "picture": existing_user.picture,
                    "email": existing_user.email,
                    "steamId": existing_user.steamid,
                    "name": existing_user.name}
        else:
            return False, False
        return data, existing_user

    @staticmethod
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
        if steam_id_final:
            existing_user = User.query.filter_by(steamid=steam_id_final).first()
            if existing_user:
                return False, steam_id_final
        return True, steam_id_final

    @staticmethod
    def create_user(data):
        user = User()
        user.ign = data["ign"]
        user.name = data["name"]
        user.email = data["email"]
        user.picture = data["picture"]
        user.steamid = data["steamId"]
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=data["ign"]).first()
        data = {"ign": user.ign,
                "picture": user.picture,
                "email": user.email,
                "steamId": user.steamid,
                "name": user.name}
        return data