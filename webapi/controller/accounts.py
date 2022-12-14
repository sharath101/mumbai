from flask import request
from flask_login import login_user, login_required
from flask_restful import Resource

from webapi.Service.accounts import LoginService


class LoginController(Resource):
    def post(self):
        data = request.get_json()
        all_keys = []
        for keys in data:
            all_keys.append(keys)
        if "accessToken" in all_keys:
            token = data["accessToken"]
            user_data = LoginService().fetch_google_id(access_token=token)
            if not user_data:
                return {"success": False, "message": "Invalid Token!"}
        else:
            return {"success": False, "message": "accessToken not available!"}
        data, user = LoginService().get_user(google_data=user_data)
        if not user:
            if "ign" in all_keys:
                if data["ign"] == "":
                    return {"success": False, "message": "IGN is not valid!"}
            else:
                return {"success": False, "message": "IGN not available"}
            if "steamId" not in all_keys:
                return {"success": False, "message": "Steam URL not available!"}
            else:
                steamid = data["steamId"]
                steam_val, steam_id = LoginService().validate_steamid(steamid)
                if not steam_val:
                    return {"success": False, "message": "Steam ID already used!"}
                user_data["ign"] = data["ign"]
                user_data["steamId"] = steam_id
                if steam_id:
                    data, user = LoginService().create_user(data=user_data)
        login_user(user, remember=True)
        return {"success": True, "data": data}
