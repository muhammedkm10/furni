# Generated by Django 5.0 on 2024-01-11 15:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coupenapp", "0001_initial"),
        ("todelivery", "0023_remove_proceedtocheckout_pay_method"),
    ]

    operations = [
        migrations.AlterField(
            model_name="proceedtocheckout",
            name="applyed_coupen",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="coupenapp.coupons",
            ),
        ),
    ]
