# Generated by Django 3.0.7 on 2020-09-03 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0013_auto_20200829_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='districtstaff',
            name='gender',
            field=models.CharField(choices=[['M', 'Male'], ['F', 'Female']], max_length=1, null=True, verbose_name='Gender'),
        ),
    ]
