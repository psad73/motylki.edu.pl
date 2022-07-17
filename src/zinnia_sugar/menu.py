# coding=utf-8
# Copyright 2015 Brave Labs sp. z o.o.
# All rights reserved.
#
# This source code and all resulting intermediate files are CONFIDENTIAL and
# PROPRIETY TRADE SECRETS of Brave Labs sp. z o.o.
# Use is subject to license terms. See NOTICE file of this project for details.

import logging
from cms.menu_bases import CMSAttachMenu
from django.core.urlresolvers import reverse
from menus.base import NavigationNode
from zinnia.managers import tags_published
from django.utils.translation import ugettext as __, ugettext_lazy as _


class TagMenu(CMSAttachMenu):
    """
    Menu for the tags
    """
    name = _('Zinnia Sugar Tag Menu')

    def get_nodes(self, request):
        """
        Return menu's node for tags
        """
        nodes = []
        for tag in tags_published():
            logging.error("########## tag: %s" % tag)
            nodes.append(NavigationNode(tag.name, reverse('tag_detail', args=[tag.name]), tag.pk, 'tags'))
        logging.error("######### nodes: %s" % nodes)
        return nodes
