# Generated by Django 5.0 on 2023-12-25 08:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("todelivery", "0002_alter_address_pin"),
    ]

    operations = [
        migrations.RenameField(
            model_name="address",
            old_name="emial",
            new_name="email",
        ),
    ]
