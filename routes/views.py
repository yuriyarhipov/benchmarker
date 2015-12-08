from time import clock
from rest_framework.decorators import api_view
from rest_framework.response import Response

from elements.models import Project
from django.db import connection
from models import StandartRoute, RouteFile
from routes.route import StandartRoute as SR
from elements.tasks import write_points, create_route

from shapely.geometry import box, Point


@api_view(['POST', 'GET'])
def routes(request, project_id):
    project = Project.objects.get(id=project_id)
    data = []

    if request.method == 'POST':
        route_files = request.POST.get('files')
        route_name = request.POST.get('route_name')
        distance = request.POST.get('distance')
        color = request.POST.get('color')
        start_time = clock()
        StandartRoute.objects.filter(project=project, route_name=route_name).delete()
        sr = StandartRoute.objects.create(
            project=project,
            route_name=route_name,
            distance=distance,
            route_time='0',
            color=color,
            route_files=route_files)
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS StandartRoutes (route_id INT, longitude TEXT, latitude TEXT, row JSON)')
        sr = StandartRoute.objects.get(id=sr.id)
        route_files = sr.route_files.split(',')
        distance = sr.distance
        cursor.execute('DELETE FROM StandartRoutes WHERE (route_id=%s)', (sr.id, ))
        create_route.delay(sr.id, route_files, distance)
        sr.save()

    elif request.method == 'GET':
        for standart_route in StandartRoute.objects.filter(project=project).order_by('route_name'):
            data.append({
                'id': standart_route.id,
                'route_name': standart_route.route_name,
                'route_distance': standart_route.route_distance,
                'distance': standart_route.distance,
                'points_amount': standart_route.points_amount,
                'route_time': standart_route.route_time
            })

    return Response(data)


@api_view(['GET', 'DELETE'])
def route(request, project_id, route_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'GET':
        sr = StandartRoute.objects.get(id=route_id, project_id=project_id)
        route_id = sr.id
        route = SR(None).get_route(route_id, sr.color)
        return Response({
            'route': route[:1],
            'distance': sr.route_distance,
            'name': sr.route_name})

    elif request.method == 'DELETE':
        data = []
        StandartRoute.objects.filter(id=route_id, project_id=project_id).delete()
        for standart_route in StandartRoute.objects.filter(project=project).order_by('route_name'):
            data.append({
                'id': standart_route.id,
                'route_name': standart_route.route_name,
                'route_distance': standart_route.route_distance,
                'points_amount': standart_route.points_amount,
                'route_time': standart_route.route_time})
        return Response(data)


@api_view(['POST', ])
def route_frame(request, project_id, route_id):
    map_bounds = request.POST.get('bounds').split(',')
    map_box = box(
        float(map_bounds[1]),
        float(map_bounds[0]),
        float(map_bounds[3]),
        float(map_bounds[2]))
    sr = StandartRoute.objects.get(id=route_id, project_id=project_id)
    route_id = sr.id
    route = SR(None).get_route(route_id, sr.color)
    result = []
    for point in route:
        map_p = Point(point.get('lat'), point.get('lon'))
        if map_p.within(map_box):
            result.append(point)
    return Response(result)
