# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zinnia', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='content',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='image',
        ),
    ]
