from django.test import TestCase
from rest_framework.test import APIClient
import json
from store.models import Store

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.default_format = 'json'

    def test_add_store_success(self):
        payload = {
            "store_name": "Nandu Croma Center",
            "longitude": 42.5,
            "latitude": 22.3
        }
        response = self.client.post('/store/', payload)
        self.assertEqual(response.status_code, 200)

    def test_add_store_failure(self):
        """
        provide invalid values to update
        :return: 400

        """
        payload = {
            "store_name": "Nandu Croma Center",
            "longitude": "43.5",
            "latitude": 22.3
        }
        response = self.client.post('/store/', payload)
        self.assertEqual(response.status_code, 400)

    def test_update_store_success(self):
        payload = {
            "store_name": "Nandu Croma Center",
            "longitude": 42.5,
            "latitude": 22.3
        }
        id = "0e627601-dbaa-453a-b329-977770a27ad6"
        response = self.client.put('/store/'+id, payload)
        self.assertEqual(response.status_code, 200)

    def test_update_store_failure(self):
        """
        provide invalid values to update
        :return: 400
        """
        payload = {
            "store_name": "Nandu Croma Center",
            "longitude": "42.5",
            "latitude": 22.3
        }
        id = "0e627601-dbaa-453a-b329-977770a27ad6"
        response = self.client.put('/store/'+id, payload)
        self.assertEqual(response.status_code, 400)

    def test_get_store_by_id_success(self):
        """
        provide valid id to search for
        :return: 400
        """
        id = "0e627601-dbaa-453a-b329-977770a27ad6"
        response = self.client.get('/store/:id/'+id + '/')
        response_data = response.data['data']
        query_data = Store.objects.filter(id=id)
        self.assertEqual(len(response_data['data']), len(query_data))
        self.assertEqual(response.status_code, 200)

    def test_get_store_by_id_failure(self):
        """
        provide invalid id to search for
        :return: 400
        """
        id = "0e627601-dbaa-453a-b329-977770a27a"
        response = self.client.get('/store/:id/'+id + '/')
        self.assertEqual(response.status_code, 400)

    def test_search_api_working(self):
        response = self.client.get('/store/search/'+'?longitude=34.5&latitude=23.4&distance=3')
        self.assertEqual(response.status_code, 200)

    def test_search_zero_distance(self):
        """
        Test for 0 distance in perimeter
        :return: query set should be empty
        """
        response = self.client.get('/store/search/'+'?longitude=34.5&latitude=23.4&distance=0')
        response_data = response.data['data']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['data'], [])
