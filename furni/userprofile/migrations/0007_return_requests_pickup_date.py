# Generated by Django 4.2.7 on 2024-01-21 07:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("userprofile", "0006_return_requests_return_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="return_requests",
            name="pickup_date",
            field=models.DateField(null=True),
        ),
    ]
