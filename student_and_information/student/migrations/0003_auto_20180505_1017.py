# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-05 02:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_studentinfo_s_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='s_chinese',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='s_operate_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='s_status',
            field=models.CharField(choices=[('NONE', '正常'), ('NEXT_SCH', '留级'), ('DROP_SCH', '退学'), ('LEAVE_SCH', '休学')], max_length=20, null=True),
        ),
    ]
