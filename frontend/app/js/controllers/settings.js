var settingsControllers = angular.module('settingsControllers', []);

settingsControllers.controller('coordinatesCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService', '$location',
    function ($scope, $http, $routeParams, activeProjectService, $location) {
        var project_id = $routeParams.project
        activeProjectService.setProject(project_id);
        $scope.project = project_id;

        $http.get('/data/' + project_id + '/settings/equipments').success(function(data){
            $scope.equipments = data;
        });

        $scope.onSave = function(){

            for (i = 0;i<$scope.equipments.length;i++){
                $http.post('/data/' + project_id + '/settings/equipments', $.param(
                    {
                        'equipment_name':$scope.equipments[i].equipment_name,
                        'id':$scope.equipments[i].id,
                        'latitude': $scope.equipments[i].latitude,
                        'longitude': $scope.equipments[i].longitude}));
            }
            $http.post('/data/' + project_id + '/settings/equipments', $.param(
                    {
                        'equipment_name':$scope.equipment_name,
                        'latitude': $scope.latitude,
                        'longitude': $scope.longitude})).success(function(data){
                $scope.equipments = data;
                $scope.equipment_name = '';
                $scope.latitude = '';
                $scope.longitude = '';
                $location.path('/' + project_id + '/coordinates/');
            });
        };
}]);

settingsControllers.controller('calculationsCtrl', ['$scope', '$http','$routeParams', 'activeProjectService',
    function ($scope, $http, $routeParams, activeProjectService) {
        var project_id = $routeParams.project
        activeProjectService.setProject(project_id);
        $scope.project = project_id;
        $scope.equipments = ['TEMS', 'NETIMIZER'];
        $scope.networks = ['GSM', 'LTE', 'WCDMA'];
        $scope.operations = ['Average', 'Sum', 'Max', 'Min', 'Mode'];
        $scope.equipment = {};
        $scope.network = {};
        $scope.operation = {};
        $scope.legend = {};
        $scope.test = {};
        $http.get('/data/' + project_id + '/graphs/legends/').success(function(data){
            $scope.legends = data;
        });

        $http.get('/data/' + project_id + '/datasets/tests/').success(function(data){
            $scope.tests = data;
        });
        $http.get('/data/' + project_id + '/graphs/calculations/').success(function(data){
            $scope.calculations = data;
        });

        $scope.OnSave = function(){
            var params = {};
            params.calc_name = $scope.calc_name;
            params.equipment = $scope.equipment.selected;
            params.network = $scope.network.selected;
            params.legend = $scope.legend.selected.id;
            params.test = $scope.test.selected;
            params.column = $scope.column;
            params.operation = $scope.operation.selected;
            $http.post('/data/' + project_id + '/graphs/calculations/', $.param(params)).success(function(data){
                $scope.calc_name = '';
                $scope.equipment = {};
                $scope.network = {};
                $scope.operation = {};
                $scope.legend = {};
                $scope.test = {};
                $scope.column = '';
                $scope.calculations = data;
            });
        };

        $scope.onDelete = function(calc_id){
            $http.delete('/data/' + project_id + '/graphs/calculations/' + calc_id).success(function(data){
                $scope.calculations = data;
            });
        };

        $scope.onClick = function(calc_id){
            $http.get('/data/' + project_id + '/graphs/calculations/' + calc_id).success(function(data){
                $scope.calc_name = data.calculation_name;
                $scope.network = {'selected': data.technology};
                $scope.equipment = {'selected': data.equipment};
                $scope.test = {'selected': data.test};
                $scope.operation = {'selected': data.operation};
                $scope.column = data.column;
                $scope.legend = {'selected': data.legend};
            });
        };
}]);

settingsControllers.controller('favoritesCtrl', ['$scope', '$http',
    function ($scope, $http) {
       console.log('favorites');
}]);

settingsControllers.controller('performanceCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService',
    function ($scope, $http, $routeParams, activeProjectService) {
        $scope.selected_tests = [];
        var project_id = $routeParams.project;
        activeProjectService.setProject(project_id);
        $scope.project = project_id;
        $http.get('/data/' + project_id + '/datasets/tests/').success(function(data){
            $scope.tests = data;
        });
        $http.get('/data/' + project_id + '/datasets/performance_tests/').success(function(data){
            $scope.selected_tests = data;
        });
        $scope.onSave = function(){
            $http.post('/data/' + project_id + '/datasets/performance_tests/', $.param({
                'tests': $scope.selected_tests,
            }));
        };
}]);