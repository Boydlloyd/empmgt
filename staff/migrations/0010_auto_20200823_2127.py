# Generated by Django 3.0.7 on 2020-08-23 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0009_auto_20200822_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='empnumber',
            field=models.CharField(max_length=8, null=True, unique=True, verbose_name='Employee No.'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='tsnumber',
            field=models.CharField(max_length=8, null=True, unique=True, verbose_name='TS Number'),
        ),
    ]
