# Copyright 2015 Brave Labs sp. z o.o.
# All rights reserved.
#
# This source code and all resulting intermediate files are CONFIDENTIAL and
# PROPRIETY TRADE SECRETS of Brave Labs sp. z o.o.
# Use is subject to license terms. See NOTICE file of this project for details.
from bs4 import BeautifulSoup

from zinnia.preview import HTMLPreview


class SmartHTMLPreview(HTMLPreview):



    def build_preview(self):
        for splitter in self.splitters:
            if splitter in self.content:
                self.content = self.split(splitter)
        return self.truncate()


    def split(self, splitter):
        """
        Split the HTML content with a marker
        without breaking closing markups.
        """
        tease, more = self.content.split(splitter, 1)
        while not tease.strip():
            tease, more = more.split(splitter, 1)

        soup = BeautifulSoup(tease, 'html.parser')
        last_string = soup.find_all(text=True)[-1]
        last_string.replace_with(last_string.string + self.more_string)
        return soup
