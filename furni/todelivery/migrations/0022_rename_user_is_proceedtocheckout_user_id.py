# Generated by Django 5.0 on 2024-01-11 11:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("todelivery", "0021_remove_proceedtocheckout_addres"),
    ]

    operations = [
        migrations.RenameField(
            model_name="proceedtocheckout",
            old_name="user_is",
            new_name="user_id",
        ),
    ]
