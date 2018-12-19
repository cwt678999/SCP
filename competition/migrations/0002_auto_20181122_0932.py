# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2018-11-22 01:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='childcompetition',
            name='file',
        ),
        migrations.RemoveField(
            model_name='rootcompetition',
            name='file',
        ),
        migrations.RemoveField(
            model_name='rootcompetition',
            name='members',
        ),
        migrations.AddField(
            model_name='childcompetition',
            name='description',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
    ]
