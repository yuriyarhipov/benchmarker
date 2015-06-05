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
                range_color=range_color[i],
                range_from=range_from[i],
                range_to=range_to[i],
                range_symbol=range_symbol[i]
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
    elif request.method == 'GET':
        if Legend.objects.filter(id=legend_id).exists():
            legend = Legend.objects.get(id=legend_id)
            ranges = []
            for lr in LegendRange.objects.filter(legend=legend):
                print lr.range_from
                ranges.append({
                    'from': lr.range_from,
                    'to': lr.range_to,
                    'symbol': lr.range_symbol,
                    'color': lr.range_color
                })

            return Response({'legend_name':legend.legend_name, 'ranges':ranges})




@api_view(['POST', 'GET', 'DELETE'])
def calculations(request, project_id, calculation_id=None):
    if request.method == 'POST':
        Calculation.objects.filter(calculation_name = request.POST.get('calc_name')).delete()
        Calculation.objects.create(
            calculation_name = request.POST.get('calc_name'),
            equipment = request.POST.get('equipment'),
            technology = request.POST.get('network'),
            legend = Legend.objects.get(id=request.POST.get('legend')),
            test = request.POST.get('test'),
            column = request.POST.get('column'),
            operation = request.POST.get('operation')
        )
    elif request.method == 'DELETE':
        Calculation.objects.filter(id=calculation_id).delete()
    elif (request.method == 'GET') and calculation_id:
        calc = Calculation.objects.get(id=calculation_id)
        return Response({
            'calculation_name': calc.calculation_name,
            'equipment': calc.equipment,
            'technology': calc.technology,
            'test': calc.test,
            'legend': {'id':calc.legend.id, 'legend_name':calc.legend.legend_name},
            'column': calc.column,
            'operation': calc.operation,
        })
    data = []
    for calc in Calculation.objects.all():
        data.append({
            'id':calc.id,
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
        graph_id = workspace.graph_id()
        data.append(dict(workspace_name=workspace.workspace_name, graph_id=graph_id, route_id=workspace.route.id))
    return Response(data)

@api_view(['GET', ])
def graph(request, project_id, graph_id):
    graph = Workspace.get_graph(graph_id)
    data = []
    for key, value in graph.iteritems():
        data.append({'data': [value, ], 'name': key})
    return Response(data)


@api_view(['GET', ])
def graphs_map(request, project_id, map_id):
    graphs_map = Workspace.get_map(map_id)
    return Response(graphs_map)


