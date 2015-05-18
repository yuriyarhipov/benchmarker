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

routeControllers.controller('createStandartRouteCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService', '$location', 'ngProgress',
    function ($scope, $http, $routeParams, activeProjectService, $location, ngProgress) {
        var project_id = $routeParams.project
        activeProjectService.setProject(project_id);
        $scope.project = project_id;
        $scope.selected_files = [];
        $scope.distance = 5;

        $http.get('/data/' + project_id + '/routes/').success(function(data){
            $scope.routes = data;
        });

        $http.get('/data/' + project_id + '/modules/').success(function(data){
            $scope.modules = data;
        });

        $scope.onModule = function(module_id){
            $http.get('/data/' + project_id + '/module_files/' + module_id).success(function(data){
                $scope.files = data;
            });
        }

        $scope.onSelectAllClick = function(){
            $scope.selected_files = $scope.files.map(function(item) { return item.filename; });

        };


        $scope.saveRoute = function(){
            ngProgress.start();
            $http.post('/data/' + project_id + '/routes/',$.param(
                    {
                        'route_name':$scope.route_name,
                        'distance': $scope.distance,
                        'files': $scope.selected_files.toString()})).success(function(){
                ngProgress.stop();
                ngProgress.set(0);
                $location.path('/' + project_id +   '/routes/');
            })
        };
}]);

routeControllers.controller('routeCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService',
    function ($scope, $http, $routeParams, activeProjectService) {
        var project_id = $routeParams.project
        var route_id = $routeParams.route;
        var custom_style = {
                image: {
                    icon: {
                        anchor: [0.5, 1],
                        anchorXUnits: 'fraction',
                        anchorYUnits: 'fraction',
                        opacity: 0.90,
                        src: 'static/bul.png'
                    }
                }
            };
        activeProjectService.setProject(project_id);
        $http.get('/data/' + project_id + '/routes/' + route_id).success(function(data){
            $scope.markers = data.route;
            $scope.distance = data.distance;
            latitude = parseFloat($scope.markers[0].lat);
            longitude = parseFloat($scope.markers[0].lon);
            $scope.zoom = 15;
            $scope.center = {
                    lat: latitude,
                    lon: longitude,
                    zoom: $scope.zoom,
                };
            $scope.custom_style = custom_style;
            $scope.controls = [
                { name: 'zoom', active: true },
                { name: 'rotate', active: true },
                { name: 'attribution', active: true }
            ]
        });
        $scope.onZoom = function(){
            $scope.center = {
                lat: latitude,
                lon: longitude,
                zoom: $scope.zoom,
            };
        };
}]);

routeControllers.controller('routesCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService',
    function ($scope, $http, $routeParams, activeProjectService) {
        var project_id = $routeParams.project
        activeProjectService.setProject(project_id);
        $scope.project = project_id;
        $http.get('/data/' + project_id + '/routes/').success(function(data){
            $scope.routes = data;
        });

        $scope.onDelete = function(route_id){
            $http.delete('/data/' + project_id + '/routes/' + route_id).success(function(data){
                $scope.routes = data;
            });
        };

}]);

routeControllers.controller('merge_routesCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService',
    function ($scope, $http, $routeParams, activeProjectService) {
        $scope.colors = [
            '#468966',
            '#FFF0A5',
            '#FFB03B',
            '#B64926',
            '#8E2800',
            '#e1e1e1'
        ];
        var project_id = $routeParams.project
        activeProjectService.setProject(project_id);
        $scope.routes = {};
        $scope.routeMarkers = [];
        $scope.project = project_id;
        $http.get('/data/' + project_id + '/routes/').success(function(data){
            $scope.routes.entities = data;
        });

        $scope.onMerge = function(){
            for (i=0;i<$scope.routes.entities.length; i++){
                if ($scope.routes.entities[i].isChecked){
                    $http.get('/data/' + project_id + '/routes/' + $scope.routes.entities[i].id).success(function(data){
                        $scope.routeMarkers = data.route;
                        $scope.distance = data.distance;
                        latitude = parseFloat($scope.routeMarkers[0].latitude);
                        longitude = parseFloat($scope.routeMarkers[0].longitude);
                        $scope.map = { center: { latitude: latitude, longitude: longitude }, zoom: 10 };
                    });
                }
            }
        };

}]);
