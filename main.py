import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'stoutsd.settings'

# Google App Engine imports.
from google.appengine.ext.webapp import util

# Force Django to reload its settings.
from django.conf import settings
settings._target = None

import logging
import django.core.handlers.wsgi
import django.core.signals
import django.db
import django.dispatch.dispatcher

def log_exception (*args, **kwargs):
    logging.exception('Exception in request:')

# Log errors.
django.dispatch.dispatcher.connect(
    log_exception, django.core.signals.got_request_exception)

# Unregister the rollback event handler.
django.dispatch.dispatcher.disconnect(
    django.db._rollback_on_exception,
    django.core.signals.got_request_exception)

def main():
    util.run_wsgi_app(django.core.handlers.wsgi.WSGIHandler())

if __name__ == '__main__':
    main()
