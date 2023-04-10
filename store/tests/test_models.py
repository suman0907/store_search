from django.test import TestCase
from rest_framework.test import APIClient

from store.models import Store
from django.contrib.gis.geos import Point

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.default_format = 'json'

    def test_create(self):
        longitude = 42.5
        latitude = 22.3
        store_name = "Skm Trader"
        geolocation = Point(longitude, latitude)
        store = Store.objects.create(store_name=store_name, longitude=42.5, latitude=22.3, geolocation=geolocation)
        self.assertEqual(str(store.__dict__['store_name']), str(store_name))

    def test_get_model(self):
        id = "0e627601-dbaa-453a-b329-977770a27ad6"
        response = self.client.get('/store/:id/' + id + '/')
        response_data = response.data['data']
        query_data = Store.objects.filter(id=id)
        self.assertEqual(len(response_data['data']), len(query_data))
        self.assertEqual(response.status_code, 200)