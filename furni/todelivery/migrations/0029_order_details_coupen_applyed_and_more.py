# Generated by Django 4.2.7 on 2024-01-12 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todelivery', '0028_alter_proceedtocheckout_applyed_coupen'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_details',
            name='coupen_applyed',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='proceedtocheckout',
            name='coupen_applyed',
            field=models.BooleanField(default=False),
        ),
    ]
