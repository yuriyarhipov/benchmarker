from rest_framework.decorators import api_view
from rest_framework.response import Response

from graphs.models import Legend, LegendRange, Calculation, Workspaces
from routes.models import StandartRoute
from workspace import Workspace

@api_view(['GET', ])
def graphs(request):
    return Response()

@api_view(['POST', 'GET'])
def legends(request, project_id):
    if request.method == 'POST':
        legend_name = request.POST.get('legend_name')
        range_color = request.POST.getlist('range_color[]')
        range_from = request.POST.getlist('range_from[]')
        range_to = request.POST.getlist('range_to[]')
        range_symbol = request.POST.getlist('range_symbol[]')
        if Legend.objects.filter(legend_name=legend_name).exists():
            legend = Legend.objects.get(legend_name=legend_name)
            LegendRange.objects.filter(legend=legend).delete()
            Legend.objects.filter(legend_name=legend_name).delete()
        legend = Legend.objects.create(legend_name=legend_name)
        i = 0
        while i < len(range_color):
            LegendRange.objects.create(
                legend=legend,
                range_color=range_color,
                range_from=range_from,
                range_to=range_to,
                range_symbol=range_symbol
            )
            i += 1
    legends = [{'legend_name':legend.legend_name, 'id': legend.id} for legend in Legend.objects.all()]
    return Response(legends)

@api_view(['DELETE', 'GET'])
def legend(request, project_id, legend_id):
    if request.method == 'DELETE':
        if Legend.objects.filter(id=legend_id).exists():
            legend = Legend.objects.get(id=legend_id)
            LegendRange.objects.filter(legend=legend).delete()
            Legend.objects.filter(id=legend_id).delete()
    legends = [{'legend_name':legend.legend_name, 'id': legend.id} for legend in Legend.objects.all()]
    return Response(legends)

@api_view(['POST', 'GET'])
def calculations(request, project_id):
    if request.method == 'POST':
        Calculation.objects.create(
            calculation_name = request.POST.get('calc_name'),
            equipment = request.POST.get('calc_name'),
            technology = request.POST.get('network'),
            legend = Legend.objects.get(id=request.POST.get('legend')),
            test = request.POST.get('test'),
            column = request.POST.get('column'),
            operation = request.POST.get('operation')
        )
    data = []
    for calc in Calculation.objects.all():
        data.append({
            'calculation_name': calc.calculation_name,
            'equipment': calc.equipment,
            'technology': calc.technology,
            'test': calc.test,
            'legend': calc.legend.legend_name,
            'column': calc.column,
            'operation': calc.operation,
        })
    return Response(data)


@api_view(['POST', 'GET'])
def workspaces(request, project_id):
    if request.method == 'POST':
        Workspaces.objects.filter(workspace_name=request.POST.get('workspace')).delete()
        ws = Workspaces.objects.create(
            workspace_name = request.POST.get('workspace'),
            route = StandartRoute.objects.get(id=request.POST.get('route')),
            competitor = request.POST.get('competitor'),
            network = request.POST.get('network'),
            test = request.POST.get('test'),
            calculation = Calculation.objects.get(calculation_name=request.POST.get('calculation'))
        )
        ws = Workspace(ws.workspace_name)

    data = []
    for workspace in Workspaces.objects.all():
        workspace_name = workspace.workspace_name
        graph_id = workspace.graph_id()
        data.append(dict(workspace_name=workspace.workspace_name, graph_id=graph_id, route_id=workspace.route.id))
    return Response(data)

@api_view(['GET', ])
def graph(request, project_id, graph_id):
    print graph_id
    return Response([])

