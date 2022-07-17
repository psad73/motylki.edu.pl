# coding=utf-8
# Copyright 2015 Brave Labs sp. z o.o.
# All rights reserved.
#
# This source code and all resulting intermediate files are CONFIDENTIAL and
# PROPRIETY TRADE SECRETS of Brave Labs sp. z o.o.
# Use is subject to license terms. See NOTICE file of this project for details.
import cgi

import logging
import os

logging.basicConfig(format='%(asctime)s %(levelname)-7s %(thread)-5d %(filename)s:%(lineno)s | %(funcName)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.DEBUG)
logging.disable(logging.NOTSET)
logging.info('Loading %s', __name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

import json
from datetime import datetime
from django.core.files import File
from django.db import transaction
from django.utils.html import strip_tags
from django.utils.text import Truncator, slugify
from django.contrib.sites.models import Site
from filer.models import Image, Folder
from pathlib import Path
from zinnia.managers import PUBLISHED
import requests

with open(str(Path('..').resolve() / 'data' / 'cms.json')) as db:
    dump = json.load(db)

with open(str(Path('..').resolve() / 'data' / 'menu.json')) as db:
    menu = json.load(db)

def by_url(nodes, url):
    for node in nodes:
        if node['url'] == url:
            return node
        rv = by_url(node['nodes'], url)
        if rv:
            return rv

nauczyciele = [n['key'] for n in by_url(menu, '/nauczyciele/')['nodes']]
absolwenci = [n['key'] for n in by_url(menu, '/nasi-absolwenci')['nodes']]


import django
django.setup()

covers = Folder.objects.get(pk=2)
galleries = Folder.objects.get(pk=1)

sites = [Site.objects.get(pk=1), Site.objects.get(pk=2)]

from zinnia.models.author import Author
author = Author.objects.get(pk=2)

entry_defaults = {
    "content_template": "zinnia/_entry_detail.html",
    "detail_template": "entry_detail.html",
    "start_publication": None,
    "pingback_enabled": True,
    # "related": [],
    "featured": False,
    "pingback_count": 0,
    "trackback_count": 0,
    "comment_enabled": True,
    "login_required": False,
    # "sites_set": sites,
    "comment_count": 0,
    "trackback_enabled": True,
    "end_publication": None,
    # "status": 2,
    # "authors_set": authors,
    "password": "",
    # "categories": []
}

def to_html(post):
    for box in post['boxes']:
        box = dump['boxes'][box["ref"]]
        kind = box["kind"]
        content = {
            "MarkdownBox": lambda box: box['text'],
            "HtmlBox": lambda box: box['html'],
            "PicasaGalleryBox": lambda box: "  ".join(box['urls']),
        }
        yield content[kind](box)


def to_date(s):
    import re
    return datetime(*map(int, re.split('\D', s)))


def download_image(url, name=None, **kwargs):
    logging.error("url: %s" % url)
    r = requests.get(url)
    if r.status_code == 200:
        if name is None:
            name = cgi.parse_header(r.headers['content-disposition'])[1]['filename']
        if "." in name:
            name, ext = name.rsplit(".", 1)
            name = str(slugify(unicode(name))) + "." + str(ext)
        else:
            name = str(slugify(unicode(name)))
        img_file = Path("./images/").absolute() / name
        if not img_file.parent.exists():
            img_file.parent.mkdir(parents=True)
        with open(str(img_file), 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)
        with open(str(img_file), 'rb') as f:
            file_obj = File(f, name=img_file.name)
            image = Image.objects.create(original_filename=img_file.name, file=file_obj, **kwargs)
        img_file.unlink()
        return image


def to_image(src, folder=covers):
    url = src['url']
    name = src['name']
    locy = int(float(src['focal_y']) * int(src['height']))
    locx = int(float(src['focal_x']) * int(src['width']))
    subject_location = str(locx) + "," + str(locy)
    return download_image(url, name, folder=folder, subject_location=subject_location)



posts = dump['posts']
logging.error("len(posts): %s" % len(posts))

from zinnia.models import Entry, Category
from cms.models import Page

def get_html(post):
    html = ""
    gallery = None
    for box in post['boxes']:
        box = dump['boxes'][box["ref"]]
        kind = box["kind"]
        if kind == "MarkdownBox":
            html += box['body']
        elif kind == "HtmlBox":
            html + box['html']
        elif kind == "PicasaGalleryBox":
            gallery = Folder.objects.filter(name=post['title']).first() or Folder.objects.create(name=title, parent=galleries)
            for i, url in enumerate(box['urls']):
                download_image(url, folder=gallery)
    return html, gallery


def page(post, parent, folder):
    from cms.api import create_page, add_plugin
    data = {
        "template": "person.html",
        "parent": parent,
        "publication_date": to_date(post['updated']),
        "published": True,
        "position": 'last-child',
        "language": "pl",
        "title": post['title'],
    }
    html, gallery = get_html(post)
    page = create_page(**data)
    cover = to_image(dump['images'][post['image']], folder)
    from djangocms_page_meta.models import PageMeta
    page.pagemeta = PageMeta(extended_object=page, image=cover)
    page.pagemeta.save()
    placeholder = page.placeholders.get(slot='page_content')
    add_plugin(placeholder, 'TextPlugin', 'pl', body=html)
    page.publish("pl")


nauczyciele_parent = Page.objects.get(pk=8)
# absolwenci_parent = Page.objects.get(pk=334)

teachers = Folder.objects.get(pk=211)
alumni = Folder.objects.get(pk=214)

for key in nauczyciele:
    page(posts[key], nauczyciele_parent, teachers)

# page(posts[nauczyciele[0]], nauczyciele_parent, teachers)

# for key in absolwenci:
#     page(posts[key], absolwenci_parent, alumni)



def entry(key, post):
    logging.error("key: %s" % key)
    e = Entry.objects.create(**entry_defaults)
    title = post['title']
    e.creation_date = to_date(post['created'])
    e.last_update = to_date(post['updated'])
    e.title = title
    e.slug = post['url'].split("/")[-1] or slugify(title)
    for s in sites:
        e.sites.add(s)
    e.authors.add(author)
    labels = post['labels']
    if labels:
        category, e.tags = labels[0], ",".join(labels)
        category = Category.objects.filter(title=category).first() or Category.objects.create(title=category, slug=slugify(category))
        e.categories.add(category)

    html = ""
    for box in post['boxes']:
        box = dump['boxes'][box["ref"]]
        kind = box["kind"]
        if kind == "MarkdownBox":
            html += box['text']
        elif kind == "HtmlBox":
            html + box['html']
        elif kind == "PicasaGalleryBox":
            gallery = Folder.objects.filter(name=title).first() or Folder.objects.create(name=title, parent=galleries)
            for i, url in enumerate(box['urls']):
                download_image(url, folder=gallery)
            e.gallery = gallery
    e.excerpt = Truncator(strip_tags(html)).words(50)
    e.content = html
    e.status = PUBLISHED

    with transaction.atomic():
        cover = post['image']
        if cover:
            logging.error("cover: %s" % cover)
            e.image = to_image(dump['images'][cover])
        e.save()

# for key, post in posts.items():
#     entry(key, post)



entry = {
  "fields": {
    "content_template": "zinnia/_entry_detail.html",
    "detail_template": "entry_detail.html",
    "start_publication": None,
    "pingback_enabled": True,
    "excerpt": "",
    "related": [],
    "creation_date": "2015-04-08T13:35:19Z",
    "featured": False,
    "pingback_count": 0,
    "trackback_count": 0,
    "comment_enabled": True,
    "title": "Wielkanocne \u017byczenia \u015awi\u0105teczne",
    "login_required": False,
    "sites": [
      2
    ],
    "last_update": "2015-04-08T13:39:58.956Z",
    "content": "",
    "comment_count": 0,
    "trackback_enabled": True,
    "end_publication": None,
    "image": "uploads/zinnia/2015/04/08/_mg_8160.JPG",
    "status": 2,
    "tags": "",
    "authors": [
      1
    ],
    "password": "",
    "slug": "wielkanocne-zyczenia-swiateczne",
    "categories": []
  },
  "model": "zinnia.entry",
  "pk": 1
}
