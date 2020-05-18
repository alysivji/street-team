# Generated by Django 3.0.6 on 2020-05-18 00:43

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [("teams", "0001_set_up_teams_model"), ("events", "0003_rename_table")]

    operations = [
        migrations.AddField(
            model_name="teamevent",
            name="team",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, related_name="events", to="teams.Team"
            ),
        ),
        migrations.AddField(
            model_name="teamevent", name="uuid", field=models.UUIDField(default=uuid.uuid4, null=True, unique=True)
        ),
    ]
