# Generated by Django 5.0 on 2023-12-27 10:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("todelivery", "0009_ordered_items_addres_ordered_items_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ordered_items",
            name="user_id",
            field=models.IntegerField(),
        ),
    ]
