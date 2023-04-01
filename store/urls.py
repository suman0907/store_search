from django.urls import path
from .views import *
from django.urls import re_path as url


urlpatterns = [
    url(r'^add_store/$', add_store),
    url(r'^get_stores/$', get_stores),
]