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

        $http.get('/data/' + project_id + '/module_files/').success(function(data){
            $scope.modules = data;
        });

        $scope.saveRoute = function(){
            var selected_files = []
            for (i=0; i<$scope.selected_files.length; i++){
                selected_files.push($scope.selected_files[i].filename);
            }
            console.log(selected_files);
            $http.post('/data/' + project_id + '/routes/',$.param(
                    {
                        'route_name':$scope.route_name,
                        'distance': $scope.distance,
                        'files': selected_files.toString()})).success(function(){
                $http.get('/data/' + project_id + '/routes/').success(function(data){
                    $scope.routes = data;
                });
            })
        };
}]);

routeControllers.controller('routeCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService',
    function ($scope, $http, $routeParams, activeProjectService) {
        var project_id = $routeParams.project
        var route_id = $routeParams.route;
        $scope.routeMarkers = []
        activeProjectService.setProject(project_id);
        $scope.routeMarkers = [];
        $http.get('/data/' + project_id + '/routes/' + route_id).success(function(data){
            $scope.routeMarkers = data.route;
            $scope.distance = data.distance;
            latitude = parseFloat($scope.routeMarkers[0].latitude);
            longitude = parseFloat($scope.routeMarkers[0].longitude);
            $scope.map = { center: { latitude: latitude, longitude: longitude }, zoom: 10 };
        });
}]);

routeControllers.controller('routesCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService',
    function ($scope, $http, $routeParams, activeProjectService) {
        var project_id = $routeParams.project
        activeProjectService.setProject(project_id);
        $scope.project = project_id;
        $http.get('/data/' + project_id + '/routes/').success(function(data){
            $scope.routes = data;
        });

}]);
