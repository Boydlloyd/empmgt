# Generated by Django 3.0.7 on 2020-08-23 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20200823_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobileformat',
            name='mformat',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='serviceprovider',
            name='provider',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
