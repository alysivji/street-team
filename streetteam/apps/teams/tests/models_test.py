from dateutil.relativedelta import relativedelta
from django.db import IntegrityError
import pytest

from ..models import (
    can_perform_group_modifications,
    is_admin,
    team_was_just_created,
    Team,
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


@pytest.mark.django_db
class TestTeamUserMembershipModel:
    def test_create_and_retrieve_membership(self):
        membership = UserTeamMembershipFactory()

        record = UserTeamMembership.objects.first()

        assert record.user == membership.user
        assert record.team == membership.team

    def test_unique_together_constraint(self):
        membership = UserTeamMembershipFactory()
        user = membership.user
        team = membership.team

        with pytest.raises(IntegrityError):
            UserTeamMembershipFactory(user=user, team=team)


@pytest.mark.django_db
class TestUserTeamMembershipStateMachine:
    def test_user_is_only_member_of_team__happy_path(self):
        member = UserTeamMembershipFactory()
        assert user_is_only_member_of_team(member)

    def test_user_is_only_member_of_team__group_has_two_members(self):
        first_member = UserTeamMembershipFactory(user=UserFactory())
        second_member = UserTeamMembershipFactory(user=UserFactory(), team=first_member.team)
        assert not user_is_only_member_of_team(second_member)

    @pytest.mark.freeze_time
    def test_team_was_just_created__happy_path(self, freezer, ago):
        # Arrange
        now = ago()
        fifty_nine_seconds_ago = now - relativedelta(seconds=59)
        freezer.move_to(fifty_nine_seconds_ago)
        team = TeamFactory()
        membership = UserTeamMembershipFactory(team=team, position_state=UserTeamMembership.PositionState.MEMBER)

        # Act
        freezer.move_to(now)
        result = team_was_just_created(membership)

        assert result is True

    @pytest.mark.freeze_time
    def test_team_was_just_created__boundary(self, freezer, ago):
        # Arrange
        now = ago()
        sixty_seconds_ago = now - relativedelta(seconds=60)
        freezer.move_to(sixty_seconds_ago)
        team = TeamFactory()
        membership = UserTeamMembershipFactory(team=team, position_state=UserTeamMembership.PositionState.MEMBER)

        # Act
        freezer.move_to(now)
        result = team_was_just_created(membership)

        assert result is False

    @pytest.mark.freeze_time
    def test_team_was_just_created__outside_boundary(self, freezer, ago):
        # Arrange
        now = ago()
        over_sixty_seconds_ago = ago(seconds=61)
        freezer.move_to(over_sixty_seconds_ago)
        team = TeamFactory()
        membership = UserTeamMembershipFactory(team=team, position_state=UserTeamMembership.PositionState.MEMBER)

        # Act
        freezer.move_to(now)
        result = team_was_just_created(membership)

        assert result is False

    @pytest.mark.parametrize(
        "position_state, expected_result",
        [
            (UserTeamMembership.PositionState.WITHDREW, False),
            (UserTeamMembership.PositionState.RELEASED, False),
            (UserTeamMembership.PositionState.MEMBER, False),
            (UserTeamMembership.PositionState.TEAM_LEAD, False),
            (UserTeamMembership.PositionState.ORGANIZER, True),
            (UserTeamMembership.PositionState.ADMIN, True),
        ],
    )
    def test_can_perform_group_modifications(self, position_state, expected_result):
        user = UserFactory()
        membership = UserTeamMembershipFactory(user=user, position_state=position_state)
        assert can_perform_group_modifications(membership, user) is expected_result

    @pytest.mark.parametrize(
        "position_state, expected_result",
        [
            (UserTeamMembership.PositionState.WITHDREW, False),
            (UserTeamMembership.PositionState.RELEASED, False),
            (UserTeamMembership.PositionState.MEMBER, False),
            (UserTeamMembership.PositionState.TEAM_LEAD, False),
            (UserTeamMembership.PositionState.ORGANIZER, False),
            (UserTeamMembership.PositionState.ADMIN, True),
        ],
    )
    def test_is_admin(self, position_state, expected_result):
        user = UserFactory()
        membership = UserTeamMembershipFactory(user=user, position_state=position_state)
        assert is_admin(membership, user) is expected_result
