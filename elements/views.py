from os.path import basename

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings

from elements.models import Project, Competitor, DataSet, RouteFile, StandartRoute
from lib.excel import Excel
from lib.archive import Archive
from lib.route import Route
from lib.datatset import DataSet


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


@api_view(['POST', ])
def competitors_upload_template(request):
    project_id = request.POST.get('project_id')
    project = Project.objects.get(id=project_id)
    filename = handle_uploaded_file(request.FILES.getlist('excel'))[0]
    for competitor in Excel(filename).get_competitors_template():
        if competitor[0]:
            Competitor.objects.filter(competitor=competitor[0]).delete()
            Competitor.objects.create(
                project=project,
                competitor=competitor[0],
                gsm = True if competitor[1] else False,
                wcdma = True if competitor[2] else False,
                lte = True if competitor[3] else False,
                future = competitor[4],
                mcc = competitor[5],
                mnc = competitor[6],
                gsm_freq = competitor[7],
                wcdma_carriers = competitor[8],
                lte_carriers = competitor[9],
                future_carriers = competitor[10])
    return Response([])


@api_view(['GET', ])
def competitors(request, project_id):
    project = Project.objects.get(id=project_id)
    data = []
    for competitor in Competitor.objects.filter(project=project):
        row = [
            competitor.competitor,
            'X' if competitor.gsm else '',
            'X' if competitor.wcdma else '',
            'X' if competitor.lte else '',
            competitor.future,
            competitor.mcc,
            competitor.mnc,
            competitor.gsm_freq,
            competitor.wcdma_carriers,
            competitor.lte_carriers,
            competitor.future_carriers
        ]
        data.append(row)
    return Response(data)


@api_view(['POST', ])
def upload_data_set(request):
    project = Project.objects.filter().first()
    filename = handle_uploaded_file(request.FILES.getlist('excel'))[0]
    data = Excel(filename).get_data_set()
    equipment = data[0][1]
    columns = [col for col in data[1]][1:]
    dataset = DataSet()
    for data_row in data[2:]:
        module = data_row[0]
        data_row = data_row[1:]
        dataset.add_row(project.id, equipment, module, columns, data_row)
    return Response([])


@api_view(['GET', ])
def datasets(request, project_id):
    data = DataSet().get_dataset(project_id)
    return Response(data)


@api_view(['GET', ])
def get_modules(request):
    modules = ['%s' % i for i in range(1,51)]
    return Response(modules)


@api_view(['POST', ])
def save_file(request):
    project_id = request.POST.get('project')
    module = request.POST.get('module')
    filetype = request.POST.get('filetype')
    project = Project.objects.get(id=project_id)
    uploaded_files = Archive(handle_uploaded_file(request.FILES.getlist('uploaded_file'))[0]).get_files()
    for f in uploaded_files:
        Route().parse(project_id,filetype, module, f)
        RouteFile.objects.filter(project=project,
                                 filename=f,
                                 module=module).delete()
        RouteFile.objects.create(project=project,
                                 filename=f,
                                 filetype=filetype,
                                 module=module,
                                 latitude='All-Latitude Decimal Degree',
                                 longitude='All-Longitude Decimal Degree')

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
    points = Route().get_points(project_id, module_id, files, distance)
    return Response(points)


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







