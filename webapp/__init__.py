import importlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restful import Api
from sqlalchemy import create_engine

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# api_match_start = Api(app)
'''
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
connection = engine.connect()
table_models = importlib.import_module('cargo.models')
if not engine.dialect.has_table(connection, "User"):
    ORMTable = getattr(table_models, "User")
    ORMTable.__table__.create(bind=engine, checkfirst=True)

if not engine.dialect.has_table(connection, "Tournament"):
    ORMTable = getattr(table_models, "Tournament")
    ORMTable.__table__.create(bind=engine, checkfirst=True)

if not engine.dialect.has_table(connection, "Team"):
    ORMTable = getattr(table_models, "Team")
    ORMTable.__table__.create(bind=engine, checkfirst=True)

if not engine.dialect.has_table(connection, "Match"):
    ORMTable = getattr(table_models, "Match")
    ORMTable.__table__.create(bind=engine, checkfirst=True)

if not engine.dialect.has_table(connection, "MapStats"):
    ORMTable = getattr(table_models, "MapStats")
    ORMTable.__table__.create(bind=engine, checkfirst=True)

if not engine.dialect.has_table(connection, "Registration"):
    ORMTable = getattr(table_models, "Registration")
    ORMTable.__table__.create(bind=engine, checkfirst=True)

if not engine.dialect.has_table(connection, "Servers"):
    ORMTable = getattr(table_models, "Servers")
    ORMTable.__table__.create(bind=engine, checkfirst=True)

if not engine.dialect.has_table(connection, "PlayerStats"):
    ORMTable = getattr(table_models, "PlayerStats")
    ORMTable.__table__.create(bind=engine, checkfirst=True)

if not engine.dialect.has_table(connection, "Rounds"):
    ORMTable = getattr(table_models, "Rounds")
    ORMTable.__table__.create(bind=engine, checkfirst=True)
'''
