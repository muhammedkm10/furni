# Generated by Django 5.0 on 2023-12-24 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afterlogin', '0004_cart_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
