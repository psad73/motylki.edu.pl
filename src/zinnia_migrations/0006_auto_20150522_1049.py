# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zinnia', '0005_entry_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='priority',
            field=models.IntegerField(default=0, null=True, verbose_name='Priorytet', blank=True, choices=[(0, b'0 Domy\xc5\x9blny'), (1, b'1 Wyr\xc3\xb3\xc5\xbcniony'), (2, b'2 Istotny'), (3, b'3 Wa\xc5\xbcny'), (4, b'4 Wa\xc5\xbcniejszy'), (5, b'5 Bardzo wa\xc5\xbcny')]),
            preserve_default=True,
        ),
    ]
