from rest_framework.decorators import api_view
from rest_framework.response import Response

from equipment.models import Equipment
from elements.models import Project


@api_view(['POST', 'GET'])
def equipments(request, project_id):
    data = []
    project = Project.objects.get(id=project_id)
    if request.method == 'GET':
        if Equipment.objects.filter().count() == 0:
            Equipment.objects.create(project=project, equipment_name='NETIMIZER', latitude='Latitude', longitude='Longitude')
            Equipment.objects.create(project=project, equipment_name='TEMS', latitude='Latitude', longitude='Longitude')

    elif request.method == 'POST':
        id = request.POST.get('id')
        equipment_name = request.POST.get('equipment_name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if equipment_name and latitude and longitude:
            if id:
                Equipment.objects.filter(project=project, id=id).update(equipment_name=equipment_name, latitude=latitude, longitude=longitude)
            else:
                Equipment.objects.create(project=project, equipment_name=equipment_name, latitude=latitude, longitude=longitude)

    for equipment in  Equipment.objects.filter(project=project).order_by('equipment_name'):
        data.append({
            'id': equipment.id,
            'equipment_name': equipment.equipment_name,
            'latitude':equipment.latitude,
            'longitude':equipment.longitude})
    return Response(data)


@api_view(['GET', ])
def equipment(request, project_id):
    return Response([])