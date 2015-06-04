var graphsControllers = angular.module('graphsControllers', []);

graphsControllers.controller('legendsCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService',
    function ($scope, $http, $routeParams, activeProjectService) {
        var project_id = $routeParams.project
        activeProjectService.setProject(project_id);
        $scope.project = project_id;
        $scope.ranges = [];
        $scope.range_color = '#00FF00';

        $scope.legends = $http.get('/data/' + project_id + '/graphs/legends/').success(function(data){
            $scope.legends = data;
        });

        $scope.onDelete = function(legend_id){
            $http.delete('/data/' + project_id + '/graphs/legends/'+legend_id).success(function(data){
                $scope.legends = data;
            });
        };

        $scope.onLegend = function(legend_id){
            $http.get('/data/' + project_id + '/graphs/legends/'+legend_id).success(function(data){
                $scope.legend_name = data.legend_name;
                $scope.ranges = data.ranges;
            });
        };


        $scope.onAddRange = function(range){
            $scope.ranges.push({'from': range[0], 'symbol': range[1], 'to': range[2], 'color': range[3]});
            $scope.range_from = '';
            $scope.range_symbol = '';
            $scope.range_to = '';
            $scope.range_color = '#00FF00';
        };

        $scope.onSaveLegend = function(){
            var params = {};
            params['legend_name'] = $scope.legend_name;
            params['range_from'] = [];
            params['range_to'] = [];
            params['range_color'] = [];
            params['range_symbol'] = [];
            for (i=0;i<$scope.ranges.length;i+=1){
                params['range_from'].push($scope.ranges[i]['from']);
                params['range_to'].push($scope.ranges[i]['to']);
                params['range_color'].push($scope.ranges[i]['color']);
                params['range_symbol'].push($scope.ranges[i]['symbol']);
            }
            $http.post('/data/' + project_id + '/graphs/legends/',$.param(params)).success(function(data){
                $scope.legends = data;
            });
        }

}]);
graphsControllers.controller('workspaceCtrl', ['$scope', '$http','$routeParams', 'activeProjectService', 'ngProgress',
    function ($scope, $http, $routeParams, activeProjectService, ngProgress) {
        var project_id = $routeParams.project
        activeProjectService.setProject(project_id);
        $scope.project = project_id;
        $scope.networks = ['GSM', 'LTE', 'WCDMA'];
        $scope.route = {'selected': {}};
        $scope.competitor = {};
        $scope.network = {};
        $scope.test = {};
        $scope.calculation = {};

        $http.get('/data/' + project_id + '/routes/').success(function(data){
            $scope.routes = data;
        });
        $http.get('/data/' + project_id + '/competitors/competitor_names/').success(function(data){
            $scope.competitors = data;
        });
        $http.get('/data/' + project_id + '/datasets/').success(function(data){
            $scope.datasets = data;
        });

        $http.get('/data/' + project_id + '/datasets/performance_tests/').success(function(data){
            $scope.tests = data;
        });
        $http.get('/data/' + project_id + '/graphs/calculations/').success(function(data){
            $scope.calculations = data;
        });

        $http.get('/data/' + project_id + '/graphs/workspaces/').success(function(data){
            $scope.workspaces = data;
        });

        $scope.onChangeDataset = function(dataset_id){
            $http.get('/data/' + project_id + '/datasets/' + dataset_id + '/tests/').success(function(data){
                $scope.tests = data;
            });
        };

        $scope.OnSave = function(){
            ngProgress.start();
            var params = {}
            params.workspace = $scope.workspace;
            params.route = $scope.route.selected.id;
            params.competitor = $scope.competitor.selected;
            params.network = $scope.network.selected;
            params.test = $scope.test.selected;
            params.calculation = $scope.calculation.selected.calculation_name;
            $http.post('/data/' + project_id + '/graphs/workspaces/',$.param(params)).success(function(data){
                $scope.workspaces = data;
                ngProgress.stop();
                ngProgress.set(0);
            });

        };
}]);

graphsControllers.controller('graphCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService',
    function ($scope, $http, $routeParams, activeProjectService) {
        var project_id = $routeParams.project
        var graph_id = $routeParams.graph_id
        activeProjectService.setProject(project_id);
        $scope.project = project_id;
        $http.get('/data/' + project_id + '/graphs/graph/' + graph_id).success(function(series_data){
            console.log(series_data);
            $scope.chartConfig = {
                options: {
                    chart: {
                        type: 'column'
                    }
                },
                series: series_data,
                title: {
                    text: 'Legend'
                },
                tooltip: {
                    pointFormat: '<b>{point.y} </b>'
                },
                xAxis: {
                    type: 'category',
                    labels: {
                        rotation: -45,
                        align: 'right',
                        style: {
                            fontSize: '13px',
                            fontFamily: 'Verdana, sans-serif'
                        }
                    }
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'value'
                    }
                },
                legend: {
                    enabled: false
                }
            };
        });
}]);