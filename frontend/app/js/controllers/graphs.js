var graphsControllers = angular.module('graphsControllers', []);

graphsControllers.controller('legendsCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $scope.ranges = [];
        $scope.range_color = '#00FF00';
        $scope.onAddRange = function(range){
            $scope.ranges.push({'from': range[0], 'symbol': range[1], 'to': range[2], 'color': range[3]});
            $scope.range_from = '';
            $scope.range_symbol = '';
            $scope.range_to = '';
            $scope.range_color = '#00FF00';
        }

        $scope.onSaveLegend = function(){
            $http.post('/data/' + project_id + '/routes/',$.param()).success(function(){
                console.log('save');
            })
        }

}]);
graphsControllers.controller('graphsCtrl', ['$scope', '$http',
    function ($scope, $http) {
        console.log('ok');
}]);