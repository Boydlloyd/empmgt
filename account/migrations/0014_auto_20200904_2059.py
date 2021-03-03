# Generated by Django 3.0.7 on 2020-09-04 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_auto_20200830_0045'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mobilelength',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.IntegerField(default=10)),
                ('datecreated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='mobileformat',
            name='length',
        ),
    ]