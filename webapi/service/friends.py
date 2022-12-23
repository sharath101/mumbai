from webapi import app, db
from webapi.models import User, Team
from webapi.service.accounts import get_userinfo


class FriendsService:
    def send_friend_request(self):
        pass


class SearchService:
    @staticmethod
    def search_users(query):
        results = User.query.msearch(query, limit=20).all()
        search_results = []
        for user in results:
            data = {"ign": user.ign,
                    "picture": app.config["SERVER_URL"] + user.picture,
                    "name": user.name}
            search_results.append(data)
        return search_results


class TeamService:
    def get_team(self):
        user = get_userinfo()
        team = Team.query.filter_by(captain=user.id).first()

        cap_data = {"ign": user.ign,
                    "picture": app.config["SERVER_URL"] + user.picture,
                    "name": user.name}
        if team:
            members = []
            data = {"captain": cap_data}
            for i in range(10):
                exists = False
                exec("exists = team.p" + str(i))
                if exists:
                    mem_data = False
                    exec("mem_data = User.query.filter_by(id=team.p" + str(i) + ").first()")
                    if mem_data:
                        mem_info = {"ign": mem_data.ign,
                                    "picture": app.config["SERVER_URL"] + mem_data.picture,
                                    "name": mem_data.name}
                        members.append(mem_info)
            data["name"] = team.name
            data["members"] = members
            return data
        else:
            return False

    def create_team(self, team_name):
        data = self.get_team()
        if data:
            user = get_userinfo()
            team = Team()
            team.name = team_name
            team.captain = user.id
            db.session.add(team)
            db.session.commit()
            data = self.get_team()
        return data

    def edit_team(self, team_name):
        user = get_userinfo()
        team = Team.query.filter_by(captain=user.id).first()
        team.name = team_name
        db.session.commit()
        data = self.get_team()
        return data
