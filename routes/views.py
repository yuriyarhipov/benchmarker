from rest_framework.decorators import api_view
from rest_framework.response import Response

from elements.models import Project
from models import StandartRoute
from routes.route import Route


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
    route = []
    distance = float(0)
    sr = StandartRoute.objects.get(id=route_id, project_id=project_id)
    route_files = sr.route_files.split(',')
    distance = sr.distance
    for f in route_files:
        file_distance, file_route = Route(f).get_points(distance)
        route.extend(file_route)
        distance = distance + file_distance

    return Response({'route': route, 'distance': distance})
