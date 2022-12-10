import importlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

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
