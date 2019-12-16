# Generated by Django 2.2.6 on 2019-12-03 03:05

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [("twilio_integration", "0002_add_datetime_fields_to_model")]

    operations = [
        migrations.AddField(
            model_name="phonenumber",
            name="account_link_state",
            field=django_fsm.FSMField(
                choices=[
                    ("unlinked_phone_number", "unlinked_phone_number"),
                    ("attempt_phone_link", "attempt_phone_link"),
                    ("phone_link_success", "phone_link_success"),
                    ("phone_link_failed", "phone_link_failed"),
                ],
                default="unlinked_phone_number",
                max_length=50,
            ),
        )
    ]
