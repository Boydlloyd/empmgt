# Generated by Django 3.0.7 on 2020-09-04 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20200904_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='mobileformat',
            name='length',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.DO_NOTHING, to='account.Mobilelength'),
            preserve_default=False,
        ),
    ]