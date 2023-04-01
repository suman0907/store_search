from .base import *

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'store_management',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

GDAL_LIBRARY_PATH="/opt/homebrew/opt/gdal/lib/libgdal.dylib"
GEOS_LIBRARY_PATH="/opt/homebrew/opt/geos/lib/libgeos_c.dylib"
