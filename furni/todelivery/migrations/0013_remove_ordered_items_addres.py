# Generated by Django 5.0 on 2023-12-27 10:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("todelivery", "0012_remove_ordered_items_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ordered_items",
            name="addres",
        ),
    ]
