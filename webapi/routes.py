from webapi import api
from webapi.controller.accounts import LoginController, ProfileController
from webapi.controller.friends import SearchController, TeamController

api.add_resource(LoginController, "/login")
api.add_resource(ProfileController, "/profile")
api.add_resource(SearchController, "/search/<string:query>")
api.add_resource(TeamController, "/team")
