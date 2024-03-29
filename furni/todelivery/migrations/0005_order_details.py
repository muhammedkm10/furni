# Generated by Django 5.0 on 2023-12-25 10:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("logintohome", "0003_customuser1_otp_fld_customuser1_otp_secret_and_more"),
        ("product_manage", "0007_products_is_listed"),
        ("todelivery", "0004_address_post"),
    ]

    operations = [
        migrations.CreateModel(
            name="order_details",
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
                ("status", models.CharField(max_length=50)),
                ("order_date", models.DateField()),
                (
                    "pro_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product_manage.products",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="logintohome.customuser1",
                    ),
                ),
            ],
        ),
    ]
