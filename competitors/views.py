from rest_framework.decorators import api_view
from rest_framework.response import Response

from elements.models import Project
from lib.files import handle_uploaded_file
from lib.excel import Excel
from competitors.competitor import Competitor


@api_view(['POST', 'GET' ])
def competitors(request, project_id):
    columns = ''
    data = []
    if request.method == 'POST':
        filename = handle_uploaded_file(request.FILES.getlist('file'))[0]
        Competitor().parse_file(project_id, filename)

    elif request.method == 'GET':
        columns, data = Competitor().get_competitors(project_id)
    return Response(dict(data=data, columns=columns))


@api_view(['POST', 'GET' ])
def competitor(request, project_id, competitor_name):
    if request.method == 'GET':
        return Response(Competitor().get_competitor(project_id, competitor_name))
    if request.method == 'POST':
        Competitor().save_competitor(project_id, competitor_name, request.POST)
    return Response([])

@api_view(['GET', ])
def competitor_names(request, project_id):
    columns, data = Competitor().get_competitors(project_id)
    return Response([row[columns.index('Competitor')] for row in data])

