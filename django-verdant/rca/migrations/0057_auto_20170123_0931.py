# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-01-23 09:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rca', '0056_auto_20170123_0924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programmepagecontactemail',
            name='page',
        ),
        migrations.RemoveField(
            model_name='programmepagecontactphone',
            name='page',
        ),
        migrations.RemoveField(
            model_name='programmepage',
            name='contact_address',
        ),
        migrations.RemoveField(
            model_name='programmepage',
            name='contact_link',
        ),
        migrations.RemoveField(
            model_name='programmepage',
            name='contact_link_text',
        ),
        migrations.RemoveField(
            model_name='programmepage',
            name='contact_title',
        ),
        migrations.DeleteModel(
            name='ProgrammePageContactEmail',
        ),
        migrations.DeleteModel(
            name='ProgrammePageContactPhone',
        ),
    ]
