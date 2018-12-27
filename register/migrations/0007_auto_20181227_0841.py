# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-12-27 00:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
        ('register', '0006_judgeinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='judgeinfo',
            name='name',
        ),
        migrations.AddField(
            model_name='judgeinfo',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='login.UserLogin'),
        ),
    ]
