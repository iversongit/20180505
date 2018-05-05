# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-02 10:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uauth', '0002_user_u_ticket'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_path_name', models.CharField(max_length=20, null=True)),
                ('c_path_count', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'request_count',
            },
        ),
    ]