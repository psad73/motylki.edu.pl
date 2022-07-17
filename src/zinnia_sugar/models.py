# coding=utf-8
# Copyright 2015 Brave Labs sp. z o.o.
# All rights reserved.
#
# This source code and all resulting intermediate files are CONFIDENTIAL and
# PROPRIETY TRADE SECRETS of Brave Labs sp. z o.o.
# Use is subject to license terms. See NOTICE file of this project for details.

from django.db import models
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from filer.fields.folder import FilerFolderField
from filer.fields.image import FilerImageField
from zinnia.models_bases import entry
from django.utils.translation import ugettext as __, ugettext_lazy as _
from zinnia.preview import HTMLPreview
from zinnia_sugar.preview import SmartHTMLPreview


class Picture(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='gallery')


class Gallery(models.Model):
    title = models.CharField(max_length=50)
    pictures = models.ManyToManyField(Picture)

ENTRY_PRIORITY = (
    (0, '0 Domyślny'),
    (1, '1 Wyróżniony'),
    (2, '2 Istotny'),
    (3, '3 Ważny'),
    (4, '4 Ważniejszy'),
    (5, '5 Bardzo ważny'),
)


class Entry(
    entry.CoreEntry,
    entry.DiscussionsEntry,
    entry.RelatedEntry,
    entry.ExcerptEntry,
    entry.FeaturedEntry,
    entry.AuthorsEntry,
    entry.CategoriesEntry,
    entry.TagsEntry,
    entry.LoginRequiredEntry,
    entry.PasswordRequiredEntry,
    entry.ContentTemplateEntry,
    entry.DetailTemplateEntry):

    image = FilerImageField(blank=True, default=None, null=True, help_text=_('Used for illustration.'))
    gallery = FilerFolderField(blank=True, default=None, null=True, help_text=_('Attach a folder to make it a gallery entry.'))
    content = models.TextField(_('content'), blank=True)
    html_content = models.TextField(_('html_content'), default=None, blank=True, null=True)
    drive_folder = models.CharField(_('drive folder'), default=None, blank=True, null=True, max_length=250, help_text=_("Google drive folder ID to show in the entry"))
    priority = models.IntegerField(_('Priorytet'), default=0, blank=True, null=True, choices=ENTRY_PRIORITY)

    @property
    def html_preview(self):
        """
        Returns a preview of the "content" field formmated in HTML.
        """
        return SmartHTMLPreview(self.html_content)

    @property
    def word_count(self):
        """
        Counts the number of words used in the content.
        """
        return len(strip_tags(self.html_content).split())

    def __str__(self):
        return 'SugarEntry %s' % self.title

    class Meta(entry.CoreEntry.Meta):
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        from markdown import markdown
        self.html_content = markdown(self.content)
        super(Entry, self).save(force_insert, force_update, using, update_fields)

    @property
    def main_tag(self):
        return self.tags.split(",")[0] or u"aktualności"

    def preview_gallery(self):
        return self.gallery.files[:4]


    @cached_property
    def cover(self):
        if self.image:
            return self.image
        if self.gallery:
            return self.gallery.files.first()

