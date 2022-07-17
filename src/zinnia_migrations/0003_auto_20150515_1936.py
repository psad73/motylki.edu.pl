# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.folder
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '__first__'),
        ('zinnia', '0002_auto_20150515_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='content',
            field=models.TextField(verbose_name='content', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='drive_folder',
            field=models.CharField(default=None, max_length=250, blank=True, help_text='Google drive folder ID to show in the entry', null=True, verbose_name='drive folder'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='gallery',
            field=filer.fields.folder.FilerFolderField(default=None, blank=True, to='filer.Folder', help_text='Attach a folder to make it a gallery entry.', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='html_content',
            field=models.TextField(default=None, null=True, verbose_name='html_content', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='image',
            field=filer.fields.image.FilerImageField(default=None, blank=True, to='filer.Image', help_text='Used for illustration.', null=True),
            preserve_default=True,
        ),
    ]
