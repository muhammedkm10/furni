# Generated by Django 5.0 on 2023-12-25 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todelivery', '0003_rename_emial_address_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='post',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]