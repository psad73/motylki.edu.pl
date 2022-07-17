# coding=utf-8
# Copyright (c) 2014 Janusz Skonieczny
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import logging
import os
import sys

DJANGO_SETTINGS_MODULE = "website.settings"
VE_NAME = ".pve"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(format='%(asctime)s %(levelname)-7s %(thread)-5d %(filename)s:%(lineno)s | %(funcName)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.DEBUG)
logging.disable(logging.NOTSET)
logging.info('Loading %s', __name__)

def activate_ve():
    global ve_bin, activate_script
    # Activate Virtual Environment
    ve_bin = "Scripts" if sys.platform == 'win32' else "bin"
    activate_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), VE_NAME, ve_bin, "activate_this.py")
    execfile(activate_script, dict(__file__=activate_script))


if __name__ == "__main__":
    activate_ve()

    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)

    from django.conf import settings
    from django.core.management import call_command
    logging.debug("settings.DATABASES: %s" % settings.DATABASES)
    import django
    django.setup()
    # call_command("syncdb", all=True, interactive=False)  # this will not prompt for sysop creation
    # call_command("schemamigration", initial=True, all=True)

    # call_command("migrate", auto=True)
    # --fake is help full when converting an app
    # http://south.readthedocs.org/en/latest/commands.html#options
    # call_command("migrate", fake=True)  #

    call_command("makemigrations")  #
    call_command("migrate")  #
    call_command("loaddata", os.path.join(ROOT_DIR, "fixtures", "all.json"))
    # call_command("loaddata", os.path.join(ROOT_DIR, "fixtures", "auth.json"))
    # call_command("loaddata", os.path.join(ROOT_DIR, "fixtures", "filer.json"))
    # call_command("loaddata", os.path.join(ROOT_DIR, "fixtures", "sites.json"))
    # call_command("loaddata", os.path.join(ROOT_DIR, "fixtures", "cms.json"))


def createsuperuser():
    """
    Almost automated sysop creation, add just passwords.
    For full auto use fixtures
    """
    from django.conf import settings
    if len(settings.ADMINS) > 0:
        import re
        sysop = settings.ADMINS[0]
        if not isinstance(sysop, basestring):
            sysop = sysop[0]
        sysop = "".join(re.findall("(?<=^)\w|(?<=\s)\w", sysop)).lower()
        print "Provide password for sysop account: {}".format(sysop)
        call_command("createsuperuser", username=sysop, email=settings.ADMINS[0][1])



