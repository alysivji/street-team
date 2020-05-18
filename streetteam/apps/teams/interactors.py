from .models import UserTeam


def add_user_team_relationship(user, team):
    user_team_relationship = UserTeam(user=user, team=team)
    user_team_relationship.save()
