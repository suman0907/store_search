from django.urls import path
from .views import *
from django.urls import re_path as url


urlpatterns = [
    url(r'^$', add_store),
    url(r'^(?P<uuid>[0-9a-f\-]{32,})$', update_store),
    url(r'^search/$', search),
    url(r'^:id/(?P<uuid>[0-9a-f\-]{32,})/$', get_store_by_id),
    url(r'^all/$', fetch_all_stores),

]