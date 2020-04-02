SECRET_KEY = 'Please never use this in production I swear to god'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
    }
}

INSTALLED_APPS = (
   'short_stuff.tests.dummy_app',
)
