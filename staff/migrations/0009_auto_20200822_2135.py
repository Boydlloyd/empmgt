# Generated by Django 3.0.7 on 2020-08-22 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0008_auto_20200822_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='mname',
            field=models.CharField(blank=True, max_length=20, verbose_name='Middle Name'),
        ),
    ]
