# Copyright (C) 2008 Stout Public House. All Rights Reserved

import os

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
from django.core.signals import request_started, request_finished

def log_exception (*args, **kwargs):
    logging.exception('Exception in request:')

# Log errors.
request_started.connect(log_exception)

# Unregister the rollback event handler.
request_finished.disconnect(django.db._rollback_on_exception)

def main():
    util.run_wsgi_app(django.core.handlers.wsgi.WSGIHandler())

if __name__ == '__main__':
    main()
