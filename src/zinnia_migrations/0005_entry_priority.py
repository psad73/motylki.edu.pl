# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zinnia', '0004_auto_20150520_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='priority',
            field=models.IntegerField(default=0, null=True, verbose_name='Priorytet', blank=True),
            preserve_default=True,
        ),
    ]
