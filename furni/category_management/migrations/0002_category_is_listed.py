# Generated by Django 5.0 on 2023-12-24 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_listed',
            field=models.BooleanField(default=True),
        ),
    ]