# coding=utf-8
"""
Django settings for website project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import logging
import os

logging.debug("Importing: %s" % __file__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

import socket

HOSTNAME = socket.gethostname()
DEV = HOSTNAME.lower() in ("odyn", "thor")
DEBUG = DEV
TEMPLATE_DEBUG = DEV

gettext = lambda s: s

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'txyg=3d9(gf_4-n!asdfa(*&98234)z5_b0t!9l'

ALLOWED_HOSTS = (
    'localhost',
    '127.0.0.1',
    'dev.example.com',
    'test.motylki.edu.pl',
    'cms.motylki.edu.pl',
    'motylki.edu.pl',
    'www.motylki.edu.pl',
    '46.101.171.42',
)
INTERNAL_IPS = ('127.0.0.1', '46.101.171.42')

ADMINS = (("Janusz Skonieczny", "js@pspo.edu.pl"),)
DEFAULT_FROM_EMAIL = "www@pspo.edu.pl"
SERVER_EMAIL = "www@pspo.edu.pl"


# Application definition

ROOT_URLCONF = 'website.urls'
WSGI_APPLICATION = 'website.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'pl'
TIME_ZONE = 'Europe/Warsaw'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')
STATIC_ROOT = os.path.join(ROOT_DIR, 'static')

STATICFILES_DIRS = (
    ('assets', os.path.join(ROOT_DIR, 'assets')),
    ('vendor', os.path.join(ROOT_DIR, 'vendor')),
)
SITE_ID = 1

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
    'app_namespace.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.csrf',
    'django.core.context_processors.tz',
    'sekizai.context_processors.sekizai',
    'django.core.context_processors.static',
    'cms.context_processors.cms_settings'
)

TEMPLATE_DIRS = (
    os.path.join(ROOT_DIR, 'templates'),
    os.path.join(ROOT_DIR, "templates", "errors"),
)

INSTALLED_APPS = (
    # Djanog CMS settings
    # 'djangocms_admin_style',  # for the admin skin. You **must** add 'djangocms_admin_style' in the list before 'django.contrib.admin'.
    'djangocms_text_ckeditor',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.redirects',

    'django_assets',
    'bootstrapform',
    'babeldjango',
    'debug_toolbar',
    'guardian',

    'cms',  # django CMS itself
    'mptt',  # utilities for implementing a modified pre-order traversal tree
    'menus',  # helper for model independent hierarchical website navigation
    'sekizai',  # for javascript and css management
    # 'djangocms_style',
    # 'djangocms_column',
    # 'djangocms_file',
    # 'djangocms_flash',
    # 'djangocms_googlemap',
    # 'djangocms_inherit',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_teaser',
    # 'djangocms_video',
    'djangocms_snippet',
    'reversion',
    'easy_thumbnails',
    'filer',
    # 'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_link',
    'cmsplugin_filer_image',
    # 'cmsplugin_filer_teaser',
    # 'cmsplugin_filer_video',

    'meta',
    'meta_mixin',
    'djangocms_page_meta',

    # Django Blog Zinnia
    'django_comments',
    'tagging',
    'zinnia_bootstrap',
    'zinnia',
    'cmsplugin_zinnia',
    # 'tinymce',
    # 'zinnia_tinymce',
    # 'sorl.thumbnail',
    # 'ckeditor',
    # 'zinnia_ckeditor',

    # other website settings
    'zinnia_sugar',
    # 'pspo',

)

import re
IGNORABLE_404_URLS = (
    re.compile(r'\.(php|cgi)$'),
    re.compile(r'^/admin/'),
    re.compile(r'^/phpmyadmin/'),
)

MIGRATION_MODULES = {
    'cms': 'cms.migrations_django',
    'menus': 'menus.migrations_django',
    'djangocms_snippet': 'djangocms_snippet.migrations_django',
    'djangocms_link': 'djangocms_link.migrations_django',
    'djangocms_teaser': 'djangocms_teaser.migrations_django',
    'djangocms_picture': 'djangocms_picture.migrations_django',
    'djangocms_text_ckeditor': 'djangocms_text_ckeditor.migrations_django',

    'filer': 'filer.migrations_django',
    'cmsplugin_filer_file': 'cmsplugin_filer_file.migrations_django',
    'cmsplugin_filer_folder': 'cmsplugin_filer_folder.migrations_django',
    'cmsplugin_filer_link': 'cmsplugin_filer_link.migrations_django',
    'cmsplugin_filer_image': 'cmsplugin_filer_image.migrations_django',
    'cmsplugin_filer_teaser': 'cmsplugin_filer_teaser.migrations_django',
    'cmsplugin_filer_video': 'cmsplugin_filer_video.migrations_django',

    # http://django-blog-zinnia.readthedocs.org/en/latest/how-to/extending_entry_model.html#considerations-about-the-database
    'zinnia': 'zinnia_migrations',
}

LANGUAGES = (
    # # Customize this
    ('pl', gettext('pl')),
    ('en', gettext('en')),
)

# django-guardian
# http://django-guardian.readthedocs.org/en/v1.2/configuration.html

ANONYMOUS_USER_ID = -1
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # this is default
    'guardian.backends.ObjectPermissionBackend',
)

DEBUG_TOOLBAR_PATCH_SETTINGS = False
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": 'zinnia_sugar.show_debug_toolbar',
}

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    # 'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

META_SITE_PROTOCOL = "http"
META_SITE_DOMAIN = "motylki.edu.pl"
META_USE_OG_PROPERTIES = True

CMS_LANGUAGES = {
    # # Customize this
    'default': {
        # Determines whether this language is accessible in the frontend.
        # You may want for example to keep a language private until your content has been fully translated.
        'public': True,
        # Hide untranslated pages in menus
        'hide_untranslated': False,
        # Determines behaviour when the preferred language is not available.
        # If True, will redirect to the URL of the same page in the fallback language.
        # If False, the content will be displayed in the fallback language, but there will be no redirect.
        'redirect_on_fallback': True,
        # A list of alternative languages, in order of preference, that are to be used if a page is not translated yet.
        'fallbacks': ['pl'],
    },
    1: [
        {
            'code': 'pl',
            'name': gettext('Polski'),
            'hide_untranslated': False,
        },
        {
            'name': gettext('Angielski'),
            'code': 'en',
            'hide_untranslated': False,
            'fallbacks': ['pl'],
        },
    ],
}

CMS_TEMPLATES = (
    ('article.html', u'Artykuł'),
    ('section.html', u'Artykuł i listą pod artykułów'),
    ('person.html', u'Osoba'),
    ('start.html', u'Startowa'),
)

CMS_PERMISSION = True
CMS_HIDE_UNTRANSLATED = False
CMS_SEO_FIELDS = True
CMS_MENU_TITLE_OVERWRITE = True
CMS_REDIRECTS = True
CMS_FLAT_URLS = True
CMS_TEMPLATE_INHERITANCE = False

CMS_PLACEHOLDER_CONF = {
    'post_image': {
        'plugins': ['PicturePlugin']
    },
    # 'post_content': {
    #     'plugins': ['TextPlugin', 'PicturePlugin', 'Text (Markdown)', 'SnippetPlugin']
    # },
}

TEXT_SAVE_IMAGE_FUNCTION = 'cmsplugin_filer_image.integrations.ckeditor.create_image_plugin'

CMSPLUGIN_FILER_FOLDER_STYLE_CHOICES = (
    ("gallery", "Galeria"),
    # ("list", "Lista"),
    ("slider", "Slajdy"),
)
CMSPLUGIN_FILER_FOLDER_DEFAULT_STYLE = "gallery"

SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations'
}


# django-assets
# http://django-assets.readthedocs.org/en/latest/settings.html

ASSETS_LOAD_PATH = STATIC_ROOT
ASSETS_ROOT = os.path.join(ROOT_DIR, 'assets', "compressed")
ASSETS_DEBUG = DEV  # Enable when testing compressed file in DEBUG mode
if ASSETS_DEBUG:
    ASSETS_URL = STATIC_URL
    ASSETS_MANIFEST = "json:{}".format(os.path.join(ASSETS_ROOT, "manifest.json"))
else:
    ASSETS_URL = STATIC_URL + "assets/compressed/"
    ASSETS_MANIFEST = "json:{}".format(os.path.join(STATIC_ROOT, 'assets', "compressed", "manifest.json"))
ASSETS_AUTO_BUILD = ASSETS_DEBUG
ASSETS_MODULES = ('website.assets',)

# Djrill: Mandrill Transactional Email for Django
# https://github.com/brack3t/Djrill
MANDRILL_API_KEY = "VOCTrKPr5FHb1Rqn063sCA"
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"

if DEV:
    # https://docs.djangoproject.com/en/1.6/topics/email/#console-backend
    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ZINNIA_ENTRY_BASE_MODEL = 'cmsplugin_zinnia.placeholder.EntryPlaceholder'
ZINNIA_ENTRY_BASE_MODEL = 'zinnia_sugar.models.Entry'
# ZINNIA_MARKUP_LANGUAGE = 'markdown'
ZINNIA_PREVIEW_SPLITTERS = ['<!-- more -->', '<!--more-->', 'h1', 'h2', 'h3']
ZINNIA_PREVIEW_MORE_STRING = u' […]'
ZINNIA_PING_EXTERNAL_URLS = False
ZINNIA_PING_DIRECTORIES = []

CMSPLUGIN_ZINNIA_HIDE_ENTRY_MENU = False
# CMSPLUGIN_ZINNIA_APP_MENUS = ['cmsplugin_zinnia.menu.TagMenu']
CMSPLUGIN_ZINNIA_APP_MENUS = ['zinnia_sugar.menu.TagMenu']
ZINNIA_ENTRY_CONTENT_TEMPLATES = [('zinnia/person.html', gettext('Osoba'))]
CKEDITOR_UPLOAD_PATH = "uploads/"

if DEV:
    from settings_dev import *
elif ROOT_DIR.endswith('dev'):
    from settings_qa import *
else:
    from settings_prd import *

logging.debug("DB: %s" % DATABASES['default']['NAME'])
logging.debug("DATABASES: %s" % DATABASES)
