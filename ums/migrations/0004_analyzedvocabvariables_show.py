# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-13 08:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ums', '0003_auto_20170509_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyzedvocabvariables',
            name='show',
            field=models.BooleanField(default=True),
        ),
    ]
