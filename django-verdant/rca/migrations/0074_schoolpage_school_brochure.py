# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-02-01 09:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0007_merge'),
        ('rca', '0073_auto_20170201_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolpage',
            name='school_brochure',
            field=models.ForeignKey(blank=True, help_text=b'Link to the school brochure document', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.Document'),
        ),
    ]
