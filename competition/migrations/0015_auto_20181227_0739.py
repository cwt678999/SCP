# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-12-26 23:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
        ('competition', '0014_auto_20181226_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rootcompetition',
            name='img',
        ),
        migrations.AddField(
            model_name='rootcompetition',
            name='img',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='upload.File'),
        ),
    ]