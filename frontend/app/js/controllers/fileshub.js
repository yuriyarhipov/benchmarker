var filesControllers = angular.module('filesControllers', []);

filesControllers.controller('fileshubCtrl', ['$scope', '$http', '$routeParams', 'activeProjectService',
    function ($scope, $http, $routeParams, activeProjectService) {
        $scope.module = {};
        var project_id = $routeParams.project;
        $scope.project = project_id;
        activeProjectService.setProject(project_id);


        $http.get('/data/get_modules/').success(function(data){
            $scope.modules = data;
        });

        $http.get('/data/' + project_id + '/get_files/').success(function(data){
            $scope.files = data;
        });

        $scope.complete = function(){
            $http.get('/data/' + project_id + '/get_files/').success(function(data){
                $scope.files = data;
            });
        };
 }]);