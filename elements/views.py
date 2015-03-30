from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings

from elements.models import Project, Competitor, DataSet
from lib.excel import Excel


def handle_uploaded_file(files):
    path = settings.STATICFILES_DIRS[0]
    result = []
    for f in files:
        filename = '/xml/'.join([path, f.name])
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

    data = [project.project_name for project in Project.objects.all().order_by('project_name')]
    return Response(data)


@api_view(['POST', ])
def competitors_upload_template(request):
    project = Project.objects.filter().first()
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
def competitors(request):
    data = []
    for competitor in Competitor.objects.all():
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
    modules = [col for col in data[1]][1:]
    for data_row in data[2:]:
        module = data_row[0]
        data_row = data_row[1:]
        for ms in data_row:
            if ms:
                idx = data_row.index(ms)
                DataSet.objects.create(
                    project=project,
                    module=module,
                    equipment=equipment,
                    measurement_device=modules[idx],
                    value=ms
                )

    return Response([])


@api_view(['GET', ])
def datasets(request):
    data = dict()
    data['equipment'] = DataSet.objects.filter().first().equipment
    data['measurement_devices'] =[m.measurement_device for m in DataSet.objects.filter().distinct('measurement_device')]
    return Response(data)

