# Generated by Django 5.0 on 2023-12-18 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_manage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='img1',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='products',
            name='img2',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='products',
            name='img3',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='products',
            name='img4',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
