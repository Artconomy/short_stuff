from .lib import *
try:
    # Automatically registering the URL converter has to be done early
    # in the import proces-- it can't be used on AppConfig.ready, which
    # is not run until far after the URL configuration is initialized.
    from . import django
    from django.urls import register_converter

    from .django import converters
    register_converter(converters.ShortCodeConverter, 'short_code')
    del converters
    del register_converter
except ImportError:  # pragma: no cover
    pass
