import importlib
import os

from flask import Flask, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_login import LoginManager
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

from webapi import routes
from webapi.service.accounts import token_required, get_userinfo


@app.errorhandler(404)
def page_not_found(e):
    return {"success": False, "message": "404! Invalid URL!"}, 404


@app.route('/pics/<path:filename>', methods=['GET'])
def download(filename):
    uploads = os.path.join(app.config["PROFILE_PICS"], filename)
    return send_file(uploads, as_attachment=False)


@app.route('/bgpics', methods=['GET'])
def download_bg():
    uploads = os.path.join(app.config["BG_PICS"], "1.jpg")
    return send_file(uploads, as_attachment=False)


engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
connection = engine.connect()
table_models = importlib.import_module('webapi.models')
if not engine.dialect.has_table(connection, "User"):
    ORMTable = getattr(table_models, "User")
    ORMTable.__table__.create(bind=engine, checkfirst=True)

if not engine.dialect.has_table(connection, "Tournament"):
    ORMTable = getattr(table_models, "Tournament")
    ORMTable.__table__.create(bind=engine, checkfirst=True)

if not engine.dialect.has_table(connection, "MapList"):
    ORMTable = getattr(table_models, "MapList")
    ORMTable.__table__.create(bind=engine, checkfirst=True)

if not engine.dialect.has_table(connection, "MatchStats"):
    ORMTable = getattr(table_models, "MatchStats")
    ORMTable.__table__.create(bind=engine, checkfirst=True)

if not engine.dialect.has_table(connection, "Servers"):
    ORMTable = getattr(table_models, "Servers")
    ORMTable.__table__.create(bind=engine, checkfirst=True)

if not engine.dialect.has_table(connection, "Team"):
    ORMTable = getattr(table_models, "Team")
    ORMTable.__table__.create(bind=engine, checkfirst=True)

if not engine.dialect.has_table(connection, "TournamentTeam"):
    ORMTable = getattr(table_models, "TournamentTeam")
    ORMTable.__table__.create(bind=engine, checkfirst=True)

if not engine.dialect.has_table(connection, "PlayerStats"):
    ORMTable = getattr(table_models, "PlayerStats")
    ORMTable.__table__.create(bind=engine, checkfirst=True)

if not engine.dialect.has_table(connection, "StageStats"):
    ORMTable = getattr(table_models, "StageStats")
    ORMTable.__table__.create(bind=engine, checkfirst=True)
