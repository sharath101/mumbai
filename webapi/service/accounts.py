import datetime
import os.path
import shutil
from functools import wraps
import jwt
import requests
from flask import make_response, request
from secrets import token_hex

from webapi import app, db
from webapi.models import User


def get_userinfo():
    auth_data = request.headers.get("Authorization")
    if not auth_data:
        return {"success": False, "message": "Token is missing!"}, 401
    token = auth_data.split("Bearer ")[-1]
    a = jwt.decode(token, app.config["SECRET_KEY"], algorithms=['HS256'])
    user_id = a["user"]
    user = User.query.get(user_id)
    return user


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_data = request.headers.get("Authorization")
        if not auth_data:
            return {"success": False, "message": "Token is missing!"}, 401
        token = auth_data.split("Bearer ")[-1]
        try:
            a = jwt.decode(token, app.config["SECRET_KEY"], algorithms=['HS256'])
            user_id = a["user"]
            user = User.query.get(user_id)
            if not user:
                return {"success": False, "message": "Token invalid!"}, 401
        except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return {"success": False, "message": "Token invalid!"}, 401
        return f(*args, **kwargs)

    return decorated


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
                    "picture": app.config["SERVER_URL"] + existing_user.picture,
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
        except IndexError:
            vanity_url = url
            steam_id = url
        steam_response = requests.get(app.config["STEAM_API_LINK1"] +
                                      app.config['STEAM_API_KEY'] + '&vanityurl=' + vanity_url)
        steam_json = steam_response.json()
        if steam_json['response']['success'] == 1:
            steam_id_final = steam_json['response']['steamid']
        else:
            steam_response = requests.get(app.config["STEAM_API_LINK2"] +
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

    def create_user(self, data):
        pic_string = token_hex(20)
        user = User()
        user.ign = data["ign"]
        user.name = data["name"]
        user.email = data["email"]
        user.steamid = data["steamId"]
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=data["email"]).first()
        user.picture = "/pics/" + str(user.id) + "_" + str(pic_string) + ".jpg"
        self.save_user_image(data["picture"], str(user.id) + "_" + str(pic_string))
        db.session.commit()
        data = {"ign": user.ign,
                "picture": app.config["SERVER_URL"] + user.picture,
                "email": user.email,
                "steamId": user.steamid,
                "name": user.name}
        return data, user

    def save_user_image(self, url, filename):
        directory = app.config["PROFILE_PICS"]
        filepath = os.path.join(directory, filename + ".jpg")
        image = requests.get(url, stream=True)
        if image.status_code == 200:
            with open(filepath, 'wb') as f:
                shutil.copyfileobj(image.raw, f)
            return True
        else:
            return False

    def get_token(self, user, return_obj):
        resp = make_response(return_obj)
        user_id = user.id
        token = jwt.encode({'user': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
                           app.config["SECRET_KEY"], algorithm="HS256")
        resp.headers["Authorization"] = "Bearer " + token
        resp.headers["Access-Control-Expose-Headers"] = "Authorization"
        return resp


class ProfileService:
    def update_steam(self, data, user):
        url = data["steamId"]
        ign = data["ign"]
        try:
            vanity_url = url[30:]
            if vanity_url[-1] == '/':
                vanity_url = vanity_url[0:-1]
            steam_id = url[36:]
            if steam_id[-1] == '/':
                steam_id = steam_id[0:-1]
        except IndexError:
            vanity_url = url
            steam_id = url
        steam_response = requests.get(app.config["STEAM_API_LINK1"] +
                                      app.config['STEAM_API_KEY'] + '&vanityurl=' + vanity_url)
        steam_json = steam_response.json()
        if steam_json['response']['success'] == 1:
            steam_id_final = steam_json['response']['steamid']
        else:
            steam_response = requests.get(app.config["STEAM_API_LINK2"] +
                                          app.config['STEAM_API_KEY'] + '&steamids=' + steam_id)
            steam_json = steam_response.json()
            if steam_json['response']['players']:
                steam_id_final = steam_json['response']['players'][0]['steamid']
            else:
                steam_id_final = False
        if steam_id_final:
            existing_user = User.query.filter_by(steamid=steam_id_final).first()
            if existing_user and existing_user.id != user.id:
                return False, "Steam ID already used by another user!"
        if steam_id_final:
            user.steamid = steam_id_final
            user.ign = ign
            db.session.commit()
            user = User.query.get(user.id)
            data = {"ign": user.ign,
                    "picture": app.config["SERVER_URL"] + user.picture,
                    "email": user.email,
                    "steamId": user.steamid,
                    "name": user.name}
            return True, data
        return False, "Steam ID invalid!"
