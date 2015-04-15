var routeControllers = angular.module('routeControllers', []);

routeControllers.controller('originalCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $scope.routeMarkers = [];
        $http.get('/data/get_points/').success(function(data){
            $scope.routeMarkers = data
            latitude = parseFloat($scope.routeMarkers[0].latitude);
            longitude = parseFloat($scope.routeMarkers[0].longitude);

            $scope.map = { center: { latitude: latitude, longitude: longitude }, zoom: 3 };
        });
}]);

routeControllers.controller('createStandartRouteCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService',
    function ($scope, $http, $routeParams, activeProjectService) {
        var project_id = $routeParams.project
        activeProjectService.setProject(project_id);

        $scope.project = project_id;
        $http.get('/data/' + project_id + '/routes/').success(function(data){
            $scope.routes = data;
        });
        $scope.saveRoute = function(){
            $http.post('/data/' + project_id + '/save_standart_route/',$.param({'route_name':$scope.route_name, 'distance': $scope.distance})).success(function(){
                $http.get('/data/' + project_id + '/routes/').success(function(data){
                    $scope.routes = data;
                });
            })
        };
}]);

routeControllers.controller('routeCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService',
    function ($scope, $http, $routeParams, activeProjectService) {
        var project_id = $routeParams.project
        var standart_route_id = $routeParams.route;

        activeProjectService.setProject(project_id);
        $scope.routeMarkers = [];
        $scope.module = {};
        $scope.route = {};

        $http.get('/data/' + project_id + '/modules/').success(function(data){
            $scope.modules = data;
        });

        $http.get('/data/' + project_id + '/routes/').success(function(data){
            $scope.routes = data;
        });

        $scope.showRoute = function(){
            $scope.module
            $http.get('/data/' + project_id + '/' + $scope.route.selected.id + '/' + $scope.module.selected + '/get_points/').success(function(data){
                $scope.routeMarkers = data.route;
                $scope.distance = data.distance;
                latitude = parseFloat($scope.routeMarkers[0].latitude);
                longitude = parseFloat($scope.routeMarkers[0].longitude);
                $scope.map = { center: { latitude: latitude, longitude: longitude }, zoom: 10 };
            });
        };
}]);