from rest_framework.decorators import api_view
from rest_framework.response import Response

from elements.models import Project
from models import StandartRoute
from lib.files import handle_uploaded_file
from lib.excel import Excel


@api_view(['POST', 'GET'])
def routes(request, project_id):
    project = Project.objects.get(id=project_id)
    data = []

    if request.method == 'POST':
        route_files = request.POST.get('files')
        route_name = request.POST.get('route_name')
        distance = request.POST.get('distance')
        StandartRoute.objects.create(
            project=project,
            route_name=route_name,
            distance=distance,
            route_files=route_files)

    elif request.method == 'GET':
        for standart_route in StandartRoute.objects.filter(project=project).order_by('route_name'):
            data.append({'id': standart_route.id, 'route_name': standart_route.route_name})
    return Response(data)


@api_view(['POST', 'GET'])
def route(request, project_id, route_id):
    data = []
    route_files = StandartRoute.objects.get(id=route_id, project_id=project_id).route_files.split(',')

    return Response(data)
