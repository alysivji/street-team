# Generated by Django 2.2.6 on 2019-11-18 02:50

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0001_replace_django_user_table")]

    operations = [
        migrations.AddField(model_name="user", name="uuid", field=models.UUIDField(default=uuid.uuid4, null=True))
    ]