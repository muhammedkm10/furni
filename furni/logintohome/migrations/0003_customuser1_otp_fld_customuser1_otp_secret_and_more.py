# Generated by Django 5.0 on 2023-12-20 11:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("logintohome", "0002_customuser1_is_blocked"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser1",
            name="otp_fld",
            field=models.CharField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="customuser1",
            name="otp_secret",
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name="otpverification",
        ),
    ]
