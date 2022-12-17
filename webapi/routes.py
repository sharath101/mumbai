from webapi import api
from webapi.controller.accounts import LoginController
from webapi.controller.testbearer import TestController


api.add_resource(LoginController, "/login")
api.add_resource(TestController, "/test")