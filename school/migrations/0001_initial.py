# Generated by Django 3.0.7 on 2020-08-15 21:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(max_length=30, unique=True, verbose_name='Location')),
                ('datecreated', models.DateTimeField(auto_now_add=True)),
                ('schoolnumber', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=30, unique=True, verbose_name='Province')),
                ('datecreated', models.DateTimeField(auto_now_add=True)),
                ('districtnumber', models.IntegerField(default=0)),
                ('schoolnumber', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Schoolmodule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datecreated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_code', models.IntegerField(unique=True)),
                ('school_name', models.CharField(max_length=50, unique=True, verbose_name='School Name')),
                ('school_address', models.CharField(max_length=50, unique=True, verbose_name='Address')),
                ('staffnumber', models.IntegerField(default=0)),
                ('datecreated', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='school.District')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='school.Province')),
            ],
        ),
        migrations.AddField(
            model_name='district',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='school.Province'),
        ),
    ]
