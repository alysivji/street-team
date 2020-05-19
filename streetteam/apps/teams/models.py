from datetime import datetime, timedelta, timezone
import logging
import uuid

from django_fsm import FSMField, transition
from django_fsm_log.decorators import fsm_log_by
from django.db import models
from django.urls import reverse

from .managers import UserTeamManager
from apps.users.models import User
from common.models import BaseModel

logger = logging.getLogger(__name__)


class Team(BaseModel):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(null=False, max_length=255)

    def get_absolute_url(self):
        return reverse("teams:detail", args=[str(self.uuid)])


##############################################
# User to Team many-to-many relationship table
##############################################
def user_is_only_member_of_team(instance):
    conditions = {"team": instance.team}
    members = UserTeam.objects.filter(**conditions).all()
    if len(members) == 1 and members[0].user == instance.user:
        return True
    return False


def user_has_position_state_requested(instance):
    if instance.position_state == UserTeam.PositionState.REQUESTED:
        return True
    return False


def team_was_just_created(instance):
    if (datetime.now(timezone.utc) - instance.created_at) < timedelta(seconds=60):
        return True
    return False


def can_perform_group_modifications(instance, user):
    conditions = {"user": user, "team": instance.team}
    membership = UserTeam.objects.filter(**conditions).first()
    return membership.position in [UserTeam.PositionState.ORGANIZER, UserTeam.PositionState.ADMIN]


def is_admin(instance, user):
    conditions = {"user": user, "team": instance.team}
    membership = UserTeam.objects.filter(**conditions).first()
    return membership.position == UserTeam.PositionState.ADMIN


class UserTeam(BaseModel):
    """TODO rename to UserTeamMembership"""

    # TODO user, team are unique together

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="memberships", on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name="memberships", on_delete=models.CASCADE)

    objects = UserTeamManager()

    class PositionState:
        """Position user holds in group

        ADMIN to other states has a lot of complexity we haven't thought about
        """

        REQUESTED = "request_to_join"  # user has requested to join team
        REJECTED = "request_rejected"  # user request to join team has been rejected
        WITHDREW = "withdrew_from_team"  # user has withdrawn from team, removed request
        RELEASED = "released_by_team"  # team admin has released user from team
        MEMBER = "community_member"  # can send pictures and add captions for own images
        TEAM_LEAD = "team_lead"  # can crop pictures and modify captions and approve for posting
        ORGANIZER = "organizer"  # create events and approve invited members
        ADMIN = "admin"  # can change group settings

        CHOICES = [
            (REQUESTED,) * 2,
            (REJECTED,) * 2,
            (WITHDREW,) * 2,
            (RELEASED,) * 2,
            (MEMBER,) * 2,
            (TEAM_LEAD,) * 2,
            (ORGANIZER,) * 2,
            (ADMIN,) * 2,
        ]

        INITIAL_STATE = MEMBER

    position_state = FSMField(default=PositionState.REQUESTED, choices=PositionState.CHOICES)

    @fsm_log_by
    @transition(
        field=position_state,
        source=PositionState.REQUESTED,
        target=PositionState.ADMIN,
        conditions=[user_is_only_member_of_team, team_was_just_created, user_has_position_state_requested],
    )
    def make_admin_of_newly_created_group(self, by):
        pass

    @fsm_log_by
    @transition(
        field=position_state,
        source=PositionState.REQUESTED,
        target=PositionState.REJECTED,
        permission=can_perform_group_modifications,
    )
    def reject_request(self, by):
        pass

    @fsm_log_by
    @transition(
        field=position_state,
        source=PositionState.REQUESTED,
        target=PositionState.MEMBER,
        permission=can_perform_group_modifications,
    )
    def approve_application(self, by):
        pass

    @fsm_log_by
    @transition(
        field=position_state,
        source=[PositionState.MEMBER, PositionState.TEAM_LEAD],
        target=PositionState.ORGANIZER,
        permission=can_perform_group_modifications,
    )
    def promote_to_organizer(self, by):
        pass

    @fsm_log_by
    @transition(
        field=position_state,
        source=[PositionState.MEMBER, PositionState.ORGANIZER],
        target=PositionState.TEAM_LEAD,
        permission=can_perform_group_modifications,
    )
    def change_position_to_team_lead(self, by):
        pass

    @fsm_log_by
    @transition(
        field=position_state,
        source=[PositionState.TEAM_LEAD, PositionState.ORGANIZER],
        target=PositionState.MEMBER,
        permission=can_perform_group_modifications,
    )
    def change_position_to_member(self, by):
        pass

    @fsm_log_by
    @transition(field=position_state, source=PositionState.REQUESTED, target=PositionState.WITHDREW)
    def withdraw_application(self, by):
        pass

    @fsm_log_by
    @transition(
        field=position_state,
        source=[PositionState.MEMBER, PositionState.ORGANIZER, PositionState.TEAM_LEAD],
        target=PositionState.WITHDREW,
    )
    def quit_team(self, by):
        pass

    @fsm_log_by
    @transition(
        field=position_state,
        source=[PositionState.REJECTED, PositionState.WITHDREW, PositionState.RELEASED],
        target=PositionState.REQUESTED,
    )
    def reapply(self, by):
        # TODO can only reapply after meeting some requirement
        pass
