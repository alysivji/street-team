# Generated by Django 2.2.6 on 2019-11-11 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("twilio_integration", "0001_create_phone_number_and_message_table")]

    operations = [
        migrations.AddField(model_name="phonenumber", name="created_at", field=models.DateTimeField(auto_now_add=True)),
        migrations.AddField(model_name="phonenumber", name="updated_at", field=models.DateTimeField(auto_now=True)),
        migrations.AddField(
            model_name="receivedmessage", name="created_at", field=models.DateTimeField(auto_now_add=True)
        ),
        migrations.AddField(model_name="receivedmessage", name="updated_at", field=models.DateTimeField(auto_now=True)),
    ]
