# Generated by Django 3.0.7 on 2020-08-16 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20200816_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='mobile',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
