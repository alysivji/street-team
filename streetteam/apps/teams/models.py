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


def user_has_position_member(instance):
    if instance.position == UserTeam.PositionState.MEMBER:
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

    # TODO state machine for invitation status: requested, accepted, rejected
    # probably not the right place, but wanted to make a note

    # state machine for position
    class PositionState:
        """Has phone_number been linked to account"""

        MEMBER = "community_member"  # can send pictures and add captions for own images
        TEAM_LEAD = "team_lead"  # can crop pictures and modify captions and approve for posting
        ORGANIZER = "organizer"  # create events and invite members
        ADMIN = "admin"  # can change group settings

        CHOICES = [(MEMBER,) * 2, (TEAM_LEAD,) * 2, (ORGANIZER,) * 2, (ADMIN,) * 2]

        INITIAL_STATE = MEMBER

    position = FSMField(default=PositionState.INITIAL_STATE, choices=PositionState.CHOICES)

    @fsm_log_by
    @transition(
        field=position,
        source=PositionState.MEMBER,
        target=PositionState.ADMIN,
        conditions=[user_is_only_member_of_team, team_was_just_created],
    )
    def make_user_admin_of_newly_created_group(self, by):
        # TODO test audit log by
        pass
