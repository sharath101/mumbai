from webapi import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return {"success": False,
            "message": "Access Denied"}, 403


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    ign = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    steamid = db.Column(db.String, unique=True)
    picture = db.Column(db.String)


class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    max_teams = db.Column(db.Integer)
    prize = db.Column(db.String)
    reg_start_date = db.Column(db.String)
    reg_start_time = db.Column(db.String)
    reg_end_date = db.Column(db.String)
    reg_end_time = db.Column(db.String)
    tour_start = db.Column(db.String)
    tour_end = db.Column(db.String)
    tour_type = db.Column(db.String)
    reg_no = db.Column(db.Integer, default=0)
    reg_open = db.Column(db.Boolean, default=True)
    rules = db.Column(db.String)
    admin_wh = db.Column(db.String)
    players_wh = db.Column(db.String)
    discord_invite = db.Column(db.String)
    organiserId = db.Column(db.Integer)


class MapList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    map_code = db.Column(db.String)
    tour_id = db.Column(db.Integer)


class MatchStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer)
    match_ident = db.Column(db.Integer)
    status = db.Column(db.Integer, nullable=False, default=0)
    team1_id = db.Column(db.Integer)
    team2_id = db.Column(db.Integer)
    winner = db.Column(db.Integer)
    forfeit = db.Column(db.Boolean, default=False)
    team1_score = db.Column(db.Integer, default=0)
    team2_score = db.Column(db.Integer, default=0)
    api_key = db.Column(db.String)


class Servers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String)
    rcon_pass = db.Column(db.String, nullable=False)
    port = db.Column(db.Integer, nullable=False, default=27015)
    ip = db.Column(db.String, nullable=False)
    tour_id = db.Column(db.Integer)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    captain = db.Column(db.Integer)
    name = db.Column(db.String(15), nullable=False)
    flag = db.Column(db.String(2), nullable=False, default='FR')
    logo = db.Column(db.String(4), nullable=False, default='nip')
    p0 = db.Column(db.Integer)
    p1 = db.Column(db.Integer)
    p2 = db.Column(db.Integer)
    p3 = db.Column(db.Integer)
    p4 = db.Column(db.Integer)
    p5 = db.Column(db.Integer)
    p6 = db.Column(db.Integer)
    p7 = db.Column(db.Integer)
    p8 = db.Column(db.Integer)
    p9 = db.Column(db.Integer)


class TournamentTeam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    captain = db.Column(db.Integer)
    name = db.Column(db.String(15), nullable=False)
    flag = db.Column(db.String(2), nullable=False, default='FR')
    logo = db.Column(db.String(4), nullable=False, default='nip')
    p0 = db.Column(db.Integer)
    p1 = db.Column(db.Integer)
    p2 = db.Column(db.Integer)
    p3 = db.Column(db.Integer)
    p4 = db.Column(db.Integer)
    p5 = db.Column(db.Integer)


class StageStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer)
    map_number = db.Column(db.Integer)
    map_name = db.Column(db.String(64))
    winner = db.Column(db.Integer)
    team1_score = db.Column(db.Integer, default=0)
    team2_score = db.Column(db.Integer, default=0)

    @staticmethod
    def get_or_create(match_id, map_number, map_name=''):
        match = MatchStats.query.filter_by(matchid=match_id).first()
        if match is None:
            return None

        rv = StageStats.query.filter_by(
            match_id=match_id, map_number=map_number).first()
        if rv is None:
            rv = StageStats()
            rv.match_id = match_id
            rv.map_number = map_number
            rv.map_name = map_name
            rv.team1_score = 0
            rv.team2_score = 0
            db.session.add(rv)
        return rv


class PlayerStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer)
    map_id = db.Column(db.Integer)
    team_id = db.Column(db.Integer)
    steam_id = db.Column(db.String(40))
    name = db.Column(db.String(40))
    kills = db.Column(db.Integer, default=0)
    deaths = db.Column(db.Integer, default=0)
    roundsplayed = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    flashbang_assists = db.Column(db.Integer, default=0)
    teamkills = db.Column(db.Integer, default=0)
    suicides = db.Column(db.Integer, default=0)
    headshot_kills = db.Column(db.Integer, default=0)
    damage = db.Column(db.Integer, default=0)
    bomb_plants = db.Column(db.Integer, default=0)
    bomb_defuses = db.Column(db.Integer, default=0)
    v1 = db.Column(db.Integer, default=0)
    v2 = db.Column(db.Integer, default=0)
    v3 = db.Column(db.Integer, default=0)
    v4 = db.Column(db.Integer, default=0)
    v5 = db.Column(db.Integer, default=0)
    k1 = db.Column(db.Integer, default=0)
    k2 = db.Column(db.Integer, default=0)
    k3 = db.Column(db.Integer, default=0)
    k4 = db.Column(db.Integer, default=0)
    k5 = db.Column(db.Integer, default=0)
    firstkill_t = db.Column(db.Integer, default=0)
    firstkill_ct = db.Column(db.Integer, default=0)
    firstdeath_t = db.Column(db.Integer, default=0)
    firstdeath_ct = db.Column(db.Integer, default=0)

    @staticmethod
    def get_or_create(matchid, mapnumber, steam_id):
        mapstats = StageStats.get_or_create(matchid, mapnumber)

        rv = PlayerStats.query.filter_by(match_id=matchid, steam_id=steam_id, map_id=mapstats.id).first()

        if rv is None:
            rv = PlayerStats()
            rv.match_id = matchid
            rv.map_number = mapstats.id
            rv.steam_id = steam_id
            rv.map_id = mapstats.id
            db.session.add(rv)

        return rv
