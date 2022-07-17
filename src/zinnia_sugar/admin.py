# Copyright 2015 Brave Labs sp. z o.o.
# All rights reserved.
#
# This source code and all resulting intermediate files are CONFIDENTIAL and
# PROPRIETY TRADE SECRETS of Brave Labs sp. z o.o.
# Use is subject to license terms. See NOTICE file of this project for details.

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from zinnia.models.entry import Entry
from zinnia.admin.entry import EntryAdmin as ZinniaEntryAdmin


class EntryAdmin(ZinniaEntryAdmin):
    # In our case we put the gallery field
    # into the 'Content' fieldset
    fieldsets = (
                    (
                        _('Content'), {
                            'fields': (('title', 'status', 'priority'), 'content', ('image', 'gallery'), 'drive_folder')
                        }
                    ),
                 ) + ZinniaEntryAdmin.fieldsets[1:]


admin.site.register(Entry, EntryAdmin)
