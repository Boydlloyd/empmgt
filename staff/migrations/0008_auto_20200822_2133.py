# Generated by Django 3.0.7 on 2020-08-22 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0007_auto_20200820_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='mname',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='Middle Name'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='status',
            field=models.CharField(choices=[('Registred', 'Registered'), ('Pending', 'Pending'), ('Updated', 'Updated'), ('Approved', 'Approved'), ('Disapproved', 'Disapproved')], default='Registered', max_length=11, verbose_name='STATUS'),
        ),
    ]