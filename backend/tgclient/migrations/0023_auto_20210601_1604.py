# Generated by Django 3.2.3 on 2021-06-01 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgclient', '0022_alter_warehouseitem_receipt_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rack',
            name='rack_number',
            field=models.CharField(choices=[('С1', 'С1'), ('С2', 'С2'), ('С3', 'С3'), ('С4', 'С4'), ('С5', 'С5'), ('С6', 'С6'), ('С7', 'С7'), ('С8', 'С8'), ('С9', 'С9')], default='', max_length=2, verbose_name='стеллаж №'),
        ),
        migrations.AlterField(
            model_name='rack',
            name='section',
            field=models.CharField(choices=[('М1', 'М1'), ('М2', 'М2'), ('М3', 'М3')], default='', max_length=2, verbose_name='место'),
        ),
        migrations.AlterField(
            model_name='rack',
            name='shelf',
            field=models.CharField(choices=[('П1', 'П1'), ('П2', 'П2'), ('П3', 'П3'), ('П4', 'П4'), ('П5', 'П5'), ('П6', 'П6'), ('П7', 'П7'), ('П8', 'П8'), ('П9', 'П9')], default='', max_length=2, verbose_name='полка'),
        ),
    ]
