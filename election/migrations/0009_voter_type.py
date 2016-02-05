# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-04 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0008_auto_20160131_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='voter',
            name='type',
            field=models.SmallIntegerField(choices=[(0, 'ug'), (1, 'pg')], default=0),
        ),
    ]
