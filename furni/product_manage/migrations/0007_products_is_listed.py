# Generated by Django 5.0 on 2023-12-20 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_manage', '0006_alter_products_img1_alter_products_img2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='is_listed',
            field=models.BooleanField(default=True),
        ),
    ]