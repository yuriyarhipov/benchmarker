var graphsControllers = angular.module('graphsControllers', []);

graphsControllers.controller('legendsCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $scope.ranges = [
            {'from':'from_1', 'symbol':'symbol_1', 'to':'to_1', 'color':'color_1'},
            {'from':'from_2', 'symbol':'symbol_2', 'to':'to_2', 'color':'color_2'},
            {'from':'from_3', 'symbol':'symbol_3', 'to':'to_3', 'color':'color_3'},
        ];

}]);
graphsControllers.controller('graphsCtrl', ['$scope', '$http',
    function ($scope, $http) {
        console.log('ok');
}]);