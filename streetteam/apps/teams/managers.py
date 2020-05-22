from django.db import models


class UserTeamManager(models.Manager):
    def get_teams(self):
        return [relationship.team for relationship in self.all()]

    def get_members(self):
        return [relationship.user for relationship in self.all()]
