# Generated by Django 3.0.6 on 2020-05-22 04:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0006_join_code_requires_less_states"),
        ("mediahub", "0006_require_fk_relationship"),
        ("events", "0005_make_fk_and_uuid_required"),
    ]

    operations = [migrations.RenameModel(old_name="TeamEvent", new_name="Event")]