from django.db import models


class UserTeamManager(models.Manager):
    # TODO test these
    def get_teams(self):
        return [relationship.team for relationship in self.all()]

    def get_members(self):
        return [relationship.user for relationship in self.all()]

    def get_leadership(self):
        from .models import UserTeamMembership

        return [
            membership.user
            for membership in self.all()
            if membership.position_state
            in [UserTeamMembership.PositionState.ORGANIZER, UserTeamMembership.PositionState.ADMIN]
        ]
