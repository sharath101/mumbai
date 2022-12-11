from webapi import app, db
from flask_login import login_user, login_required, logout_user, current_user, login_manager
from flask import request

from webapi.functions import steam_id_profile, check_request
from webapi.models import User


@app.errorhandler(404)
def page_not_found(e):
    return {"success": False,
            "message": "404! Invalid URL!"}


@app.route('/login', methods=['POST'])
def login():
    login_result = {"success": False,
                    "ign": {"success": False, "message": ""},
                    "name": {"success": False, "message": ""},
                    "email": {"success": False, "message": ""},
                    "steamid": {"success": False, "message": ""},
                    "loggedIn": False}
    data = request.get_json()
    all_keys = []
    for keys in data:
        all_keys.append(keys)
    if "email" in all_keys and "name" in all_keys:
        name = data["name"]
        email = data["email"]
        login_result["name"]["success"] = True
        login_result["email"]["success"] = True
    else:
        return login_result
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        login_user(existing_user, remember=True)
        login_result["success"] = True
        login_result["loggedIn"] = True
        return login_result
    else:
        if "ign" in all_keys:
            ign = data["ign"]
            login_result["ign"]["success"] = True
        else:
            return login_result
        if "steamid" in all_keys:
            steamid = data["steamid"]
            steamid_verified = steam_id_profile(steamid)
            if steamid_verified:
                login_result["steamid"]["success"] = True
                user = User()
                user.ign = ign
                user.name = name
                user.email = email
                user.steamid = steamid_verified
                db.session.add(user)
                db.session.commit()
                user = User.query.filter_by(email=email).first()
                login_user(user, remember=True)
                login_result["success"] = True
                login_result["loggedIn"] = True
                return login_result
            else:
                login_result["steamid"]["message"] = "Steam ID verification failed"
                return login_result
        else:
            return login_result


@app.route('/loginStatus')
@login_required
def test_logged_in():
    return {"success": True,
            "message": "Logged in",
            "user": current_user.name,
            "loggedIn": False}
