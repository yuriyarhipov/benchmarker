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
graphsControllers.controller('graphsCtrl', ['$scope', '$http',
    function ($scope, $http) {
        console.log('ok');
}]);