# Generated by Django 4.2.7 on 2024-01-18 11:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userprofile", "0003_return_requests"),
    ]

    operations = [
        migrations.AddField(
            model_name="return_requests",
            name="reason",
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
