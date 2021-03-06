# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-02-02 12:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.db.migrations import RunPython


def remove_empty_links(apps, schema_editor):
    """
    Having empty links is bad and you should feel bad. Also, I'll delete them.
    """
    ProgrammePageHowToApply = apps.get_model('rca.ProgrammePageHowToApply')
    ProgrammePageKeyContent = apps.get_model('rca.ProgrammePageKeyContent')
    ProgrammePageFindOutMore = apps.get_model('rca.ProgrammePageFindOutMore')

    for l in ProgrammePageHowToApply.objects.filter(link__isnull=True):
        l.delete()

    for l in ProgrammePageKeyContent.objects.filter(link__isnull=True):
        l.delete()

    for l in ProgrammePageFindOutMore.objects.filter(link__isnull=True):
        l.delete()

def do_nothing(apps, schema_editor):
    pass  # Allows us to reverse this migration


class Migration(migrations.Migration):

    dependencies = [
        ('rca', '0069_auto_20170130_1415'),
    ]

    operations = [
        RunPython(remove_empty_links, do_nothing),
        migrations.AlterField(
            model_name='programmepagefindoutmore',
            name='link',
            field=models.ForeignKey(help_text=b'Find out more link', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Page'),
        ),
        migrations.AlterField(
            model_name='programmepagehowtoapply',
            name='link',
            field=models.ForeignKey(help_text=b'How to apply link', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='rca.StandardPage'),
        ),
        migrations.AlterField(
            model_name='programmepagekeycontent',
            name='link',
            field=models.ForeignKey(help_text=b'Key content link', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='rca.StandardPage'),
        ),
    ]
