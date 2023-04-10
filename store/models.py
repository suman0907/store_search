from django.db import models
import uuid
import django.contrib.gis.gdal
from django.contrib.gis.db import models


# Create your models here.
class Store(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    store_name = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=30, null=True)
    active = models.BooleanField(null=True)
    address = models.CharField(max_length=1000, null=True)
    address_city = models.CharField(max_length=100, null=True)
    address_state = models.CharField(max_length=100, null=True)
    pincode = models.CharField(max_length=10, null=True)
    latitude = models.DecimalField(null=False, max_digits=50, decimal_places=20)
    longitude = models.DecimalField(null=False, max_digits=50, decimal_places=20)
    geolocation = models.PointField(srid=4326, null=False)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    @staticmethod
    def create(data):
        req_key = ['store_name', 'phone', 'active', 'address', 'address_city', 'address_state', 'pincode', 'latitude', 'longitude', 'geolocation']
        store_data = {x: data.get(x) or None for x in req_key}
        store = Store(**store_data)
        store.save()