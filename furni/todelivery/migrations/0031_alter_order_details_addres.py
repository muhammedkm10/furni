# Generated by Django 4.2.7 on 2024-01-12 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("todelivery", "0030_order_details_after_discount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order_details",
            name="addres",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="todelivery.address"
            ),
        ),
    ]
