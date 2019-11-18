# Generated by Django 2.2.6 on 2019-11-18 02:53

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0003_data_migration__fill_uuid_fields")]

    operations = [
        migrations.AlterField(model_name="user", name="uuid", field=models.UUIDField(default=uuid.uuid4, unique=True))
    ]
