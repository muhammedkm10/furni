# Generated by Django 5.0 on 2024-01-04 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_manage', '0007_products_is_listed'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='original_price',
            field=models.IntegerField(null=True),
        ),
    ]