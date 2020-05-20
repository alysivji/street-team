import factory

from ..models import Team, UserTeamMembership
from apps.users.tests.factories import UserFactory


class TeamFactory(factory.DjangoModelFactory):
    class Meta:
        model = Team

    name = "Chicago Python"


class UserTeamMembershipFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserTeamMembership

    user = factory.SubFactory(UserFactory)
    team = factory.SubFactory(TeamFactory)
    position_state = UserTeamMembership.PositionState.REQUESTED
