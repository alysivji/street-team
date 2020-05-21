from datetime import datetime, timezone

from dateutil.relativedelta import relativedelta
import pytest

from ..models import (
    can_perform_group_modifications,
    is_admin,
    team_was_just_created,
    Team,
    user_has_position_state_requested,
    user_is_only_member_of_team,
    UserTeamMembership,
)
from .factories import TeamFactory, UserTeamMembershipFactory
from apps.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestTeamModel:
    def test_create_and_retrieve_team(self):
        team = TeamFactory()

        record = Team.objects.first()

        assert record.name == team.name

    def test_generate_new_join_code(self):
        team = TeamFactory()
        old_code = team.join_code
        code = team.generate_new_join_code()

        record = Team.objects.first()

        assert record.join_code != old_code
        assert record.join_code == code


##############################################
# User to Team many-to-many relationship tests
##############################################
@pytest.mark.django_db
def test_user_is_only_member_of_team__happy_path():
    member = UserTeamMembershipFactory()
    assert user_is_only_member_of_team(member)


@pytest.mark.django_db
def test_user_is_only_member_of_team__group_has_two_members():
    first_member = UserTeamMembershipFactory(user=UserFactory())
    second_member = UserTeamMembershipFactory(user=UserFactory(), team=first_member.team)
    assert not user_is_only_member_of_team(second_member)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "position_state, expected_result",
    [
        (UserTeamMembership.PositionState.REQUESTED, True),
        (UserTeamMembership.PositionState.REJECTED, False),
        (UserTeamMembership.PositionState.WITHDREW, False),
        (UserTeamMembership.PositionState.RELEASED, False),
        (UserTeamMembership.PositionState.MEMBER, False),
        (UserTeamMembership.PositionState.TEAM_LEAD, False),
        (UserTeamMembership.PositionState.ORGANIZER, False),
        (UserTeamMembership.PositionState.ADMIN, False),
    ],
)
def test_user_has_position_state_requested(position_state, expected_result):
    membership = UserTeamMembershipFactory(user=UserFactory(), position_state=position_state)
    assert user_has_position_state_requested(membership) is expected_result


@pytest.mark.django_db
@pytest.mark.freeze_time
def test_team_was_just_created__happy_path(freezer):
    # Arrange
    now = datetime.now(timezone.utc)
    fifty_nine_seconds_ago = now - relativedelta(seconds=59)
    freezer.move_to(fifty_nine_seconds_ago)
    team = TeamFactory()
    membership = UserTeamMembershipFactory(team=team, position_state=UserTeamMembership.PositionState.REQUESTED)

    # Act
    freezer.move_to(now)
    result = team_was_just_created(membership)

    assert result is True


@pytest.mark.django_db
@pytest.mark.freeze_time
def test_team_was_just_created__boundary(freezer):
    # Arrange
    now = datetime.now(timezone.utc)
    sixty_seconds_ago = now - relativedelta(seconds=60)
    freezer.move_to(sixty_seconds_ago)
    team = TeamFactory()
    membership = UserTeamMembershipFactory(team=team, position_state=UserTeamMembership.PositionState.REQUESTED)

    # Act
    freezer.move_to(now)
    result = team_was_just_created(membership)

    assert result is False


@pytest.mark.django_db
@pytest.mark.freeze_time
def test_team_was_just_created__outside_boundary(freezer):
    # Arrange
    now = datetime.now(timezone.utc)
    over_sixty_seconds_ago = now - relativedelta(seconds=61)
    freezer.move_to(over_sixty_seconds_ago)
    team = TeamFactory()
    membership = UserTeamMembershipFactory(team=team, position_state=UserTeamMembership.PositionState.REQUESTED)

    # Act
    freezer.move_to(now)
    result = team_was_just_created(membership)

    assert result is False


@pytest.mark.django_db
@pytest.mark.parametrize(
    "position_state, expected_result",
    [
        (UserTeamMembership.PositionState.REQUESTED, False),
        (UserTeamMembership.PositionState.REJECTED, False),
        (UserTeamMembership.PositionState.WITHDREW, False),
        (UserTeamMembership.PositionState.RELEASED, False),
        (UserTeamMembership.PositionState.MEMBER, False),
        (UserTeamMembership.PositionState.TEAM_LEAD, False),
        (UserTeamMembership.PositionState.ORGANIZER, True),
        (UserTeamMembership.PositionState.ADMIN, True),
    ],
)
def test_can_perform_group_modifications(position_state, expected_result):
    user = UserFactory()
    membership = UserTeamMembershipFactory(user=user, position_state=position_state)
    assert can_perform_group_modifications(membership, user) is expected_result


@pytest.mark.django_db
@pytest.mark.parametrize(
    "position_state, expected_result",
    [
        (UserTeamMembership.PositionState.REQUESTED, False),
        (UserTeamMembership.PositionState.REJECTED, False),
        (UserTeamMembership.PositionState.WITHDREW, False),
        (UserTeamMembership.PositionState.RELEASED, False),
        (UserTeamMembership.PositionState.MEMBER, False),
        (UserTeamMembership.PositionState.TEAM_LEAD, False),
        (UserTeamMembership.PositionState.ORGANIZER, False),
        (UserTeamMembership.PositionState.ADMIN, True),
    ],
)
def test_is_admin(position_state, expected_result):
    user = UserFactory()
    membership = UserTeamMembershipFactory(user=user, position_state=position_state)
    assert is_admin(membership, user) is expected_result
