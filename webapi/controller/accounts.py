import jwt
from flask import request
from flask_restful import Resource

from webapi import app
from webapi.service.accounts import LoginService, get_userinfo, token_required, ProfileService


class LoginController(Resource):
    def post(self):
        data_posted = request.get_json()
        all_keys = []
        for keys in data_posted:
            all_keys.append(keys)
        if "accessToken" in all_keys:
            token = data_posted["accessToken"]
            user_data = LoginService().fetch_google_id(access_token=token)
            if not user_data:
                return {"success": False, "message": "Invalid Token!"}
        else:
            return {"success": False, "message": "accessToken not available!"}
        data, user = LoginService().get_user(google_data=user_data)
        return_obj = {"success": True, "data": data}
        if not user:
            if "ign" in all_keys:
                if data_posted["ign"] == "":
                    return {"success": False, "message": "IGN is not valid!"}
            else:
                return {"success": False, "message": "IGN not available"}
            if "steamId" not in all_keys:
                return {"success": False, "message": "Steam URL not available!"}
            else:
                steamid = data_posted["steamId"]
                steam_val, steam_id = LoginService().validate_steamid(steamid)
                if not steam_val:
                    return {"success": False, "message": "Steam ID already used!"}
                user_data["ign"] = data_posted["ign"]
                user_data["steamId"] = steam_id
                if not steam_id:
                    return {"success": False, "message": "Steam ID is invalid!"}
                if steam_id:
                    data, user = LoginService().create_user(data=user_data)
                    return_obj = {"success": True, "data": data}
        login_data = LoginService().get_token(user, return_obj)
        return login_data

    @token_required
    def get(self):
        user = get_userinfo()
        data = {"ign": user.ign,
                "picture": app.config["SERVER_URL"] + user.picture,
                "email": user.email,
                "steamId": user.steamid,
                "name": user.name}
        return_obj = {"success": True, "data": data}
        login_data = LoginService().get_token(user, return_obj)
        return login_data


class ProfileController(Resource):
    @token_required
    def put(self):
        """
        body required in the format {"ign": <ign>, "steamID": <steamUrl>}
        :return:
        if successful {"success": True, "data": <user_data>}
        else {"success": False, "message": <reason>}
        """
        user = get_userinfo()
        data_posted = request.get_json()
        all_keys = []
        for keys in data_posted:
            all_keys.append(keys)
        if "ign" in all_keys or data_posted["ign"] != '':
            pass
        else:
            return_data = {"success": False, "message": "IGN not available or blank!"}
            user = get_userinfo()
            ret = LoginService().get_token(user, return_data)
            return ret
        if "steamId" not in all_keys:
            return_data = {"success": False, "message": "steamId not available!"}
            user = get_userinfo()
            ret = LoginService().get_token(user, return_data)
            return ret
        success, message = ProfileService().update_steam(data_posted, user)
        if success:
            return_data = {"success": success, "data": message}
            user = get_userinfo()
            ret = LoginService().get_token(user, return_data)
            return ret
        return_data = {"success": success, "message": message}
        user = get_userinfo()
        ret = LoginService().get_token(user, return_data)
        return ret
