import factory

from ..models import Team, UserTeam
from apps.users.tests.factories import UserFactory


class TeamFactory(factory.DjangoModelFactory):
    class Meta:
        model = Team

    name = "Chicago Python"


class UserTeamMembershipFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserTeam

    user = factory.SubFactory(UserFactory)
    team = factory.SubFactory(TeamFactory)
    position_state = UserTeam.PositionState.MEMBER
