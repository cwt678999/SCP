# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2019-01-06 07:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0002_file_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
