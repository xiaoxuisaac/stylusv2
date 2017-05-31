# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-31 20:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ums', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VocabVariables',
            fields=[
                ('request_id', models.CharField(max_length=125, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('glossary_dict', models.TextField(blank=True, null=True)),
                ('initial_select_table', models.TextField(blank=True, null=True)),
                ('select_table', models.TextField(blank=True, null=True)),
                ('quiz_select_table', models.TextField(blank=True, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mining_vocab_variables', to='ums.Profile')),
            ],
        ),
    ]
