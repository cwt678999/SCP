# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-12-27 00:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
        ('competition', '0016_auto_20181227_0751'),
    ]

    operations = [
        migrations.AddField(
            model_name='rootcompetition',
            name='judge',
            field=models.ManyToManyField(null=True, related_name='juser', to='login.UserLogin'),
        ),
        migrations.AlterField(
            model_name='rootcompetition',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
