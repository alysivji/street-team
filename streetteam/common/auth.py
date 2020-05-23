from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from apps.teams.models import Team


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class TeamAdminRoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        team_uuid = self.kwargs["uuid"]
        try:
            team = Team.objects.get(uuid=team_uuid)
        except Team.DoesNotExist:
            return False

        if self.request.user not in team.memberships.get_leadership():
            return False

        return True
