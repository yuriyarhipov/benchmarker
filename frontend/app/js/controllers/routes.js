var routeControllers = angular.module('routeControllers', []);

routeControllers.controller('originalCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $scope.routeMarkers = [];
        $http.get('/data/get_points/').success(function(data){
            $scope.routeMarkers = data
            latitude = parseFloat($scope.routeMarkers[0].latitude);
            longitude = parseFloat($scope.routeMarkers[0].longitude);

            $scope.map = { center: { latitude: latitude, longitude: longitude }, zoom: 10 };
        });
}]);

routeControllers.controller('createStandartRouteCtrl', ['$scope', '$http', '$routeParams',
    function ($scope, $http, $routeParams) {
        var project = $routeParams.project
        $scope.project = project;
        $http.get('/data/' + project + '/routes/').success(function(data){
            $scope.routes = data;
        });
        $scope.saveRoute = function(){
            $http.post('/data/' + project + '/save_standart_route/',$.param({'route_name':$scope.route_name, 'distance': $scope.distance})).success(function(){
                $http.get('/data/' + project + '/routes/').success(function(data){
                    $scope.routes = data;
                });
            })
        };
}]);
routeControllers.controller('routeCtrl', ['$scope', '$http', '$routeParams',
    function ($scope, $http, $routeParams) {
        var project_id = $routeParams.project
        var standart_route_id = $routeParams.route;
        $scope.routeMarkers = [];
        $scope.module = {};
        $http.get('/data/get_modules/').success(function(data){
            $scope.modules = data;
        });

        $scope.showRoute = function(){
            $scope.module
            $http.get('/data/' + project_id + '/' + standart_route_id + '/' + $scope.module.selected + '/get_points/').success(function(data){
                $scope.routeMarkers = data
                latitude = parseFloat($scope.routeMarkers[0].latitude);
                longitude = parseFloat($scope.routeMarkers[0].longitude);
                $scope.map = { center: { latitude: latitude, longitude: longitude }, zoom: 10 };
            });
        };



}]);