from rest_framework.decorators import api_view
from rest_framework.response import Response

from graphs.models import Legend, LegendRange, Calculation, Workspaces, Report
from routes.models import StandartRoute
from workspace import Workspace
from lib.files import handle_uploaded_file
from lib.excel import Excel

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


@api_view(['POST', ])
def upload_legend(request, project_id):
    filename = handle_uploaded_file(request.FILES.getlist('file'))[0]
    data = Excel(filename).get_data()
    legends_data = dict()
    current_legend = None
    for row in data:
        if row[0] == '**':
            current_legend = row[1]
            legends_data[current_legend] = []
        elif ('From' not in str(row[1])) and (row[1] or row[2]):
            legends_data[current_legend].append(row[1:])
    for legend_name, legend_ranges in legends_data.iteritems():
        Legend.objects.filter(legend_name=legend_name).delete()
        legend = Legend.objects.create(legend_name=legend_name)
        for legend_range in legend_ranges:
            LegendRange.objects.create(
                legend=legend,
                range_color=legend_range[2],
                range_from=legend_range[0],
                range_to=legend_range[1],
                range_symbol='>='
            )

    return Response([])

@api_view(['POST', ])
def upload_calculation(request, project_id):
    filename = handle_uploaded_file(request.FILES.getlist('file'))[0]
    data = Excel(filename).get_data()[1:]
    for calc in data:
        if Legend.objects.filter(legend_name__iexact=calc[3]).exists():
            Calculation.objects.create(
                calculation_name = calc[0],
                equipment = calc[1],
                technology = calc[2],
                legend = Legend.objects.filter(legend_name__iexact=calc[3]).first(),
                test = calc[4],
                column = calc[5],
                operation = calc[6]
            )
    return Response([])


@api_view(['GET', ])
def reports(request, project_id):
    data = []
    for r in Report.objects.all():
        data.append(dict(
            id= r.id,
            page=r.page,
            workspace=r.workspace,
            report_map='X' if r.report_map == True else '',
            graph='X' if r.graph == True else '',
            full_slide='X' if r.full_slide == True else '',
            title='X' if r.title == True else '',
            ppt='X' if r.ppt == True else '',
            excel='X' if r.excel == True else '',
            kmz='X' if r.kmz == True else '',
            tab='X' if r.tab == True else '',

        ))
    return Response(data)

@api_view(['POST', ])
def upload_report(request, project_id):
    filename = handle_uploaded_file(request.FILES.getlist('file'))[0]
    data = Excel(filename).get_data()[1:]
    for row in data:
        Report.objects.filter(workspace = row[1], page = row[0]).delete()
        Report.objects.create(
            page = row[0],
            workspace = row[1],
            report_map = True if row[2] == 'X' else False,
            graph = True if row[2] == 'X' else False,
            full_slide = True if row[2] == 'X' else False,
            title = True if row[2] == 'X' else False,
            ppt = True if row[2] == 'X' else False,
            excel = True if row[2] == 'X' else False,
            kmz = True if row[2] == 'X' else False,
            tab = True if row[2] == 'X' else False
        )
    return Response([])


