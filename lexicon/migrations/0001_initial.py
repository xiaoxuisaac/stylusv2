# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-31 20:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CocaDict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coca', models.DecimalField(decimal_places=4, max_digits=15)),
                ('bnc', models.DecimalField(decimal_places=4, max_digits=15)),
                ('soap', models.DecimalField(decimal_places=4, max_digits=15)),
                ('y1950_89', models.DecimalField(decimal_places=4, max_digits=15)),
                ('y1900_49', models.DecimalField(decimal_places=4, max_digits=15)),
                ('y1800s', models.DecimalField(decimal_places=4, max_digits=15)),
                ('coca_spok', models.DecimalField(decimal_places=4, max_digits=15)),
                ('coca_fic', models.DecimalField(decimal_places=4, max_digits=15)),
                ('coca_mag', models.DecimalField(decimal_places=4, max_digits=15)),
                ('coca_news', models.DecimalField(decimal_places=4, max_digits=15)),
                ('coca_acad', models.DecimalField(decimal_places=4, max_digits=15)),
                ('bnc_spok', models.DecimalField(decimal_places=4, max_digits=15)),
                ('bnc_fic', models.DecimalField(decimal_places=4, max_digits=15)),
                ('bnc_mag', models.DecimalField(decimal_places=4, max_digits=15)),
                ('bnc_news', models.DecimalField(decimal_places=4, max_digits=15)),
                ('bnc_noAc', models.DecimalField(decimal_places=4, max_digits=15)),
                ('bnc_acad', models.DecimalField(decimal_places=4, max_digits=15)),
                ('bnc_misc', models.DecimalField(decimal_places=4, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='CocaFreq',
            fields=[
                ('rank', models.IntegerField(primary_key=True, serialize=False)),
                ('headword', models.CharField(max_length=30)),
                ('lemma', models.CharField(max_length=30)),
                ('pos', models.CharField(max_length=30)),
                ('cap_freq', models.DecimalField(blank=True, decimal_places=17, max_digits=18, null=True)),
                ('us_uk', models.CharField(blank=True, max_length=5, null=True)),
                ('raw_freq', models.IntegerField()),
                ('freq_dict', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='as_freq', to='lexicon.CocaDict')),
            ],
        ),
        migrations.CreateModel(
            name='CollegiateRaw',
            fields=[
                ('alpha', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('data', models.TextField(max_length=50000)),
            ],
        ),
        migrations.CreateModel(
            name='EntryData',
            fields=[
                ('entry_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('dict_type', models.CharField(blank=True, max_length=50)),
                ('type_id', models.CharField(max_length=100)),
                ('headword', models.CharField(blank=True, max_length=100)),
                ('data', models.TextField(max_length=50000)),
            ],
        ),
        migrations.CreateModel(
            name='EntryPointer',
            fields=[
                ('entry_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('dict_type', models.CharField(blank=True, max_length=50)),
                ('type_id', models.CharField(max_length=100)),
                ('headword', models.CharField(blank=True, max_length=100)),
                ('pos', models.CharField(blank=True, max_length=50)),
                ('has_def', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='LearnerRaw',
            fields=[
                ('alpha', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('data', models.TextField(max_length=50000)),
            ],
        ),
        migrations.CreateModel(
            name='Ngrams',
            fields=[
                ('word', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('raw_freq', models.DecimalField(decimal_places=4, max_digits=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UndefinedWordPointer',
            fields=[
                ('word', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('undefined', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='WordPointer',
            fields=[
                ('word', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('lemmas', models.ManyToManyField(blank=True, related_name='derivations', to='lexicon.WordPointer')),
            ],
        ),
        migrations.AddField(
            model_name='ngrams',
            name='word_pointer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ngrams', to='lexicon.WordPointer'),
        ),
        migrations.AddField(
            model_name='entrypointer',
            name='derivations',
            field=models.ManyToManyField(related_name='dict_lemmas', to='lexicon.WordPointer'),
        ),
        migrations.AddField(
            model_name='entrypointer',
            name='word_pointer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dict_entry', to='lexicon.WordPointer'),
        ),
        migrations.AddField(
            model_name='entrydata',
            name='pointer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='data_model', to='lexicon.EntryPointer'),
        ),
        migrations.AddField(
            model_name='cocafreq',
            name='lemma_pointer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coca_as_lemma', to='lexicon.WordPointer'),
        ),
        migrations.AddField(
            model_name='cocafreq',
            name='raw_freq_dict',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='as_raw_freq', to='lexicon.CocaDict'),
        ),
        migrations.AddField(
            model_name='cocafreq',
            name='raw_text_dict',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='as_raw_text', to='lexicon.CocaDict'),
        ),
        migrations.AddField(
            model_name='cocafreq',
            name='text_dict',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='as_text', to='lexicon.CocaDict'),
        ),
        migrations.AddField(
            model_name='cocafreq',
            name='word_pointer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coca', to='lexicon.WordPointer'),
        ),
    ]
