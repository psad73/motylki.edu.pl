"""
WSGI config for website project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import logging
import os
import sys

print "Importing: %s" % __file__

logging.basicConfig(format='%(asctime)s %(levelname)-7s %(thread)-5d %(filename)s:%(lineno)s | %(funcName)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.disable(logging.NOTSET)
logging.getLogger().setLevel(logging.INFO)
logging.info('Loading %s', __name__)

import socket
PRODUCTION = False if socket.gethostname() in ('ODYN',) else True
DEBUG = True

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

# determine where is the single absolute path that
# will be used as a reference point for other directories
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Activate Virtual Environment
try:
    import virtualenv
    VE_NAME = ".pve"
    commands = "Scripts" if sys.platform == 'win32' else "bin"
    activate_this = os.path.join(SITE_ROOT, VE_NAME, commands, "activate_this.py")
    virtualenv.logger.notify("Activating: %s" % activate_this)
    execfile(activate_this, dict(__file__=activate_this))
    # this is required for Pip to run subprocess on the VE python
    # instead of the default one, the one used to call this script
    executable = sys.executable.rsplit(os.path.sep)[-1]
    sys.executable = os.path.join(SITE_ROOT, VE_NAME, commands, executable)
except ImportError:
    logging.info("Could not import virtualenv to activate. Assuming it's already activated")

SRC = os.path.join(SITE_ROOT, 'src')
if not SRC in sys.path:
    sys.path.insert(0, SRC)

# Show a debugging info on console
logging.debug("__file__ = %s", __file__)
logging.debug("sys.version = %s", sys.version)
logging.debug("os.getpid() = %s", os.getpid())
logging.debug("os.getcwd() = %s", os.getcwd())
logging.debug("os.curdir = %s", os.curdir)
logging.debug("sys.path:\n\t%s", "\n\t".join(sys.path))
logging.debug("PYTHONPATH:\n\t%s", "\n\t".join(os.environ.get('PYTHONPATH', "").split(';')))
logging.debug("sys.modules.keys() = %s", repr(sys.modules.keys()))
logging.debug("sys.modules.has_key('website') = %s", sys.modules.has_key('website'))
if 'website' in sys.modules:
    logging.debug("sys.modules['website'].__name__ = %s", sys.modules['website'].__name__)
    logging.debug("sys.modules['website'].__file__ = %s", sys.modules['website'].__file__)
logging.debug("os.environ['DJANGO_SETTINGS_MODULE']= %s", os.environ.get('DJANGO_SETTINGS_MODULE', None))
from django.conf import settings
settings._setup()
logging.debug("settings.__dir__: %s", settings.__dir__())
logging.debug("settings.DEBUG: %s", settings.DEBUG)

# Setup proper logging
from website.logcfg import setup_logging
log_file = os.path.join(SITE_ROOT, "logs", 'website.log')
setup_logging(log_file=log_file, console_verbosity=logging.DEBUG if PRODUCTION else logging.DEBUG)


def info(environ, start_response):
    headers = []
    headers.append(('Content-Type', 'text/plain'))
    write = start_response('200 OK', headers)

    input = environ['wsgi.input']
    import cStringIO
    output = cStringIO.StringIO()

    print >> output, "PID: %s" % os.getpid()
#    print >> output, "UID: %s" % os.getuid()
#    print >> output, "GID: %s" % os.getgid()
    print >> output

    keys = environ.keys()
    keys.sort()
    for key in keys:
        print >> output, '%s: %s' % (key, repr(environ[key]))
        print '%s: %s' % (key, repr(environ[key]))
    print >> output

    content_length = environ.get('CONTENT_LENGTH', '0')
    if content_length:
        output.write(input.read(int()))

    write(output.getvalue())
    return len(output.getvalue())


def log_exception(*args, **kwds):
    """Django signal handler to log an exception."""
    if sys:
        cls, err = sys.exc_info()[:2]
        logging.exception(u'Exception in request: %s: %s', cls.__name__, err)
    else:
        logging.exception(u'Exception in request (sys is None): %s %s', args, kwds)


def setup_django():
    # Log all exceptions detected by Django.
    # import django.core.signals
    # signal = django.core.signals.got_request_exception
    # signal.connect(log_exception)

    # Obtain WSGIHandler
    from django.core.wsgi import get_wsgi_application
    return get_wsgi_application()

try:
    application = setup_django()
except:
    logging.error("Django setup failed", exc_info=True)

# application = info
logging.debug("application: %s" % application)
