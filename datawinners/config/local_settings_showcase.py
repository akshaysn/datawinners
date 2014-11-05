SITE_ID = 2
DEBUG = False
TEMPLATE_DEBUG = False
COMPRESS_ENABLED = True

ADMINS = (('DWBLR', 'datawinnersblr@thoughtworks.com'),)

COMPRESS = False

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'mangrove',                      # Or path to database file if using sqlite3.
        'USER': 'mangrover',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

API_KEYS = {
    '184.72.223.168': 'AIzaSyCr4DDqoKgR5MzPci7GHWaXms8bYNprY-g'
}

HNI_SUPPORT_EMAIL_ID = 'datawinnersblr@thoughtworks.com'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'test.datawinners@gmail.com'
EMAIL_HOST_PASSWORD = 'd@t@winner'
EMAIL_PORT = 587

COUCHDBMAIN_USERNAME = 'admin'
COUCHDBMAIN_PASSWORD = 'admin'
COUCHDBMAIN_CREDENTIALS = (COUCHDBMAIN_USERNAME, COUCHDBMAIN_PASSWORD)
COUCHDBFEED_USERNAME = 'admin'
COUCHDBFEED_PASSWORD = 'admin'
COUCHDBFEED_CREDENTIALS = (COUCHDBFEED_USERNAME, COUCHDBFEED_PASSWORD)

CRS_ORG_ID = 'JHW14178'

FEEDS_ENABLED=True
MAX_FEED_ENTRIES=10000

VUMI_API_URL = "http://41.77.23.82:7000"

GOOGLE_MAPS_ENABLED = True
GOOGLE_ANALYTICS_ENABLED = False
