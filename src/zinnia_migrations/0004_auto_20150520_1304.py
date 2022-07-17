# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zinnia', '0003_auto_20150515_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='content_template',
            field=models.CharField(default=b'zinnia/_entry_detail.html', help_text="Template used to display the entry's content.", max_length=250, verbose_name='content template', choices=[(b'zinnia/_entry_detail.html', 'Default template'), (b'zinnia/person.html', b'Osoba')]),
            preserve_default=True,
        ),
    ]
