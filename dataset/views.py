from os.path import basename

from rest_framework.decorators import api_view
from rest_framework.response import Response

from elements.models import Project
from lib.files import handle_uploaded_file
from lib.excel import Excel

from models import DataSet


@api_view(['POST', 'GET' ])
def datasets(request, project_id):
    project = Project.objects.get(id=project_id)
    data = []
    if request.method == 'POST':
        dataset_name = request.POST.get('dataset_name')
        filename = handle_uploaded_file(request.FILES.getlist('file'))[0]
        DataSet.objects.create(project=project, filename=filename, dataset_name=dataset_name, columns='')
    elif request.method == 'GET':
        data = [{'id':ds.id, 'dataset_name': ds.dataset_name, 'filename': basename(ds.filename)} for ds in DataSet.objects.filter().order_by('dataset_name')]
    return Response(data)

@api_view(['GET' ])
def dataset(request, project_id, dataset_id):
    dataset = DataSet.objects.get(id=dataset_id)
    data = Excel(dataset.filename).get_data()
    columns = data[0]
    data = data[1:]
    return Response({'columns': columns, 'data': data})

@api_view(['GET' ])
def tests(request, project_id):

    return Response(['test1', 'test2', ])







