from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import StoreSerializer
from .models import Store
import json
#from django.contrib.gis import gdal, geos
from .constants import *
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import Point




@api_view(http_method_names=['POST'])
def add_store(request):
    try:
        data = json.loads(request.body)
        print(data.get('id'))
        if data.get('id') is None:
            fetched_fields = data.keys()
            for field in store_req_fields:
                if field not in fetched_fields:
                    raise Exception("Missing Required field for store addition %s", field)
            data['geolocation'] = Point(data['longitude'], data['latitude'])
            serializer = StoreSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
        else:
            id = data['id']
            if (data.get('latitude') and data.get('longitude') is None) or (data.get('latitude') is None and data.get('longitude')):
                raise Exception("latitude or longitude cant be partially updated: Provide both values")
            if data.get('latitude') and data.get('longitude'):
                data['geolocation'] = Point(data['longitude'], data['latitude'])
            store_obj = Store.objects.filter(id=id)
            if store_obj:
                store_obj[0].update(**data)

        return Response(data={
            'message': 'successful',
            'success': True,
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data={
            "data": {
                "message": "Error: %s" % e,
            }, "success": False
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET', 'OPTIONS'])
def get_stores(request):
    try:
        longitude = request.query_params.get('longitude')
        latitude = request.query_params.get('latitude')
        distance = request.query_params.get('distance')
        if not longitude:
            raise Exception("Please provide longitude")
        if not latitude:
            raise Exception("Please provide latitude")
        if not distance:
            raise Exception("Please provide distance range")
        print(longitude, latitude)
        point = Point((float(longitude), float(latitude)), srid=4326)
        print(point)
        store_list = Store.objects.filter(
         geolocation__distance_lte=(point, Distance(m=distance*1000)))
        serializer = StoreSerializer(store_list, many=True)
        return Response({
            "data": {
                "data": serializer.data
            },
            "success": True
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data={
            "data": {
                "message": "Error: %s" % e,
            }, "success": False
        }, status=status.HTTP_400_BAD_REQUEST)





