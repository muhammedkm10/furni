# Generated by Django 5.0 on 2024-01-11 11:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("logintohome", "0004_customuser1_profile"),
        ("todelivery", "0019_ordered_items_size"),
    ]

    operations = [
        migrations.CreateModel(
            name="proceedtocheckout",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pay_method", models.CharField(max_length=50)),
                ("order_date", models.DateField()),
                ("addres", models.TextField()),
                ("total_amount", models.BigIntegerField(default=0)),
                ("applyed_coupen", models.IntegerField(null=True)),
                ("discount_amount", models.BigIntegerField(null=True)),
                (
                    "user_is",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="logintohome.customuser1",
                    ),
                ),
            ],
        ),
    ]
