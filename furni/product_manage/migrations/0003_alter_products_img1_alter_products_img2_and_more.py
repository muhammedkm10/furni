# Generated by Django 5.0 on 2023-12-18 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_manage', '0002_alter_products_img1_alter_products_img2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='img1',
            field=models.ImageField(upload_to='static/'),
        ),
        migrations.AlterField(
            model_name='products',
            name='img2',
            field=models.ImageField(upload_to='static/'),
        ),
        migrations.AlterField(
            model_name='products',
            name='img3',
            field=models.ImageField(upload_to='static/'),
        ),
        migrations.AlterField(
            model_name='products',
            name='img4',
            field=models.ImageField(upload_to='static/'),
        ),
    ]
