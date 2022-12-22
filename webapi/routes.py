from webapi import api
from webapi.controller.accounts import LoginController, ProfileController

api.add_resource(LoginController, "/login")
api.add_resource(ProfileController, "/profile")
