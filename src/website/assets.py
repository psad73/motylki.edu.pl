# coding=utf-8
# Copyright 2014 Janusz Skonieczny

import os
from os.path import normcase

from webassets import Bundle
from django_assets import Bundle, register

CSS = (
    # vendor
    "vendor/font-awesome/css/font-awesome.css",
    "vendor/eonasdan-bootstrap-datetimepicker/build/css/bootstrap-datetimepicker.min.css",
    "vendor/fancybox/source/jquery.fancybox.css",
    "vendor/flexslider/flexslider.css",
    # assets
    # "assets/file-uploader/fineuploader.css",
    #"select2/select2-bootstrap.css",
    "assets/css/bootstrap.css",
    "assets/css/screen.css",
)

JS = (
    # load it fast
    "assets/js/facebook.js",

    # vendor
    "vendor/jquery/dist/jquery.js",
    "vendor/jquery-ui/jquery-ui.js",
    "vendor/jquery-ui/ui/i18n/datepicker-pl.js",
    "vendor/bootstrap-sass-official/assets/javascripts/bootstrap.js",

    # <script src="{% static "bootstrap-sass-official/assets/javascripts/bootstrap/affix.js" %}"></script>
    # <script src="{% static "bootstrap-sass-official/assets/javascripts/bootstrap/button.js" %}"></script>
    # <script src="{% static "bootstrap-sass-official/assets/javascripts/bootstrap/carousel.js" %}"></script>
    # <script src="{% static "bootstrap-sass-official/assets/javascripts/bootstrap/collapse.js" %}"></script>
    # <script src="{% static "bootstrap-sass-official/assets/javascripts/bootstrap/dropdown.js" %}"></script>
    # <script src="{% static "bootstrap-sass-official/assets/javascripts/bootstrap/tab.js" %}"></script>
    # <script src="{% static "bootstrap-sass-official/assets/javascripts/bootstrap/transition.js" %}"></script>
    # <script src="{% static "bootstrap-sass-official/assets/javascripts/bootstrap/scrollspy.js" %}"></script>
    # <script src="{% static "bootstrap-sass-official/assets/javascripts/bootstrap/modal.js" %}"></script>
    # <script src="{% static "bootstrap-sass-official/assets/javascripts/bootstrap/tooltip.js" %}"></script>
    # <script src="{% static "bootstrap-sass-official/assets/javascripts/bootstrap/popover.js" %}"></script>

    "vendor/select2/select2.js",
    "vendor/moment/moment.js",
    "vendor/eonasdan-bootstrap-datetimepicker/src/js/bootstrap-datetimepicker.js",
    "vendor/fancybox/source/jquery.fancybox.js",
    "vendor/flexslider/jquery.flexslider.js",
    # assets
    "assets/js/html5boilerplate-logging.js",
    "assets/js/datetimepicker.js",
    "assets/js/google-analitycs.js",
    "assets/js/boot.fancybox.js",
    "assets/js/pspo.js",
)

IE_JS = (
    "vendor/html5shiv/dist/html5shiv.js",
    "vendor/respond/dest/respond.src.js",
)

JS = [normcase(f) for f in JS]
IE_JS = [normcase(f) for f in IE_JS]
CSS = [normcase(f) for f in CSS]


register('js', Bundle(*JS, filters='yui_js', output='script.%(version)s.js'))
register('js_ie', Bundle(*IE_JS, filters='yui_js', output='script.ie.%(version)s.js'))
register('css', Bundle(*CSS, filters='yui_css', output='style.%(version)s.css'))
