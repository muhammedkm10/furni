# Generated by Django 5.0 on 2024-01-11 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todelivery', '0022_rename_user_is_proceedtocheckout_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proceedtocheckout',
            name='pay_method',
        ),
    ]