from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
@api_view(http_method_names=['GET', 'HEAD'])
def ping(request):
    print("hi")
    return Response({
        'message': 'successful',
        'success': True,
    })