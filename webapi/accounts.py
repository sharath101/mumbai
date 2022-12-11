import requests
from webapi import app, db
from flask_login import login_user, login_required, current_user
from flask import request
from webapi.functions import steam_id_profile
from webapi.models import User


@app.errorhandler(404)
def page_not_found(e):
    return {"success": False, "message": "404! Invalid URL!"}


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    all_keys = []
    for keys in data:
        all_keys.append(keys)
    if "accessToken" in all_keys:
        token = data["accessToken"]
        data_google = requests.get("https://www.googleapis.com/oauth2/v1/userinfo?access_token=" + token)
        data_google = data_google.json()
        data_avail = []
        for keys in data_google:
            data_avail.append(keys)
        if "error" in data_avail:
            return {"success": False, "message": "accessToken Failed!"}
        name = data_google["name"]
        email = data_google["email"]
        picture = data_google["picture"]
    else:
        return {"success": False, "message": "accessToken not available!"}
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        login_user(existing_user, remember=True)
        data = {"ign": existing_user.ign,
                "picture": existing_user.picture,
                "email": existing_user.email,
                "steamId": existing_user.steamid,
                "name": existing_user.name}
        return {"success": True, "data": data}
    else:
        if "ign" in all_keys:
            ign = data["ign"]
            if ign == "":
                return {"success": False, "message": "IGN is not valid!"}
        else:
            return {"success": False, "message": "IGN not available"}
        if "steamId" in all_keys:
            steamid = data["steamId"]
            steamid_verified = steam_id_profile(steamid)
            if steamid_verified:
                existing_user = User.query.filter_by(steamid=steamid_verified).first()
                if existing_user:
                    return {"success": False, "message": "Steam ID already used!"}
                user = User()
                user.ign = ign
                user.name = name
                user.email = email
                user.picture = picture
                user.steamid = steamid_verified
                db.session.add(user)
                db.session.commit()
                user = User.query.filter_by(email=email).first()
                login_user(user, remember=True)
                data = {"ign": ign,
                        "picture": picture,
                        "email": email,
                        "steamId": steamid_verified,
                        "name": name}
                return {"success": True, "data": data}
            else:
                return {"success": False, "message": "Steam URL invalid!"}
        else:
            return {"success": False, "message": "Steam URL not available!"}


@app.route('/loginStatus')
@login_required
def test_logged_in():
    return {"success": True,
            "message": "Logged in",
            "user": current_user.name,
            "loggedIn": False}
