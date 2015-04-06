var routeControllers = angular.module('routeControllers', []);

routeControllers.controller('originalCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $scope.routeMarkers = [];
        $http.get('/data/get_points/').success(function(data){

            $scope.routeMarkers = data
        });
        $scope.map = { center: { latitude: 13, longitude: -59 }, zoom: 8 };
}]);