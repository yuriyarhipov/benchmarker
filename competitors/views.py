from rest_framework.decorators import api_view
from rest_framework.response import Response

from elements.models import Project
from models import Competitor
from lib.files import handle_uploaded_file
from lib.excel import Excel


@api_view(['POST', 'GET' ])
def competitors(request, project_id):
    columns = ''
    project = Project.objects.get(id=project_id)
    data = []
    if request.method == 'POST':
        filename = handle_uploaded_file(request.FILES.getlist('file'))[0]
        Competitor.objects.filter(project=project).delete()
        Competitor.objects.create(project=project, filename=filename)
    elif request.method == 'GET':
        filename = Competitor.objects.filter(project=project).first().filename
        data = Excel(filename).get_data()
        columns = data[0]
        data = data[1:]
    return Response(dict(data=data, columns=columns))


@api_view(['POST', 'GET' ])
def competitor(request):
    pass