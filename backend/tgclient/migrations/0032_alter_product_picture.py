# Generated by Django 3.2.3 on 2021-06-07 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgclient', '0031_product_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='picture',
            field=models.ImageField(blank=True, upload_to='uploads/'),
        ),
    ]
