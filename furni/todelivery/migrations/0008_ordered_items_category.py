# Generated by Django 5.0 on 2023-12-26 04:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("todelivery", "0007_ordered_items_product_name_ordered_items_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="ordered_items",
            name="category",
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
