# Generated by Django 5.0 on 2023-12-26 03:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("afterlogin", "0005_alter_cart_total"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="category",
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
