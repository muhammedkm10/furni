# Generated by Django 4.2.7 on 2024-01-12 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todelivery', '0029_order_details_coupen_applyed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_details',
            name='after_discount',
            field=models.BigIntegerField(default=0),
        ),
    ]
