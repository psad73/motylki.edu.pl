# coding=utf-8
# Copyright 2015 Brave Labs sp. z o.o.
# All rights reserved.
#
# This source code and all resulting intermediate files are CONFIDENTIAL and
# PROPRIETY TRADE SECRETS of Brave Labs sp. z o.o.
# Use is subject to license terms. See NOTICE file of this project for details.

from classytags.arguments import Argument, KeywordArgument
from classytags.core import Options
from classytags.helpers import InclusionTag
from cms.templatetags.cms_tags import _show_placeholder_for_page, ShowPlaceholderById
from django.template.defaultfilters import truncatewords_html
from django.template.defaulttags import register
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from zinnia.models import Category, Entry


@register.inclusion_tag('zinnia/tags/dummy.html', takes_context=True)
def get_categories(context, template='zinnia/tags/categories.html'):
    """
    Return the published categories.
    """
    return {'template': template,
            'categories': Category.published.all(),
            'context_category': context.get('category')}


@register.inclusion_tag('zinnia/tags/dummy.html', takes_context=True)
def front_page_news(context, template='zinnia/entry_frontpage.html'):
    """
    Return the published categories.
    """
    return {
        'template': template,
        'object_list': Entry.objects.order_by("-priority", "-creation_date")[:12],
    }


class TeasePlaceholder(ShowPlaceholderById):
    template = 'cms/content.html'
    name = 'tease_placeholder'

    options = Options(
        Argument('placeholder_name'),
        Argument('reverse_id'),
        # Argument('lang', required=False, default=None),
        # Argument('site', required=False, default=None),
        Argument('words', required=False, default=None),
    )

    def get_context(self, *args, **kwargs):
        words = kwargs.pop("words")
        context = super(TeasePlaceholder, self).get_context(*args, **kwargs)
        if words:
            html = context["content"]
            # html = truncatewords_html(html, words)
            html = Truncator(html).words(words, html=True, truncate=u' […]')
            context["content"] = mark_safe(html)
        return context


    def get_kwargs(self, context, placeholder_name, reverse_id):
        cache_result = True
        if 'preview' in context['request'].GET:
            cache_result = False
        return {
            'context': context,
            'placeholder_name': placeholder_name,
            'page_lookup': reverse_id,
            # 'lang': lang,
            # 'site': site,
            'cache_result': cache_result,
        }

register.tag(TeasePlaceholder)

@register.filter(name='no_dash')
def no_dash(value):
    """Removes all values of arg from the given string"""
    return value.replace('-', ' ')
