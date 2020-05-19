from django_fsm import TransitionNotAllowed
from .models import UserTeam


def make_user_admin_of_team(user, team):
    user_team_membership = UserTeam(user=user, team=team)
    user_team_membership.save()

    try:
        user_team_membership.make_user_admin_of_newly_created_group()
    except TransitionNotAllowed:
        pass
        # TODO log
        # TODO add a custom exception handler
        # https://rock-it.pl/custom-exception-handler-in-django/
    user_team_membership.save()
