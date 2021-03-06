# Generated by Django 2.2.6 on 2019-12-03 05:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("twilio_integration", "0003_add_account_link_state_column_to_phonenumber"),
    ]

    operations = [
        migrations.AddField(
            model_name="phonenumber",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="phone_numbers",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="receivedmessage",
            name="phone_number",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="messages",
                to="twilio_integration.PhoneNumber",
            ),
        ),
    ]
