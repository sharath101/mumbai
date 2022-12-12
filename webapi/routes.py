from webapi import api
from webapi.accounts import Login


api.add_resource(Login, "/login")
