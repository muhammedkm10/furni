# Generated by Django 5.0 on 2024-01-11 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todelivery', '0020_proceedtocheckout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proceedtocheckout',
            name='addres',
        ),
    ]