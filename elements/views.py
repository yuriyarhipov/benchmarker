from os.path import basename

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings

from elements.models import Project
from routes.models import RouteFile, StandartRoute
import tasks

from lib.archive import Archive


def handle_uploaded_file(files):
    path = settings.STATICFILES_DIRS[0]
    result = []
    for f in files:
        filename = '/'.join([path, f.name])
        destination = open(filename, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        result.append(filename)
    return result


@api_view(['GET', ])
def get_elements(request):
    data = ['test', ]
    return Response(data)


@api_view(['POST', 'GET', ])
def projects(request):
    if request.POST:
        project_name = request.POST.get('project_name')
        if not Project.objects.filter(project_name=project_name).exists():
            Project.objects.create(project_name=project_name)

    data = [dict(id=project.id, project_name=project.project_name) for project in Project.objects.all().order_by('project_name')]
    return Response(data)


@api_view(['GET', ])
def get_modules(request):
    modules = ['%s' % i for i in range(1,51)]
    return Response(modules)


@api_view(['POST', ])
def save_file(request, project_id):
    module = request.POST.get('module')
    equipment = request.POST.get('equipment')
    project = Project.objects.get(id=project_id)
    uploaded_files = Archive(handle_uploaded_file(request.FILES.getlist('file'))[0]).get_files()
    for f in uploaded_files:
        RouteFile.objects.filter(project=project,
                                 filename__contains=basename(f),
                                 module=module).delete()
        RouteFile.objects.create(project=project,
                                 filename=f,
                                 filetype=equipment,
                                 module=module,
                                 latitude='All-Latitude Decimal Degree',
                                 longitude='All-Longitude Decimal Degree',
                                 status='file')
        tasks.worker.delay(project, module, f)


    return Response(dict(message='OK'))


@api_view(['GET', ])
def get_files(request, project_id):
    project = Project.objects.get(id=project_id)
    files= []
    for f in RouteFile.objects.filter(project=project).order_by('module', 'filename'):
        files.append({
            'filename': basename(f.filename),
            'module': f.module,
            'latitude': f.latitude,
            'longitude': f.longitude,
            })

    return Response(files)

@api_view(['GET', ])
def get_points(request,  project_id, route_id, module_id):
    project = Project.objects.get(id=project_id)
    distance = StandartRoute.objects.get(id=route_id).distance
    files = [f.filename for f in RouteFile.objects.filter(project=project, module=module_id)]
    distance, points = Route().get_points(project_id, module_id, files, distance)
    return Response(dict(route=points, distance=distance))


@api_view(['POST', ])
def save_standart_route(request, project_id):
    route_name = request.POST.get('route_name')
    distance = request.POST.get('distance')
    project = Project.objects.get(id=project_id)
    StandartRoute.objects.filter(project=project, route_name=route_name).delete()
    StandartRoute.objects.create(project=project, route_name=route_name, distance=distance)
    return Response([])


@api_view(['GET', ])
def routes(request, project_id):
    routes = []
    project = Project.objects.get(id=project_id)
    for route in StandartRoute.objects.filter(project=project).order_by('route_name'):
        routes.append(dict(id=route.id, route_name=route.route_name))
    return Response(routes)

@api_view(['GET', ])
def modules(request, project_id):
    project = Project.objects.get(id=project_id)
    modules = [ m.module for m in RouteFile.objects.filter(project=project).distinct('module').order_by('module')]
    return Response(modules)


@api_view(['GET', ])
def module_files(request, project_id, module_name):
    project = Project.objects.get(id=project_id)
    data = list(dict(label=basename(f.filename), filename=f.filename) for f in RouteFile.objects.filter(project=project, module=module_name))
    return Response(data)








