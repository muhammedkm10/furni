# Generated by Django 5.0 on 2024-01-01 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('afterlogin', '0007_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='stock',
        ),
    ]