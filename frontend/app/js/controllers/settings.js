var settingsControllers = angular.module('settingsControllers', []);

routeControllers.controller('coordinatesCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService', '$location',
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