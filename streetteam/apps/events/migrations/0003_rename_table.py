# Generated by Django 3.0.6 on 2020-05-18 00:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("mediahub", "0006_require_fk_relationship"), ("events", "0002_improve_field_name")]

    operations = [migrations.RenameModel(old_name="Event", new_name="TeamEvent")]