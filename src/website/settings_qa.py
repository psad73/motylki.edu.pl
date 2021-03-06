# coding=utf-8
# Created 2014 by Janusz Skonieczny
import logging
import os

logging.debug("Importing: %s" % __file__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pspo_www_qa',
        'USER': 'pspo_www_qa',
        'PASSWORD': '?',
        'HOST': 'localhost'
    }
}
