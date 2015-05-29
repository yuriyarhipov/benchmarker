from rest_framework.decorators import api_view
from rest_framework.response import Response

from lib.files import handle_uploaded_file
from dataset import Datasets

from models import DataSet


@api_view(['POST', 'GET' ])
def datasets(request, project_id):
    data = []
    if request.method == 'POST':
        dataset_name = request.POST.get('dataset_name')
        filename = handle_uploaded_file(request.FILES.getlist('file'))[0]
        Datasets().save_dataset(dataset_name, project_id, filename)
    elif request.method == 'GET':
        data = [{'id':ds.id, 'dataset_name': ds.dataset_name} for ds in DataSet.objects.filter().order_by('dataset_name')]
    return Response(data)

@api_view(['GET' ])
def dataset(request, project_id, dataset_id):
    columns, data = Datasets().get_dataset(dataset_id)
    return Response({'columns': columns, 'data': data})

@api_view(['GET' ])
def tests(request, project_id):
    return Response(Datasets.get_test(project_id))







