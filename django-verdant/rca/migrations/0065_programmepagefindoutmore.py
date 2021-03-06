# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-24 09:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0029_unicode_slugfield_dj19'),
        ('rca', '0064_auto_20170124_0935'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgrammePageFindOutMore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_text', models.CharField(blank=True, help_text=b'', max_length=255)),
                ('link', models.ForeignKey(blank=True, help_text=b'', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Page')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='find_out_more', to='rca.ProgrammePage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
