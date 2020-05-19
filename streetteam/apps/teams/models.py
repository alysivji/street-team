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


class UserTeam(BaseModel):
    """TODO rename to UserTeamMembership"""

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="memberships", on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name="memberships", on_delete=models.CASCADE)

    objects = UserTeamManager()

    class PositionState:
        """Position user holds in group"""

        REQUESTED = "request_to_join"  # user has requested to join team
        REJECTED = "request_rejected"  # user request to join team has been rejected
        WITHDREW = "withdrew_from_team"  # user has withdrawn from team, removed request
        RELEASED = "released_by_team"  # team admin has released user from team
        MEMBER = "community_member"  # can send pictures and add captions for own images
        TEAM_LEAD = "team_lead"  # can crop pictures and modify captions and approve for posting
        ORGANIZER = "organizer"  # create events and invite members
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
    def make_user_admin_of_newly_created_group(self, by):
        pass
