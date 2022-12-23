from flask import request
from flask_restful import Resource

from webapi import app
from webapi.service.accounts import LoginService, get_userinfo, token_required
from webapi.service.friends import SearchService, TeamService


class FriendsController(Resource):
    @token_required
    def post(self):
        user = get_userinfo()
        data_posted = request.get_json()
        all_keys = []
        for keys in data_posted:
            all_keys.append(keys)
        if "friendId" in all_keys:
            pass
        return {"success": True}


class SearchController(Resource):
    # @token_required
    def get(self, query):
        user = get_userinfo()
        ret_data = SearchService.search_users(query)
        if len(ret_data):
            ret_val = {"success": True, "data": ret_data}
            ret = LoginService().get_token(user, ret_val)
            return ret
        else:
            ret_val = {"success": False, "message": "No users matched your query!"}
            ret = LoginService().get_token(user, ret_val)
            return ret


class TeamController(Resource):
    @token_required
    def get(self):
        user = get_userinfo()
        team_info = TeamService().get_team()
        if team_info:
            ret_data = {"success": True, "data": team_info}
        else:
            ret_data = {"success": False, "message": "Team does not exists!"}
        ret = LoginService().get_token(user, ret_data)
        return ret

    @token_required
    def post(self):
        user = get_userinfo()
        data_posted = request.get_json()
        all_keys = []
        for keys in data_posted:
            all_keys.append(keys)
        if "name" in all_keys or data_posted["name"] != '':
            data = TeamService().create_team(data_posted["name"])
            ret_data = {"success": True, "data": data}
        else:
            ret_data = {"success": False, "message": "Team name empty!"}
        ret = LoginService().get_token(user, ret_data)
        return ret

    @token_required
    def put(self):
        user = get_userinfo()
        data_posted = request.get_json()
        all_keys = []
        for keys in data_posted:
            all_keys.append(keys)
        if "name" in all_keys or data_posted["name"] != '':
            data = TeamService().edit_team(data_posted["name"])
            ret_data = {"success": True, "data": data}
        else:
            ret_data = {"success": False, "message": "Team name empty!"}
        ret = LoginService().get_token(user, ret_data)
        return ret
