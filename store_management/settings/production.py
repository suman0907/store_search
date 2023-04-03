from .base import *

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'store_management',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': '172-31-11-58',
        'PORT': '5432',
    }
}
