# Generated by Django 3.0.7 on 2020-08-29 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_province_staffnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='district',
            name='staffnumber',
            field=models.IntegerField(default=0),
        ),
    ]