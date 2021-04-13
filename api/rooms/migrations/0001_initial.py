# Generated by Django 3.1.8 on 2021-04-13 21:13

import core.managers.redis_manager
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hotels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.CharField(db_index=True, editable=False, max_length=15, unique=True, verbose_name='public_id')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created date')),
                ('last_modified', models.DateTimeField(auto_now=True, null=True, verbose_name='last modified')),
                ('name', models.CharField(max_length=255)),
                ('hotel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hotel', to='hotels.hotel', verbose_name='hotel')),
            ],
            options={
                'verbose_name': 'room',
                'verbose_name_plural': 'rooms',
            },
            bases=(models.Model, core.managers.redis_manager.RedisConnection),
        ),
    ]
