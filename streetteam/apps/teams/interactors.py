from .models import UserTeamMembership


def make_user_admin_of_team(user, team):
    user_team_membership = UserTeamMembership(user=user, team=team)
    user_team_membership.save()

    user_team_membership.make_admin_of_newly_created_group(by=user)
    # except TransitionNotAllowed:
    # pass
    # TODO log
    # TODO add a custom exception handler
    # https://rock-it.pl/custom-exception-handler-in-django/
    user_team_membership.save()
