"""Management command to create superuser with parameters

We use this because the createsuperuser management command requires a password

To use:
    python streetteam/manage.py createsuperuser_parameterized \
        --email email@address.com
        --password admin-password

Code adapted from https://stackoverflow.com/a/42491469/4326704
"""

import logging
from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError

logger = logging.getLogger(__name__)


class Command(createsuperuser.Command):
    help = "If a superuser does not exist, create and allow password to be provided"

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            "--password", dest="password", default=None, help="Specifies the password for the superuser."
        )

    def handle(self, *args, **options):
        email = options.get("email")
        password = options.get("password")

        if not email or not password:
            raise CommandError("--email and --password are required")

        try:
            self.UserModel.objects.get(email=email)
        except self.UserModel.DoesNotExist:
            super(Command, self).handle(*args, **options)
            print("New user created")
        else:
            print("User already created")
            return

        user = self.UserModel.objects.get(email=email)
        user.set_password(password)
        user.save()
