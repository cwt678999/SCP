# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-12-26 04:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0009_auto_20181226_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='competition',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
