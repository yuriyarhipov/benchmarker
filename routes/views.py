from rest_framework.decorators import api_view
from rest_framework.response import Response

from elements.models import Project
from models import StandartRoute, RouteFile
from routes.route import Route, StandartRoute as SR
from elements.tasks import create_standart_route


@api_view(['POST', 'GET'])
def routes(request, project_id):
    project = Project.objects.get(id=project_id)
    data = []

    if request.method == 'POST':
        route_files = request.POST.get('files')
        route_name = request.POST.get('route_name')
        distance = request.POST.get('distance')
        sr = StandartRoute.objects.create(
            project=project,
            route_name=route_name,
            distance=distance,
            route_files=route_files)
        create_standart_route.delay(sr.id)


    elif request.method == 'GET':
        for standart_route in StandartRoute.objects.filter(project=project).order_by('route_name'):
            data.append({'id': standart_route.id, 'route_name': standart_route.route_name})
    return Response(data)


@api_view(['GET', ])
def route(request, project_id, route_id):
    distance = float(0)
    sr = StandartRoute.objects.get(id=route_id, project_id=project_id)
    route_id = sr.id
    route = SR(None).get_route(route_id)


    return Response({'route': route, 'distance': sr.route_distance})






















