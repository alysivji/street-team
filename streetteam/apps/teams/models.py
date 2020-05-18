import logging
import uuid

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
        return reverse("team-detail", args=[str(self.uuid)])


class UserTeam(BaseModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="memberships", on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name="members", on_delete=models.CASCADE)
    # position should be an enum: Organizer, Lead, Member

    objects = UserTeamManager()

    # state machine for invitation status: requested, accepted, rejected
