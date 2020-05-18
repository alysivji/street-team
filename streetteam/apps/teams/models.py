import logging
import uuid

from django.db import models
from django.urls import reverse

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
    user = models.ForeignKey(User, related_name="teams", on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name="users", on_delete=models.CASCADE)
    # position should be an enum: Organizer, Lead, Member

    # state machine for invitation status: requested, accepted, rejected
