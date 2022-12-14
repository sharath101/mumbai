from webapi import api
from webapi.controller.accounts import LoginController


api.add_resource(LoginController, "/login")
