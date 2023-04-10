import logging

from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import StoreSerializer
from .models import Store
import json
from .constants import *
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import Point




@api_view(http_method_names=['POST'])
def add_store(request):
    """
    :param request: required field to add a new store
    :return: 200 with success message
    """
    try:
        data = json.loads(request.body)
        fetched_fields = data.keys()
        for field in store_req_fields:
            if field not in fetched_fields:
                raise Exception("Missing Required field for store addition %s", field)
        data['geolocation'] = Point(data['longitude'], data['latitude'])
        serializer = StoreSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={
                'message': 'successful',
                'success': True,
            }, status=status.HTTP_200_OK)
        else:
            raise Exception("Error in Data serialization :%s", serializer.errors)

    except Exception as e:
        return Response(data={
            "data": {
                "message": "Error: %s" % e,
            }, "success": False
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(http_method_names=['PUT'])
def update_store(request, uuid):
    try:
        """
        :param request: required id of store and attributes to be updated
        :return: 200 with success message
        """
        data = json.loads(request.body)
        store_id = uuid

        if (data.get('latitude') and data.get('longitude') is None) or (
                data.get('latitude') is None and data.get('longitude')):
            raise Exception("latitude or longitude cant be partially updated: Provide both values")
        if data.get('latitude') and data.get('longitude'):
            data['geolocation'] = Point(data['longitude'], data['latitude'])

        store_obj = Store.objects.filter(id=store_id)
        if store_obj:
            store_obj[0].update(**data)

        return Response(data={
            'message': 'Update successful for store id: %s' % uuid,
            'success': True,
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(data={
            "data": {
                "message": "Error: %s" % e,
            }, "success": False
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(http_method_names=['GET'])
def get_store_by_id(request, uuid):
    """
    :param request: None(fetch store_id from url)
    :return: data with same store id or empty if not exists
    """
    try:
        store_id = uuid
        store_list = Store.objects.filter(id=store_id)
        result = []
        if store_list:
            serializer = StoreSerializer(store_list, many=True)
            result = serializer.data
        return Response({
            "data": {
                "data": result
            },
            "success": True
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data={
            "data": {
                "message": "Error: %s" % e,
            }, "success": False
        }, status=status.HTTP_400_BAD_REQUEST)



@api_view(http_method_names=['GET', 'OPTIONS'])
def search(request):
    """
    :param request: latitude, longitude and radius distance for store search
    :return: All the stores with matched params
    """
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

        point = Point((float(longitude), float(latitude)), srid=4326)

        store_list = Store.objects.filter(
         geolocation__distance_lte=(point, Distance(km=distance)))

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

@api_view(http_method_names=['GET', 'OPTIONS'])
def fetch_all_stores(request):
    """
    :param request: None
    :return: All the stores
    """
    try:
        store_list = Store.objects.all()
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







