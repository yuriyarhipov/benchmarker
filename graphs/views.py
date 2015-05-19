from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', ])
def graphs(request):
    return Response()

@api_view(['POST', 'GET'])
def legends(request):
    return Response()