# Generated by Django 5.0 on 2023-12-25 13:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("todelivery", "0006_remove_order_details_pro_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="ordered_items",
            name="product_name",
            field=models.CharField(default=0, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ordered_items",
            name="quantity",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
