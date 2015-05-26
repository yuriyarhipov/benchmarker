from time import clock
from rest_framework.decorators import api_view
from rest_framework.response import Response

from elements.models import Project
from django.db import connection
from models import StandartRoute
from routes.route import StandartRoute as SR



@api_view(['POST', 'GET'])
def routes(request, project_id):
    project = Project.objects.get(id=project_id)
    data = []

    if request.method == 'POST':
        route_files = request.POST.get('files')
        route_name = request.POST.get('route_name')
        distance = request.POST.get('distance')
        start_time = clock()
        sr = StandartRoute.objects.create(
            project=project,
            route_name=route_name,
            distance=distance,
            route_time='0',
            route_files=route_files)
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS StandartRoutes (route_id INT, longitude TEXT, latitude TEXT)')
        sr = StandartRoute.objects.get(id=sr.id)
        route_files = sr.route_files.split(',')
        distance = sr.distance

        points = SR(route_files).get_points(distance)
        sr.route_distance = int(0)

        cursor.execute('DELETE FROM StandartRoutes WHERE (route_id=%s)', (sr.id, ))
        for point in points:
            cursor.execute('INSERT INTO StandartRoutes (route_id, latitude, longitude) VALUES (%s, %s, %s)', (sr.id, point[0], point[1]))
        connection.commit()
        sr.route_time = int(clock()- start_time)
        sr.points_amount = len(points)
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
        route = SR(None).get_route(route_id)
        return Response({'route': route, 'distance': sr.route_distance})

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























